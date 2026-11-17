"""Module 2: the Chimera country, the Resistance 1933 scenario and the
1933-1941 Siberian outbreak story (war path).  Called from gen.py."""
import json, os, re
import people, ai

ROOT = os.path.dirname(os.path.abspath(__file__))
PROV = {int(k): v[0] for k, v in json.load(open(os.path.join(ROOT, "provinces.json"))).items()}
C = "UA0"
GROUND_ZERO = 1155          # Norilsk province: covers the Evenk/Tunguska wilderness
UNIT_TYPE = 19500           # unit id "type" for the Chimera (95000 was rejected: "illegal id-type")
HIVE_ARMIES = 6              # balance knobs for the starting Hive
SWARMS_PER_ARMY = 5
THRALLS_PER_ARMY = 2
CONVERSION_IC = 3            # per pre-war conversion (9500520+n), also built at Norilsk
HIVE_HEART_IC = 30          # the rest of the Hive's industry grows with the tower network (breakout.TOWER_IC)
UNIT_ID0 = 95000            # unit id numbers start here, to stay clear of other countries

ADJNAME = {int(k): v["name"] for k, v in json.load(open(os.path.join(ROOT, "adjacency.json"))).items()}
def name(p): return ADJNAME.get(p, PROV[p])

# ------------------------------------------------------------------ quiet spread, 1934-36
QUIET = [  # (event id, province, date)
    # each province borders Norilsk or an earlier one (adjacency from savedebug.txt)
    (9500510, 1164, (1, "august", 1934)),     # Ust-Kut
    (9500511, 1165, (1, "march", 1935)),      # Bratsk
    (9500512, 1177, (1, "november", 1935)),   # Nyurba
    (9500513, 1163, (1, "june", 1936)),       # Bodaybo (borders Ust-Kut)
]
OUTBREAK_DATE = (1, "february", 1937)
SOROKIN_TEAM = 1500251                        # people.SOV_TEAMS
# choices that hide the truth; three or more and the NKVD takes the lead
COVERUP_FLAGS = ["res_sov_coverup", "res_expedition_refused", "res_evenki_detained",
                 "res_weather_blamed", "res_secretary_removed", "res_sorokin_silenced"]
OUTBREAK_PROVINCE = 1156                      # Krasnoyarsk

# Chimera bonuses when they take Soviet cities (control, not ownership)
CITY_CONVERSIONS = [1156, 1142, 1148, 1138, 1162, 1167, 1151, 1132, 1131, 1128]

URAL_LINE = [1151, 1128, 1127, 1132, 1137, 1138]          # fort sites
URAL_LINE_DAYS, URAL_LINE_DONE = 42, 9500590
EVACUATION_DAYS = 90                           # the evacuation can be ordered for this long after Krasnoyarsk falls
EVACUATE = [(1142, 572), (1144, 672), (1145, 553), (1140, 654)]   # (from, to)
SCORCH = [1147, 1158, 1144, 1140, 1162, 1165]

# Cordon garrisons (OGPU troops in 1933, NKVD troops from July 1934) around the Closed Zone, at 15% strength.
# (key, province, name, event that removes it) - id type 19501 is unused by DH Full.
GARRISON_TYPE = 19501
GARRISONS = [  # (key, province, name, event that removes it, strength %): posts ~500 men, detachments ~1500
    ("cp14",     1156, "Cordon Checkpoint 14",              9500502, 5),
    ("yenisei",  1156, "Yenisei Cordon Regiment",      None,    15),
    ("kansk",    1157, "Kansk Cordon Detachment",      None,    15),
    ("ob",       1148, "Ob Cordon Detachment",         None,    15),
    ("arctic",   1152, "Arctic Cordon Detachment",     None,    15),
    ("lena",     1179, "Lena Cordon Detachment",       None,    15),
    ("ustkut",   1164, "Ust-Kut Cordon Post",          9500510, 5),
    ("bratsk",   1165, "Bratsk Cordon Post",           9500511, 5),
    ("nyurba",   1177, "Nyurba Cordon Post",           9500512, 5),
    ("bodaybo",  1163, "Bodaybo Cordon Post",          9500513, 5),
]
def garrison_id(i): return 2 * i + 2           # landunit id 2i+1, division id 2i+2

def remove_garrisons(eid):
    return [f"type = remove_division which = {GARRISON_TYPE} value = {garrison_id(i)}"
            for i, g in enumerate(GARRISONS) if g[3] == eid]

def garrisons_in(prov):
    """Locked garrisons cannot retreat: when their province is given to the Hive they are lost with it
    (otherwise they would simply take it back)."""
    return [f"type = remove_division which = {GARRISON_TYPE} value = {garrison_id(i)}"
            for i, g in enumerate(GARRISONS) if g[1] == prov]

def garrison_units():
    L = ["", "# RESISTANCE MOD: cordon garrisons (OGPU, later NKVD, troops) around the Closed Zone (understrength)"]
    for i, (_, prov, nm, _, st) in enumerate(GARRISONS):
        L += ["landunit = {", f"\tid = {{ type = {GARRISON_TYPE} id = {2 * i + 1} }}", f'\tname = "{nm}"',
              f"\tlocation = {prov}", "\tdivision = {", f"\t\tid = {{ type = {GARRISON_TYPE} id = {garrison_id(i)} }}",
              f'\t\tname = "{nm}"', f"\t\tstrength = {st}", f"\t\tmax_strength = {st}", "\t\ttype = garrison", "\t\tmodel = 3", "\t\textra = police", "\t\tbrigade_model = 1", "\t\tlocked = yes", "\t}", "}"]
    return "\n".join(L) + "\n"

def soviet_inc(src):
    s = open(src, encoding="latin-1").read().replace("\r\n", "\n")
    m = re.search(r"landunit = \{\s*\n\tid = \{ type = 10848 id = 5 \}", s)
    assert m, "NKVD landunit not found"
    import burrowers
    s = s[:m.start()] + garrison_units().lstrip("\n") + burrowers.dormant_units("SOV") + s[m.start():]
    for block in ("ownedprovinces", "controlledprovinces"):
        m = re.search(block + r"(\s*=\s*\{)([^}]*)\}", s)
        ids = [i for i in m.group(2).split() if i != str(GROUND_ZERO)]
        s = s[:m.start()] + block + m.group(1) + "  " + " ".join(ids) + " \n                             }" + s[m.end():]
    s = s.replace(" # Ministres OK", " # Ministres OK\n # RESISTANCE MOD: province 1155 (Norilsk) starts under Chimeran control", 1) \
        if " # Ministres OK" in s else "# RESISTANCE MOD: province 1155 (Norilsk) starts under Chimeran control\n" + s
    return s.split("\n")

# the Hive's starting human techs: the old hand-picked list, which hive_research extends
# Only static anti-air, researched well ahead (the Hive's Thralls, Hybrids and AA Turrets come from its own techs;
# the human infantry and AA brigade lines brought garrisons, military police and human AA)
HIVE_START_TECHS = [2800, 2450, 21180, 21190, 21200, 2460, 2470, 2480]

def _rows(xs, n=16):
    return [xs[i:i + n] for i in range(0, len(xs), n)]

def chimera_inc(hive_known):
    div = lambda i, nm, typ, model: [
        "     Division =",
        f"     {{  id       = {{  type = {UNIT_TYPE} id = {UNIT_ID0 + i}  }}",
        f'       name     = "{nm}"',
        f"       type     = {typ}",
        f"       model    = {model}",
        "       strength = 100",
        "      }"]
    L = ["##############################", "# Country definition for UA0 #", "# The Chimera (Resistance mod) #",
         "##############################", "", "country =",
         f"{{  tag                    = {C}",
         f"   capital                = {GROUND_ZERO}",
         '   ai                     = "chimera.ai"',
         "   manpower               = 600", "   energy                 = 40000", "   metal                  = 20000",
         "   rare_materials         = 10000", "   oil                    = 5000", "   supplies               = 10000",
         "   money                  = 100", "   transports             = 0", "   escorts                = 0",
         "   dissent                = 0", "",
         "   diplomacy =", "   {  relation = {  tag = SOV value = -200  }", "   }",
         f"   nationalprovinces      = {{  {GROUND_ZERO}  }}",
         f"   ownedprovinces         = {{  {GROUND_ZERO}  }}",
         f"   controlledprovinces    = {{  {GROUND_ZERO}  }}",
         "   techapps               = {",
         "   # Human groundwork (hive_research.py): static anti-air to 1942, the missions and buildings the Hive",
         "   # needs, logistics and industrial improvements up to 1936, the land doctrine trunk",
         ] + [f"   {' '.join(map(str, row))}" for row in _rows(hive_known)] + [
         "   # Chimeran Strains, Hive Warfare doctrine",
         "   95010 95510 95560 95570 95580",
         "   }",
         "   policy =",
         "   {  date              = {  year = 0 month = january day = 0  }",
         "     democratic        = 1", "     political_left    = 5", "     freedom           = 1",
         "     free_market       = 1", "     professional_army = 10", "     defense_lobby     = 10",
         "     interventionism   = 10", "    }",
         "   peacetime_ic_mod       = 1.0", "   wartime_ic_mod         = 1.0",
        ] + people.inc_ministers() + [
         "   landunit =",
         f'   {{  name     = "{people.hive_name("armynames", 1)}"',
         f"     location = {GROUND_ZERO}",
         f"     id       = {{  type = {UNIT_TYPE} id = {UNIT_ID0 + 1}  }}"]
    n, swarm, thrall = 2, 1, 1
    for army in range(HIVE_ARMIES):
        if army:
            L += ["    }", "   landunit =", f'   {{  name     = "{people.hive_name("armynames", army + 1)}"',
                  f"     location = {GROUND_ZERO}", f"     id       = {{  type = {UNIT_TYPE} id = {UNIT_ID0 + n}  }}"]
            n += 1
        L += div(n, people.div_name("HQ", army + 1), "HQ", 6); n += 1          # Angel Nexus
        for _ in range(SWARMS_PER_ARMY):
            L += div(n, people.div_name("Inf", swarm), "infantry", 18); n += 1; swarm += 1
        for _ in range(THRALLS_PER_ARMY):
            L += div(n, people.div_name("Mil", thrall), "militia", 10); n += 1; thrall += 1
    L += ["    }"]
    # dormant, locked tower guards (vanilla pattern: UK Home Guard); the tower-rise events wake them in place
    import breakout_towers
    for i, p in enumerate(breakout_towers.TOWER_PROVINCES):
        for j in range(2):
            gid = TOWER_GUARD_ID0 + 2 * i + j
            nm, typ, model = TOWER_GUARD[j]
            L.append(f'   landdivision = {{ dormant = yes id = {{ type = {UNIT_TYPE} id = {gid} }} '
                     f'name = "{ADJNAME[p]} {nm}" type = {typ} model = {model} locked = yes }}')
    # the Hive Heart's own guard at Norilsk: dormant and locked, woken by The Outbreak (9500530)
    # cycle 0 is woken by The Outbreak; cycles 1-3 by The Heart Regrows (breakout.heart_events)
    for cycle in range(HEART_GUARD_CYCLES):
        for j, (nm, typ, model) in enumerate(HEART_GUARD):
            suffix = f" ({ROMAN_REGROWN[cycle]})" if cycle else ""
            L.append(f'   landdivision = {{ dormant = yes id = {{ type = {UNIT_TYPE} id = {heart_guard_id(cycle, j)} }} '
                     f'name = "{nm}{suffix}" type = {typ} model = {model} locked = yes }}')
    # the Fall of Europe: Spire batteries for every British foothold, the London Tower's guard
    import fall_of_europe
    L += fall_of_europe.dormant_hive()
    L += ["}"]
    return L

TOWER_GUARD_ID0 = 95900          # + 2*tower index + (0|1)
HEART_GUARD_ID0 = 95950
# the guards are the Hive's own units (locked in place, so they need not be garrisons): Thralls and a Hybrid Brood
HEART_GUARD = [("Heart Thralls I", "militia", 10), ("Heart Thralls II", "militia", 10),
               ("Heart Brood", "infantry", 18)]
TOWER_GUARD = [("Brood", "infantry", 18), ("Thralls", "militia", 10)]

HEART_GUARD_CYCLES = 4           # the original guard + one per Heart Regrows (breakout.HEART_CYCLES = 3)
ROMAN_REGROWN = ["", "Regrown", "Regrown II", "Regrown III"]

def heart_guard_id(cycle, j):
    return HEART_GUARD_ID0 + len(HEART_GUARD) * cycle + j

def wake_heart_guard(cycle=0):
    return [f"type = activate_division which = {UNIT_TYPE} value = {heart_guard_id(cycle, j)} where = {GROUND_ZERO} when = 0"
            for j in range(len(HEART_GUARD))]

def scenario(src):
    s = open(src, encoding="latin-1").read().replace("\r\n", "\n")
    s = s.replace('name       = "1933_SCENARIO"', 'name       = "RES_1933_SCENARIO"', 1)
    s = s.replace('{ name       = "Grand Campaign"', '{ name       = "Resistance: The Fall of Europe"', 1)
    s = s.replace("         UPE      }", f"         UPE {C}     }}", 1)
    s = s.replace("  U02 \t     = { }\n}", f"  U02 \t     = {{ }}\n  {C}        = {{ }}\n}}", 1)
    # Non-aggression pact keeps the Soviet AI from attacking the hidden zone before the outbreak
    s = s.replace("  # ###################### 1933 TRADES #####################",
        "  # RESISTANCE MOD: the Closed Zone stays quiet until the outbreak\n"
        "  treaty =\n  { id         = { type = 16384 id = 9500 }\n    type       = non_aggression\n"
        f'    country    = "SOV"\n    country    = "{C}"\n'
        "    startdate  = { year = 1932 month = december day = 29 }\n"
        "    expirydate = { year = 1937 month = january day = 15 }\n  }\n"
        "  # ###################### 1933 TRADES #####################", 1)
    s = s.replace("  queued_events = { ",
        "  queued_events = { \n"
        "    event = { tag = SOV  id = 9500500 hour = 48 } # RESISTANCE: The Closed Zone\n"
        f"    event = {{ tag = {C}  id = 9500600 hour = 0 }} # RESISTANCE: The Hive Heart", 1)
    s = s.replace('event 	   = "db\\events\\DayofDecision.txt"',
        '# RESISTANCE MOD events\n'
        'event      = "db\\events\\res_chimeran_tech.txt"\n'
        'event      = "db\\events\\res_1933_outbreak.txt"\n'
        'event      = "db\\events\\res_breakout.txt"\n'
        'event      = "db\\events\\res_infection.txt"\n'
        'event      = "db\\events\\res_infection_abroad.txt"\n'
        'event      = "db\\events\\res_harvest.txt"\n'
        'event      = "db\\events\\res_cloven.txt"\n'
        'event      = "db\\events\\res_occupation.txt"\n'
        'event      = "db\\events\\res_towers.txt"\n'
        'event      = "db\\events\\res_cordon.txt"\n'
        'event      = "db\\events\\res_refugees.txt"\n'
        'event      = "db\\events\\res_processing.txt"\n'
        'event      = "db\\events\\res_burrowers.txt"\n'
        'event      = "db\\events\\res_fall_of_europe.txt"\n\n'
        'event 	   = "db\\events\\DayofDecision.txt"', 1)
    s = s.replace('include = "scenarios\\1933\\soviet union.inc"',
        'include = "scenarios\\resistance_1933\\soviet union.inc"\n'
        'include = "scenarios\\resistance_1933\\chimera.inc"', 1)
    # country files the mod patches (dormant Burrower coastal militia): include the mod's copies instead
    import burrowers
    for fn in burrowers.PATCHED_INC.values():
        a, b = f'include = "scenarios\\1933\\{fn}"', f'include = "scenarios\\resistance_1933\\{fn}"'
        assert a in s, a
        s = s.replace(a, b, 1)
    for must in ("RES_1933_SCENARIO", f"UPE {C}", "9500600", "res_1933_outbreak", "res_breakout", "resistance_1933\\chimera.inc", "id = 9500 }"):
        assert must in s, must
    return s.split("\n")

def owned_by_sov(p): return f"owned = {{ province = {p} data = SOV }}"
def at_war(): return f"war = {{ country = SOV country = {C} }}"

ADJ = {int(k): v["adj"] for k, v in json.load(open(os.path.join(ROOT, "adjacency.json"))).items()}

def check_spread():
    held = {GROUND_ZERO}
    for _, p, _ in QUIET + [(0, OUTBREAK_PROVINCE, 0)]:
        assert held & set(ADJ[p]), f"{name(p)} ({p}) does not border Chimeran territory"
        held.add(p)

def nkvd_empowered():
    """True when at least three cover-up flags are set (DH triggers cannot count, so list the triples)."""
    from itertools import combinations
    return "OR = { " + " ".join("AND = { " + " ".join(f"flag = {f}" for f in c) + " }"
                                for c in combinations(COVERUP_FLAGS, 3)) + " }"

def sorokin_and_report(g):
    E = []
    E += g.event(9500490, "Academician Sorokin Writes Abroad",
        "Academician Lev Sorokin, the pathologist who came back from the impact site, has been smuggling letters out "
        "of his Tomsk laboratory. They travel by courier to Barentsburg, our coal settlement on Spitsbergen, and leave "
        "on the Norwegian colliers that call there. The OGPU intercepted one. At least two others reached a colleague "
        "in Cambridge. Sorokin writes of tissue that rewrites itself and of a cold that spreads like an infection. He "
        "says the world must be told, and that he alone understands the samples.",
        [("He has seen too much. Silence him.", 60, [f"type = sleepteam which = {SOROKIN_TEAM}",
            "type = setflag which = res_sorokin_silenced", "type = trigger which = 9500491"]),
         ("Leave him to his work, whatever he says", 40, ["type = dissent value = 3",
            "type = setflag which = res_sorokin_spared", "type = setflag which = res_sanitary_protocols",
            "type = trigger which = 9500491"])],
        country="SOV", trigger=["flag = res_academy_samples", "NOT = { flag = res_outbreak }"],
        date=(1, "march", 1934), offset=60, deathdate=(31, "december", 1935))
    E += g.event(9500491, "A Letter from Barentsburg",
        "A letter from a Soviet scientist has reached Cambridge in the mailbag of a Norwegian collier out of Spitsbergen. "
        "It describes an infection in central Siberia that turns men into something else, and a cordon the Soviets "
        "have held in secret since 1926. The Secret Intelligence Service thinks it is either a hoax or the most "
        "important document of the decade.",
        [("Pass it to Porton Down", 70, ["type = activate which = 95310", "type = activate which = 95320",
            "type = activate which = 95330", "type = setflag which = res_porton_down",
            "trigger = { flag = res_sorokin_spared } type = gain_tech which = 95310"]),
         ("File it with the other Bolshevik fantasies", 30, [])],
        country="ENG")

    facts = ("Collated from OGPU and NKVD files, 1926 to 1935. The anthrax story has held for nine years. Since 1926 "
             "the Closed Zone has moved south every spring, by between forty and one hundred and twenty kilometres. "
             "Patrols that enter it do not come back as they went in. Herders, checkpoints and whole districts have "
             "fallen silent, and the frost now comes six weeks early on the Yenisei. ")
    inference = ("Inference: either this is a natural plague that will burn itself out, or it is directed and it is "
                 "preparing. If the second is true, at the present rate it will reach the Trans-Siberian Railway "
                 "within eighteen months.")
    E += g.event(9500492, "NKVD Special Report on the Closed Zone",
        "NKVD, MAIN DIRECTORATE OF STATE SECURITY. SPECIAL REPORT, MOST SECRET. " + facts + inference + " The Red Army, as presently led, is not ready to "
        "meet it. Its commanders are men who hesitate. The Organs propose to make it ready.",
        [("The Organs may proceed", 70, ["type = setflag which = res_purge_early"]),
         ("Not yet. Restrain the Organs.", 30, ["type = dissent value = 3", "type = setflag which = res_nkvd_restrained"])],
        country="SOV", trigger=[f"exists = {C}", "NOT = { flag = res_outbreak }", nkvd_empowered()],
        date=(1, "december", 1935), offset=20, deathdate=(31, "december", 1936))
    E += g.event(9500493, "Military Intelligence Report on the Closed Zone",
        "INTELLIGENCE DIRECTORATE, GENERAL STAFF OF THE RKKA. MOST SECRET. " + facts + inference + " We recommend that the Siberian "
        "Military District be prepared quietly: winter equipment, flamethrowers, quarantine drill, and officers who "
        "are told the truth.",
        [("Prepare the Siberian District quietly", 60, ["type = supplies value = -2000", "type = manpowerpool value = -10",
                                                         "type = setflag which = res_army_prepared"]),
         ("File it", 40, [])],
        country="SOV", trigger=[f"exists = {C}", "NOT = { flag = res_outbreak }", f"NOT = {{ {nkvd_empowered()} }}"],
        date=(1, "december", 1935), offset=20, deathdate=(31, "december", 1936))
    E += g.event(9500494, "The Organs Move First",
        "Armed with the Siberian file, the NKVD has convinced the Politburo that the high command of the Red Army "
        "cannot be trusted with what is coming. The arrests begin tonight.",
        [("Purge the traitors", ["type = trigger which = 9500497", "type = sleepevent which = 2007025"])],
        country="SOV", trigger=["flag = res_purge_early", f"NOT = {{ war = {{ country = SOV country = {C} }} }}",
                                "NOT = { flag = res_great_purge }"],
        date=(1, "march", 1936), offset=30, deathdate=(31, "december", 1937))
    import breakout
    E += g.event(9500497, "The Great Purge",
        "The NKVD has its lists, and the Politburo has signed them. Marshals, army commanders, commissars and "
        "thousands of officers are arrested in a single season. The Organs say the Red Army is now clean. "
        "Whether it can still fight is another question.",
        [("Purge the traitors", breakout.vanilla_purge_commands(os.path.join(g.SRC, "USSR.txt")) +
          ["type = setflag which = res_great_purge"])],
        country="SOV")
    E += g.event(9500496, "The Cold Front Is Moving",
        "The meteorologists we kept measuring have sent an urgent report. For three years the cold has crept south "
        "from the Closed Zone at a few kilometres a month, and the Zone has always followed it. Since October the "
        "front has been moving a kilometre a day. On its present course it will reach Krasnoyarsk in about ten weeks.",
        [("Alert the Siberian Military District", 70, ["type = supplies value = -500", "type = manpowerpool value = -5",
                                                        "type = setflag which = res_forewarned"]),
         ("Weathermen are not generals", 30, [])],
        country="SOV", trigger=["flag = res_cold_front_mapped", f"exists = {C}", "NOT = { flag = res_outbreak }"],
        date=(20, "november", 1936), offset=10, deathdate=(31, "january", 1937))
    E += g.event(9500495, "The Purge Is Postponed",
        "The NKVD's lists are ready, but the men on them are the only commanders who have fought the thing in "
        "Siberia. Comrade Stalin has set the files aside. They are not closed.",
        [("The Army is needed at the front", [])],
        country="SOV", trigger=[f"war = {{ country = SOV country = {C} }}", "headofstate = 30002",
                                "NOT = { flag = res_great_purge }"],
        date=(1, "january", 1936), offset=30)
    return E

# Human models the Hive picks up from its starting techs but must not build: human HQs (20th Century military
# concept), garrisons and military police (the 1870-1939 infantry techs) and human AA brigades (it has its own
# AA Turrets, model 7, from the Tunguska Strain).
SCRAP_HUMAN_MODELS = ([f"type = scrap_model which = infantry value = 0", "type = scrap_model which = militia value = 0"]
                      + [f"type = scrap_model which = hq value = {m}" for m in range(6)]
                      + [f"type = scrap_model which = garrison value = {m}" for m in range(6)]
                      + [f"type = scrap_model which = police value = {m}" for m in range(2)]
                      + [f"type = scrap_model which = anti_air value = {m}" for m in range(3)])
LOCK0 = 9500610                 # + batch: the research lock, 50 deactivations per event (hive_research.py)

def lock_events(g):
    E = []
    for k, batch in enumerate(g.hive_lock_batches):
        E += g.event(LOCK0 + k, "The Hive Has No Use for Human Science",
            "Rifles, engines, wireless sets: the Hive studies none of it. What it needs from mankind it takes.",
            [("Ignore it", batch)], country=C, text_id="RES_HIVE_LOCK")
    return E

def events(g):
    check_spread()
    E = ["#########################################################################",
         "#  RESISTANCE MOD - The Siberian Outbreak, 1933-1941 (war path)",
         "#  9500500-507  The Closed Zone (prelude) 9500510-523  Quiet spread",
         "#  9500530-531  The Outbreak              9500540-543  Foreign reactions",
         "#  9500550-553  Soviet decisions          9500560-563  Foreign aid",
         "#  9500570-573  Hive surges               9500580-589  City conversions",
         "#  9500600      The Hive Heart (start)",
         "#########################################################################", ""]
    path = ["type = activate which = 95310", "type = activate which = 95320", "type = activate which = 95330"]
    research = ["trigger = { technology = 95310 NOT = { technology = 95320 } } type = gain_tech which = 95320",
                "trigger = { NOT = { technology = 95310 } } type = gain_tech which = 95310"]

    E += g.event(9500600, "The Hive Heart",
        "Far beneath the taiga where the sky-stone fell in 1908, the Hive has grown a heart. Conversion chambers churn day and night.",
        # the Hive cannot research human weapons, vehicles, aircraft, ships or doctrines (hive_research.py)
        [("The Hive grows", SCRAP_HUMAN_MODELS + [f"type = trigger which = {LOCK0 + k}" for k in range(len(g.hive_lock_batches))]
                            + [f"type = construct which = ic where = {GROUND_ZERO} value = {HIVE_HEART_IC}",
                             f"type = construct which = infrastructure where = {GROUND_ZERO} value = 20"])],
        country=C)

    # ---------------------------------------------------------------- the prelude, 1933-34
    # A cover-up that has been running since 1926. In 1933 the secret police is the OGPU (NKVD from July 1934).
    E += g.event(9500500, "The Closed Zone",
        "TOP SECRET - OGPU, SECRET OPERATIONAL DIRECTORATE. Since the winter of 1926 the taiga around the Podkamennaya Tunguska "
        "has been closed by decree. The official story, repeated in every newspaper in the Union, is an anthrax "
        "outbreak among the Evenki reindeer herds. The truth sits in one file in the Lubyanka. Whole camps of herders "
        "vanished overnight. Patrols came back feverish, with too many eyes, and had to be shot. A vaccine trial at "
        "Tomsk in 1927 ended so badly that its records were burned. Thirty thousand men now hold a cordon that has "
        "quietly been moved south every spring. This winter the Norilsk district stopped answering altogether, "
        "and the file is now on Comrade Stalin's desk.",
        [("The cover story holds. Seal the zone tighter.", 70, ["type = setflag which = res_sov_coverup"] + path),
         ("Send an OGPU expedition into the zone", 30, ["type = manpowerpool value = -10"] + path + research[1:]
                                                        + ["type = trigger which = 9500501"])],
        country="SOV")
    E += g.event(9500501, "The Expedition Has Not Returned",
        "Radio contact with the OGPU expedition was lost after eleven days. Its last transmissions described "
        "frost in the middle of summer, empty camps with the meals still on the tables, and black towers rising "
        "out of the forest. The final message was a single word, repeated for an hour: 'cold'.",
        [("Classify everything", ["type = dissent value = 1"])], country="SOV")

    E += g.event(9500502, "Checkpoint 14 Does Not Report",
        "Cordon Checkpoint 14, on the Yenisei at the southern edge of the Closed Zone, has missed three scheduled "
        "reports. The relief column found the barracks intact, the rifles racked, the stove still warm, and no one "
        "there. Something had been dragged through the snow towards the north.",
        [("Replace the garrison and double the patrols", 60, ["type = manpowerpool value = -5"]),   # fresh men man the post
         ("Pull the cordon back fifty kilometres", 40, remove_garrisons(9500502) + ["type = dissent value = 1", "type = setflag which = res_cordon_pulled"])],
        country="SOV", trigger=[f"exists = {C}", "NOT = { flag = res_outbreak }"],
        date=(15, "may", 1933), offset=20, deathdate=(31, "december", 1933))
    E += g.event(9500503, "The Evenki Exodus",
        "Evenki herding families are crossing the cordon at night and arriving in Tura and Krasnoyarsk. Their elders "
        "tell the same story: the shamans in the north have turned into demons who devour the herds and leave "
        "sickness behind them. The local Party is asking what to do with them.",
        [("Detain them as plague carriers", 60, ["type = dissent value = 1", "type = setflag which = res_evenki_detained"]),
         ("Resettle them quietly in Kazakhstan", 40, ["type = manpowerpool value = 2"])],
        country="SOV", trigger=[f"exists = {C}", "NOT = { flag = res_outbreak }", "event = 9500502"],
        date=(1, "july", 1933), offset=20, deathdate=(31, "march", 1934))
    E += g.event(9500504, "The Academy Asks for Permission",
        "The Academy of Sciences wants to send a meteorite expedition to the 1908 impact site, unaware that it lies "
        "inside the Closed Zone. Refusing will raise questions. Agreeing means letting scientists see what we have "
        "spent seven years hiding.",
        [("Refuse, citing the anthrax quarantine", 60, ["type = dissent value = 1", "type = setflag which = res_expedition_refused",
                                                            f"type = sleepteam which = {SOROKIN_TEAM}"]),
         ("Let them go, under OGPU escort", 40, ["type = manpowerpool value = -3", "type = trigger which = 9500505"])],
        country="SOV", trigger=[f"exists = {C}", "NOT = { flag = res_outbreak }"],
        date=(1, "september", 1933), offset=20, deathdate=(31, "march", 1934))
    E += g.event(9500505, "The Academy Expedition Returns",
        "Two of the eleven scientists came back. They carried crates of samples: crystalline fragments that are "
        "always cold to the touch, and tissue that keeps growing in the jar. They have been confined to a closed "
        "laboratory in Tomsk, and they are begging to keep working.",
        [("Put them to work", ["trigger = { NOT = { technology = 95310 } } type = gain_tech which = 95310",
                               "type = setflag which = res_academy_samples"])],
        country="SOV")
    E += sorokin_and_report(g)
    E += g.event(9500506, "Winter Comes Early",
        "Frost has come to Krasnoyarsk six weeks early, and the Yenisei is freezing in October. The meteorologists "
        "cannot explain it. The cold seems to be coming from the north, from inside the Closed Zone.",
        [("Blame the weather. Say nothing.", 70, ["type = dissent value = 1", "type = setflag which = res_weather_blamed"]),
         ("Order the meteorologists to keep measuring", 30, ["type = setflag which = res_cold_front_mapped"])],
        country="SOV", trigger=[f"exists = {C}", "NOT = { flag = res_outbreak }"],
        date=(10, "october", 1933), offset=15, deathdate=(31, "january", 1934))
    E += g.event(9500507, "The Krasnoyarsk Secretary Asks Questions",
        "The First Secretary of the Krasnoyarsk regional committee has written directly to Moscow. Refugees, frozen "
        "rivers, checkpoints that fall silent: he wants to know what is happening in his own region, and he "
        "says he will not be fobbed off with anthrax.",
        [("Remove him. The cover story must hold.", 60, ["type = dissent value = -1", "type = setflag which = res_secretary_removed"]),
         ("Tell him the truth and make him part of the cordon", 40, ["type = manpowerpool value = 10",
                                                                      "type = setflag which = res_krasnoyarsk_warned"])],
        country="SOV", trigger=[f"exists = {C}", "NOT = { flag = res_outbreak }", "event = 9500506"],
        date=(1, "february", 1934), offset=20, deathdate=(31, "july", 1934))

    for n, (eid, p, date) in enumerate(QUIET):
        conv = 9500520 + n
        E += g.event(eid, f"{name(p)} Falls Silent",
            f"Telegraph lines to {name(p)} have gone dead. Supply convoys report empty villages and strange, warm towers of black metal rising from the forest.",
            [("Extend the cordon", 70, remove_garrisons(eid) + [f"type = secedeprovince which = {C} value = {p}", f"type = trigger which = {conv}"]),
             ("Send the Red Army in", 30, remove_garrisons(eid) + ["type = manpowerpool value = -15", "type = dissent value = 1"] + research +
              [f"type = secedeprovince which = {C} value = {p}", f"type = trigger which = {conv}"])],
            country="SOV", date=date, offset=60,
            trigger=[f"exists = {C}", owned_by_sov(p), "NOT = { flag = res_outbreak }"])
        E += g.event(conv, f"Conversion of {name(p)}",
            f"The people of {name(p)} have been taken into the conversion chambers. The Hive is stronger.",
            [("The Hive grows", ["type = manpowerpool value = 50",
                                 f"type = construct which = ic where = {GROUND_ZERO} value = {CONVERSION_IC}",
                                 f"type = setflag which = res_heart_conv_{n}"])],      # the Heart events darken/restore it
            country=C)

    E += g.event(9500530, "The Outbreak",
        "The Hive no longer needs to hide. From the forests of Siberia, a tide of creatures pours towards the cities of the Soviet Union.",
        [("Consume them", wake_heart_guard() + ["type = setflag which = res_outbreak", "type = war which = SOV", "type = manpowerpool value = 100",
                           "type = trigger which = 9500531", "type = trigger which = 9500540", "type = trigger which = 9500541",
                           "type = trigger which = 9500542", "type = trigger which = 9500543",
                           "type = event which = 9500565 where = SOV when = 180"])],   # cordon.py: The Yenisei Question
        country=C, date=OUTBREAK_DATE, offset=30,
        trigger=[f"exists = {C}", "NOT = { flag = res_outbreak }", f"NOT = {{ {at_war()} }}"])
    E += g.event(9500531, f"{name(OUTBREAK_PROVINCE)} Falls Silent",
        f"In a single night, {name(OUTBREAK_PROVINCE)} has been overrun. Survivors describe swarms of creatures and soldiers who changed into something else. The cordon has failed.",
        [("Declare the Siberian Emergency", 80, ["trigger = { flag = res_krasnoyarsk_warned } type = manpowerpool value = 50",
            "trigger = { flag = res_army_prepared } type = manpowerpool value = 100",
            "trigger = { flag = res_forewarned } type = manpowerpool value = 50",
            "trigger = { flag = res_forewarned } type = dissent value = -2",
            "trigger = { flag = res_army_prepared } type = gain_tech which = 95410",
            *garrisons_in(OUTBREAK_PROVINCE),
            f"type = secedeprovince which = {C} value = {OUTBREAK_PROVINCE}",
            "type = manpowerpool value = 200", "type = dissent value = 5", "type = domestic which = defense_lobby value = 1",
            ai.cmd("switch/SOV_siberian_front.ai")]),
         ("Blame saboteurs and hide the truth", 20, garrisons_in(OUTBREAK_PROVINCE) + [f"type = secedeprovince which = {C} value = {OUTBREAK_PROVINCE}",
            "type = dissent value = -2", "type = setflag which = res_sov_hidden", ai.cmd("switch/SOV_siberian_front.ai")])],
        country="SOV")

    foreign = [
        (9500540, "JAP", "Refugees on the Amur",
         "Thousands of Soviet refugees are crossing into Manchukuo with stories of monsters in Siberia. The Kwantung Army is alarmed.",
         [("Reinforce the border and study the reports", 70, path), ("This is Russia's problem", 30, ["type = belligerence value = 2"])]),
        (9500541, "GER", "Abwehr Reports from Siberia",
         "German intelligence confirms that the Soviet Union is fighting an unknown enemy in Siberia. Some in Berlin see an opportunity.",
         [("Russia's misfortune is our opportunity", 60, ["type = relation which = SOV value = -20", "type = belligerence value = 2"]),
          ("This threatens all of Europe", 40, ["type = relation which = SOV value = 20"] + path)]),
        (9500542, "ENG", "The Siberian Question",
         "The Foreign Office has received alarming reports of a catastrophe in Siberia. Moscow denies everything, but the evidence is mounting.",
         [("Watch closely", 70, path), ("Not our concern", 30, [])]),
        (9500543, "USA", "Strange News from Russia",
         "American newspapers carry wild stories of plague and monsters in Soviet Siberia. Most readers dismiss them as Bolshevik propaganda.",
         [("Keep an eye on it", ["type = relation which = SOV value = 5"])]),
    ]
    for eid, tag, title, desc, acts in foreign:
        E += g.event(eid, title, desc, acts, country=tag)

    # ------------------------------------------------------------ Soviet decisions
    war_cond = ["flag = res_outbreak", at_war()]
    # The line takes engineers on the spot and weeks of work: every line province the USSR holds needs a division
    # in it (DH's garrison trigger counts divisions; it can't see brigades), and the forts only go up after URAL_LINE_DAYS where a division still stands.
    def sov_div(p): return f"garrison = {{ country = SOV province = {p} type = land size = 1 }}"
    manned = [f"OR = {{ NOT = {{ control = {{ province = {p} data = SOV }} }} {sov_div(p)} }}" for p in URAL_LINE]
    E += g.event(9500550, "Decision: The Ural Quarantine Line",
        "Fortify the Urals and the West Siberian cities. If Siberia cannot be held, the line must hold here. Every "
        "sector needs troops and sappers on the ground, and the work will take weeks.",
        [("Build the line", ["type = setflag which = res_ural_line_building",
                             f"type = event which = {URAL_LINE_DONE} where = SOV when = {URAL_LINE_DAYS}"])],
        country="SOV", decision=war_cond,
        decision_trigger=war_cond + [f"control = {{ province = {OUTBREAK_PROVINCE} data = {C} }}",
                                     ] + manned,
        trigger=war_cond + manned, date=(1, "january", 1937), offset=7,
        deathdate=(29, "december", 1963))
    E += g.event(URAL_LINE_DONE, "The Ural Line Is Complete",
        "The sappers have finished. Where our divisions held their sectors, the Urals are now a wall of concrete "
        "and wire. Where they were driven off, the work was abandoned.",
        [("Man the line", [f"trigger = {{ control = {{ province = {p} data = SOV }} {sov_div(p)} }} "
                           f"type = construct which = land_fort where = {p} value = 2" for p in URAL_LINE]
                          + ["type = clrflag which = res_ural_line_building"])], country="SOV")
    evac_window = ["event = 9500531", f"NOT = {{ event = {{ id = 9500531 days = {EVACUATION_DAYS} }} }}"]
    E += g.event(9500551, "Decision: Evacuate Siberian Industry",
        "Dismantle the factories of Western Siberia and move them beyond the Volga before the creatures arrive.",
        [("Load the trains", sum(([f"trigger = {{ control = {{ province = {a} data = SOV }} }} type = construct which = ic where = {a} value = -2",
                                   f"trigger = {{ control = {{ province = {a} data = SOV }} }} type = construct which = ic where = {b} value = 2"]
                                  for a, b in EVACUATE), []) + ["type = dissent value = 2"])],
        # a window: from the fall of Krasnoyarsk (9500531) for EVACUATION_DAYS, after which the Hive is at the
        # factory gates. Each factory only moves if the USSR still holds its town.
        country="SOV", decision=war_cond + evac_window, decision_trigger=war_cond + evac_window, trigger=war_cond + evac_window,
        date=(1, "january", 1937), offset=7, deathdate=(29, "december", 1963))
    E += g.event(9500552, "Decision: Scorched Earth in Siberia",
        "Destroy the roads, railways and bridges in the path of the Hive. Nothing left behind can be used by the enemy, or converted.",
        [("Burn it all", [f"trigger = {{ control = {{ province = {p} data = SOV }} }} type = construct which = infrastructure where = {p} value = -30" for p in SCORCH] +
          ["type = dissent value = 3", "type = setflag which = res_sov_scorched"])],
        country="SOV", decision=war_cond, decision_trigger=war_cond + ["control = { province = 1142 data = UA0 }"],
        trigger=war_cond, date=(1, "january", 1937), offset=7, deathdate=(29, "december", 1963))
    E += g.event(9500553, "Decision: Appeal to the World",
        "Admit the truth to the capitalist powers and ask for their help. It will cost us our pride, and perhaps more.",
        [("Send the appeal", ["type = dissent value = 3", "type = relation which = ENG value = 25", "type = relation which = FRA value = 25",
                              "type = relation which = USA value = 25", "type = trigger which = 9500560", "type = trigger which = 9500561"])],
        country="SOV", decision=war_cond + ["NOT = { flag = res_sov_hidden }"],
        decision_trigger=war_cond + ["control = { province = 1142 data = UA0 }"],
        trigger=war_cond + ["NOT = { flag = res_sov_hidden }"], date=(1, "january", 1937), offset=7, deathdate=(29, "december", 1963))

    for eid, tag, reply in ((9500560, "ENG", 9500562), (9500561, "USA", 9500563)):
        E += g.event(eid, "Moscow Asks for Help",
            "The Soviet government has admitted that it is losing a war against an unknown enemy in Siberia, and asks for supplies.",
            [("Send aid", 60, ["type = money value = -100", "type = relation which = SOV value = 30", f"type = trigger which = {reply}"] + path),
             ("Refuse", 40, ["type = relation which = SOV value = -10"])],
            country=tag)
        E += g.event(reply, f"Aid from {'Britain' if tag == 'ENG' else 'America'}",
            "Ships loaded with supplies and money have arrived. It will not turn the tide, but it will help.",
            [("We are grateful", ["type = supplies value = 2000", "type = money value = 100"])], country="SOV")

    for n, year in enumerate((1938, 1939, 1940, 1941)):
        E += g.event(9500570 + n, "The Hive Surges",
            "Fed by the conquered, the conversion chambers produce new waves of Hybrids.",
            [("Onward", [f"type = manpowerpool value = {100 + 50 * n}", f"type = construct which = ic where = {GROUND_ZERO} value = 2"])],
            country=C, date=(1, "june", year), offset=30, trigger=[f"exists = {C}", at_war()])

    for n, p in enumerate(CITY_CONVERSIONS):
        E += g.event(9500580 + n, f"Conversion of {name(p)}",
            f"The population of {name(p)} has been taken. Few escaped.",
            [("The Hive grows", ["type = manpowerpool value = 50"])],
            country=C, trigger=[f"control = {{ province = {p} data = {C} }}"])
    return E

# ------------------------------------------------------------------ the Hive Harvest
# Siberia can't feed a 50+ IC war economy, so the Hive "strips the land" every month.
# One dated event per month (DH events fire once). Amounts per tier: (from year, multiplier)
HARVEST_BASE = dict(energypool=5000, metalpool=2500, rarematerialspool=1250, oilpool=400, supplies=1500, manpowerpool=60)
HARVEST_TIERS = [(1933, 1.0), (1937, 2.0), (1942, 3.0), (1947, 4.0)]
HARVEST_BONUS = [  # extra each month while the Hive controls these (province, multiplier of base)
    (1151, 0.5), (1132, 0.5), (1142, 0.5), (572, 1.0), (553, 0.5), (617, 0.5), (232, 0.5), (163, 1.0), (55, 1.0)]
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september",
          "october", "november", "december"]

def harvest_events(g):
    E = ["#########################################################################",
         "#  RESISTANCE MOD - The Hive Harvest (9502000+): monthly resources for the Chimera",
         "#  Commands: oilpool is used by vanilla; energypool, metalpool and",
         "#  rarematerialspool follow the same pattern (check savedebug.txt).",
         "#########################################################################", ""]
    n = 0
    for year in range(1933, 1964):
        mult = [m for y, m in HARVEST_TIERS if year >= y][-1]
        for mi, month in enumerate(MONTHS):
            if year == 1933 and mi < 3:
                continue
            cmds = [f"type = {k} value = {int(v * mult)}" for k, v in HARVEST_BASE.items()]
            for prov, bonus in HARVEST_BONUS:
                cmds += [f"trigger = {{ control = {{ province = {prov} data = {C} }} }} type = {k} value = {int(v * bonus)}"
                         for k, v in HARVEST_BASE.items() if k != "manpowerpool"]
            E += g.event(9502000 + n, "The Hive Harvest",
                "The Hive strips forests, mines and cities alike, feeding the conversion chambers with whatever it finds.",
                [("Consume", cmds)], country=C, trigger=[f"exists = {C}"],
                date=(1, month, year), offset=5, deathdate=(28, month, year), text_id=9502000)
            n += 1
    return E

def build(g):
    src, out = g.SRC, g.OUT
    g.write("scenarios/resistance_1933.eug", scenario(os.path.join(src, "1933.eug")))
    g.write("scenarios/resistance_1933/soviet union.inc", soviet_inc(os.path.join(src, "soviet union.inc")))
    import burrowers, fall_of_europe
    for tag, fn in burrowers.PATCHED_INC.items():
        txt = open(os.path.join(src, "inc1933", fn), encoding="latin-1").read().replace("\r\n", "\n").rstrip()
        assert txt.endswith("}"), fn
        # dormant divisions go just before the country block's closing brace, as vanilla's Home Guard does
        g.write(f"scenarios/resistance_1933/{fn}", (txt[:-1].rstrip() + "\n" + burrowers.dormant_units(tag)
                                                       + fall_of_europe.dormant_units(tag) + "}\n").split("\n"))
    import hive_research
    known, allowed, locked = hive_research.plan(src, HIVE_START_TECHS)
    cmds = hive_research.deactivate_cmds(locked)
    g.hive_lock_batches = [cmds[i:i + 50] for i in range(0, len(cmds), 50)]
    assert LOCK0 + len(g.hive_lock_batches) < 9500650
    print(f"hive research: {len(known)} known, {len(allowed)} researchable, {len(locked)} locked")
    g.write("scenarios/resistance_1933/chimera.inc", chimera_inc(hive_research.ORDER))   # prerequisite order
    g.write("db/events/res_1933_outbreak.txt", events(g) + lock_events(g))
    g.write("db/events/res_harvest.txt", harvest_events(g))
    g.write("db/events/res_fall_of_europe.txt", fall_of_europe.events(g))
    g.loc("RES_1933_SCENARIO", "Resistance: The Fall of Europe (1933)")
    ai.build(g)
    import breakout
    sov = open(os.path.join(src, "soviet union.inc"), encoding="latin-1").read()
    sov_owned = [int(i) for i in re.search(r"ownedprovinces\s*=\s*\{([^}]*)\}", sov).group(1).split()]
    breakout.build(g, ["type = activate which = 95310", "type = activate which = 95320", "type = activate which = 95330"],
                   [p for p in sov_owned if p != GROUND_ZERO], ADJ)
