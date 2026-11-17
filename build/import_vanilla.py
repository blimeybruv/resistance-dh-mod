"""Copy the vanilla Darkest Hour Full files the build reads into src/.

The public repo doesn't carry Paradox's or the DH Full team's files. The generators read them from src/ and
add the mod to them, so copy them from your own install first:

    python3 build/import_vanilla.py "C:/Games/Darkest Hour Full"
    sh build/package.sh 1

The install must be DH Full on patch 1.05.2 (the UA0-UF9 country tags don't exist before 1.05).
"""
import os, shutil, sys

# file in src/  ->  path in the DH Full folder (matched case-insensitively, as a path ending)
FILES = {
    "1933.eug": "scenarios/1933.eug",
    "soviet union.inc": "scenarios/1933/soviet union.inc",
    "inc1933/united kingdom.inc": "scenarios/1933/united kingdom.inc",
    "inc1933/japan.inc": "scenarios/1933/japan.inc",
    "inc1933/spain.inc": "scenarios/1933/spain.inc",
    "inc1933/usa.inc": "scenarios/1933/usa.inc",
    "USSR.txt": "db/events/USSR.txt",
    "revolt.txt": "db/revolt.txt",
    "minor_default.ai": "ai/minor_default.ai",
    "country.csv": "country.csv",
    "models.csv": "config/models.csv",
    "mods.csv": "config/mods.csv",
    "tech_names.csv": "config/tech_names.csv",
    "unit_names.csv": "config/unit_names.csv",
    "unitnames.csv": "db/unitnames.csv",
    "armynames.csv": "db/armynames.csv",
    "airnames.csv": "db/airnames.csv",
    "navynames.csv": "db/navynames.csv",
    "secret_weapons_tech.txt": "db/tech/secret_weapons_tech.txt",
    "land_doctrines_tech.txt": "db/tech/land_doctrines_tech.txt",
}
for t in ("industry", "infantry", "armor", "aircraft", "naval", "air_doctrines", "naval_doctrines"):
    FILES[f"tech/{t}_tech.txt"] = f"db/tech/{t}_tech.txt"
for d in ("cas", "cavalry", "hq", "infantry", "interceptor", "militia", "naval_bomber", "strategic_bomber"):
    FILES[f"units/divisions/{d}.txt"] = f"db/units/divisions/{d}.txt"
for b in ("anti_air", "artillery", "engineer", "heavy_armor", "medium_armor", "super_heavy_armor"):
    FILES[f"units/brigades/{b}.txt"] = f"db/units/brigades/{b}.txt"

SKIP_DIRS = {"mods", "save games", "scenarios/save games"}

def index(root):
    """Every file under the install, by lower-case relative path (mod folders and saves left out)."""
    out = {}
    for d, dirs, files in os.walk(root):
        rel = os.path.relpath(d, root).replace("\\", "/").lower()
        dirs[:] = [x for x in dirs if (rel + "/" + x.lower()).lstrip("./") not in SKIP_DIRS and x.lower() not in SKIP_DIRS]
        for f in files:
            out[(rel + "/" + f.lower()).lstrip("./")] = os.path.join(d, f)
    return out

def find(idx, ending):
    ending = ending.lower()
    hits = sorted((k for k in idx if k == ending or k.endswith("/" + ending)), key=len)
    return idx[hits[0]] if hits else None

def main(root, src):
    if not os.path.isdir(root):
        sys.exit(f"not a folder: {root}")
    idx = index(root)
    missing = []
    for dst, ending in FILES.items():
        path = find(idx, ending) or find(idx, os.path.basename(ending))
        if not path:
            missing.append(ending); continue
        out = os.path.join(src, dst)
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        shutil.copyfile(path, out)
    print(f"copied {len(FILES) - len(missing)} of {len(FILES)} vanilla files into {src}/")
    if missing:
        print("not found (check the folder is DH Full 1.05.2):\n  " + "\n  ".join(missing))
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
