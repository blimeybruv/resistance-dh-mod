"""What the Hive may research.

The Hive doesn't invent human technology. It starts with the human groundwork it needs to function (the
missions, buildings, logistics and industrial improvements up to KNOWN_YEAR), may go on researching
later improvements of the same kind, and everything else human is deactivated at game start: weapons,
vehicles, aircraft, ships, radar, codes, nuclear research and the human doctrine branches. Its own
trees (95xxx) are untouched; human weapons only reach it through The Hive Learns (steal_tech).

Deactivation is DH Full's own doctrine-exclusivity mechanism (type = deactivate which = <id>), run once by
The Hive Heart (9500600) for the Hive only.
"""
import os, re

KNOWN_YEAR = 1936
FILES = ["tech/industry_tech.txt", "tech/infantry_tech.txt", "tech/armor_tech.txt", "tech/aircraft_tech.txt",
         "tech/naval_tech.txt", "tech/air_doctrines_tech.txt", "tech/naval_doctrines_tech.txt",
         "land_doctrines_tech.txt", "secret_weapons_tech.txt"]

# known from the start whatever their kind: the missions and buildings the Hive needs, and the land
# doctrine trunk before its first branch (the Hive's own branch is Hive Warfare)
ENABLERS = {
    6500: "Tribal Warfare (attack mission)", 6510: "19th century tactics", 6530: "20th Century military concept",
    1920: "Mobilization (strategic redeployment)",
    5800: "Early Construction engineering (IC, infrastructure, forts)", 5080: "Basic Construction Engineering (air bases)",
    27500: "air doctrine root", 27510: "Bomb-dropping Doctrine (Dropship ground attack)",
    27530: "Close Air Support Concept (interdiction)", 27540: "Tactical Bomber Concept (installation strikes)",
    27550: "Strategic Bombing Concept (Chimeran Battleship strategic bombardment)",
}

# human lines the Hive has no use for, whatever their effects: it doesn't farm
EXCLUDE = ({5700, 5710, 5010, 5020, 5030, 5040, 5720, 53000, 53010}          # agriculture: it doesn't farm
           | {5600, 5610, 5620, 5630, 5640, 5650, 5660, 5670}                      # medicine: it converts its dead
           | {14000, 14010, 14020, 14030, 14040, 14110, 14120, 14130})            # hospitals
# static anti-air past the 1942 start: researchable (provincial flak, not a unit)
EXTRA_ALLOWED = {2490, 2500, 11080}
# never known or researchable: human infantry (garrisons, military police, militia) and AA brigades
NEVER = set(range(1010, 1121, 10)) | {2810, 2820, 2510}
# what these gave is replaced by the Chimeran Hive Physiology tech (95560, known from the start)

# an 'improvement' only changes the economy, logistics or construction, never a unit
IMPROVE = {"industrial_modifier", "industrial_multiplier", "research_mod", "building_prod_mod", "allow_building",
           "supply_dist_mod", "attrition_mod", "repair_mod", "tc_mod", "tc_occupied_mod", "supply_consumption",
           "relative_manpower", "trickleback_mod", "build_time", "task_efficiency"}
UNIT = {"new_model", "activate_unit_type", "scrap_model"}

def parse(path):
    s = open(path, encoding="latin-1").read()
    out = []
    for m in re.finditer(r"application\s*=\s*\{", s):
        i, depth = m.end(), 1
        while depth:
            depth += {"{": 1, "}": -1}.get(s[i], 0); i += 1
        b = re.sub(r"#[^\n]*", "", s[m.end():i - 1])
        aid = int(re.search(r"\bid\s*=\s*(\d+)", b).group(1))
        yr = re.search(r"\byear\s*=\s*(\d+)", b)
        req = re.search(r"\brequired\s*=\s*\{([^}]*)\}", b)
        orreq = re.search(r"\bor_required\s*=\s*\{([^}]*)\}", b)
        effs = b.split("effects", 1)[1] if "effects" in b else ""
        out.append(dict(id=aid, year=int(yr.group(1)) if yr else 0,
                        req=[int(x) for x in req.group(1).split()] if req else [],
                        orreq=[int(x) for x in orreq.group(1).split()] if orreq else [],
                        eff={t for t in re.findall(r"type\s*=\s*(\w+)", effs)},
                        pairs=set(re.findall(r"type\s*=\s*(\w+)(?:\s+which\s*=\s*(\w+))?", effs))))
    return out

# buildings and missions an improvement may unlock (no radar, reactors or rocket sites)
ECONOMIC_BUILDINGS = {"ic", "infrastructure", "land_fort", "coastal_fort", "naval_base", "air_base", "flak", ""}
LOGISTIC_TASKS = {"strat_redeploy"}

def is_improvement(a):
    if not a["eff"] or not a["eff"] <= IMPROVE or a["eff"] & UNIT:
        return False
    for t, w in a["pairs"]:
        if t == "allow_building" and w not in ECONOMIC_BUILDINGS: return False
        if t == "task_efficiency" and w not in LOGISTIC_TASKS: return False
    return True

def plan(src, start_known):
    """Returns (known, allowed, locked) sets of human application ids."""
    apps = {}
    for f in FILES:
        for a in parse(os.path.join(src, f)):
            if 95000 <= a["id"] < 96000:            # the mod's own Chimeran techs
                continue
            apps[a["id"]] = a
    def closure(ids):
        out, todo = set(), list(ids)
        while todo:
            t = todo.pop()
            if t in out or t not in apps: continue
            out.add(t)
            todo += apps[t]["req"]
            if apps[t]["orreq"] and not set(apps[t]["orreq"]) & out:
                todo.append(apps[t]["orreq"][0])
        return out
    improvements = {i for i, a in apps.items() if is_improvement(a) and i not in EXCLUDE}
    known = closure(set(start_known) | set(ENABLERS) |
                    {i for i in improvements if apps[i]["year"] <= KNOWN_YEAR})
    # an improvement stays researchable only if everything it requires is known or itself researchable
    allowed = (improvements | EXTRA_ALLOWED) - known
    while True:
        ok = known | allowed
        drop = {i for i in allowed if not set(apps[i]["req"]) <= ok
                or (apps[i]["orreq"] and not set(apps[i]["orreq"]) & ok)}
        if not drop: break
        allowed -= drop
    locked = set(apps) - known - allowed
    assert not known & (EXCLUDE | NEVER), known & (EXCLUDE | NEVER)
    assert not allowed & NEVER, allowed & NEVER
    global ORDER
    ORDER = prerequisite_order(known, apps)
    # sanity: nothing allowed may depend on something locked
    for i in allowed:
        assert not set(apps[i]["req"]) & locked, (i, set(apps[i]["req"]) & locked)
    return known, allowed, locked

def deactivate_cmds(locked):
    return [f"type = deactivate which = {t}" for t in sorted(locked)]

ORDER = []

def prerequisite_order(ids, apps):
    """Every tech after the techs it requires (DH may read a techapps list in order)."""
    out, seen = [], set()
    def visit(t):
        if t in seen or t not in ids: return
        seen.add(t)
        for r in apps[t]["req"] + apps[t]["orreq"]:
            visit(r)
        out.append(t)
    for t in sorted(ids, key=lambda t: (apps[t]["year"], t)):
        visit(t)
    return out
