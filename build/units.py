"""Module 5: Chimeran unit models.

DH unit stats live in db/units and are shared by every country, so the Chimera can't get
private stats for existing models. Instead, new models are appended to three unit types,
and only Chimeran techs unlock them:

  infantry (div 0)          18-20  Hybrid Swarm Gen. I-III
  cavalry (div 1)           15-16  Leaper Swarm Gen. I-II  (fast, no fuel)
  super_heavy_armor (brig)  2-3    Stalkers, Goliaths     (machines: slow, lightly armoured, heavy guns)
  heavy_armor (brig)        6      Titans                 (giant Chimera carrying Stalker-grade guns)
  medium_armor (brig)       11     Widowmakers            (Fall of Man's "main battle tank" strain)

Lore notes (Resistance wiki pages on the Stalker, Chimera and Chimeran War): Stalkers are
anti-aircraft weapons platforms that deny air support, manoeuvrable but slower than human
vehicles. Goliaths are siege batteries. Titans carry Stalker weapons and rely on
thick hide rather than armour. Widowmakers are the Chimeran equivalent of a main battle tank
in Fall of Man. Leapers are small, fast, easily killed swarmers bred to hunt hiding humans.

Targets: about 1.5x a human division of the same era in attack and staying power, much
higher morale (they don't break), no fuel use, and low supply use (they live off the land).
Comparisons are in the comments, using DH Full's own numbers."""
import os

def block(title, fields, equipment):
    L = [f"# {title}", "model = {"]
    w = max(len(k) for k in fields)
    L += [f"\t{k:<{w}} = {v}" for k, v in fields.items()]
    L += [f"\tequipment = {{ {equipment} }}", "}", ""]
    return L

def division(cost, buildtime, manpower, speed, org, morale, defence, tough, softness, supp, airdef,
             soft, hard, air, supply, upgrade=0.20):
    return {"cost": cost, "buildtime": buildtime, "manpower": manpower, "maxspeed": speed,
            "defaultorganisation": org, "morale": morale, "defensiveness": defence, "toughness": tough,
            "softness": softness, "suppression": supp, "airdefence": airdef, "softattack": soft,
            "hardattack": hard, "airattack": air, "transportweight": 10, "supplyconsumption": supply,
            "fuelconsumption": 0, "upgrade_time_factor": upgrade, "upgrade_cost_factor": 0.75,
            "reinforce_time": 0.40, "reinforce_cost": 0.30}

# NOTE: in DH Full defensiveness, toughness and airdefence are VULNERABILITIES (shown as "Defensive /
# Offensive / Air Vulnerability"): lower is better. Vanilla militia improves from 50/65 to 45/55, and
# armoured cavalry is 18/14 against horse cavalry's 22/28. Brigades lower them with negative values.
# Human 1942 infantry (model 11): soft 13 hard 4 def 35 tough 40 org 30 morale 30 airdef 14, cost 5, build 290
# Hybrid wiki: a second heart and an enlarged brain stem let them "function despite massive trauma";
# their fire is inaccurate, but "Hybrids that gang together are almost unstoppable". So: very tough,
# only moderately better firepower, and cheap and quick to build so they come in numbers.
INFANTRY = [
    (18, "Hybrid Swarm Gen. I (Chimera, 1933)",   division(4, 220, 9, 7, 40, 60, 30, 34, 90, 4, 12, 16, 4, 2, 0.8)),
    (19, "Advanced Hybrid Swarm (Chimera, 1942)",  division(4, 220, 9, 7, 45, 65, 27, 31, 88, 5, 11, 19, 6, 3, 0.8)),
    (20, "Steelhead Swarm (Chimera, 1950)", division(4, 220, 9, 7, 50, 70, 24, 28, 85, 6, 10, 22, 8, 4, 0.8)),
]
# Human 1942 mech cavalry (model 12): speed 23 soft 15 def 20 tough 26 but burns 7.5 fuel.
# Leapers are fast on foot and use no fuel, but are fragile.
CAVALRY = [
    (15, "Leaper Swarm Gen. I (Chimera, 1936)",  division(6, 280, 8, 12, 40, 60, 24, 30, 95, 6, 8, 16, 2, 1, 1.0)),
    (16, "Leaper Swarm Gen. II (Chimera, 1946)", division(6, 280, 8, 13, 45, 65, 20, 24, 92, 7, 7, 20, 4, 2, 1.0)),
]
# Human best super-heavy (model 1, 1944): soft 7 hard 10, burns 5 fuel and 4.6 supply.
def walker(soft, hard, defence, tough, org, speed_cap, cost, softness=-12):
    return {"cost": cost, "buildtime": 180, "manpower": 2, "defensiveness": defence, "toughness": tough,
            "maxspeed": 0, "softness": softness, "defaultorganisation": org, "hardattack": hard, "softattack": soft,
            "supplyconsumption": 0.6, "fuelconsumption": 0, "upgrade_time_factor": 0.8,
            "upgrade_cost_factor": 0.6, "speed_cap": speed_cap}
SUPER_HEAVY = [
    # Stalker (wiki intel): "mobile heavy weapons platform" with an AA autocannon, missile pod and
    # anti-personnel gun; "a single Stalker can make friendly air support over a battlefield
    # impossible"; superior manoeuvrability over all terrain; armoured against a catastrophic kill.
    (2, "Stalker walkers (Chimera, 1937)", dict(walker(6, 6, -3, -3, 10, 8, 9, softness=-8), airattack=6)),
    # Goliath: massive walkers that "served as siege batteries"; crushed German armour on the Oder.
    (3, "Goliath walkers (Chimera, 1946)", dict(walker(16, 16, -6, -6, 15, 5, 12, softness=-12), airattack=2)),
]
# Spire launchers and Chimeran AA turrets, so Chimeran brigades stop listing horses as equipment.
# Human 1955 field artillery: soft 9 hard 3 def -3 tough -3. Human 1956 AA: air attack 6 hard 2.
ARTILLERY = [(14, "Spire Launcher Battery (Chimera, 1936)",
              {"cost": 6, "buildtime": 120, "manpower": 2, "defensiveness": -2, "toughness": -2, "maxspeed": 0,
               "softattack": 9, "hardattack": 3, "supplyconsumption": 0.5, "fuelconsumption": 0,
               "upgrade_time_factor": 0.4, "upgrade_cost_factor": 0.55, "speed_cap": 8})]
ANTI_AIR = [(7, "Chimeran AA Turrets (Chimera, 1933)",
             {"cost": 5, "buildtime": 70, "manpower": 2, "defensiveness": 0, "hardattack": 2, "airattack": 6,
              "airdefence": -4, "maxspeed": 0, "supplyconsumption": 0.12, "fuelconsumption": 0,
              "upgrade_time_factor": 0.4, "upgrade_cost_factor": 0.5, "speed_cap": 8})]

# Menial Labour Gangs: the unarmed worker caste, attached to divisions to bridge rivers and clear the way.
# Human 1930 engineer: cost 3.5, morale 1, supply 0.1, fuel 0.09, horses and trucks. Menials need neither.
ENGINEER = [(8, "Menial Labour Gangs (Chimera, 1933)",
             {"cost": 3.5, "buildtime": 90, "manpower": 3.5, "toughness": 0, "defensiveness": 0, "maxspeed": 0,
              "morale": 1, "supplyconsumption": 0.1, "fuelconsumption": 0,
              "upgrade_time_factor": 0.4, "upgrade_cost_factor": 0.42})]

# Human heavy tank brigade 1945: soft 3 hard 6 def -4 tough -4, fuel 4.6
HEAVY = [(6, "Titans (Chimera, 1946)", walker(6, 6, -5, -5, 5, 7, 8, softness=-4))]
# Human medium tank brigade 1948: soft 6 hard 4 def -3 tough -3, fuel 3.3
MEDIUM = [(11, "Widowmakers (Chimera, 1936)", walker(6, 5, -3, -3, 6, 10, 9, softness=-8))]

# Angel Nexus HQ: an Angel and its psychic relays. Human 1943 HQ: speed 11, def 15, tough 15, supply 1.4,
# fuel 5, halftracks and tanks. The Angel keeps pace with the Hybrids, needs no fuel and no horses.
HQ = [(6, "Angel Nexus (Chimera, 1933)", {**division(8, 240, 4, 7, 40, 60, 12, 12, 70, 2, 5, 4, 1, 4, 0.8, 0.6),
                                          "transportweight": 35})]
# Thrall Horde: freshly converted humans, barely armed, thrown forward in numbers.
# Human 1945 militia (model 6): soft 6 hard 2 def 45 tough 60 org 20 morale 35, but it carries trucks and guns.
MILITIA = [(10, "Thrall Horde (Chimera, 1933)", division(3, 150, 8, 6, 30, 55, 45, 55, 100, 3, 14, 6, 1, 1, 0.3))]

def append_models(src, models, kind, equipment):
    rows = open(src, encoding="latin-1").read().replace("\r\n", "\n").rstrip("\n").split("\n")
    existing = sum(1 for r in rows if r.strip().startswith("model = {") or r.strip() == "model = {")
    assert existing == models[0][0], f"{src}: expected {models[0][0]} vanilla models, found {existing}"
    rows += ["", "#######################################################################",
             f"# RESISTANCE MOD - Chimeran {kind} (only Chimeran techs unlock these)",
             "#######################################################################", ""]
    for n, title, fields in models:
        rows += block(f"{n} - {title}", fields, equipment)
    return rows

def build(g):
    g.write("db/units/divisions/infantry.txt",
            append_models(os.path.join(g.SRC, "units/divisions/infantry.txt"), INFANTRY, "infantry", "manpower = 10000"))
    g.write("db/units/divisions/hq.txt",
            append_models(os.path.join(g.SRC, "units/divisions/hq.txt"), HQ, "HQ", "manpower = 5000"))
    g.write("db/units/divisions/militia.txt",
            append_models(os.path.join(g.SRC, "units/divisions/militia.txt"), MILITIA, "militia", "manpower = 10000"))
    g.write("db/units/divisions/cavalry.txt",
            append_models(os.path.join(g.SRC, "units/divisions/cavalry.txt"), CAVALRY, "cavalry", "manpower = 8000"))
    for name, models, kind, equipment in (("interceptor", INTERCEPTOR, "fighters", "fighter = 100 manpower = 100"),
                                          ("cas", CAS, "dropships", "bomber = 100 manpower = 200"),
                                          ("strategic_bomber", STRAT, "battleships", "heavy_bomber = 100 manpower = 1000"),
                                          ("naval_bomber", NAVAL_BOMBER, "hunter dropships", "bomber = 100 manpower = 200")):
        g.write(f"db/units/divisions/{name}.txt",
                append_models(os.path.join(g.SRC, f"units/divisions/{name}.txt"), models, kind, equipment))
    g.write("db/units/brigades/artillery.txt",
            append_models(os.path.join(g.SRC, "units/brigades/artillery.txt"), ARTILLERY, "Spire launchers", "manpower = 2000"))
    g.write("db/units/brigades/anti_air.txt",
            append_models(os.path.join(g.SRC, "units/brigades/anti_air.txt"), ANTI_AIR, "AA turrets", "manpower = 2000"))
    g.write("db/units/brigades/engineer.txt",
            append_models(os.path.join(g.SRC, "units/brigades/engineer.txt"), ENGINEER, "Menial labour gangs", "manpower = 3500"))
    g.write("db/units/brigades/heavy_armor.txt",
            append_models(os.path.join(g.SRC, "units/brigades/heavy_armor.txt"), HEAVY, "Titans", "manpower = 2000"))
    g.write("db/units/brigades/medium_armor.txt",
            append_models(os.path.join(g.SRC, "units/brigades/medium_armor.txt"), MEDIUM, "Widowmakers", "manpower = 2000"))
    g.write("db/units/brigades/super_heavy_armor.txt",
            append_models(os.path.join(g.SRC, "units/brigades/super_heavy_armor.txt"), SUPER_HEAVY, "walkers", "manpower = 2000"))

def generic_names():
    """{key: name} for config/unit_names.csv: MODEL_<type>_<n> / BRIG_MODEL_<brigade>_<n>."""
    clean = lambda t: t.split(" (")[0]
    out = {}
    for typ, models in (("0", INFANTRY), ("1", CAVALRY), ("10", HQ), ("11", MILITIA), ("13", INTERCEPTOR),
                        ("17", CAS), ("14", STRAT), ("16", NAVAL_BOMBER)):
        for n, title, _ in models:
            out[f"MODEL_{typ}_{n}"] = clean(title)
    for brig, models in (("9", SUPER_HEAVY), ("8", HEAVY), ("29", MEDIUM), ("1", ARTILLERY), ("11", ANTI_AIR), ("13", ENGINEER)):
        for n, title, _ in models:
            out[f"BRIG_MODEL_{brig}_{n}"] = clean(title)
    return out

# names for models.csv: (unit-type key, model, Chimera name, Cloven name for the USSR)
MODEL_NAMES_LAND = ([("0", 18, "Hybrid Swarm", "Cloven Rifle Division"), ("0", 19, "Advanced Hybrid Swarm", "Cloven Rifle Division II"),
                ("0", 20, "Steelhead Swarm", "Cloven Rifle Division III")]
               + [("1", n, f"Leaper Swarm Gen. {r}", f"Cloven Shock Division Gen. {r}") for n, r in ((15, "I"), (16, "II"))])
HQ_NAMES = [("10", n, "Angel Nexus") for n in range(7)] + [("11", 10, "Thrall Horde")]   # Angels command the hive mind
BRIG_NAMES = [("9", 2, "Stalkers", "Captured Stalkers"), ("9", 3, "Goliaths", "Captured Goliaths"),
              ("8", 6, "Titans", "Cloven Titans"), ("1", 14, "Spire Launcher Battery", "Captured Spire Launchers"),
              ("11", 7, "Chimeran AA Turrets", "Captured AA Turrets"), ("29", 11, "Widowmakers", "Tamed Widowmakers"),
              ("13", 8, "Menial Labour Gangs", "Captured Menial Gangs")]  # 9 = super-heavy armour in models.csv (Mark I, Maus); 35 is super-heavy artillery


# ------------------------------------------------------------------ the Chimeran air fleet
def plane(cost, build, speed, sdet, adet, sdef, adef, air, strat, soft, hard, naval, rng, supply, morale=60, org=40,
          transport=None):
    d = {"cost": cost, "buildtime": build, "defaultorganisation": org, "morale": morale, "manpower": 1,
         "maxspeed": speed, "surfacedetectioncapability": sdet, "airdetectioncapability": adet,
         "surfacedefence": sdef, "airdefence": adef, "airattack": air, "strategicattack": strat,
         "softattack": soft, "hardattack": hard, "navalattack": naval, "range": rng,
         "supplyconsumption": supply, "fuelconsumption": 0, "upgrade_time_factor": 0.60,
         "upgrade_cost_factor": 0.50, "reinforce_time": 0.60, "reinforce_cost": 0.50}
    return d

# Chimeran Fighter (wiki): "could easily take on modern day fighter planes, particularly the F-86 Sabre",
# but their pilots are "systematic" and predictable. Human 1950 interceptor: air attack 11, speed 1100,
# air defence 3, air detection 11.
INTERCEPTOR = [
    (17, "Chimeran Fighter (Chimera, 1938)", plane(22, 200, 950, 6, 8, 3, 6, 11, 0, 1, 0, 0, 800, 1.0)),
    (18, "Chimeran Fighter II (Chimera, 1950)", plane(24, 200, 1200, 7, 9, 3, 7, 14, 0, 2, 1, 1, 1000, 1.0)),
]
# Dropship "buzzard" (wiki intel): armed shuttles giving "limited close air-support", "better armoured
# than equivalent human aircraft". Human 1948 CAS: soft 6 hard 6 air defence 8.
# surfacedefence and airdefence are VULNERABILITIES for aircraft too (human interceptor airdefence 30 -> 3 over
# the tree): "better armoured" means lower. Human 1938 CAS: surface 5-8, air 15.
CAS = [(7, "Chimeran Dropship (Chimera, 1938)", plane(18, 230, 500, 4, 2, 4, 10, 3, 0, 6, 4, 2, 700, 1.0))]
# Hunter Dropship: the Dropship hull fitted to hunt shipping. Human 1941 naval bomber: naval 6, speed 350,
# surface 8, air 30, range 1500. Shorter-ranged: it never strays far from the tower network.
NAVAL_BOMBER = [(9, "Hunter Dropship (Chimera, 1940)", plane(17, 240, 450, 3, 2, 5, 16, 3, 0, 2, 3, 8, 1000, 1.2))]
# Chimeran Battleship: airships "as large as the towers", energy blasts, Spire missiles and hundreds of
# fighters in their hangars. Human 1958 intercontinental bomber: strategic 14, air defence 8, speed 800.
STRAT = [(10, "Chimeran Battleship (Chimera, 1950)", plane(45, 360, 300, 6, 6, 2, 6, 6, 14, 8, 4, 4, 6000, 3.0, org=50))]

AIR_MODEL_NAMES = [("13", 17, "Chimeran Fighter", "Captured Chimeran Fighter"),
                   ("13", 18, "Chimeran Fighter II", "Captured Chimeran Fighter II"),
                   ("17", 7, "Dropship 'Buzzard'", "Captured Dropship"),
                   ("16", 9, "Hunter Dropship", "Captured Hunter Dropship"),
                   ("14", 10, "Chimeran Battleship", "Captured Chimeran Battleship")]

MODEL_NAMES = MODEL_NAMES_LAND + AIR_MODEL_NAMES
