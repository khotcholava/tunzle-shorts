"""Tunzle renderer (bright style).
Usage: python3 make_tunzle.py episode.json out.mp4
episode.json: {"title_top": "GUESS THE", "title_bottom": "MELODY", "rounds": [
   {"answer": "...", "hint": "optional", "notes": [[t, midi, dur_optional], ...]}  or
   {"answer": "...", "audio": "clip.mp3", "start": 0}]}
"""
import json, math, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont
SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__))

W, H, FPS = 1080, 1920, 30
F = os.path.join(HERE, "fonts", "Poppins-Bold.ttf")
INTRO, LISTEN, COUNT, REVEAL, OUTRO = 0.3, 8.0, 2.1, 3.0, 0.0
RL = INTRO + LISTEN + COUNT + REVEAL
NAVY = (30, 27, 75); WHITE = (255, 255, 255)
CANDY = [(255, 82, 119), (255, 159, 28), (255, 214, 10), (46, 196, 182), (58, 134, 255), (157, 78, 221), (255, 112, 166), (120, 210, 90)]
NST = 8
_fc = {}
def font(s):
    if s not in _fc: _fc[s] = ImageFont.truetype(F, s)
    return _fc[s]

# ---------- audio ----------
def tone(midi, dur):
    f = 440 * 2 ** ((midi - 69) / 12); n = int(SR * (dur + 0.6)); t = np.arange(n) / SR
    env = np.exp(-t * 4.5) * (1 - np.exp(-t * 500))
    s = (np.sin(2*np.pi*f*t) + 0.4*np.sin(2*np.pi*2*f*t)*np.exp(-t*6) + 0.25*np.sin(2*np.pi*4*f*t)*np.exp(-t*16)
         + 0.1*np.sin(2*np.pi*f*7.1*t)*np.exp(-t*40))
    return (s * env * 0.22).astype(np.float32)

def render(notes, length):
    b = np.zeros(int(SR*(length+2)), np.float32)
    for n in notes:
        t, m = n[0], n[1]; d = n[2] if len(n) > 2 else 0.3
        x = tone(m, d); i = int(t*SR); b[i:i+len(x)] += x
    b = b[:int(SR*length)]; fade = int(SR*.3); b[-fade:] *= np.linspace(1, 0, fade)
    return b

def ding():
    return render([[0, 84, .2], [0.1, 88, .2], [0.2, 91, .5]], 1.2) * 1.4

# ---------- visuals ----------
def bg():
    g = np.linspace(0, 1, H)[:, None, None]
    a = (np.array([120, 220, 255])*(1-g) + np.array([80, 140, 255])*g).repeat(W, 1).astype(np.uint8)
    im = Image.fromarray(a); d = ImageDraw.Draw(im)
    rng = np.random.default_rng(4)
    for _ in range(70):
        x, y = rng.uniform(0, W), rng.uniform(0, H); r = rng.uniform(5, 11); c = CANDY[rng.integers(len(CANDY))]
        c = tuple(int(v*.55 + 255*.45*0 + a[int(min(y,H-1)), 0, i]*.45) for i, v in enumerate(c))
        if rng.random() < .5: d.ellipse((x-r, y-r, x+r, y+r), fill=c)
        else: d.rounded_rectangle((x-r*1.7, y-r*.6, x+r*1.7, y+r*.6), r*.5, fill=c)
    d.ellipse((-300, 1640, 700, 2300), fill=(255, 214, 10)); d.ellipse((450, 1680, 1450, 2350), fill=(255, 159, 28))
    return im

def step_rect(k):
    x0 = 95 + k*110; y0 = 640 + k*98
    return x0, y0, x0+118, y0+32

def ctext(d, y, s, size, fill, stroke=0, sc=NAVY):
    f = font(size); w = d.textlength(s, font=f)
    d.text(((W-w)/2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=sc)

def pill(d, y, s, size, fg=WHITE, bgc=NAVY, padx=34, pady=14):
    f = font(size); w = d.textlength(s, font=f)
    d.rounded_rectangle(((W-w)/2-padx, y-pady+4, (W+w)/2+padx, y+size*1.25+pady), 60, fill=bgc)
    d.text(((W-w)/2, y), s, font=f, fill=fg)

def marble(d, x, y, r, c):
    d.ellipse((x-r-6, y-r-6, x+r+6, y+r+6), fill=NAVY); d.ellipse((x-r, y-r, x+r, y+r), fill=c)
    d.chord((x-r, y-r, x+r, y+r), 20, 160, fill=tuple(int(v*.78) for v in c))
    d.ellipse((x-r*.55, y-r*.6, x-r*.1, y-r*.2), fill=WHITE)

def header(d, cfg, ri, n):
    ctext(d, 120, cfg["title_top"], 104, WHITE, 9)
    sz = 128
    while d.textlength(cfg["title_bottom"], font=font(sz)) > 1000: sz -= 6
    ctext(d, 245 + (128-sz)//2, cfg["title_bottom"], sz, (255, 214, 10), 10)
    pill(d, 420, cfg["rounds"][ri].get("tag", f"LEVEL {ri+1}"), 44, NAVY, (255, 214, 10))

def frame(base, cfg, ri, rnd, tr, ev):
    im = base.copy(); d = ImageDraw.Draw(im); header(d, cfg, ri, len(cfg["rounds"]))
    tl = tr - INTRO
    for k in range(NST):
        x0, y0, x1, y1 = step_rect(k); c = CANDY[k]
        lit = max([max(0, 1-(tl-t)/0.3) for t, s in ev if s == k and 0 <= tl-t] + [0])
        dy = 10*lit
        d.rounded_rectangle((x0-6, y0-6+dy, x1+6, y1+6+dy), 20, fill=NAVY)
        cc = tuple(int(v + (255-v)*0.5*lit) for v in c)
        d.rounded_rectangle((x0, y0+dy, x1, y1+dy), 16, fill=cc)
    FALL = 0.5
    for t, s in ev:
        dt = tl - t
        if -FALL < dt < 0.55:
            x0, y0, x1, _ = step_rect(s); cx = (x0+x1)/2; land = y0 - 30
            if dt < 0:
                p = 1 + dt/FALL; y = land - min(380, land-560)*(1-p*p); x = cx - 30*(1-p); r = 26
            else:
                y = land - 240*dt + 1100*dt*dt; x = cx + 170*dt; r = 26*max(0, 1-dt/0.55)
            if r > 3: marble(d, x, y, r, CANDY[(s+3) % len(CANDY)])
    if tr < INTRO:
        pill(d, 1520, "LISTEN... 🎧".replace(" 🎧", ""), 72)
    elif tr < INTRO+LISTEN:
        p = (tr-INTRO)/LISTEN
        d.rounded_rectangle((134, 1514, 946, 1566), 26, fill=NAVY)
        d.rounded_rectangle((140, 1520, 140+800*p, 1560), 20, fill=(255, 214, 10))
        ctext(d, 1590, rnd.get("prompt", "Name this melody!"), 60, WHITE, 6)
        if rnd.get("hint") and p > 0.55: pill(d, 1700, "Hint: " + rnd["hint"], 40, NAVY, WHITE)
    elif tr < INTRO+LISTEN+COUNT:
        x = (tr-INTRO-LISTEN)/COUNT*3; n = 3 - int(x); fr = x % 1
        ctext(d, 1440 + 30*fr, str(n), int(250 - 70*fr), (255, 82, 119), 12)
    else:
        pill(d, 1450, "ANSWER", 44, NAVY, (255, 214, 10))
        s = 96
        while d.textlength(rnd["answer"], font=font(s)) > 1000: s -= 4
        ctext(d, 1540, rnd["answer"], s, WHITE, 9)
        if rnd.get("sub"): ctext(d, 1545 + s*1.3, rnd["sub"], 44, NAVY)
        ctext(d, 1790, "Got it? Follow @tunzlequiz", 50, WHITE, 6)
    return im

def outro(base, cfg):
    im = base.copy(); d = ImageDraw.Draw(im)
    ctext(d, 560, "HOW MANY", 130, WHITE, 10); ctext(d, 710, "DID YOU GET?", 130, (255, 214, 10), 10)
    pill(d, 940, f"Comment your score  ?/{len(cfg['rounds'])}", 56)
    ctext(d, 1080, "Follow @tunzlequiz", 66, WHITE, 7); ctext(d, 1170, "for the next round!", 66, WHITE, 7)
    return im

def render_short(rnd, out, title_top="GUESS THE", title_bottom="MELODY", ffmpeg="ffmpeg"):
    """rnd: dict(answer, sub, tag, prompt, notes=[[t, midi, dur], ...]) -> writes out (.mp4)"""
    cfg = {"title_top": title_top, "title_bottom": title_bottom, "rounds": [rnd]}
    notes = [n for n in rnd["notes"] if n[0] < LISTEN+COUNT-0.4]
    a = render(notes, LISTEN+COUNT)
    ps = sorted({n[1] for n in notes}, reverse=True); lo, hi = min(ps), max(ps)
    ev = [(n[0], int(round((hi-n[1])/(max(1, hi-lo))*(NST-1)))) for n in notes]
    seg = np.zeros(int(SR*RL), np.float32); i = int(SR*INTRO); seg[i:i+len(a)] += a
    dg = ding(); j = int(SR*(INTRO+LISTEN+COUNT)); seg[j:j+len(dg)] += dg[:len(seg)-j]
    audio = seg / max(1, np.abs(seg).max()/0.9)
    wav = out + ".wav"
    with wave.open(wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(audio, -1, 1)*32767).astype(np.int16).tobytes())
    base = bg(); total = RL
    p = subprocess.Popen([ffmpeg, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-shortest", out], stdin=subprocess.PIPE)
    for fi in range(int(total*FPS)):
        p.stdin.write(frame(base, cfg, 0, rnd, fi/FPS, ev).tobytes())
    p.stdin.close(); p.wait(); os.remove(wav)
    if p.returncode != 0: raise RuntimeError("ffmpeg failed for " + out)
