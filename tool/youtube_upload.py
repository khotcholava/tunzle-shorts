#!/usr/bin/env python3
"""Tunzle YouTube uploader: the small part of Metricool we actually need.

Reads every schedule/<date>.json, uploads each Short that isn't uploaded yet straight to
YouTube with the Data API, and lets YouTube publish it at its post_datetime
(the video is uploaded as private with publishAt, YouTube flips it to public on time).
Posts whose time has already passed are published right away.

What has been uploaded is recorded in schedule/uploaded.json, so every post goes up once.

Credentials come from environment variables (GitHub Actions secrets):
  YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN   -> get them with youtube_auth.py

Usage:
  python youtube_upload.py --dry-run                # show what would be uploaded
  python youtube_upload.py                          # upload (max 5 per run, see --max)
  python youtube_upload.py --since 2026-11-13       # ignore posts due before this date
  python youtube_upload.py --mark-done 2026-11-12   # record posts due before this date as already
                                                    # uploaded (e.g. you uploaded them by hand)

Quota: a video upload costs 1600 of the default 10,000 daily API units, so at most 6 uploads
a day fit. --max defaults to 5 (one batch). Upcoming posts go first, overdue ones after.
"""
import argparse, datetime as dt, glob, json, os, sys, time
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
SCHED = os.path.join(REPO, "schedule")
STATE = os.path.join(SCHED, "uploaded.json")
TZ = dt.timezone(dt.timedelta(hours=4))  # Asia/Tbilisi, UTC+4 all year
CATEGORY = {"ENTERTAINMENT": "24", "MUSIC": "10", "EDUCATION": "27", "GAMING": "20", "COMEDY": "23"}


def log(*a): print("[youtube]", *a, flush=True)


def load_state():
    try:
        return json.load(open(STATE, encoding="utf-8"))
    except FileNotFoundError:
        return {}


def save_state(state):
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(dict(sorted(state.items())), f, ensure_ascii=False, indent=2)
        f.write("\n")


def all_posts():
    posts = []
    for path in sorted(glob.glob(os.path.join(SCHED, "????-??-??.json"))):
        batch = json.load(open(path, encoding="utf-8"))
        for p in batch["posts"]:
            p = dict(p)
            p["_key"] = p["video_url"].rsplit("/", 1)[-1]
            p["_file"] = os.path.join(REPO, p["video_url"].split("/main/", 1)[1])
            p["_when"] = dt.datetime.fromisoformat(p["post_datetime"]).replace(tzinfo=TZ)
            p["_category"] = batch.get("category", "ENTERTAINMENT")
            p["_kids"] = bool(batch.get("made_for_kids", False))
            posts.append(p)
    return posts


def access_token():
    need = ["YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN"]
    missing = [k for k in need if not os.environ.get(k)]
    if missing:
        return None, missing
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}, timeout=30)
    if r.status_code != 200:
        sys.exit(f"[youtube] could not refresh the Google token ({r.status_code}): {r.text}\n"
                 "If it says invalid_grant, the refresh token expired or was revoked: run youtube_auth.py again "
                 "and update the YT_REFRESH_TOKEN secret.")
    return r.json()["access_token"], []


def clean(text, limit):
    text = text.replace("<", "").replace(">", "")  # YouTube rejects angle brackets
    return text[:limit]


def fit_tags(tags, limit=450):
    out, used = [], 0
    for t in tags:
        t = clean(t, 100)
        cost = len(t) + (2 if " " in t else 0) + (1 if out else 0)
        if used + cost > limit:
            break
        out.append(t); used += cost
    return out


def metadata(p, now):
    status = {"selfDeclaredMadeForKids": p["_kids"], "containsSyntheticMedia": False,
              "embeddable": True, "license": "youtube"}
    if p["_when"] > now + dt.timedelta(minutes=15):
        status["privacyStatus"] = "private"
        status["publishAt"] = p["_when"].astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    else:
        status["privacyStatus"] = "public"
    return {"snippet": {"title": clean(p["title"], 100), "description": clean(p["description"], 5000),
                        "tags": fit_tags(p.get("tags", [])), "categoryId": CATEGORY.get(p["_category"], "24")},
            "status": status}


def upload(token, p, meta):
    size = os.path.getsize(p["_file"])
    r = requests.post("https://www.googleapis.com/upload/youtube/v3/videos",
                      params={"uploadType": "resumable", "part": "snippet,status"},
                      headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=UTF-8",
                               "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)},
                      data=json.dumps(meta), timeout=60)
    if r.status_code != 200:
        raise RuntimeError(f"start upload failed ({r.status_code}): {r.text}")
    url = r.headers["Location"]
    for attempt in range(4):
        with open(p["_file"], "rb") as f:
            r = requests.put(url, data=f, headers={"Content-Type": "video/mp4", "Content-Length": str(size)},
                             timeout=600)
        if r.status_code in (200, 201):
            return r.json()["id"]
        if r.status_code in (500, 502, 503, 504):
            time.sleep(5 * (attempt + 1)); continue
        break
    raise RuntimeError(f"upload failed ({r.status_code}): {r.text}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max", type=int, default=5, help="max uploads this run (quota: about 6 a day)")
    ap.add_argument("--since", help="ignore posts due before this date (YYYY-MM-DD)")
    ap.add_argument("--mark-done", metavar="DATE", help="record posts due before DATE as uploaded, then exit")
    a = ap.parse_args()

    state, now = load_state(), dt.datetime.now(TZ)
    posts = all_posts()

    if a.mark_done:
        cut = dt.datetime.fromisoformat(a.mark_done).replace(tzinfo=TZ)
        n = 0
        for p in posts:
            if p["_when"] < cut and p["_key"] not in state:
                state[p["_key"]] = {"video_id": None, "note": "marked done (uploaded elsewhere)",
                                    "post_datetime": p["post_datetime"]}
                n += 1
        save_state(state); log(f"marked {n} posts before {a.mark_done} as done"); return

    todo = [p for p in posts if p["_key"] not in state]
    if a.since:
        cut = dt.datetime.fromisoformat(a.since).replace(tzinfo=TZ)
        todo = [p for p in todo if p["_when"] >= cut]
    # upcoming first (soonest first), then overdue (oldest first)
    upcoming = sorted([p for p in todo if p["_when"] > now], key=lambda p: p["_when"])
    overdue = sorted([p for p in todo if p["_when"] <= now], key=lambda p: p["_when"])
    queue = (upcoming + overdue)[:a.max]
    log(f"{len(upcoming)} upcoming, {len(overdue)} overdue not on YouTube yet; uploading {len(queue)} this run")

    if a.dry_run:
        for p in queue:
            m = metadata(p, now)
            log(f"would upload {p['_key']}  {m['status'].get('publishAt', 'publish now')}  {m['snippet']['title']}")
        return

    token, missing = access_token()
    if token is None:
        log("YouTube credentials not set (" + ", ".join(missing) + "); nothing uploaded. See README.")
        return

    failed = 0
    for p in queue:
        meta = metadata(p, now)
        try:
            vid = upload(token, p, meta)
        except Exception as e:
            if "quotaExceeded" in str(e) or "uploadLimitExceeded" in str(e):
                log("daily YouTube limit reached; the rest go up on the next run"); break
            failed += 1
            log(f"FAILED {p['_key']}: {e}")
            continue
        state[p["_key"]] = {"video_id": vid, "url": f"https://youtube.com/shorts/{vid}",
                            "post_datetime": p["post_datetime"], "publish_at": meta["status"].get("publishAt"),
                            "uploaded_at": now.isoformat(timespec="seconds")}
        save_state(state)
        log(f"uploaded {p['_key']} -> https://youtube.com/shorts/{vid}  ({meta['status'].get('publishAt', 'public now')})")
    if failed:
        sys.exit(f"[youtube] {failed} upload(s) failed")


if __name__ == "__main__":
    main()
