#!/usr/bin/env python3
"""Measurama height-comparison renderer (1920x1080, 30 fps).
Usage: python3 render_height.py out.mp4 [--test]
"""
import math, os, subprocess, sys, wave, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from data_tallest import BUILDINGS, REFERENCES

W, H, FPS, SR = 1920, 1080, 30, 44100
GROUND = 965
FIT = 610                      # px the focused item is scaled to
FOCUS_X = 0.60                 # focused item sits at 60% of screen width
AM = (255, 184, 28); AMD = (150, 105, 20); BG = (20, 20, 28); WHITE = (245, 245, 250); GREY = (150, 150, 165)
FB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tool", "fonts", "Poppins-Bold.ttf")
FM = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tool", "fonts", "Poppins-Medium.ttf")
_fc = {}
def font(path, s):
    k = (path, s)
    if k not in _fc: _fc[k] = ImageFont.truetype(path, s)
    return _fc[k]

INTRO, OUTRO, T_REF, T_BLD, T_MOVE = 5.0, 9.0, 5.0, 7.5, 1.7

# ---------------- items ----------------
def build_items(test=False):
    items = []
    for name, h, sub in REFERENCES:
        kind = {"Average adult": "human", "Statue of Liberty": "statue", "Great Pyramid of Giza": "pyramid", "Eiffel Tower": "eiffel"}[name]
        w = {"human": 0.55, "statue": 32, "pyramid": 230, "eiffel": 125}[kind]
        items.append(dict(kind=kind, name=name, h=h, w=w, sub=sub, rank=None, dur=T_REF))
    blds = sorted(BUILDINGS, key=lambda b: (b[2], -b[0]))
    if test: blds = blds[:3] + blds[-2:]
    for rank, name, h, year, city, country in blds:
        kind = "burj" if name == "Burj Khalifa" else "twin" if name == "Petronas Towers" else "merdeka" if name == "Merdeka 118" else "bld"
        w = h * (0.11 if kind != "twin" else 0.2)
        items.append(dict(kind=kind, name=name, h=h, w=w, rank=rank, year=year, city=city, country=country, dur=T_BLD,
                          seed=int(hashlib.md5(name.encode()).hexdigest()[:6], 16)))
    x = 0.0
    for i, it in enumerate(items):
        if i: x += items[i-1]["w"] / 2 + max(it["w"], items[i-1]["w"]) * 0.45 + it["w"] / 2
        it["x"] = x
    t = INTRO
    for it in items: it["t0"] = t; t += it["dur"]
    return items, t + OUTRO

# ---------------- shapes (local coords: x in metres from centre, y in metres up) ----------------
def shape_polys(it):
    h, w, k = it["h"], it["w"], it["kind"]
    if k == "human":
        return [("ell", (-0.11, 1.58, 0.11, 1.8)), ("poly", [(-0.2, 0), (-0.06, 0), (0, 0.8), (0.06, 0), (0.2, 0), (0.12, 0.9), (0.24, 1.45), (0.17, 1.55),
                 (-0.17, 1.55), (-0.24, 1.45), (-0.12, 0.9)])]
    if k == "statue":
        return [("poly", [(-16, 0), (16, 0), (16, 8), (11, 8), (9, 47), (-9, 47), (-11, 8), (-16, 8)]),
                ("poly", [(-5, 47), (5, 47), (4, 70), (6, 74), (8, 84), (9.5, 93), (7, 93), (5.5, 84), (3, 78), (1.5, 80), (-1.5, 80), (-4, 74)])]
    if k == "pyramid":
        return [("poly", [(-115, 0), (115, 0), (0, 138.5)])]
    if k == "eiffel":
        return [("poly", [(-62, 0), (-38, 0), (-28, 34), (28, 34), (38, 0), (62, 0), (40, 57), (22, 115), (12, 200), (5, 276), (2, 300), (1, 330),
                          (-1, 330), (-2, 300), (-5, 276), (-12, 200), (-22, 115), (-40, 57)]),
                ("cut", [(-26, 0), (26, 0), (20, 26), (-20, 26)])]
    def tiers(spec):  # list of (y_frac, half_width_frac) going up, mirrored
        L = [(-spec[0][1] * w, 0)]; R = [(spec[0][1] * w, 0)]
        for (y0, hw0), (y1, hw1) in zip(spec, spec[1:]):
            L += [(-hw0 * w, y1 * h), (-hw1 * w, y1 * h)]; R += [(hw0 * w, y1 * h), (hw1 * w, y1 * h)]
        return [("poly", R + L[::-1])]
    if k == "burj":
        return tiers([(0, .5), (.18, .42), (.34, .34), (.48, .27), (.6, .2), (.72, .14), (.81, .08), (.88, .035), (1.0, 0.0)])
    if k == "merdeka":
        return [("poly", [(-.5 * w, 0), (.5 * w, 0), (.38 * w, .5 * h), (.22 * w, .78 * h), (.03 * w, .8 * h), (.01 * w, h), (-.01 * w, h), (-.03 * w, .8 * h), (-.22 * w, .78 * h), (-.38 * w, .5 * h)])]
    if k == "twin":
        out = []
        for c in (-.27, .27):
            out += [("poly", [((c - .2) * w, 0), ((c + .2) * w, 0), ((c + .2) * w, .62 * h), ((c + .15) * w, .62 * h), ((c + .12) * w, .78 * h), ((c + .07) * w, .78 * h),
                              ((c + .05) * w, .86 * h), ((c + .01) * w, .86 * h), ((c + .005) * w, h), ((c - .005) * w, h), ((c - .01) * w, .86 * h), ((c - .05) * w, .86 * h),
                              ((c - .07) * w, .78 * h), ((c - .12) * w, .78 * h), ((c - .15) * w, .62 * h), ((c - .2) * w, .62 * h)])]
        out.append(("poly", [(-.07 * w, .40 * h), (.07 * w, .40 * h), (.07 * w, .43 * h), (-.07 * w, .43 * h)]))  # skybridge
        return out
    s = it["seed"]; style = s % 4
    if style == 0:   # setbacks + spire
        return tiers([(0, .5), (.7, .38), (.86, .26), (.95, .04), (1.0, 0)])
    if style == 1:   # tapered
        return [("poly", [(-.5 * w, 0), (.5 * w, 0), (.3 * w, .93 * h), (.12 * w, .97 * h), (0, h), (-.12 * w, .97 * h), (-.3 * w, .93 * h)])]
    if style == 2:   # slim box with crown
        return tiers([(0, .42), (.92, .36), (.97, .16), (1.0, .16)])
    return tiers([(0, .5), (.55, .44), (.8, .34), (.93, .22), (1.0, .22)])   # stepped block

# ---------------- background & music ----------------
def make_bg():
    g = np.linspace(0, 1, H)[:, None, None]
    a = (np.array([12, 13, 22]) * (1 - g) + np.array([26, 24, 34]) * g).repeat(W, 1).astype(np.uint8)
    im = Image.fromarray(a); d = ImageDraw.Draw(im)
    d.rectangle((0, GROUND, W, H), fill=(14, 14, 20)); d.line([(0, GROUND), (W, GROUND)], fill=AM, width=3)
    for i in range(0, W, 24):
        d.line([(i, GROUND), (i, GROUND + (14 if (i // 24) % 5 == 0 else 7))], fill=AMD, width=2)
    return im

def music(total):
    n = int(total * SR); t = np.arange(n) / SR; out = np.zeros(n, np.float32)
    prog = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]   # Am F C G
    seg = 8.0
    for k in range(int(total / seg) + 1):
        a, b = int(k * seg * SR), min(n, int((k + 1) * seg * SR + 2 * SR))
        if a >= n: break
        tt = t[a:b] - k * seg; env = np.clip(tt / 2.0, 0, 1) * np.clip((seg + 2 - tt) / 2.0, 0, 1)
        for m in prog[k % 4] + [prog[k % 4][0] - 12]:
            f = 440 * 2 ** ((m - 69) / 12)
            out[a:b] += (0.06 * env * (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 1.003 * tt))).astype(np.float32)
    out *= np.clip(t / 3, 0, 1) * np.clip((total - t) / 4, 0, 1)
    return out

def pluck(buf, at, midi=81):
    f = 440 * 2 ** ((midi - 69) / 12); n = int(1.2 * SR); tt = np.arange(n) / SR
    x = 0.12 * np.exp(-tt * 5) * np.sin(2 * np.pi * f * tt) * (1 - np.exp(-tt * 300)); i = int(at * SR)
    buf[i:i + n] += x[:len(buf) - i].astype(np.float32)

# ---------------- camera ----------------
def ease(u): return u * u * (3 - 2 * u)

def camera(items, t):
    idx = 0
    for i, it in enumerate(items):
        if t >= it["t0"]: idx = i
    cur = items[idx]
    tgt = (cur["x"], FIT / cur["h"])
    if idx == 0 or t < INTRO:
        return idx, tgt, 1.0
    prev = items[idx - 1]; u = min(1.0, (t - cur["t0"]) / T_MOVE); e = ease(u)
    x = prev["x"] + (cur["x"] - prev["x"]) * e
    s = math.exp(math.log(FIT / prev["h"]) * (1 - e) + math.log(FIT / cur["h"]) * e)
    return idx, (x, s), u

def nice_step(s):
    for st in [0.25, 0.5, 1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500]:
        if st * s >= 70: return st
    return 1000

# ---------------- drawing ----------------
def draw_item(d, it, cam, focus, alpha_focus):
    cx, s = cam; sx0 = W * FOCUS_X + (it["x"] - cx) * s
    if sx0 + it["w"] * s < -50 or sx0 - it["w"] * s > W + 50: return
    fill = (40, 40, 54) if not focus else tuple(int(a * alpha_focus + b * (1 - alpha_focus)) for a, b in zip(AM, (40, 40, 54)))
    edge = AM if focus else AMD
    for typ, data in shape_polys(it):
        if typ == "ell":
            x0, y0, x1, y1 = data; d.ellipse((sx0 + x0 * s, GROUND - y1 * s, sx0 + x1 * s, GROUND - y0 * s), fill=fill, outline=edge)
        else:
            pts = [(sx0 + x * s, GROUND - y * s) for x, y in data]
            if typ == "cut": d.polygon(pts, fill=(20, 20, 28))
            else: d.polygon(pts, fill=fill, outline=edge, width=2)
    if focus and it["kind"] in ("bld", "burj", "merdeka", "twin") and it["h"] * s > 300:
        step = 4 * 4.0 * s   # a line every ~4 floors (4 m per floor)
        y = GROUND - step
        while y > GROUND - it["h"] * s * 0.82:
            d.line([(sx0 - it["w"] * s * 0.36, y), (sx0 + it["w"] * s * 0.36, y)], fill=(200, 140, 20) if alpha_focus > .5 else (60, 60, 76), width=1)
            y -= step

def ruler(d, s, items_vis_max):
    st = nice_step(s); d.line([(78, GROUND), (78, 70)], fill=GREY, width=2)
    v = 0.0
    while GROUND - v * s > 70:
        y = GROUND - v * s
        d.line([(78, y), (98, y)], fill=GREY, width=2)
        lab = (f"{v:g} m")
        d.text((104, y - 14), lab, font=font(FM, 20), fill=GREY)
        v += st

def label(d, it, a):
    if a <= 0: return
    c = lambda col: tuple(int(v * a + b * (1 - a)) for v, b in zip(col, (22, 22, 30)))
    x0, y0 = 1210, 70
    d.rounded_rectangle((x0, y0, 1860, y0 + 250), 22, fill=(22, 22, 30), outline=c(AMD), width=2)
    tag = f"#{it['rank']}" if it["rank"] else "FOR SCALE"
    d.text((x0 + 30, y0 + 18), tag, font=font(FB, 54 if it["rank"] else 34), fill=c(AM))
    s = 46
    while d.textlength(it["name"], font=font(FB, s)) > 590: s -= 2
    d.text((x0 + 30, y0 + 88), it["name"], font=font(FB, s), fill=c(WHITE))
    sub = f"{it['city']} · {it['country']} · {it['year']}" if it["rank"] else it["sub"]
    d.text((x0 + 32, y0 + 146), sub, font=font(FM, 26), fill=c(GREY))
    hm = it["h"]; ft = hm * 3.28084
    hs = f"{hm:g} m  ·  {ft:,.0f} ft" if hm >= 10 else f"{hm:g} m  ·  {ft:.1f} ft"
    d.text((x0 + 30, y0 + 186), hs, font=font(FB, 40), fill=c(AM))

def height_marker(d, it, cam, a):
    if a <= 0: return
    cx, s = cam; sx = W * FOCUS_X + (it["x"] - cx) * s; y = GROUND - it["h"] * s
    x = 172
    while x < sx - it["w"] * s * 0.6:
        d.line([(x, y), (min(x + 14, sx), y)], fill=AM, width=2); x += 26

def title_card(img, title, sub, a=1.0):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((W / 2 - 120, 230, W / 2 + 120, 470), 36, fill=AM)
    f = font(FB, 170); w = d.textlength("M", font=f); d.text((W / 2 - w / 2, 243), "M", font=f, fill=BG)
    for i in range(9): x = W / 2 - 82 + i * 20.5; d.line([(x, 438), (x, 438 - (16 if i % 4 == 0 else 9))], fill=BG, width=4)
    d.line([(W / 2 - 82, 438), (W / 2 + 82, 438)], fill=BG, width=4)
    for txt, fnt, col, y in [(title, font(FB, 78), WHITE, 530), (sub, font(FM, 36), AM, 640)]:
        w = d.textlength(txt, font=fnt); d.text((W / 2 - w / 2, y), txt, font=fnt, fill=col)

def main(out, test=False):
    items, total = build_items(test)
    bg = make_bg()
    audio = music(total)
    for it in items: pluck(audio, it["t0"] + 0.2, 81 if it["rank"] else 76)
    audio = audio / max(1e-6, np.abs(audio).max()) * 0.6
    wav = out + ".wav"
    with wave.open(wav, "wb") as wv:
        wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((audio * 32767).astype(np.int16).tobytes())
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                          "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    nfr = int(total * FPS); end_t = items[-1]["t0"] + items[-1]["dur"]
    for fi in range(nfr):
        t = fi / FPS; img = bg.copy(); d = ImageDraw.Draw(img)
        if t < INTRO:
            title_card(img, "TALLEST BUILDINGS IN THE WORLD", "Height comparison · from 1.8 m to 828 m")
        else:
            if t < end_t:
                idx, cam, u = camera(items, t)
            else:  # outro: zoom out to show everything
                e = ease(min(1, (t - end_t) / 3)); last = items[-1]
                mid = (items[4]["x"] + last["x"]) / 2; span = last["x"] - items[4]["x"] + last["w"] * 2
                s_all = min(FIT / last["h"], W * 0.92 / span)
                cam = (last["x"] + (mid + (W * (FOCUS_X - 0.5)) / s_all - last["x"]) * e,
                       math.exp(math.log(FIT / last["h"]) * (1 - e) + math.log(s_all) * e)); idx = len(items) - 1; u = 1
            a = 0 if t >= end_t else max(0.0, min(1.0, (u - 0.75) / 0.25)) if idx > 0 else min(1, (t - INTRO) / 0.6)
            for i, it in enumerate(items):
                if i < idx: draw_item(d, it, cam, False, 0)
            draw_item(d, items[idx], cam, t < end_t, a if idx > 0 else max(a, 0.0))
            d.rectangle((0, 0, 168, GROUND - 2), fill=(16, 16, 24)); d.line([(168, 60), (168, GROUND)], fill=(40, 40, 52), width=2)
            ruler(d, cam[1], 0)
            if t < end_t:
                height_marker(d, items[idx], cam, a); label(d, items[idx], a)
                pr = (t - INTRO) / (end_t - INTRO); d.rectangle((0, H - 6, W * pr, H), fill=AM)
            else:
                ov = min(1, (t - end_t - 2.5) / 1.0)
                if ov > 0:
                    d.rounded_rectangle((W / 2 - 520, 80, W / 2 + 520, 290), 26, fill=(22, 22, 30), outline=AM, width=3)
                    for txt, fnt, col, y in [("Which one surprised you?", font(FB, 54), WHITE, 108),
                                             ("Subscribe to Measurama · the world, measured.", font(FM, 34), AM, 200)]:
                        w = d.textlength(txt, font=fnt); d.text((W / 2 - w / 2, y), txt, font=fnt, fill=col)
        p.stdin.write(img.tobytes())
        if fi % 900 == 0: print(f"frame {fi}/{nfr}", flush=True)
    p.stdin.close(); p.wait(); os.remove(wav)
    print("wrote", out, f"{total:.0f}s")

if __name__ == "__main__":
    main(sys.argv[1], "--test" in sys.argv)
