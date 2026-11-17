"""Build checks: run after every build. Errors stop packaging; warnings are listed for the release notes.

Each check targets a mistake that has already reached a playtest once:
  dates        day 30/31 (DH months run 0-29)                         v31
  ai_sums      AI unit mix must add to exactly 100                    v31
  personality  minister personality DH doesn't know                  v45
  model_names  new model without a generic name (STRING_WANTED)       v50
  text_keys    event/action text key missing from mods.csv
  pictures     mod picture name with no file behind it
  event_ids    the same event id used twice
  commands     event command never seen in a vanilla DH file
  provinces    province id that doesn't exist or is a 'free' slot
  ministers    event appoints a minister id no file defines
  garrisons    remove_division for a unit the scenario never creates
  event_files  event file not included by the scenario (or missing)
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
FACTS = json.load(open(os.path.join(ROOT, "dh_facts.json")))
PROV = {int(k): v for k, v in json.load(open(os.path.join(ROOT, "provinces.json"))).items()}
ADJ = {int(k): v for k, v in json.load(open(os.path.join(ROOT, "adjacency.json"))).items()}

# confirmed by your playtests or logs although no vanilla file we have uses them
COMMANDS_CONFIRMED_IN_MOD = set()
# used by the mod but never seen working anywhere: reported as warnings until confirmed
COMMANDS_ASSUMED = {"energypool", "metalpool", "rarematerialspool"}
DIVISION_TYPES = ["infantry", "cavalry", "motorized", "mechanized", "light_armor", "armor", "paratrooper", "marine",
                  "bergsjaeger", "garrison", "hq", "militia", "multi_role", "interceptor", "strategic_bomber",
                  "tactical_bomber", "naval_bomber", "cas", "transport_plane", "flying_bomb", "flying_rocket",
                  "battleship", "light_cruiser", "heavy_cruiser", "battlecruiser", "destroyer", "carrier",
                  "escort_carrier", "submarine", "nuclear_submarine", "transport"]

def read(p):
    return open(p, encoding="latin-1").read()

def run(out):
    errors, warnings = [], []
    E = lambda check, msg: errors.append(f"[{check}] {msg}")
    W = lambda check, msg: warnings.append(f"[{check}] {msg}")
    ev_files = sorted(glob.glob(os.path.join(out, "db/events/res_*.txt")))
    events = {}                                     # id -> (file, text)
    for f in ev_files:
        for block in re.split(r"\n(?=event = \{)", read(f)):
            m = re.search(r"\n\s*id = (\d+)\s*\n", block)
            if not m:
                continue
            eid = int(m.group(1))
            if eid in events:
                E("event_ids", f"{eid} defined twice ({os.path.basename(events[eid][0])}, {os.path.basename(f)})")
            events[eid] = (f, block)

    # dates
    for eid, (f, b) in events.items():
        for d in re.findall(r"day = (\d+)", b):
            if int(d) > 29:
                E("dates", f"event {eid}: day {d} (DH months run 0-29)")

    # text keys
    mods = read(os.path.join(out, "config/mods.csv"))
    keys = set(re.findall(r"^([^;\n]+);", mods, re.M))
    for eid, (f, b) in events.items():
        for k in re.findall(r'(?:name|desc) = "([A-Z][A-Z0-9_]+)"', b):
            if k not in keys:
                E("text_keys", f"event {eid}: text key {k} missing from mods.csv")

    # commands
    seen = set(FACTS["commands_seen_in_vanilla"]) | COMMANDS_CONFIRMED_IN_MOD
    used = {}
    for eid, (f, b) in events.items():
        for c in re.findall(r"type = ([a-z_]+)", b):
            used.setdefault(c, eid)
    for c, eid in sorted(used.items()):
        if c in COMMANDS_ASSUMED:
            W("commands", f"'{c}' (e.g. event {eid}) is still unconfirmed: check it does something in game")
        elif c not in seen:
            E("commands", f"'{c}' (event {eid}) never appears in a vanilla DH file")

    # provinces
    for eid, (f, b) in events.items():
        for p in set(map(int, re.findall(r"(?:province = |secedeprovince which = \w+ value = |where = |capital which = |addcore which = |removecore which = )(\d+)", b))):
            if p not in PROV and p not in ADJ:
                E("provinces", f"event {eid}: province {p} does not exist")
            elif ADJ.get(p, {}).get("name") == "free":
                E("provinces", f"event {eid}: province {p} is an unused 'free' slot")

    # ministers
    mids = set()
    for f in glob.glob(os.path.join(out, "db/ministers/*.csv")):
        mids |= {int(l.split(";")[0]) for l in read(f).split("\n") if re.match(r"\d+;", l)}
    slots = "headofstate|headofgovernment|foreignminister|armamentminister|ministerofsecurity|ministerofintelligence|chiefofstaff|chiefofarmy|chiefofnavy|chiefofair"
    for eid, (f, b) in events.items():
        for mid in map(int, re.findall(rf"type = (?:{slots}) which = (\d+)", b)):
            if mid >= 1500000 and mid not in mids:
                E("ministers", f"event {eid}: appoints minister {mid}, which no ministers file defines")

    # personalities
    ok = set(FACTS["personalities_confirmed_in_mod"])
    known = set(FACTS["personalities_in_dh_log"])
    bad = set(FACTS["personalities_rejected"])
    for f in glob.glob(os.path.join(out, "db/ministers/*.csv")):
        for l in read(f).split("\n"):
            c = l.split(";")
            if len(c) > 9 and re.match(r"\d+$", c[0]):
                pers = c[7]
                if pers in bad:
                    E("personality", f"{os.path.basename(f)} {c[0]} {c[2]}: '{pers}' was rejected by DH")
                elif pers not in ok:
                    (W if pers in known else E)("personality",
                        f"{os.path.basename(f)} {c[0]} {c[2]}: '{pers}' " +
                        ("is in DH's list but untested in the mod" if pers in known else "is not in DH's personality list"))

    # AI sums
    for f in glob.glob(os.path.join(out, "ai/*.ai")):
        t = read(f)
        m = re.search(r"military\s*=\s*\{(.*?)\n\}", t, re.S)
        if not m:
            continue
        vals = dict(re.findall(r"^\s*(\w+)\s*=\s*([\d.]+)", m.group(1), re.M))
        total = sum(float(vals[k]) for k in DIVISION_TYPES if k in vals)
        if abs(total - 100) > 0.01:
            E("ai_sums", f"{os.path.basename(f)}: unit mix adds to {total:g}, DH requires exactly 100")

    # pictures
    have = {os.path.splitext(os.path.basename(p))[0].lower() for p in glob.glob(os.path.join(out, "gfx/**/*.bmp"), recursive=True)}
    for eid, (f, b) in events.items():
        for pic in re.findall(r'picture = "([^"]+)"', b):
            if pic.startswith("res_") and pic.lower() not in have:
                E("pictures", f"event {eid}: picture {pic} has no file")
    for f in glob.glob(os.path.join(out, "db/ministers/*.csv")) + glob.glob(os.path.join(out, "db/leaders/*.csv")) + \
             glob.glob(os.path.join(out, "db/tech/teams/*.csv")):
        for pic in set(re.findall(r";([MLT]15\d{5});", read(f))):
            if pic.lower() not in have:
                E("pictures", f"{os.path.basename(f)}: picture {pic} has no file")

    # model names
    sys.path.insert(0, ROOT)
    import units
    un = read(os.path.join(out, "config/unit_names.csv"))
    for k in units.generic_names():
        if not re.search(rf"^{k};", un, re.M):
            E("model_names", f"{k} has no generic name in config/unit_names.csv (STRING_WANTED)")

    # garrisons
    inc = read(os.path.join(out, "scenarios/resistance_1933/soviet union.inc"))
    gids = set(map(int, re.findall(r"id = \{ type = 19501 id = (\d+) \}", inc)))
    for eid, (f, b) in events.items():
        for g in map(int, re.findall(r"remove_division which = 19501 value = (\d+)", b)):
            if g not in gids:
                E("garrisons", f"event {eid}: removes unit 19501/{g}, which the scenario never creates")

    # event files
    eug = read(os.path.join(out, "scenarios/resistance_1933.eug"))
    included = set(re.findall(r'event\s*=\s*"db\\events\\([^"]+)"', eug))
    for f in ev_files:
        if os.path.basename(f) not in included:
            E("event_files", f"{os.path.basename(f)} is not included by resistance_1933.eug")
    for n in included:
        if n.startswith("res_") and not os.path.exists(os.path.join(out, "db/events", n)):
            E("event_files", f"resistance_1933.eug includes {n}, which doesn't exist")

    return errors, warnings, len(events)

if __name__ == "__main__":
    errs, warns, n = run(sys.argv[1] if len(sys.argv) > 1 else "mod")
    print(f"validate: {n} events checked, {len(errs)} errors, {len(warns)} warnings")
    for e in errs: print("  ERROR  ", e)
    for w in warns: print("  warning", w)
    sys.exit(1 if errs else 0)
