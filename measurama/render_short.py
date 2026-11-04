#!/usr/bin/env python3
"""Measurama vertical Shorts renderer v2 (1080x1920, 30 fps).
Usage: python3 render_short.py <topic_id|all> <out_dir>
Topics live in topics.py. Kinds: bld burj merdeka twin eiffel statue pyramid human
mountain tower rocket figure planet earth saturn sun
"""
import math, os, subprocess, sys, wave, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from render_height import shape_polys as _bld_polys, music, pluck, ease, AM, AMD, BG, WHITE, GREY, FB, FM
from topics import SHORTS

W, H, FPS, SR = 1080, 1920, 30, 44100
GROUND = 1500
FIT = 820
FOCUS_X = 0.58
PANEL = 120
T_ITEM, T_MOVE, OUTRO = 4.6, 1.3, 4.0
CIRCLES = {"planet", "earth", "saturn", "sun"}
_fc = {}
def font(path, s):
    if (path, s) not in _fc: _fc[(path, s)] = ImageFont.truetype(path, s)
    return _fc[(path, s)]

WIDTH = {"human": lambda h: 0.55, "statue": lambda h: 32, "pyramid": lambda h: 230, "eiffel": lambda h: 125,
         "bld": lambda h: h * .11, "burj": lambda h: h * .11, "merdeka": lambda h: h * .11, "twin": lambda h: h * .2,
         "mountain": lambda h: h * 1.25, "tower": lambda h: h * .12, "rocket": lambda h: h * .16, "figure": lambda h: h * .32,
         "planet": lambda h: h, "earth": lambda h: h, "sun": lambda h: h, "saturn": lambda h: h * 2.1}

def build_items(spec):
    items = []
    for name, h, kind, tag, sub in spec["items"]:
        items.append(dict(name=name, h=h, kind=kind, tag=tag, sub=sub, w=WIDTH[kind](h), seed=int(hashlib.md5(name.encode()).hexdigest()[:6], 16)))
    x = 0.0
    for i, it in enumerate(items):
        if i: x += items[i-1]["w"] / 2 + max(it["w"], items[i-1]["w"]) * 0.3 + it["w"] / 2
        it["x"] = x; it["t0"] = i * T_ITEM
    return items, len(items) * T_ITEM + OUTRO

def polys(it):
    h, w, k = it["h"], it["w"], it["kind"]
    if k in ("bld", "burj", "merdeka", "twin", "eiffel", "statue", "pyramid", "human"):
        return _bld_polys(it)
    if k == "mountain":
        rng = np.random.RandomState(it["seed"] % 2**31); n = 10
        left, right = [(-w / 2, 0)], [(w / 2, 0)]
        for i in range(1, n):
            f = i / n; jag = (1 if i % 2 else -1) * 0.035
            left.append((-(1 - f) * w / 2 + rng.uniform(-.02, .02) * w, min(.97, f + jag * rng.rand()) * h))
            right.append(((1 - f) * w / 2 + rng.uniform(-.02, .02) * w, min(.97, f - jag * rng.rand()) * h))
        pts = left + [(0, h)] + right[::-1]
        return [("poly", pts), ("snow", [(-w * .085, h * .83), (-w * .04, h * .86), (-w * .02, h * .82), (0, h), (w * .03, h * .85), (w * .08, h * .84), (w * .05, h * .87), (0, h)])]
    if k == "tower":
        return [("poly", [(-.5 * w, 0), (.5 * w, 0), (.12 * w, .62 * h), (.08 * w, .66 * h), (.06 * w, .8 * h), (.02 * w, .82 * h), (.01 * w, h), (-.01 * w, h),
                          (-.02 * w, .82 * h), (-.06 * w, .8 * h), (-.08 * w, .66 * h), (-.12 * w, .62 * h)]),
                ("poly", [(-.4 * w, .66 * h), (.4 * w, .66 * h), (.3 * w, .72 * h), (-.3 * w, .72 * h)])]
    if k == "rocket":
        b = .22 * w
        return [("poly", [(-b, 0), (b, 0), (b, .82 * h), (.6 * b, .92 * h), (0, h), (-.6 * b, .92 * h), (-b, .82 * h)]),
                ("poly", [(-b, 0), (-.5 * w, 0), (-b, .18 * h)]), ("poly", [(b, 0), (.5 * w, 0), (b, .18 * h)])]
    if k == "figure":   # scaled human silhouette with a raised arm
        s = h / 1.8
        return [("ell", (-0.11 * s, 1.58 * s, 0.11 * s, 1.8 * s)),
                ("poly", [(x * s, y * s) for x, y in [(-0.2, 0), (-0.06, 0), (0, 0.8), (0.06, 0), (0.2, 0), (0.12, 0.9), (0.24, 1.45), (0.17, 1.55),
                                                       (-0.17, 1.55), (-0.24, 1.45), (-0.12, 0.9)]]),
                ("poly", [(x * s, y * s) for x, y in [(0.17, 1.5), (0.26, 1.48), (0.36, 1.78), (0.3, 1.8)]])]
    return []

def make_bg(space):
    g = np.linspace(0, 1, H)[:, None, None]
    top, bot = ((5, 6, 14), (14, 12, 26)) if space else ((12, 13, 22), (26, 24, 34))
    a = (np.array(top) * (1 - g) + np.array(bot) * g).repeat(W, 1).astype(np.uint8)
    im = Image.fromarray(a); d = ImageDraw.Draw(im)
    if space:
        rng = np.random.RandomState(7)
        for _ in range(260):
            x, y, r = rng.randint(0, W), rng.randint(0, GROUND), rng.choice([1, 1, 1, 2]); c = int(rng.randint(90, 220))
            d.ellipse((x - r, y - r, x + r, y + r), fill=(c, c, c + 20 if c < 235 else c))
    d.rectangle((0, GROUND, W, H), fill=(14, 14, 20)); d.line([(0, GROUND), (W, GROUND)], fill=AM, width=3)
    for i in range(0, W, 24):
        d.line([(i, GROUND), (i, GROUND + (14 if (i // 24) % 5 == 0 else 7))], fill=AMD, width=2)
    return im

def fit(it): return min(FIT / it["h"], (W - PANEL - 140) / it["w"])

def camera(items, t):
    idx = max(i for i, it in enumerate(items) if t >= it["t0"])
    cur = items[idx]
    if idx == 0: return idx, (cur["x"], fit(cur)), 1.0
    prev = items[idx - 1]; u = min(1.0, (t - cur["t0"]) / T_MOVE); e = ease(u)
    x = prev["x"] + (cur["x"] - prev["x"]) * e
    s = math.exp(math.log(fit(prev)) * (1 - e) + math.log(fit(cur)) * e)
    return idx, (x, s), u

def sx_of(it, cam): return W * FOCUS_X + (it["x"] - cam[0]) * cam[1]

def mix(c1, c2, a): return tuple(int(p * a + q * (1 - a)) for p, q in zip(c1, c2))
PLANET_COL = {"Mercury": (170, 160, 150), "Venus": (225, 190, 120), "Earth": (70, 130, 220), "Mars": (205, 95, 60), "Jupiter": (210, 170, 125),
              "Saturn": (225, 200, 140), "Uranus": (150, 215, 225), "Neptune": (80, 120, 230), "Moon": (190, 190, 195), "Pluto": (215, 190, 165),
              "Sun": (255, 190, 60), "Io": (230, 210, 110), "Europa": (215, 200, 180), "Ganymede": (170, 160, 150), "Callisto": (120, 110, 100), "Titan": (220, 170, 90)}

def draw_item(d, it, cam, focus, a):
    s = cam[1]; sx0 = sx_of(it, cam)
    if sx0 + it["w"] * s < -50 or sx0 - it["w"] * s > W + 50: return
    if it["kind"] in CIRCLES:
        r = it["h"] / 2 * s; cy = GROUND - r
        base = PLANET_COL.get(it["name"], (180, 180, 190)); dim = mix(base, (30, 30, 40), 0.35)
        col = mix(base, dim, a) if focus else dim
        if r < 1.2: d.ellipse((sx0 - 1.5, GROUND - 3, sx0 + 1.5, GROUND), fill=col); return
        if it["kind"] == "saturn":
            d.ellipse((sx0 - r * 2.05, cy - r * .42, sx0 + r * 2.05, cy + r * .42), outline=mix((235, 215, 160), (60, 60, 70), a if focus else 0), width=max(2, int(r * .09)))
        d.ellipse((sx0 - r, cy - r, sx0 + r, cy + r), fill=col, outline=AM if focus else AMD, width=2)
        if it["kind"] == "earth" and r > 8:
            for (ox, oy, rr) in [(-.3, -.25, .35), (.25, .15, .3), (-.1, .45, .2)]:
                d.ellipse((sx0 + (ox - rr) * r, cy + (oy - rr) * r, sx0 + (ox + rr) * r, cy + (oy + rr) * r), fill=mix((70, 160, 90), col, .8))
        if it["kind"] == "saturn":   # front half of ring over the planet
            d.arc((sx0 - r * 2.05, cy - r * .42, sx0 + r * 2.05, cy + r * .42), 0, 180, fill=mix((235, 215, 160), (60, 60, 70), a if focus else 0), width=max(2, int(r * .09)))
        return
    fill = (40, 40, 54) if not focus else mix(AM, (40, 40, 54), a)
    edge = AM if focus else AMD
    if it["kind"] == "mountain" and not focus: fill = (44, 42, 58)
    for typ, data in polys(it):
        if typ == "ell":
            x0, y0, x1, y1 = data; d.ellipse((sx0 + x0 * s, GROUND - y1 * s, sx0 + x1 * s, GROUND - y0 * s), fill=fill, outline=edge)
        else:
            pts = [(sx0 + x * s, GROUND - y * s) for x, y in data]
            if typ == "cut": d.polygon(pts, fill=(20, 20, 28))
            elif typ == "snow": d.polygon(pts, fill=mix((250, 248, 240), fill, 0.85 if focus else 0.35))
            else: d.polygon(pts, fill=fill, outline=edge, width=2)
    if focus and it["kind"] in ("bld", "burj", "merdeka", "twin") and it["h"] * s > 300:
        step = 16.0 * s; y = GROUND - step
        while y > GROUND - it["h"] * s * 0.82:
            d.line([(sx0 - it["w"] * s * 0.36, y), (sx0 + it["w"] * s * 0.36, y)], fill=(200, 140, 20) if a > .5 else (60, 60, 76), width=1)
            y -= step

STEPS = [0.25, 0.5, 1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 2000, 2500, 5000, 1e4, 2e4, 2.5e4, 5e4, 1e5, 2e5, 2.5e5, 5e5, 1e6]
def nice_step(s):
    for st in STEPS:
        if st * s >= 80: return st
    return 2e6

def compact(v, unit):
    if v >= 1e6: return f"{v / 1e6:g}M {unit}"
    if v >= 1e5: return f"{v / 1e3:g}k {unit}"
    return f"{v:,.6g} {unit}"

def ruler(d, s, unit):
    d.rectangle((0, 470, PANEL, GROUND - 2), fill=(16, 16, 24)); d.line([(PANEL, 470), (PANEL, GROUND)], fill=(40, 40, 52), width=2)
    st = nice_step(s); x = 22; d.line([(x, GROUND), (x, 480)], fill=GREY, width=2)
    v = 0.0
    while GROUND - v * s > 490:
        y = GROUND - v * s; d.line([(x, y), (x + 14, y)], fill=GREY, width=2)
        lab = compact(v, unit); f = font(FM, 18)
        while d.textlength(lab, font=f) > PANEL - 42: f = font(FM, f.size - 1)
        d.text((x + 18, y - 12), lab, font=f, fill=GREY); v += st

def hook(d, lines):
    y = 95
    for i, ln in enumerate(lines):
        f = font(FB, 74)
        while d.textlength(ln, font=f) > W - 120: f = font(FB, f.size - 2)
        w = d.textlength(ln, font=f); d.text((W / 2 - w / 2, y), ln, font=f, fill=AM if i else WHITE); y += 86

def size_str(v, unit):
    if unit == "km": return f"{v:,.0f} km · {v * 0.621371:,.0f} mi"
    ft = v * 3.28084
    return f"{v:,.6g} m · {ft:,.0f} ft" if v >= 10 else f"{v:g} m · {ft:.1f} ft"

def label(d, it, a, unit):
    if a <= 0: return
    c = lambda col: mix(col, (22, 22, 30), a)
    x0, y0, x1 = 150, 300, 1000
    d.rounded_rectangle((x0, y0, x1, y0 + 150), 20, fill=(22, 22, 30), outline=c(AMD), width=2)
    d.text((x0 + 24, y0 + 12), it["tag"], font=font(FB, 30), fill=c(AM))
    hs = size_str(it["h"], unit); hf = font(FB, 34)
    d.text((x1 - 24 - d.textlength(hs, font=hf), y0 + 10), hs, font=hf, fill=c(AM))
    s = 46
    while d.textlength(it["name"], font=font(FB, s)) > x1 - x0 - 48: s -= 2
    d.text((x0 + 24, y0 + 52), it["name"], font=font(FB, s), fill=c(WHITE))
    sf = font(FM, 24)
    while d.textlength(it["sub"], font=sf) > x1 - x0 - 50: sf = font(FM, sf.size - 1)
    d.text((x0 + 26, y0 + 108), it["sub"], font=sf, fill=c(GREY))

def marker(d, it, cam, a):
    if a <= 0: return
    s = cam[1]; sx = sx_of(it, cam); y = GROUND - it["h"] * s; x = PANEL + 6
    stop = sx - (it["w"] * s * 0.6 if it["kind"] not in CIRCLES else 0)
    while x < stop:
        d.line([(x, y), (min(x + 14, stop), y)], fill=AM, width=2); x += 26

def render(spec, out):
    unit = spec.get("unit", "m"); space = unit == "km"
    items, total = build_items(spec); bg = make_bg(space)
    audio = music(total)
    for it in items: pluck(audio, it["t0"] + 0.15, 81)
    audio = audio / max(1e-6, np.abs(audio).max()) * 0.6
    wav = out + ".wav"
    with wave.open(wav, "wb") as wv:
        wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((audio * 32767).astype(np.int16).tobytes())
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                          "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    end_t = len(items) * T_ITEM; last = items[-1]; first = items[0]
    for fi in range(int(total * FPS)):
        t = fi / FPS; img = bg.copy(); d = ImageDraw.Draw(img)
        if t < end_t:
            idx, cam, u = camera(items, t)
            a = min(1, t / 0.4) if idx == 0 else max(0.0, min(1.0, (u - 0.7) / 0.3))
        else:
            e = ease(min(1, (t - end_t) / 1.6))
            span = (last["x"] + last["w"] / 2) - (first["x"] - first["w"] / 2)
            s_all = min(fit(last), (W - PANEL - 60) / span)
            mid = ((first["x"] - first["w"] / 2) + (last["x"] + last["w"] / 2)) / 2
            tx = mid - ((PANEL + W) / 2 - W * FOCUS_X) / s_all
            cam = (last["x"] + (tx - last["x"]) * e, math.exp(math.log(fit(last)) * (1 - e) + math.log(s_all) * e)); idx = len(items) - 1; a = 0
        for i, it in enumerate(items):
            if i < idx: draw_item(d, it, cam, False, 0)
        draw_item(d, items[idx], cam, t < end_t, a)
        ruler(d, cam[1], unit); hook(d, spec["hook"])
        if t < end_t:
            marker(d, items[idx], cam, a); label(d, items[idx], a, unit)
            d.rectangle((0, GROUND + 30, W * t / end_t, GROUND + 36), fill=AM)
        elif t - end_t > 1.2:
            d.rounded_rectangle((90, 300, W - 90, 450), 22, fill=(22, 22, 30), outline=AM, width=3)
            for txt, fnt, col, y in [(spec["end"], font(FB, 44), WHITE, 318), ("Follow @Measurama for more", font(FM, 32), AM, 388)]:
                while d.textlength(txt, font=fnt) > W - 240: fnt = font(fnt.path, fnt.size - 2)
                w = d.textlength(txt, font=fnt); d.text((W / 2 - w / 2, y), txt, font=fnt, fill=col)
        p.stdin.write(img.tobytes())
    p.stdin.close(); p.wait(); os.remove(wav)
    return total

if __name__ == "__main__":
    which, outdir = sys.argv[1], sys.argv[2]; os.makedirs(outdir, exist_ok=True)
    for spec in SHORTS:
        if which in ("all", spec["id"]):
            out = os.path.join(outdir, f"ms_{spec['id']}.mp4"); tot = render(spec, out); print("wrote", out, f"{tot:.1f}s", flush=True)
