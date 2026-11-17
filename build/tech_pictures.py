"""Tech pictures in the vanilla Darkest Hour style: an old print on aged paper with a torn edge and a
paperclip, on the pure-green surround the game treats as transparent.

Your originals stay untouched in src/tech_raw/<tech id>.(jpg|png|bmp), any size. This script crops each to
the tech picture shape (344x266), turns it into a faded monochrome print and lays it into the official
"Blank Tech Picture Template" (build/tech_template: base = paper, frame = torn edge + clip + green),
writing src/assets/gfx/interface/tech/<id>.bmp. The generator then switches each tech to its picture.

Usage: python3 build/tech_pictures.py src    (package.sh runs it before the build)
A portrait-shaped original (taller than wide) is pinned whole as a page instead of cropped.
Ids listed in KEEP_COLOUR keep a trace of their own colour (for blueprints: blue ink on the paper).
"""
import os, sys
from PIL import Image, ImageOps, ImageEnhance

W, H = 344, 266
OPACITY = 140            # the template says 50%; a touch more keeps detail on the stained paper
KEEP_COLOUR = set()      # e.g. {95120} once a blueprint arrives for it
HERE = os.path.dirname(os.path.abspath(__file__))

def fit(im):
    """Centre-crop to 344:266 and resize."""
    w, h = im.size
    if w / h > W / H:
        nw = int(h * W / H); x = (w - nw) // 2; im = im.crop((x, 0, x + nw, h))
    else:
        nh = int(w * H / W); y = (h - nh) // 2; im = im.crop((0, y, w, y + nh))
    return im.resize((W, H), Image.LANCZOS)

def render(raw, colour=False):
    base = Image.open(os.path.join(HERE, "tech_template", "base.png")).convert("RGBA")
    frame = Image.open(os.path.join(HERE, "tech_template", "frame.png")).convert("RGBA")
    raw = ImageOps.autocontrast(raw.convert("RGB"), cutoff=1)        # lifts dark night scenes
    portrait = raw.height > raw.width * 1.05
    if portrait:
        # a portrait page (dossier sheet, notebook page) is pinned whole, the template's paper either side
        ph = H - 16; pw = int(raw.width * ph / raw.height)
        im = raw.resize((pw, ph), Image.LANCZOS)
    else:
        im = fit(raw)
    if not colour:
        im = ImageEnhance.Contrast(ImageOps.grayscale(im)).enhance(1.3)
    layer = im.convert("RGBA"); layer.putalpha(OPACITY + (10 if portrait else 0))
    if portrait:
        sheet = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sheet.paste(layer, ((W - pw) // 2, 10)); layer = sheet
    out = base.copy(); out.alpha_composite(layer); out.alpha_composite(frame)
    return out.convert("RGB")

def main(src):
    if not os.path.exists(os.path.join(HERE, "tech_template", "base.png")):
        # the template is DH's own modding resource and isn't in the public repo; the rendered pictures are
        print("tech pictures: no build/tech_template, keeping the pictures already in src/assets")
        return
    raw_dir = os.path.join(src, "tech_raw"); out_dir = os.path.join(src, "assets", "gfx", "interface", "tech")
    os.makedirs(out_dir, exist_ok=True)
    n = 0
    for f in sorted(os.listdir(raw_dir)):
        stem, ext = os.path.splitext(f)
        if ext.lower() not in (".jpg", ".jpeg", ".png", ".bmp") or not stem.isdigit():
            continue
        render(Image.open(os.path.join(raw_dir, f)), int(stem) in KEEP_COLOUR).save(os.path.join(out_dir, stem + ".bmp"))
        n += 1
    print(f"tech pictures: {n} rendered into the vintage template")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "src")
