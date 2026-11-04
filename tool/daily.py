#!/usr/bin/env python3
"""Tunzle daily job (runs on your PC).

For one batch day it:
  1. reads that day's 5 rows from calendar.csv
  2. renders each Short (render.py + ffmpeg)
  3. asks Qwen (Ollama) for a title + hook line  (falls back to safe templates if Ollama is off)
  4. writes schedule/<date>.json  (the list Claude reads to schedule posts in Metricool)
  5. commits + pushes videos and the schedule to GitHub

Usage:
  python daily.py                 # tomorrow's batch (default)
  python daily.py --date 2026-11-05
  python daily.py --date 2026-11-05 --no-push --no-ollama   # local test
"""
import argparse, csv, datetime as dt, json, os, random, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from melodies import M, build
from render import render_short

CFG = json.load(open(os.path.join(HERE, "config.json"), encoding="utf-8"))
REPO = os.path.abspath(os.path.join(HERE, CFG.get("repo_dir", "..")))
RAW = f"https://raw.githubusercontent.com/{CFG['github_repo']}/main"

PROMPTS = {"Easy": ["Everyone knows this one!", "Name this melody!", "You've heard this 1000 times!"],
           "Medium": ["Name this melody!", "Real music fans get this one", "Bet you can't name it!"],
           "Hard": ["Only 10% get this one!", "Impossible level!", "Prove you're a music genius"]}
FMT_PROMPT = {"three_notes": "ONLY 3 NOTES!", "backwards": "Played BACKWARDS!", "double_speed": "DOUBLE SPEED!"}
FALLBACK_TITLES = {
    "Easy": ["Everyone Knows This Melody 🎵", "Name This Tune in 8 Seconds ⏱️", "You've Heard This 1000 Times 👀"],
    "Medium": ["Can You Name This Melody? 🎶", "Only Real Music Fans Get This 🎧", "Bet You Can't Name It 😏"],
    "Hard": ["Only 10% Can Name This 🔴", "Impossible Level Melody Quiz 🔴", "Can You Beat HARD Mode? 🔴"],
    "three_notes": ["HARD: Guess It From 3 Notes 🔴"], "backwards": ["Guess the Song Played BACKWARDS 🔄"],
    "double_speed": ["Guess the Song at DOUBLE SPEED ⚡"], "xmas": ["Guess the Christmas Song 🎄", "Christmas Melody Quiz 🎅", "Name This Christmas Classic 🎄"]}
FOOTER = "\n\nNew Tunzle music quiz every day — follow @tunzlequiz for the next round 🎵🧩\n\n#shorts #guessthesong #guessthemelody #musicquiz #quiz #tunzle"


def log(*a): print("[tunzle]", *a, flush=True)


# Words that appear in melody names/subtitles but give nothing away (a title like
# "This Melody Is Impossible" must not be rejected just because the subtitle says "French melody").
GENERIC_WORDS = {"theme", "song", "songs", "folk", "traditional", "march", "carol", "english", "melody", "tune",
                 "music", "piece", "round", "rhyme", "nursery", "classic", "classical", "french", "german",
                 "american", "italian", "russian", "spanish", "irish", "scottish", "sisters", "century"}


def answer_words(key):
    words = re.findall(r"[a-zà-ÿ]{4,}", (M[key]["name"] + " " + M[key]["sub"]).lower())
    return {w for w in words if w not in GENERIC_WORDS}


def _pick(data, *names):
    """Qwen sometimes renames keys ("Title", "video_title") or nests them; find the first string that matches."""
    if isinstance(data, dict):
        for k, v in data.items():
            if any(n in k.lower() for n in names) and isinstance(v, str) and v.strip(): return v
        for v in data.values():
            found = _pick(v, *names)
            if found: return found
    return None


def ask_qwen(row, key):
    """Return (title, hook) from Ollama, or None if unavailable/invalid."""
    if not CFG.get("use_ollama", True): return None
    import requests
    m = M[key]
    prompt = (
        "You write viral YouTube Shorts titles for 'Tunzle', a music guessing quiz channel.\n"
        f"The hidden answer is: {m['name']} ({m['sub']}). Difficulty: {row['level']}. Format: {row['format']}. Theme: {row['theme']}.\n"
        "Rules: NEVER reveal or hint the name, composer, film, game or brand. Title max 50 characters, exactly 1 emoji at the end. "
        "Do NOT invent facts about the song (no counts of notes, words, lines or years). Use a challenge/curiosity hook.\n"
        "Good titles: 'Only 10% Can Name This 🔴' | 'You Heard This As A Kid… Name It? 👶' | 'Name This Tune in 5 Seconds ⏱️' | "
        "'Everyone Knows It, Nobody Can Name It 🤔' | 'Bet You Can't Guess This One 😏' | 'Your Grandma Knows This Melody 👵'.\n"
        "Write a NEW title in that style (don't copy the examples). Hook: one short sentence inviting viewers to comment their guess before the reveal.\n"
        'Reply ONLY as JSON: {"title": "...", "hook": "..."}')
    bad = answer_words(key)
    tries = int(CFG.get("ollama_retries", 3))
    for attempt in range(1, tries + 1):
        try:
            # think=False: qwen3 otherwise "reasons" first, which is slow and sometimes breaks the JSON shape.
            r = requests.post(CFG["ollama_url"].rstrip("/") + "/api/generate",
                              json={"model": CFG["ollama_model"], "prompt": prompt, "stream": False, "format": "json",
                                    "think": False, "options": {"temperature": 0.9}}, timeout=120)
            r.raise_for_status()
            data = json.loads(r.json()["response"])
            title, hook = _pick(data, "title"), _pick(data, "hook")
            if not title or not hook: raise ValueError(f"missing title/hook in {data}")
            title, hook = title.strip().strip('"'), hook.strip()
        except requests.exceptions.ConnectionError as e:
            log("Ollama not reachable, using fallback:", e); return None
        except Exception as e:
            log(f"Qwen attempt {attempt}/{tries} invalid:", e); continue
        text = (title + " " + hook).lower()
        hits = sorted(w for w in bad if w in text)  # substring on purpose: also catches "spiders", "twinkling"
        if len(title) > 70 or hits:
            log(f"Qwen attempt {attempt}/{tries} rejected ({'too long' if not hits else 'reveals ' + ', '.join(hits)}):", title)
            continue
        return title, hook
    log("Qwen gave no usable title, using fallback"); return None


def fallback(row, key, i):
    pool = FALLBACK_TITLES["xmas"] if M[key]["cat"] == "xmas" else FALLBACK_TITLES.get(row["format"]) or FALLBACK_TITLES[row["level"]]
    title = pool[i % len(pool)]
    hook = {"Easy": "Can you name it before the reveal? Comment your answer!",
            "Medium": "Can you name it? Comment before the reveal!",
            "Hard": "HARD level 🔴 Comment your guess before the reveal!"}[row["level"]]
    return title, hook


def git(*args):
    subprocess.run(["git", "-C", REPO, *args], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="batch date YYYY-MM-DD (default: tomorrow)")
    ap.add_argument("--no-push", action="store_true"); ap.add_argument("--no-ollama", action="store_true")
    ap.add_argument("--force", action="store_true", help="re-render even if videos exist")
    a = ap.parse_args()
    if a.no_ollama: CFG["use_ollama"] = False
    day = a.date or (dt.date.today() + dt.timedelta(days=1)).isoformat()
    rows = [r for r in csv.DictReader(open(os.path.join(HERE, "calendar.csv"), encoding="utf-8")) if r["batch_date"] == day]
    if not rows: log("No calendar rows for", day); return
    vdir = os.path.join(REPO, "videos", day); os.makedirs(vdir, exist_ok=True)
    sdir = os.path.join(REPO, "schedule"); os.makedirs(sdir, exist_ok=True)
    posts = []
    for i, row in enumerate(rows):
        key, fmt, lvl = row["melody"], row["format"], row["level"]
        m = M[key]; fname = f"{day}_{row['slot']}_{key}_{fmt}.mp4"; out = os.path.join(vdir, fname)
        tag = {"three_notes": "HARD · 3 NOTES", "backwards": "HARD · BACKWARDS", "double_speed": "HARD · 2X SPEED"}.get(fmt, lvl.upper())
        prompt = FMT_PROMPT.get(fmt) or random.choice(PROMPTS[lvl])
        if a.force or not os.path.exists(out):
            log(f"rendering {fname}")
            render_short(dict(answer=m["name"], sub=m["sub"], tag=tag, prompt=prompt, notes=build(key, fmt)), out,
                         title_bottom="CHRISTMAS SONG" if m["cat"] == "xmas" else "MELODY", ffmpeg=CFG.get("ffmpeg", "ffmpeg"))
        title, hook = ask_qwen(row, key) or fallback(row, key, i)
        if "#shorts" not in title: title = f"{title} #shorts"
        posts.append({"post_datetime": f"{row['post_date']}T{row['time']}:00", "timezone": CFG["timezone"],
                      "video_url": f"{RAW}/videos/{day}/{fname}", "title": title, "description": hook + FOOTER,
                      "tags": ["guess the song", "guess the melody", "music quiz", m["name"].lower(), "quiz", "tunzle"],
                      "level": lvl, "format": fmt, "answer": m["name"]})
        log(f"  {row['time']}  {title}")
    sched = os.path.join(sdir, f"{day}.json")
    json.dump({"batch_date": day, "made_for_kids": False, "category": "ENTERTAINMENT", "posts": posts},
              open(sched, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    log("wrote", sched)
    if not a.no_push:
        git("pull", "--rebase", "--autostash")
        git("add", "videos", "schedule")
        subprocess.run(["git", "-C", REPO, "commit", "-m", f"Tunzle batch {day}"])
        git("push")
        log("pushed to GitHub — Claude's daily task will schedule these in Metricool")


if __name__ == "__main__":
    main()
