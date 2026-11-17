"""Hybrid infantry map sprite (T-INFANTRY C-UA0), repainted from DH's own alien infantry set (C-ALI).

The ALI set has proper vanilla animation (stand, walk and fire in 8 directions, 108x108 frames, palette
index 0 = transparent, 1 = shadow). This keeps every frame, origin and frame count, and repaints:
  - head, arms and torso: grey-tan Hybrid skin; legs: dark brown trousers; the rifle stays gunmetal
  - amber eyes on the faces you can see; two cooling towers with amber vents behind the shoulders
  - the white firing beam becomes amber Bullseye fire
Usage: python3 build/infantry_sprite.py <ALI source folder> <out root>
"""
import math, os, re, sys, glob
import numpy as np
from PIL import Image

TAG = "UA0"; FW = 108; LEVELS = (1, 2, 3, 4)
FACING = {"E": (1, 0), "W": (-1, 0), "N": (0, -1), "S": (0, 1),
          "NE": (0.7, -0.7), "NW": (-0.7, -0.7), "SE": (0.7, 0.7), "SW": (-0.7, 0.7), None: (0.7, 0.7)}
SKIN = [(30, 28, 25), (84, 78, 68), (128, 120, 104), (176, 166, 146)]
HARNESS = [(16, 15, 14), (40, 37, 34), (66, 61, 55), (96, 90, 82)]     # dark -> light
CLOTH = [(16, 16, 15), (38, 37, 34), (60, 58, 53), (86, 83, 76)]     # charcoal trousers
STEEL = [(14, 15, 15), (34, 36, 35), (58, 60, 57), (98, 100, 95)]     # dark, slightly olive gunmetal (Advanced Hybrid armour)
GUNMETAL = [(18, 19, 22), (58, 60, 66), (104, 107, 116), (160, 164, 174)]
VARIANTS = {
    "A": {"trousers": [(26, 28, 22), (50, 53, 44), (72, 75, 64), (96, 99, 86)], "chest": "bandolier"},   # field grey
    "B": {"trousers": [(24, 21, 17), (46, 41, 34), (66, 60, 50), (88, 80, 68)], "chest": "plate", "kneepads": True},
    "C": {"trousers": [(20, 20, 19), (42, 41, 38), (62, 60, 56), (84, 82, 77)], "chest": None},
    "D": {"trousers": [(24, 21, 17), (46, 41, 34), (66, 60, 50), (88, 80, 68)], "chest": None, "kneepads": True, "boot_rows": 10},
    "F": {"trousers": [(24, 21, 17), (46, 41, 34), (66, 60, 50), (88, 80, 68)], "chest": "steelplate", "kneepads": True, "boot_rows": 10, "steel_boots": True},
    "G": {"trousers": [(24, 21, 17), (46, 41, 34), (66, 60, 50), (88, 80, 68)], "chest": "steelridge", "kneepads": True, "boot_rows": 10, "steel_boots": True},
    "H": {"trousers": [(34, 18, 12), (70, 40, 28), (104, 64, 46), (142, 96, 72)], "chest": None, "kneepads": True,
          "boot_rows": 10, "brown_armour": True, "bare_feet": True, "belt": (112, 34, 26),
          "skin": [(44, 34, 20), (110, 92, 58), (166, 146, 100), (214, 196, 148)]},     # Resistance 3 Hybrid
    "E": {"trousers": [(24, 21, 17), (46, 41, 34), (66, 60, 50), (88, 80, 68)], "chest": None, "boot_rows": 10},
}
VARIANT = os.environ.get("HYBRID_VARIANT", "H")
BOOT = (20, 18, 16); STRAP = (24, 22, 20); BELT = (30, 27, 24)
TOWER = (38, 38, 42); TOWER_HI = (78, 78, 86); AMBER = (255, 172, 40); AMBER_HOT = (255, 214, 120)

def ramp(stops, l):
    l = np.clip(l, 0, 1) * (len(stops) - 1)
    i = np.minimum(l.astype(int), len(stops) - 2); f = (l - i)[..., None]
    s = np.array(stops, float)
    return s[i] * (1 - f) + s[i + 1] * f

def repaint(idx, pal, facing, steady=None, ground=FW):
    rgb = pal[idx].astype(float)
    fig = idx > 1
    out = np.zeros_like(rgb)
    if not fig.any():
        return out, fig
    lum = rgb.mean(-1) / 255; sat = rgb.max(-1) - rgb.min(-1)
    # the firing beam: bright pixels in a thin line (few figure pixels around them)
    k = np.ones((5, 5)); pad = np.pad(fig.astype(int), 2)
    nb = sum(pad[dy:dy + FW, dx:dx + FW] for dy in range(5) for dx in range(5))
    beam = fig & (lum > 0.8) & (nb < 11)
    ys0 = np.where(fig & steady)[0] if steady is not None and (fig & steady).any() else np.where(fig)[0]
    feet = min(ys0.max(), ground)
    beam |= fig & ((np.arange(FW)[:, None] < feet - 49) | (np.arange(FW)[:, None] > feet + 1))   # nothing of the Hybrid is that high
    if steady is not None:                         # firing: the body barely moves, the beam changes each frame
        beam = beam | (fig & ~steady)
    body = fig & ~beam
    ys, xs = np.where(body)
    if len(ys) == 0:
        out[beam] = AMBER; return out, fig
    bot = min(ys.max(), feet); top = max(ys.min(), bot - 47); h = bot - top + 1   # height from the feet: a beam can rise above the head
    rows = np.arange(FW)[:, None] * np.ones((1, FW)); cols = np.ones((FW, 1)) * np.arange(FW)[None, :]
    waist = top + 0.50 * h
    V = VARIANTS[VARIANT]
    sel0 = (ys >= top) & (ys <= top + 5)
    hx0 = xs[sel0].mean() if sel0.any() else xs.mean()
    legs = body & (rows > waist)
    warm = (rgb[..., 0] - rgb[..., 2]) / np.maximum(rgb.mean(-1), 1)   # the body is beige, the ALI rifle neutral grey
    gun = body & (warm < 0.07) & (lum < 0.70) & (rows > top + 0.15 * h) & (rows < bot - 6)
    gun &= ~(legs & (np.abs(cols - hx0) < 4.5))                      # the crotch is cloth, not rifle
    legs = legs & ~gun
    skin = body & ~legs & ~gun
    fx, fy = facing
    if abs(fx) < 0.3 and fy > 0.3:                                     # front view: paint out the alien's eye spots
        eyes = skin & (rows <= top + 4) & (lum < 0.5)
        lum = np.where(eyes, 0.62, lum)
    out[skin] = ramp(V.get("skin", SKIN), lum[skin] * 1.05)
    flat = 0.5 + (lum - 0.5) * 0.35                                     # opaque cloth: gentle shading only
    out[legs] = ramp(V["trousers"], flat[legs])
    boots = legs & (rows > bot - V.get("boot_rows", 6))
    if V.get("brown_armour"):                                          # shin guards in the same brown plate, lit edges
        out[boots] = ramp(V["trousers"], flat[boots] + 0.08)
        edge = boots & (rows == bot - V["boot_rows"] + 1)
        out[edge] = ramp(V["trousers"], flat[edge] + 0.35)
        if V.get("bare_feet"):
            feet = legs & (rows > bot - 2)
            out[feet] = ramp(V["skin"], flat[feet] * 0.8)
    elif V.get("steel_boots"):                                           # armoured greaves
        out[boots] = ramp(STEEL, flat[boots] * 0.9)
        out[boots & (rows > bot - 2)] = (22, 23, 26)                    # dark soles
    else:
        out[boots] = ramp([(8, 8, 8), (18, 17, 16), (30, 28, 26)], flat[boots])
    if V.get("kneepads"):
        kr = bot - V.get("boot_rows", 6) - 2
        kp = legs & (np.abs(rows - kr) < 1.2)
        out[kp] = ramp(V["trousers"], flat[kp] + 0.4) if V.get("brown_armour") else ramp(STEEL if V.get("steel_boots") else GUNMETAL, flat[kp] + 0.18)
    out[gun] = np.clip(rgb[gun] * 1.12 + np.array([2, 4, 10]), 0, 210)   # the rifle keeps its own shading, a touch cooler
    out[body & ~gun & (rows >= waist - 1) & (rows <= waist)] = V.get("belt", BELT)
    chest = skin & (rows > top + 0.22 * h) & (rows < waist - 1)
    t = rows - (top + 0.22 * h)
    if V["chest"] == "bandolier":                                      # one strap, shoulder to opposite hip
        strap = chest & (np.abs((cols - hx0) - (2.5 - 0.42 * t)) < 0.9)
        out[strap] = STRAP
    elif V["chest"] in ("steelplate", "steelridge"):
        plate = chest & (np.abs(cols - hx0) <= 3.2)
        out[plate] = ramp(STEEL, flat[plate])
        out[plate & (rows <= top + 0.22 * h + 1)] = ramp(STEEL, flat[plate & (rows <= top + 0.22 * h + 1)] + 0.25)   # lit top edge
        if V["chest"] == "steelplate":
            seam = plate & (((rows - top).astype(int) % 4) == 0) & (rows > top + 0.22 * h + 1)
            out[seam] = ramp(STEEL, flat[seam] - 0.3)
        else:
            ridge = plate & (np.abs(cols - hx0) < 0.6)
            out[ridge] = ramp(STEEL, flat[ridge] + 0.3)
    elif V["chest"] == "plate":                                        # segmented chest plate
        plate = chest & (np.abs(cols - hx0) <= 3.2)
        out[plate] = ramp(HARNESS, flat[plate] + 0.05)
        seam = plate & (((rows - top).astype(int) % 3) == 0)
        out[seam] = ramp(HARNESS, flat[seam] + 0.35)
    out[beam] = np.where((lum[beam] > 0.93)[:, None], AMBER_HOT, AMBER)
    # head centre: mean x of the top rows of the body
    hx = hx0
    # cooling towers behind the shoulders
    front = fy > 0.3 or (abs(fy) <= 0.3)               # facing towards the viewer or sideways: towers behind
    for side in (-1, 1):
        tx = int(round(hx - fx * 3 + side * (3 if abs(fx) < 0.8 else 1.5)))
        for yy in range(top + 1, top + 11):
            for xx in (tx - 1, tx, tx + 1):
                if 0 <= xx < FW and 0 <= yy < FW and (not front or not body[yy, xx]):
                    col = AMBER if (yy <= top + 2 or yy == top + 5) and xx == tx else (TOWER_HI if xx == tx - 1 else TOWER)
                    out[yy, xx] = col; fig[yy, xx] = True
    # eyes, when the face is towards the viewer
    if fy > -0.3:
        ey = top + 3
        cx = hx + fx * 1.5
        for ex in ((cx - 1.2, cx + 1.2) if abs(fx) < 0.8 else (cx + fx * 0.8,)):
            xx = int(round(ex))
            if body[ey, xx]: out[ey, xx] = AMBER
    return out, fig

def main(src, outroot):
    units = os.path.join(outroot, "gfx", "map", "units"); bmpd = os.path.join(units, "bmp"); pald = os.path.join(outroot, "gfx", "palette")
    for p in (units, bmpd, pald): os.makedirs(p, exist_ok=True)
    pal = np.array(Image.open(os.path.join(src, "T-INFANTRY C-ALI L-1.bmp") if os.path.exists(os.path.join(src, "T-INFANTRY C-ALI L-1.bmp"))
                   else glob.glob(os.path.join(src, "*C-ALI*.bmp"))[0]).getpalette()[:768]).reshape(256, 3)
    jobs = []
    for spr in sorted(glob.glob(os.path.join(src, "T-INFANTRY *C-ALI*.spr"))):
        txt = open(spr, encoding="latin-1").read()
        bmp = re.search(r'Bitmap\s*=\s*"([^"]+)"', txt).group(1)
        m = re.search(r" D-(\w+)", os.path.basename(spr)); d = m.group(1) if m else None
        idx = np.array(Image.open(os.path.join(src, bmp)))
        jobs.append((os.path.basename(spr), txt, bmp, d, idx))
    painted = []
    for name, txt, bmp, d, idx in jobs:
        n = idx.shape[1] // FW
        frames = []
        steady = None
        oy = int(re.search(r"y\s*=\s*(\d+)", txt).group(1)); ground = oy + 10     # the anchor sits at the feet
        if "A-FIRE" in name:
            stack = np.stack([idx[:, k * FW:(k + 1) * FW] > 1 for k in range(n)])
            st = stack.mean(0) > 0.55
            pad = np.pad(st, 1)                       # allow a pixel of recoil
            steady = np.zeros_like(st)
            for dy in range(3):
                for dx in range(3): steady |= pad[dy:dy + FW, dx:dx + FW]
        for k in range(n):
            fi = idx[:, k * FW:(k + 1) * FW]
            col, fig = repaint(fi, pal, FACING[d], steady, ground)
            frames.append((fi == 1, fig, col))
        painted.append((name, txt, bmp, frames))
    sample = np.concatenate([f[2][f[1]] for _, _, _, fs in painted for f in fs]).astype("uint8")
    q = Image.fromarray(sample.reshape(-1, 1, 3)).quantize(colors=254, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    qpal = q.getpalette()[:254 * 3]; full = [255, 0, 255, 0, 255, 255] + qpal + [0] * (762 - len(qpal))
    qimg = Image.new("P", (1, 1)); qimg.putpalette(qpal + [0] * (768 - len(qpal)))
    for name, txt, bmp, frames in painted:
        strip = np.zeros((FW, FW * len(frames)), "uint8")
        for k, (shadow, fig, col) in enumerate(frames):
            fr = np.zeros((FW, FW), "uint8"); fr[shadow] = 1
            qi = np.array(Image.fromarray(np.clip(col, 0, 255).astype("uint8")).quantize(palette=qimg, dither=Image.Dither.NONE)) + 2
            fr[fig] = qi[fig]; strip[:, k * FW:(k + 1) * FW] = fr
        im = Image.fromarray(strip, "P"); im.putpalette(full)
        newbmp = bmp.replace("C-ALI", f"C-{TAG}")
        im.save(os.path.join(bmpd, newbmp))
        base = txt.replace("C-ALI", f"C-{TAG}")
        newname = name.replace("C-ALI", f"C-{TAG}")
        open(os.path.join(units, newname), "w", encoding="latin-1", newline="").write(base)
        if " L-1" in newname:                         # every Hybrid model level uses the same bitmaps
            for lv in LEVELS[1:]:
                open(os.path.join(units, newname.replace(" L-1", f" L-{lv}")), "w", encoding="latin-1", newline="").write(base)
    p = Image.fromarray(np.arange(16, dtype="uint8").reshape(4, 4), "P"); p.putpalette(full)
    p.save(os.path.join(pald, f"T-INFANTRY C-{TAG} L-1.bmp"))
    print(len(painted), "strips repainted")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
