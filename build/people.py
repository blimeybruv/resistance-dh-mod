"""Module 2b: ministers, leaders and research teams for the Chimera (UA0),
plus the mods.csv text file.  IDs 1500001-1505000 are unused by DH Full."""
import os

C = "UA0"
BASE = 1500000

# (role, name) - the Hive has no individuals, only functions
MINISTERS = [  # (post, name, personality) - spellings exactly as DH Full's savedebug lists them
    ("Head of State", "The Hive", "Ruthless Powermonger"),
    ("Head of Government", "The Hive Mind", "Silent Workhorse"),
    ("Foreign Minister", "The Silence", "Iron-fisted Brute"),
    ("Minister of Armament", "Conversion Chambers", "Infantry Proponent"),
    ("Minister of Security", "The Choir", "Prince of Terror"),
    ("Head of Military Intelligence", "The Watchers", "Technical Specialist"),
    ("Chief of Staff", "The Overmind", "School of Mass Combat"),
    ("Chief of Army", "Swarm Coordinator", "Decisive Battle Doctrine"),
    ("Chief of Navy", "Deep Spawn", "Indirect Approach Doctrine"),
    ("Chief of Air Force", "Spire Coordinator", "Army Aviation Doctrine"),
]
INC_SLOTS = ["headofstate", "headofgovernment", "foreignminister", "armamentminister",
             "ministerofsecurity", "ministerofintelligence", "chiefofstaff", "chiefofarmy",
             "chiefofnavy", "chiefofair"]

# (name, ideal rank, max skill, skill, type 0=land 1=sea 2=air)
# The Hive has no individuals, so its commanders are clones: identical names, skills and portraits.
# (name, how many, ideal rank 0=field marshal..3=major general, max skill, skill, type 0=land 1=sea 2=air)
LEADER_TIERS = [
    ("The Overmind",   8, 0, 6, 4, 0),
    ("Hive Node",     16, 1, 5, 3, 0),
    ("Swarm Node",    24, 2, 4, 2, 0),
    ("Spire Node",     4, 1, 4, 3, 2),
    ("Deep Node",      1, 2, 3, 1, 1),
]
LEADERS = [(nm, rank, mx, sk, typ, tier) for tier, (nm, n, rank, mx, sk, typ) in enumerate(LEADER_TIERS) for _ in range(n)]
assert len(LEADERS) < 100        # ids 1500101-1500199; teams start at 1500201

# (name, picture, skill, specialities) - pictures borrowed from existing DH teams
TEAMS = [
    ("Conversion Chambers", "T10510", 7, ["chemistry", "training", "infantry_focus", "individual_courage"]),
    ("Tunguska Core", "T13507", 8, ["chemistry", "electronics", "mathematics", "nuclear_physics"]),
    ("Bio-Engineering Spawn", "T10504", 6, ["mechanics", "general_equipment", "artillery", "technical_efficiency"]),
    ("Swarm Instinct", "T97200", 6, ["small_unit_tactics", "large_unit_tactics", "decentralized_execution", "combined_arms_focus"]),
    ("Tower Builders", "T13502", 5, ["industrial_engineering", "management", "mechanics"]),
]

# Soviet teams added by the mod (a separate file, so the vanilla SOV file is untouched)
SOV_TEAMS = [  # (id, name, picture, skill, start, specialities)
    (BASE + 251, "Sorokin Laboratory", "T10504", 6, 1934, ["rt_user_1", "medicine", "chemistry", "mathematics"]),
]

def sov_teams_csv():
    hdr = "SOV;Name;Pic Name;Skill;Start Year;End Year;" + ";".join(f"Speciality{i}" for i in range(1, 33)) + ";x"
    L = [hdr]
    for tid, nm, vpic, sk, start, specs in SOV_TEAMS:
        cells = specs + [""] * (32 - len(specs))
        L.append(f"{tid};{nm};{pic(f'T{tid}', vpic)};{sk};{start};1964;" + ";".join(cells) + ";x")
    return L

def ministers_csv():
    L = [f"{C};Ruling Cabinet - Start;Name;Start Year;End Year;Retirement Year;Ideology;Personality;Loyalty;Picturename;X",
         ";Replacements;;;;;;;;;X"]
    for i, (role, nm, pers) in enumerate(MINISTERS, 1):
        L.append(f"{BASE + i};{role};{nm};1908;1964;1999;FA;{pers};Very High;{pic(f'M{BASE + i}', 'unknownminister')};X")
    return L

def inc_ministers():
    return [f"   {slot:<22} = {{  type = 9 id = {BASE + i}  }} # {MINISTERS[i - 1][1]}"
            for i, slot in enumerate(INC_SLOTS, 1)]

def leaders_csv():
    L = ["Name;ID;Country;Rank 3 Year;Rank 2 Year;Rank 1 Year;Rank 0 Year;Ideal Rank;Max Skill;Traits;Skill;"
         "Experience;Loyalty;Type;Picture;Start Year;End Year;Retirement Year;x"]
    first = {}                                   # one portrait per tier: the first clone's id
    for i, (nm, rank, mx, sk, typ, tier) in enumerate(LEADERS, 1):
        first.setdefault(tier, BASE + 100 + i)
        r = [1908 if k >= rank else 1990 for k in (3, 2, 1, 0)]
        L.append(f"{nm};{BASE + 100 + i};{C};{r[0]};{r[1]};{r[2]};{r[3]};{rank};{mx};0;{sk};0;5;{typ};"
                 f"{pic(f'L{first[tier]}', 'unknownleader')};1908;1964;1999;x")
    return L

def teams_csv():
    hdr = f"{C};Name;Pic Name;Skill;Start Year;End Year;" + ";".join(f"Speciality{i}" for i in range(1, 33)) + ";x"
    L = [hdr]
    for i, (nm, vpic, sk, specs) in enumerate(TEAMS, 1):
        cells = specs + [""] * (32 - len(specs))
        L.append(f"{BASE + 200 + i};{nm};{pic(f'T{BASE + 200 + i}', vpic)};{sk};1908;1964;" + ";".join(cells) + ";x")
    return L

# Portraits: a custom picture is used once a BMP with that name exists anywhere under
# src/assets (M = minister, L = leader, T = team, followed by the ID); until then the
# vanilla placeholder is kept, so a missing picture can never break the game.
ASSET_STEMS = set()

def scan_assets(src):
    for root, _, files in os.walk(os.path.join(src, "assets")):
        ASSET_STEMS.update(os.path.splitext(f)[0].lower() for f in files if f.lower().endswith(".bmp"))

def pic(name, default):
    return name if name.lower() in ASSET_STEMS else default

FORBIDDEN = set('#;%"\\')

def insert_rows(src, rows_by_key):
    """Add rows to a vanilla text csv, before its #EOF line if it has one."""
    rows = open(src, encoding="latin-1").read().replace("\r\n", "\n").rstrip("\n").split("\n")
    new = [f"{k};" + ";".join([v] * 8) + ";;;X" for k, v in rows_by_key.items()]
    eof = next((i for i, r in enumerate(rows) if r.startswith("#EOF")), len(rows))
    return rows[:eof] + new + rows[eof:]

def mods_csv(src, text):
    rows = open(src, encoding="latin-1").read().replace("\r\n", "\n").rstrip("\n").split("\n")
    assert rows[-1].startswith("#EOF"), rows[-1]
    out = rows[:-1] + ["## ========================;RESISTANCE MOD;;;;;;;;;;X"]
    for k, v in text.items():
        bad = FORBIDDEN & set(v)
        assert not bad, f"{k}: forbidden characters {bad} in {v!r}"
        out.append(f"{k};" + ";".join([v] * 8) + ";;;X")
    out.append(rows[-1])
    return out

def append_list(src, line):
    rows = open(src, encoding="latin-1").read().replace("\r\n", "\n").rstrip("\n").split("\n")
    return rows + [line] if line not in rows else rows


ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII"]

def model_names(tag):
    """Country-specific model names (MODEL_<TAG>_<unit type>_<model>, BRIG_MODEL_<TAG>_<brigade>_<model>).
    Type numbers come from the '# MODEL_n_' / '# BRIG_MODEL_n_' headers of the db/units files:
    infantry 0, cavalry 1, militia 11, artillery brigade 1, super-heavy armour brigade 9 (the unit file header says 35, but models.csv uses 35 for super-heavy artillery)."""
    import units
    names = {}
    for typ, model, chimera, cloven in units.MODEL_NAMES:
        names[f"MODEL_{tag}_{typ}_{model}"] = chimera
        names[f"MODEL_SOV_{typ}_{model}"] = cloven          # the Cloven Red Army
    for typ, model, chimera, captured in units.BRIG_NAMES:   # Soviet names: only after The Hive Is Destroyed
        names[f"BRIG_MODEL_{tag}_{typ}_{model}"] = chimera
        names[f"BRIG_MODEL_SOV_{typ}_{model}"] = captured
    for typ, model, nm in units.HQ_NAMES:
        names[f"MODEL_{tag}_{typ}_{model}"] = nm
    for i, model in enumerate(range(6, 10)):
        names[f"MODEL_{tag}_11_{model}"] = f"Converted Thralls Gen. {ROMAN[i]}"
    for model in range(14):
        names[f"BRIG_MODEL_{tag}_1_{model}"] = "Spire Launchers"
    return names


def ordinal(n):
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"

HIVE_NAMES = {   # (unit-type code or None, name pattern, how many)
    "unitnames": [("Inf", "{} Hybrid Swarm", 300), ("Mil", "{} Thrall Horde", 200),
                  ("Cav", "{} Leaper Swarm", 150),
                  ("HQ", "{} Angel Nexus", 30), ("Gar", "{} Sentinel Node", 50)],
    "armynames": [(None, "{} Hive Brood", 100)],
    "airnames": [(None, "{} Spire Flight", 20)],
    "navynames": [(None, "{} Deep Spawn", 20)],
}

def hive_name(kind, n):
    """Name number n (1-based) from the Chimera's list, so the scenario OOB matches the names lists."""
    return HIVE_NAMES[kind][0][1].format(ordinal(n))

def div_name(code, n):
    for c, pattern, count in HIVE_NAMES["unitnames"]:
        if c == code:
            return pattern.format(ordinal(n))

def names_csv(src, kind, tag):
    rows = open(src, encoding="latin-1").read().replace("\r\n", "\n").rstrip("\n").split("\n")
    for code, pattern, count in HIVE_NAMES[kind]:
        for n in range(1, count + 1):
            nm = pattern.format(ordinal(n))
            rows.append(f"{tag};{code};{nm}" if code else f"{tag};{nm}")
    return rows
