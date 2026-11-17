"""Draw DH flag strips and shields at native size, reusing the cloth shape of the Chimera flag.

flag_<tag>.bmp   700x18: 25 animation frames of 28x18, cloth on pure green (0,255,0)
shield_<tag>.bmp 176x70: 4 frames of 44x70 (normal, highlighted, normal, dimmed), flag turned 90 deg clockwise

Usage: python3 -I flags.py <chimera flag strip> <out dir>
"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFont

GREEN = (0, 255, 0)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def fer_design(w, h):
    """Far Eastern Republic, 1920-22: red, square blue canton with red Д В Р (ratio 1:2)."""
    im = Image.new("RGB", (w, h), (190, 22, 28))
    d = ImageDraw.Draw(im)
    c = h // 2                                          # square canton, half the height
    d.rectangle([0, 0, c - 1, c - 1], fill=(24, 48, 128))
    f = ImageFont.truetype(FONT, int(c * 0.36))
    for i, ch in enumerate("ДВР"):                      # stepped down the canton, as the 1920 flag
        x, y = c * (0.12 + 0.29 * i), c * (0.08 + 0.29 * i)
        d.text((x, y), ch, font=f, fill=(200, 26, 32))
    return im

GLYPHS = {   # 5x7 pixel letters, so the canton stays sharp at shield size
    "Д": [".###.", ".#.#.", ".#.#.", ".#.#.", ".#.#.", "#####", "#...#"],
    "В": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "Р": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
}
RED, BLUE, LETTER = (190, 22, 28), (24, 48, 128), (214, 34, 40)

def fer_shield_design():
    """The flag drawn natively at 70x44 (what DH flag makers call the high-res flag), pixel by pixel."""
    im = Image.new("RGB", (70, 44), RED); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 21, 21], fill=BLUE)
    for ch, (ox, oy) in zip("ДВР", ((2, 1), (8, 7), (14, 14))):
        for y, row in enumerate(GLYPHS[ch]):
            for x, c in enumerate(row):
                if c == "#": im.putpixel((ox + x, oy + y), LETTER)
    return im

WHITE, GOLD, STEEL, DARK = (236, 236, 232), (232, 184, 48), (214, 220, 228), (120, 92, 20)

def cordon_design():
    """Siberian Cordon Administration: a red field inside a broad white border (the cordon),
    with a gold shield and an upright sword, after the badge of the state security troops."""
    im = Image.new("RGB", (70, 44), WHITE); d = ImageDraw.Draw(im)
    d.rectangle([7, 7, 62, 36], fill=RED)
    cx, top = 35, 12                                   # shield 15 wide, 18 tall
    rows = [7] * 9 + [7, 6, 6, 5, 4, 3, 2, 1, 0]       # half-width per row: straight sides, pointed base
    for i, hw in enumerate(rows):
        for x in range(cx - hw, cx + hw + 1):
            edge = x in (cx - hw, cx + hw) or i == 0 or i == len(rows) - 1
            im.putpixel((x, top + i), DARK if edge else GOLD)
    for y in range(top - 3, top + 19):                 # blade through the shield
        im.putpixel((cx, y), STEEL)
    for x in range(cx - 3, cx + 4):                    # crossguard below the point of the blade
        im.putpixel((x, top + 19), GOLD)
    im.putpixel((cx, top + 20), GOLD); im.putpixel((cx, top + 21), DARK)   # grip and pommel
    return im

def cloth_frames(chimera_strip):
    """For each of the 25 frames: the cloth mask and, per column, its top and bottom edge."""
    src = Image.open(chimera_strip).convert("RGB")
    frames = []
    for i in range(25):
        fr = src.crop((i * 28, 0, i * 28 + 28, 18)); px = fr.load()
        cols = {}
        for x in range(28):
            ys = [y for y in range(18) if px[x, y] != GREEN]
            if ys: cols[x] = (min(ys), max(ys))
        frames.append(cols)
    return frames

def flag_strip(design, frames):
    big = design.resize((560, 360), Image.LANCZOS)      # sample source, 20x a 28x18 frame
    out = Image.new("RGB", (700, 18), GREEN); op = out.load(); bp = big.load()
    for i, cols in enumerate(frames):
        xs = sorted(cols); x0, x1 = xs[0], xs[-1]
        for x in xs:
            t, b = cols[x]
            u = (x - x0 + 0.5) / (x1 - x0 + 1)
            slope = (cols.get(x + 1, cols[x])[0] - cols.get(x - 1, cols[x])[0]) / 2
            shade = max(0.85, min(1.1, 1.0 - 0.06 * slope))
            for y in range(t, b + 1):
                v = (y - t + 0.5) / (b - t + 1)
                # average a 20x20 patch of the big design for this pixel
                sx, sy = int(u * 559), int(v * 359)
                r = g_ = bl = n = 0
                for dx in range(-8, 9, 4):
                    for dy in range(-8, 9, 4):
                        p = bp[min(559, max(0, sx + dx)), min(359, max(0, sy + dy))]
                        r += p[0]; g_ += p[1]; bl += p[2]; n += 1
                c = tuple(min(255, int(ch / n * shade)) for ch in (r, g_, bl))
                op[i * 28 + x, y] = c if c != GREEN else (0, 254, 0)
    return out

def shield(native):
    """native: the 70x44 flag. Turned 90 degrees clockwise: hoist at the top, canton top-right."""
    base = native.rotate(-90, expand=True)                 # 44x70
    bp = base.load()
    for x in range(44):                                    # soft folds and a darker edge
        fold = 1.0 + 0.05 * math.sin(x / 44 * math.pi * 3.2)
        for y in range(70):
            edge = min(x, 43 - x, y, 69 - y)
            k = fold * (0.78 if edge == 0 else 0.9 if edge == 1 else 1.0)
            bp[x, y] = tuple(min(255, int(c * k)) for c in bp[x, y])
    out = Image.new("RGB", (176, 70))
    for i, k in enumerate((1.0, 1.2, 1.0, 0.54)):          # same brightness steps as the Chimera shield
        fr = base.copy(); fp = fr.load()
        for x in range(44):
            for y in range(70):
                fp[x, y] = tuple(min(255, int(c * k)) for c in fp[x, y])
        out.paste(fr, (i * 44, 0))
    return out

if __name__ == "__main__":
    strip, out = sys.argv[1], sys.argv[2]
    d = fer_design(600, 300)
    os.makedirs(os.path.join(out, "gfx/map/flags"), exist_ok=True)
    os.makedirs(os.path.join(out, "gfx/map/shields"), exist_ok=True)
    flag_strip(d, cloth_frames(strip)).save(os.path.join(out, "gfx/map/flags/flag_ua2.bmp"))
    native = fer_shield_design()
    shield(native).save(os.path.join(out, "gfx/map/shields/shield_ua2.bmp"))
    native.save(os.path.join(out, "flag_ua2_70x44.bmp"))
    cordon = cordon_design()
    flag_strip(cordon.resize((600, 377), Image.NEAREST), cloth_frames(strip)).save(os.path.join(out, "gfx/map/flags/flag_ua1.bmp"))
    shield(cordon).save(os.path.join(out, "gfx/map/shields/shield_ua1.bmp"))
    cordon.save(os.path.join(out, "flag_ua1_70x44.bmp"))
