"""Chimeran fighter map sprite (T-FIGHTER C-UA0 L-1), drawn procedurally to vanilla DH conventions.

Vanilla fighters (e.g. T-FIGHTER ... C-ENG L-1): 108x108 frames x 19, 8-bit palette, index 0 magenta =
transparent, index 1 = shadow (drawn by the engine), near top-down plan view with the aircraft in the upper
half and a half-size flat shadow below it at the unit's anchor (origin ~55,86).

Design: a compact teardrop hull (Resistance's Chimeran Fighter) with a dark cockpit band and amber slit at
the blunt nose, two short, thick swept scythe wings, two amber engine glows at the pointed tail.

Usage: python3 build/fighter_sprite.py <out root>   (writes gfx/map/units/*.spr, bmp/*.bmp, gfx/palette/)
"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw

FW = 108; N = 19; SS = 4                      # frame size, frames per strip, supersampling
CX, CY = 55, 40                               # where the aircraft sits in the frame
SCALE = 0.74                                  # overall size: span ~ the vanilla Spitfire
ORIGIN = (55, 86)                             # anchor = shadow centre, as vanilla
SQUASH = 0.86                                 # slight oblique foreshortening of the map view
TAG = "UA0"
DIRS = {"E": 0, "NE": 45, "N": 90, "NW": 135, "W": 180, "SW": 225, "S": 270, "SE": 315}

GUN = (92, 92, 102); WING = (50, 50, 57); RIM_HI = (138, 138, 148); RIM_LO = (28, 28, 32)
OUTLINE = (16, 14, 12); COCKPIT = (22, 22, 26); AMBER = (255, 176, 40); AMBER_DIM = (196, 112, 24)

def teardrop():
    pts = []
    for a in range(-90, 91, 15):                                   # rounded nose, centre (12, 0), r 9
        pts.append((12 + 9 * math.cos(math.radians(a)), 9 * math.sin(math.radians(a))))
    pts += [(-4, 7.5), (-16, 4), (-26, 0), (-16, -4), (-4, -7.5)]
    return pts

def wing(side):
    s = side
    return [(8, 6 * s), (5, 15 * s), (-2, 25 * s), (-12, 33 * s), (-22, 36 * s),      # leading edge to tip
            (-15, 29 * s), (-11, 20 * s), (-10, 11 * s), (-12, 5 * s)]              # trailing edge back

def project(pts, ang, dx=0, dy=0):
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    out = []
    for x, y in pts:                       # local: x forward, y to the right of the pilot
        x, y = x * SCALE, y * SCALE
        wx = x * c + y * s                 # right of the pilot = clockwise from heading
        wy = x * s - y * c
        out.append(((CX + dx + wx) * SS, (CY + dy - wy * SQUASH) * SS))
    return out

def shift(m, dx, dy):
    o = np.zeros_like(m)
    h, w = m.shape
    o[max(dy, 0):h + min(dy, 0), max(dx, 0):w + min(dx, 0)] = m[max(-dy, 0):h + min(-dy, 0), max(-dx, 0):w + min(-dx, 0)]
    return o

def frame(ang, k, fire=False):
    bob = round(1.2 * math.sin(2 * math.pi * k / N))
    big = Image.new("RGBA", (FW * SS, FW * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(big)
    for side in (1, -1):
        d.polygon(project(wing(side), ang, 0, bob), fill=WING + (255,))
    for side in (1, -1):                                           # amber vein along each leading edge
        le = wing(side)[1:4]
        d.line(project([(p[0] - 1.2, p[1] - 1.0 * side) for p in le], ang, 0, bob), fill=AMBER_DIM + (255,), width=int(1.1 * SS))
    d.polygon(project(teardrop(), ang, 0, bob), fill=GUN + (255,))
    # spine ridge, cockpit band with amber slit, engine glows
    d.line(project([(14, 0), (-22, 0)], ang, 0, bob), fill=(120, 120, 132, 255), width=int(2.2 * SS))
    d.polygon(project([(19.5, -6), (19.5, 6), (15, 7.5), (15, -7.5)], ang, 0, bob), fill=COCKPIT + (255,))
    d.line(project([(17.4, -4.6), (17.4, 4.6)], ang, 0, bob), fill=AMBER + (255,), width=int(1.3 * SS))
    for y in (2.6, -2.6):
        (px, py), = project([(-21, y)], ang, 0, bob)
        r = 1.9 * SS * (1.0 if k % 6 < 3 else 0.8)
        d.ellipse((px - r, py - r, px + r, py + r), fill=AMBER + (255,))
    if fire and k % 4 < 2:                                         # twin amber bolts ahead of the nose
        for y in (3.2, -3.2):
            off = 4 * (k % 4)
            d.line(project([(24 + off, y), (34 + off, y)], ang, 0, bob), fill=AMBER + (255,), width=int(1.5 * SS))
    a = np.array(big).astype(float)
    m = a[..., 3] > 128
    hi = m & ~shift(m, 4, 4); lo = m & ~shift(m, -4, -4)           # bevel: light from the top left
    grey = np.abs(a[..., 0] - a[..., 2]) < 30
    a[hi & grey, :3] = RIM_HI
    a[lo & grey, :3] = RIM_LO
    small = Image.fromarray(a.astype("uint8"), "RGBA").resize((FW, FW), Image.LANCZOS)
    s = np.array(small).astype(float)
    mask = s[..., 3] > 110
    rgb = np.clip(s[..., :3] / np.maximum(s[..., 3:4] / 255, 0.01), 0, 255)
    ring = (shift(mask, 1, 0) | shift(mask, -1, 0) | shift(mask, 0, 1) | shift(mask, 0, -1)) & ~mask
    # shadow: the aircraft silhouette at half size, flat, centred on the anchor
    sil = Image.fromarray(((mask | ring) * 255).astype("uint8")).resize((FW // 2, FW // 2), Image.NEAREST)
    shadow = np.zeros((FW, FW), bool)
    sy0 = ORIGIN[1] - (CY + bob) // 2 - 0; sx0 = ORIGIN[0] - CX // 2
    sm = np.array(sil) > 0
    ys, xs = np.where(sm)
    for y, x in zip(ys, xs):
        Y, X = y + sy0, x + sx0
        if 0 <= Y < FW and 0 <= X < FW: shadow[Y, X] = True
    if fire:                                                       # the bolts cast no shadow
        shadow = frame(ang, k, False)[3]
    return rgb, mask, ring, shadow

def build(out):
    units = os.path.join(out, "gfx", "map", "units"); bmpd = os.path.join(units, "bmp"); pald = os.path.join(out, "gfx", "palette")
    for p in (units, bmpd, pald): os.makedirs(p, exist_ok=True)
    jobs = [("WALK", dname, ang, False) for dname, ang in DIRS.items()] + \
           [("FIRE", dname, ang, True) for dname, ang in DIRS.items()] + [("STAND", None, DIRS["E"], False)]
    strips = []
    for anim, dname, ang, fire in jobs:
        frames = [frame(ang, k, fire) for k in range(N)]
        strips.append((anim, dname, frames))
    # one shared palette: 0 magenta, 1 shadow (cyan, as vanilla), 2.. quantised aircraft colours
    px = np.concatenate([np.concatenate([f[0][f[1]], np.tile(OUTLINE, (int(f[2].sum()), 1))]) for _, _, fs in strips for f in fs])
    sample = Image.fromarray(px.reshape(-1, 1, 3).astype("uint8"))
    q = sample.quantize(colors=254, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    qpal = q.getpalette()[:254 * 3]
    pal = [255, 0, 255, 0, 255, 255] + qpal + [0] * (768 - 6 - len(qpal))
    qimg = Image.new("P", (1, 1)); qimg.putpalette(qpal + [0] * (768 - len(qpal)))
    def sprname(anim, dname):
        return f"T-FIGHTER A-{anim} C-{TAG} L-1" + (f" D-{dname}" if dname else "")
    for anim, dname, frames in strips:
        strip = np.zeros((FW, FW * N), "uint8")
        for k, (rgb, mask, ring, shadow) in enumerate(frames):
            fr = np.zeros((FW, FW), "uint8")
            fr[shadow] = 1
            col = rgb.copy(); col[ring] = OUTLINE
            idx = np.array(Image.fromarray(col.astype("uint8")).quantize(palette=qimg, dither=Image.Dither.NONE)) + 2
            sel = mask | ring
            fr[sel] = idx[sel]
            strip[:, k * FW:(k + 1) * FW] = fr
        im = Image.fromarray(strip, "P"); im.putpalette(pal)
        name = sprname(anim, dname)
        im.save(os.path.join(bmpd, name + ".bmp"))
        with open(os.path.join(units, name + ".spr"), "w", newline="\r\n") as f:
            f.write(f'Sprite = {{\n\tBitmap = "{name}.bmp"\n\tOrigin = {{ x = {ORIGIN[0]} y = {ORIGIN[1]} }}\n'
                    f'\tFrames = {N}\n\tSpeed = 5\n\tPalette = "T-FIGHTER C-{TAG} L-1.bmp"\n}}\n')
    p = Image.fromarray(np.arange(16, dtype="uint8").reshape(4, 4), "P"); p.putpalette(pal)
    p.save(os.path.join(pald, f"T-FIGHTER C-{TAG} L-1.bmp"))
    return len(strips)

if __name__ == "__main__":
    print(build(sys.argv[1] if len(sys.argv) > 1 else "out_fighter"), "strips")
