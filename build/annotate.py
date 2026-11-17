"""Hand-letter the empty callout circles on a study sheet (sepia ink, Caveat handwriting).
NOTES = list of (circle_x, circle_y, text, side) in the original image's pixels; side = 'l', 'r', 'u' or 'd'."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
INK = (58, 40, 24)

def annotate(src, notes, out, size=34):
    im = Image.open(src).convert("RGB")
    font = ImageFont.truetype(os.path.join(HERE, "fonts", "Caveat.ttf"), size)
    try: font.set_variation_by_axes([600])
    except Exception: pass
    for (cx, cy, text, side) in notes:
        lines = text.split("\n")
        layer = Image.new("RGBA", (600, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
        y = 0; w = 0
        for ln in lines:
            d.text((0, y), ln, font=font, fill=INK + (235,)); bb = d.textbbox((0, y), ln, font=font)
            w = max(w, bb[2]); y += int(size * 0.92)
        layer = layer.crop((0, 0, w + 4, y + 8)).rotate(-2, expand=True, resample=Image.BICUBIC)
        lw, lh = layer.size; g = 22
        pos = {"l": (cx - g - lw, cy - lh // 2), "r": (cx + g, cy - lh // 2),
               "u": (cx - lw // 2, cy - g - lh), "d": (cx - lw // 2, cy + g)}[side]
        im.paste(layer, pos, layer)
    im.save(out)
    return im
