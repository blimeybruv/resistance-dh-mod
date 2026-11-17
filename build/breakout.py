"""Module 3: the Soviet collapse, the Chimeran breakout (east, south, west)
and the WWII interplay in Europe.  War path.  Called from gen.py."""
import os, re
import ai

C = "UA0"
def ctl(p, tag=C): return f"control = {{ province = {p} data = {tag} }}"
def war(a, b=C): return f"war = {{ country = {a} country = {b} }}"
def any_of(*conds): return "OR = { " + " ".join(conds) + " }"
DEATH = (29, "december", 1963)

# key provinces (ids from the DH Full map_1 adjacency report)
P = dict(moscow=572, leningrad=553, kazan=672, kuybyshev=668, gorky=680, saratov=669, stalingrad=663,
         yaroslavl=677, kiev=617, minsk=599, kharkov=636, sverdlovsk=1151, chelyabinsk=1132, perm=687,
         ufa=1131, irkutsk=1162, chita=1169, tashkent=1103, almaata=504, ashkhabad=1097, baku=713,
         tbilisi=709, warsaw=232, berlin=163, vienna=195, prague=207, budapest=284, bucharest=316,
         paris=55, calais=49, dunkirk=51, brussels=116, amsterdam=122, rotterdam=125)

# breakout stages: (event id, title, description, trigger provinces (any), countries to attack)
STAGES = [
    (9500750, "The Hive Turns East",
     "Having consumed eastern Siberia, the Hive spills over the Mongolian steppe and the Amur.",
     ["irkutsk", "chita"], ["MON", "TAN", "MAN", "U62"]),
    (9500751, "The Hive Turns South",
     "The cities of Soviet Central Asia have fallen. The Hive now looks south, to Persia, Afghanistan and Xinjiang.",
     ["tashkent", "almaata", "ashkhabad"], ["PER", "AFG", "SIK", "UPE"]),
    (9500752, "Through the Caucasus",
     "The Hive has crossed the Caucasus. Turkey and Persia stand in its path.",
     ["baku", "tbilisi"], ["TUR", "PER"]),
    (9500753, "Breakout West: The Borderlands",
     "With the heart of Russia consumed, the Hive turns on the nations of Eastern Europe.",
     ["moscow", "leningrad", "minsk", "kiev"],
     ["FIN", "EST", "LAT", "LIT", "POL", "ROM", "U40", "U41", "U43", "U44"]),
    (9500754, "Into the Heart of Europe",
     "Warsaw and Bucharest have fallen. Nothing now stands between the Hive and Central Europe.",
     ["warsaw", "bucharest"], ["GER", "HUN", "CZE", "SLO", "AUS", "YUG", "BUL", "SWE", "NOR", "DEN"]),
    (9500755, "The West Will Burn",
     "Berlin, Vienna and Prague are silent. The Hive marches on Western Europe.",
     ["berlin", "vienna", "prague"], ["FRA", "VIC", "U01", "HOL", "BEL", "LUX", "SCH", "ITA", "GRE", "ALB"]),
    (9500756, "The Channel",
     "The Hive stands on the shores of the English Channel. Britain is the last bastion of free Europe.",
     ["paris", "calais", "dunkirk", "brussels", "amsterdam", "rotterdam"], ["ENG", "IRE", "POR", "SPA", "SPR"]),
]
STAGE_AI = {9500753: "switch/UA0_europe.ai", 9500755: "switch/UA0_west.ai", 9500756: "switch/UA0_channel.ai"}

# Germany's eastern provinces for the Ostwall (fortified only if Germany controls them)
OSTWALL = [184, 181, 167, 158, 224, 223, 254, 232, 235, 243, 247]
VOLGA_LINE = ["kazan", "kuybyshev", "saratov", "stalingrad", "gorky", "yaroslavl"]

# nations that get a "The Chimera Are Here" mobilisation event when the Hive attacks them
FRONT_NATIONS = ["FIN", "EST", "LAT", "LIT", "POL", "ROM", "GER", "HUN", "CZE", "AUS", "YUG", "BUL", "GRE",
                 "SWE", "NOR", "DEN", "FRA", "HOL", "BEL", "ITA", "ENG", "TUR", "PER", "AFG", "MON", "JAP",
                 "MAN", "SCH", "SPA", "POR", "IRE", "CHI", "SIK"]

EUROPE_CITIES = ["moscow", "leningrad", "kiev", "minsk", "kazan", "gorky", "kuybyshev", "stalingrad", "kharkov",
                 "warsaw", "berlin", "prague", "vienna", "budapest", "bucharest", "paris", "brussels",
                 "amsterdam", "tashkent", "baku"]

# ------------------------------------------------------------------ the Stavka junta (9500710)
# Ten days after Moscow falls, Stalin and the Politburo are missing and the generals take over.
# Who is left to take over depends on whether the Great Purge happened (vanilla event 2007025).
# (post slot, post name, personality, [after the Purge: name, picture], [no Purge: name, picture])
JUNTA = [
    ("headofstate", "Head of State", "Resigned Generalissimo", ("Kliment Y. Voroshilov", "3183"), ("Mikhail N. Tukhachevsky", "L10342")),
    ("headofgovernment", "Head of Government", "Old General", ("Boris M. Shaposhnikov", "3195"), ("Aleksandr I. Egorov", "L9896")),
    ("foreignminister", "Foreign Minister", "General Staffer", ("Aleksandr M. Vasilevsky", "3198"), ("Kliment Y. Voroshilov", "3183")),
    ("armamentminister", "Minister of Armament", "Infantry Proponent", ("Grigory I. Kulik", "L10055"), ("Ieronim P. Uborevich", "L10346")),
    ("ministerofsecurity", "Minister of Security", "Efficient Sociopath", ("Filipp I. Golikov", "3194"), ("Yan B. Gamarnik", "L9934")),
    ("ministerofintelligence", "Head of Military Intelligence", "Technical Specialist", ("Ivan I. Proskurov", "3193"), ("Yan K. Berzin", "3181")),
    ("chiefofstaff", "Chief of Staff", "School of Maneuver", ("Georgy K. Zhukov", "3197"), ("Boris M. Shaposhnikov", "3195")),
    ("chiefofarmy", "Chief of Army", ("Elastic Defense Doctrine", "Decisive Battle Doctrine"), ("Semyon K. Timoshenko", "3201"), ("Iona E. Yakir", "L10371")),
    ("chiefofnavy", "Chief of Navy", "Base Control Doctrine", ("Nikolai G. Kuznetsov", "3202"), ("Vladimir M. Orlov", "M4009")),
    ("chiefofair", "Chief of Air Force", "Army Aviation Doctrine", ("Aleksandr A. Novikov", "3208"), ("Yakov I. Alksnis", "3184")),
]
JUNTA_ID = {True: 1500340, False: 1500350}       # +1..+10, after the Purge / without it
STALIN_CABINET = [30001, 30002, 30003, 30004, 30012, 30015, 30016, 30017, 30019, 30021, 30026, 30028, 30032]

def junta_ministers_csv():
    L = ["SOV;Ruling Cabinet - Start;Name;Start Year;End Year;Retirement Year;Ideology;Personality;Loyalty;Picturename;X",
         ";Replacements;;;;;;;;;X"]
    for purged in (True, False):
        for i, (slot, post, pers, after, before) in enumerate(JUNTA, 1):
            nm, pic = after if purged else before
            p_ = (pers[0] if purged else pers[1]) if isinstance(pers, tuple) else pers
            # available from 1936 so the event can appoint them (an unavailable minister may not be appointable)
            L.append(f"{JUNTA_ID[purged] + i};{post};{nm};1936;1964;1999;ST;{p_};Very High;{pic};X")
    return L

SOROKIN_TEAM, SOROKIN_ENG_TEAM, SOROKIN_CHECKPOINT = 1500251, 1500265, 9500498

def sorokin_checkpoint_event(g):
    """Two versions: Britain knows the name from the Barentsburg letter (he was spared and wrote), or not."""
    acts = [("Fly him to Porton Down", 90, ["type = setflag which = res_sorokin_britain",
                "type = activate which = 95310", "type = activate which = 95320", "type = activate which = 95330",
                f"type = waketeam which = {SOROKIN_ENG_TEAM}",
                "trigger = { NOT = { technology = 95310 } } type = gain_tech which = 95310",
                "trigger = { technology = 95310 } type = gain_tech which = 95320"]),
            ("Leave him to the refugee commission", 10, [])]
    tail = ("He was travelling on forged papers with two of his assistants and a suitcase of notebooks. The "
            "local police have handed all three over to men from our legation, and he has asked for asylum. "
            "Moscow, such as it is now, has not asked for him back.")
    return (g.event(SOROKIN_CHECKPOINT, "A Name at the Checkpoint",
                "A refugee checkpoint in eastern Europe has flagged a name on our watch list: Academician Lev "
                "Sorokin, the Tomsk pathologist whose letters from Barentsburg first told us what was in Siberia. "
                + tail, acts, country="ENG")
            + g.event(SOROKIN_CHECKPOINT + 1, "A Name at the Checkpoint",
                "A refugee checkpoint in eastern Europe has stopped a man whose papers do not match his face. Under "
                "questioning he gave his real name: Academician Lev Sorokin, a Tomsk pathologist who says he has "
                "studied the Siberian infection since 1927. " + tail, acts, country="ENG"))

def junta_event(g):
    purged, kept = "flag = res_great_purge", "NOT = { flag = res_great_purge }"
    cmds = ["type = setflag which = res_stavka"] + [f"type = sleepminister which = {m}" for m in STALIN_CABINET]
    for is_purged, cond in ((True, purged), (False, kept)):
        cmds += [f"trigger = {{ {cond} }} type = {slot} which = {JUNTA_ID[is_purged] + i}"
                 for i, (slot, *_rest) in enumerate(JUNTA, 1)]
    # Sorokin, if still working for the USSR, slips out in the chaos; Britain picks him up (9500498)
    alive = "NOT = { flag = res_sorokin_silenced } NOT = { flag = res_expedition_refused }"
    cmds += [f"trigger = {{ {alive} }} type = sleepteam which = {SOROKIN_TEAM}",
             f"trigger = {{ {alive} }} type = setflag which = res_sorokin_fled",
             f"trigger = {{ {alive} flag = res_sorokin_spared }} type = event which = {SOROKIN_CHECKPOINT} where = ENG when = 45",
             f"trigger = {{ {alive} NOT = {{ flag = res_sorokin_spared }} }} type = event which = {SOROKIN_CHECKPOINT + 1} where = ENG when = 45"]
    cmds += ["type = dissent value = 5", "type = domestic which = democratic value = -1",
             "type = domestic which = defense_lobby value = 2"]
    return g.event(9500710, "The Kremlin Is Silent",
        "The special train that left Moscow on the last night never reached Kuibyshev. Somewhere east of the "
        "Volga the line goes dead, and the reconnaissance flights find only the carriages, their doors open, "
        "standing in the snow. Comrade Stalin, the Politburo and the People's Commissars are gone. The marshals "
        "and commanders who are still alive have formed a State Defence Council and taken every ministry into "
        "military hands. Nobody voted for them. Nobody is left who could have.",
        [("The Stavka takes command", cmds)], country="SOV")

def patch_ussr(src):
    """Stop the vanilla 'Transfer of Industry to Siberia' decisions from moving factories into Chimeran
    Siberia.  Harmless in other scenarios, where UA0 never exists."""
    s = open(src, encoding="latin-1").read().replace("\r\n", "\n")
    guard = "NOT = { war = { country = SOV country = UA0 } } # RESISTANCE MOD"
    for eid in (2007041, 2007042, 2007043):
        start = s.index(f"\tid = {eid}\n")
        end = s.index("\n}\n", start)
        block = s[start:end]
        new = re.sub(r"(\n\t(decision|trigger) = \{\n)", r"\1\t\t" + guard + "\n", block)
        assert new.count(guard) == 2, eid
        s = s[:start] + new + s[end:]
    # The Great Officer Purge waits while the Hive is at war with the USSR
    start = s.index("\tid = 2007025\n"); end = s.index("\n}\n", start)
    block = s[start:end]
    new = block.replace("\ttrigger = {\n", "\ttrigger = {\n\t\t" + guard + "\n", 1)
    assert new != block
    # mark that the Purge happened, whichever event carried it out (vanilla's or the mod's early one)
    a = new.index("\taction = {")
    new = new[:a] + new[a:].replace("\t\tcommand =", "\t\tcommand = { type = setflag which = res_great_purge } # RESISTANCE MOD\n\t\tcommand =", 1)
    s = s[:start] + new + s[end:]
    return s.split("\n")

def vanilla_purge_commands(src):
    """The command lines of vanilla 2007025's action, to replay in the mod's own early-Purge event
    (firing 2007025 itself with 'trigger' did nothing in game: its own date/trigger evidently still apply)."""
    t = open(src, encoding="latin-1").read().replace("\r\n", "\n")
    start = t.index("\tid = 2007025\n"); end = t.index("\n}\n", start)
    act = t[t.index("\taction = {", start, end):end]
    return [re.sub(r"\s*#.*$", "", l).strip()[len("command = {"):-1].strip()
            for l in act.split("\n") if l.strip().startswith("command = {") and l.strip().endswith("}")
            or (l.strip().startswith("command = {") and "#" in l)]

def events(g, path_cmds):
    E = ["#########################################################################",
         "#  RESISTANCE MOD - The Breakout (war path)",
         "#  9500700-709  Soviet collapse (709 replaces vanilla 2007041)        9500750-756  Chimeran breakout stages",
         "#  9500760-769  WWII in Europe         9500800-832  Nations attacked by the Hive",
         "#  9500850-860  Late Hive surges       9500900-919  City conversions",
         "#########################################################################", ""]
    sov_war = war("SOV")

    # ---------------------------------------------------------------- Soviet collapse
    # replaces vanilla 2007041 (blocked above while fighting the Hive), with the same effect
    E += g.event(9500709, "The State Defence Committee",
        "The Hive is tearing through Siberia. To direct the war against an enemy no one understands, Comrade Stalin "
        "has formed the State Defence Committee and taken personal control of the government.",
        [("All power to the Committee", ["trigger = { headofgovernment = 30016 } type = headofgovernment which = 30144",
                                          "type = dissent value = -2"])],
        # fires on its own (it was a decision, easily forgotten, and only ever a benefit)
        country="SOV", trigger=[sov_war, "lost_national = { country = SOV value = 3 }"],
        date=(1, "january", 1937), offset=5, deathdate=DEATH)

    E += g.event(9500700, "The Urals Have Fallen",
        "Sverdlovsk and Chelyabinsk have gone silent. The industrial heart of the Urals now feeds the Hive.",
        [("Not one step back!", 60, ["type = manpowerpool value = 150", "type = dissent value = 3", ai.cmd("switch/SOV_volga_line.ai")]),
         ("Evacuate the Ural population westward", 40, ["type = manpowerpool value = 50", "type = dissent value = -2", ai.cmd("switch/SOV_volga_line.ai")])],
        country="SOV", trigger=[sov_war, any_of(ctl(P["sverdlovsk"]), ctl(P["chelyabinsk"]))],
        date=(1, "january", 1937), offset=7, deathdate=DEATH)
    E += g.event(9500701, "Decision: The Volga Line",
        "Fortify the cities of the Volga. If the Hive crosses the river, Moscow is lost.",
        [("Dig in on the Volga", ["type = money value = -200"] +
          [f"trigger = {{ {ctl(P[c], 'SOV')} }} type = construct which = land_fort where = {P[c]} value = 3" for c in VOLGA_LINE])],
        country="SOV", decision=[sov_war, "event = 9500700"], decision_trigger=[sov_war, ctl(P["ufa"])],
        trigger=[sov_war, "event = 9500700"], date=(1, "january", 1937), offset=7, deathdate=DEATH)
    E += g.event(9500702, "Moscow in Peril",
        "The Hive has crossed the Volga. Its vanguard is days from the capital.",
        [("Comrade Stalin stays in Moscow", 50, ["type = dissent value = -3", "type = manpowerpool value = 100"]),
         ("Evacuate the government to Leningrad", 50, [f"type = capital which = {P['leningrad']}", "type = dissent value = 3",
                                                       "type = setflag which = res_sov_evacuated"])],
        country="SOV", trigger=[sov_war, ctl(P["moscow"], "SOV"), ctl(P["leningrad"], "SOV"),
                                any_of(ctl(P["kazan"]), ctl(P["gorky"]), ctl(P["kuybyshev"]))],
        date=(1, "january", 1937), offset=7, deathdate=DEATH)
    E += g.event(9500703, "The Fall of Moscow",
        "Moscow has fallen. The Kremlin is silent, and the red flag no longer flies over the city.",
        [("Fight on from Leningrad", 70, [f"trigger = {{ {ctl(P['leningrad'], 'SOV')} }} type = capital which = {P['leningrad']}",
                                          "type = dissent value = 10", "type = manpowerpool value = 100",
                                          "type = event which = 9500710 where = SOV when = 10"]),
         ("Disperse into the forests and fight on as partisans", 30, ["type = dissent value = 5", "type = setflag which = res_sov_partisans",
                                                                      "type = event which = 9500710 where = SOV when = 10"])]
        , country="SOV", trigger=[sov_war, ctl(P["moscow"])], date=(1, "january", 1937), offset=7, deathdate=DEATH)
    E += g.event(9500704, "The Soviet Union Is No More",
        "Moscow and Leningrad have fallen. What remains of the Soviet state is a scattering of armies and refugees fleeing west.",
        [("Remember us", ["type = setflag which = res_sov_collapse", "type = trigger which = 9500705",
                          "type = trigger which = 9500706", "type = trigger which = 9500707", "type = trigger which = 9500708"])],
        country="SOV", trigger=[sov_war, ctl(P["moscow"]), ctl(P["leningrad"])],
        date=(1, "january", 1937), offset=7, deathdate=DEATH)
    for eid, tag, opts in (
        (9500705, "ENG", [("Rearm at once", 70, ["type = domestic which = defense_lobby value = 1", "type = dissent value = -2"] + path_cmds),
                          ("Hope the Germans hold", 30, [])]),
        (9500706, "FRA", [("Strengthen the Maginot Line", 70, ["type = domestic which = defense_lobby value = 1"] + path_cmds),
                          ("Hope the Germans hold", 30, [])]),
        (9500707, "GER", [("Germany is now Europe's shield", 100, ["type = domestic which = defense_lobby value = 1", "type = dissent value = -3"] + path_cmds)]),
        (9500708, "USA", [("This is Europe's war", 50, []),
                          ("America must prepare", 50, ["type = domestic which = interventionism value = 1",
                                                        "type = relation which = ENG value = 20"] + path_cmds)])):
        E += g.event(eid, "The Fall of Russia",
            "The Soviet Union has collapsed. Refugees describe an enemy that does not take prisoners, only converts. "
            "The Hive will not stop at the old Soviet border.", opts, country=tag)

    # ---------------------------------------------------------------- Chimeran AI retargeting
    E += g.event(9500740, "The Hive Looks West",
        "Western Siberia is falling. The Hive turns its attention to the Urals and the factories beyond them.",
        [("Onward to the Urals", [ai.cmd("switch/UA0_urals.ai")])], country=C,
        trigger=[any_of(ctl(1142), ctl(1138))], date=(1, "january", 1937), offset=7, deathdate=DEATH)
    E += g.event(9500741, "Beyond the Urals",
        "The Ural mountains are no barrier. Ahead lie the Volga, Moscow and the heart of Russia.",
        [("Onward to Moscow", [ai.cmd("switch/UA0_russia.ai")])], country=C,
        trigger=[any_of(ctl(1151), ctl(1132))], date=(1, "january", 1937), offset=7, deathdate=DEATH)

    # ---------------------------------------------------------------- breakout stages
    for eid, title, desc, provs, targets in STAGES:
        cmds = [f"trigger = {{ exists = {t} NOT = {{ {war(t)} }} }} type = war which = {t}" for t in targets]
        cmds += [f"type = manpowerpool value = 150", f"type = setflag which = res_stage_{eid}"]
        if eid in STAGE_AI: cmds.append(ai.cmd(STAGE_AI[eid]))
        E += g.event(eid, title, desc, [("The Hive hungers", cmds)], country=C,
                     trigger=[f"exists = {C}", any_of(*[ctl(P[p]) for p in provs])],
                     date=(1, "january", 1937), offset=7, deathdate=DEATH)

    # ---------------------------------------------------------------- WWII in Europe
    gerwar = war("GER")
    E += g.event(9500760, "The Eastern Horror",
        "The Soviet Union is being devoured by an enemy no one understands. The generals ask how the Reich should respond.",
        [("Build the Ostwall", 80, ["type = money value = -150"] +
          [f"trigger = {{ {ctl(p, 'GER')} }} type = construct which = land_fort where = {p} value = 2" for p in OSTWALL]),
         ("Strike Russia while it bleeds", 20, ["type = belligerence value = 5", "type = relation which = SOV value = -50"])],
        country="GER", trigger=["exists = GER", sov_war, any_of(ctl(P["moscow"]), ctl(P["kazan"]), ctl(P["gorky"]))],
        date=(1, "january", 1937), offset=7, deathdate=DEATH)
    E += g.event(9500761, "Armistice in the West?",
        "The Reich is fighting the Hive in the East and the Western Allies at the same time. Some in Berlin argue that "
        "Europe must stand together or fall separately.",
        [("Offer an armistice to London and Paris", 70, ["type = trigger which = 9500762", "type = trigger which = 9500763"]),
         ("Fight on two fronts", 30, ["type = dissent value = 2"])],
        country="GER", trigger=["exists = GER", gerwar, any_of(war("GER", "ENG"), war("GER", "FRA"))],
        date=(1, "january", 1938), offset=14, deathdate=DEATH)
    for eid, tag in ((9500762, "ENG"), (9500763, "FRA")):
        E += g.event(eid, "Berlin Offers an Armistice",
            "Germany proposes an end to the war in the West so that every army in Europe can face the Hive.",
            [("Accept. Europe must stand together", 60, [f"trigger = {{ {war(tag, 'GER')} }} type = peace which = GER",
                                                        "type = relation which = GER value = 50", "type = setflag which = res_armistice"]),
             ("Never. Not with Hitler", 40, ["type = relation which = GER value = -20"])],
            country=tag)

    # ---------------------------------------------------------------- the United European Defence
    UED = ["FRA", "BEL", "HOL", "LUX", "POL", "CZE", "DEN", "NOR", "SWE", "SCH", "AUS", "GER", "ITA"]
    E += g.event(9500770, "The United European Defence",
        "Towns along the old Soviet border are emptying overnight. Whatever is coming out of Russia, no European "
        "nation can face it alone. London proposes a supranational alliance: the United European Defence.",
        [("Form the UED", 70, [f"trigger = {{ exists = {t} NOT = {{ war = {{ country = ENG country = {t} }} }} }} type = alliance which = {t}"
                                for t in UED] + ["type = setflag which = res_ued"]),
         ("Britain will look after Britain", 30, ["type = setflag which = res_avalon"])],
        country="ENG", trigger=["flag = res_stage_9500753"], date=(1, "january", 1937), offset=14, deathdate=DEATH)

    # ---------------------------------------------------------------- nations under attack
    for n, tag in enumerate(FRONT_NATIONS):
        E += g.event(9500800 + n, "The Chimera Are Here",
            "The creatures have crossed our border. Every man and woman who can hold a rifle is called to the colours.",
            [("To arms!", ["type = manpowerpool value = 50", "type = dissent value = 2",
                           "type = domestic which = defense_lobby value = 1"])],
            country=tag, trigger=[war(tag)], date=(1, "january", 1937), offset=3, deathdate=DEATH)

    # ---------------------------------------------------------------- the Hive keeps growing
    for n, year in enumerate(range(1942, 1953)):
        E += g.event(9500850 + n, "The Hive Surges",
            "Fed by the conquered, the conversion chambers produce new waves of Hybrids.",
            [("Onward", [f"type = manpowerpool value = {300 + 50 * n}", "type = construct which = ic where = 1155 value = 2"])],
            country=C, date=(1, "june", year), offset=30, trigger=[f"exists = {C}", "atwar = yes"])
    for n, city in enumerate(EUROPE_CITIES):
        p = P[city]
        nm = g_name(p)
        E += g.event(9500900 + n, f"Conversion of {nm}",
            f"The population of {nm} has been taken. Few escaped.",
            [("The Hive grows", ["type = manpowerpool value = 100"])], country=C, trigger=[ctl(p)])
    return E

# No free units: the programme ties up factories (as building the divisions would) until the first Cloven are ready
CLOVEN_IC, CLOVEN_DAYS, CLOVEN_READY = 10, 90, 9500424
CLOVEN_IC_FROM = [572, 553, 672]          # Moscow, Leningrad, Kazan: the first the USSR holds lends the IC

def cloven_ic(sign):
    """sign -1: take the IC from the first held city and remember which; +1: give it back there."""
    cmds = []
    for k, p in enumerate(CLOVEN_IC_FROM):
        if sign < 0:
            cond = " ".join([f"control = {{ province = {p} data = SOV }}"] +
                            [f"NOT = {{ control = {{ province = {q} data = SOV }} }}" for q in CLOVEN_IC_FROM[:k]])
            cmds += [f"trigger = {{ {cond} }} type = construct which = ic where = {p} value = -{CLOVEN_IC}",
                     f"trigger = {{ {cond} }} type = setflag which = res_cloven_ic_{p}"]
        else:
            cmds += [f"trigger = {{ flag = res_cloven_ic_{p} }} type = construct which = ic where = {p} value = {CLOVEN_IC}",
                     f"type = clrflag which = res_cloven_ic_{p}"]
    return cmds

CLOVEN_SPAWN = [1151, 672, 572]          # Sverdlovsk, Kazan, Moscow: the first the USSR holds
CLOVEN_DIVS = ["1st Cloven Rifle Division", "2nd Cloven Rifle Division"]

def cloven_corps():
    """The first volunteers, as divisions on the map (model 18 is the Cloven Rifle Division for the USSR).
    Building more needs the Tunguska Strain the decision unlocks."""
    cmds = []
    for k, p in enumerate(CLOVEN_SPAWN):
        cond = " ".join([f"control = {{ province = {p} data = SOV }}"] +
                        [f"NOT = {{ control = {{ province = {q} data = SOV }} }}" for q in CLOVEN_SPAWN[:k]])
        cmds.append(f'trigger = {{ {cond} }} type = add_corps which = "Special Corps Cloven" value = land where = {p}')
        cmds += [f'trigger = {{ {cond} }} type = add_division which = "{d}" value = infantry when = 18' for d in CLOVEN_DIVS]
    return cmds

# Tunguska Strain opens Hive Mind (and Hive Physiology after it) to whoever knows it. Both are the Hive's own
# (Angel Nexus HQ, Thrall Hordes, the Hive's body), so a USSR given the Strain has them locked first.
HIVE_ONLY_LOCK = [f"type = deactivate which = {t}" for t in (95510, 95560, 95570, 95580)]

def cloven_events(g, path_cmds):
    """The Cloven: Soviet soldiers given a Chimeran serum. In Resistance lore the vaccine made them immune
    to conversion but drove them mad. Here it hands the USSR the Hive's own strains: an alien-influenced Red Army."""
    sov_war = war("SOV")
    E = ["#########################################################################",
         "#  RESISTANCE MOD - The Cloven (9500420-439): the alien-influenced Red Army, and its price",
         "#########################################################################", ""]
    E += g.event(9500420, "Decision: The Cloven Programme",
        "Our doctors believe the inhibitor serum can do more than slow the infection. Injected in massive doses, "
        "it makes a soldier immune to conversion and gives him some of the Hive's own strength. The volunteers "
        "who survive are no longer quite human. The NKVD calls them the Cloven.",
        [("Begin the injections", HIVE_ONLY_LOCK + ["type = activate which = 95010", "type = gain_tech which = 95010", "type = manpowerpool value = -30",
                                   "type = dissent value = 3", "type = setflag which = res_cloven"] + cloven_ic(-1)
                                  + [f"type = event which = {CLOVEN_READY} where = SOV when = {CLOVEN_DAYS}"])],
        # no longer needs lost national provinces: a USSR that holds the line could never take it
        country="SOV", decision=[sov_war, "technology = 95320"], decision_trigger=[sov_war, "technology = 95320"],
        trigger=[sov_war, "technology = 95320"],
        date=(1, "january", 1937), offset=7, deathdate=DEATH)
    E += g.event(CLOVEN_READY, "The First Cloven",
        "Three months of injections, fevers and funerals are over. The volunteers who lived are ready: two divisions "
        "of men who no longer feel cold or pain. The laboratories and the factories they borrowed return to normal work.",
        [("Send them to the front", cloven_ic(+1) + cloven_corps())], country="SOV")
    # canon: Malikov's vaccine (1927) turned almost 90% of inoculated soldiers into feral cannibals by 1930
    E += g.event(9500421, "Cloven Madness",
        "The Cloven fight like devils, but they no longer sleep, rarely speak, and have begun to eat the dead. "
        "Whole companies have turned on their officers. In Russia this has happened before: the old Tsarist "
        "files speak of a Doctor Malikov, a vaccine, and an army that went mad.",
        [("Isolate them in special camps", 50, ["type = manpowerpool value = -150", "type = dissent value = 3"]),
         ("Point them at the enemy and look away", 50, ["type = dissent value = 8", "type = setflag which = res_cloven_unleashed",
                                                        "type = trigger which = 9500423"])],
        country="SOV", trigger=["event = { id = 9500420 days = 180 }"],
        date=(1, "january", 1937), offset=14, deathdate=DEATH)
    E += g.event(9500423, "The Cloven Desert",
        "Unleashed Cloven divisions have abandoned the front. They roam the rear areas in packs, attacking Hybrids "
        "and Red Army soldiers alike. The NKVD reports entire villages devoured.",
        [("Hunt them down", 60, ["type = manpowerpool value = -200", "type = dissent value = 5"]),
         ("Let the Hive and the Cloven kill each other", 40, ["type = dissent value = 10"])],
        country="SOV", trigger=["flag = res_cloven_unleashed", "event = { id = 9500421 days = 120 }"],
        date=(1, "january", 1937), offset=14, deathdate=DEATH)
    E += g.event(9500422, "Decision: Expand the Cloven Divisions",
        "The serum works. With a second, refined strain, every rifle division in the Red Army could fight like the Cloven.",
        [("Inoculate the army", ["type = activate which = 95020", "type = activate which = 95030",
                                 "type = gain_tech which = 95020", "type = gain_tech which = 95030",
                                 "type = dissent value = 4", "type = manpowerpool value = -50"])],
        country="SOV", decision=["event = 9500421", "technology = 95330"], decision_trigger=["event = 9500421", "technology = 95330"],
        trigger=["event = 9500421", "technology = 95330"], date=(1, "january", 1937), offset=14, deathdate=DEATH)
    # if the Hive is wiped out
    E += g.event(9500430, "The Hive Is Destroyed",
        "The last Chimeran stronghold has been burned out. Siberia is ours again, littered with alien machines, "
        "conversion chambers and things our scientists cannot name.",
        # the only human route into Chimeran Engineering: the Hive's own machines, taken from its corpse
        # 95010 must be activated too: every Engineering tech needs it, and gain_tech alone is only a blueprint
        [("Seize the alien technology", 70, HIVE_ONLY_LOCK + [f"type = activate which = {t}" for t in (95010, 95110, 95120, 95130, 95140, 95150, 95160, 95170)] + [
            "type = gain_tech which = 95110", "type = gain_tech which = 95010",
            "type = dissent value = -5", "type = setflag which = res_hive_destroyed",
            "type = trigger which = 9500431", "type = trigger which = 9500432", "type = trigger which = 9500433"] + path_cmds),
         ("Burn it all. Nothing from the Hive must survive", 30, ["type = dissent value = -10", "type = setflag which = res_hive_destroyed",
            "type = trigger which = 9500431", "type = trigger which = 9500432", "type = trigger which = 9500433"])],
        country="SOV", trigger=["flag = res_outbreak", f"NOT = {{ exists = {C} }}"],
        date=(1, "january", 1937), offset=7, deathdate=DEATH)
    for eid, tag, opts in (
        (9500431, "GER", [("The Bolsheviks now have alien weapons. We must strike first", 40, ["type = belligerence value = 5"]),
                          ("Prepare the Reich for what Russia has become", 60, ["type = domestic which = defense_lobby value = 1"])]),
        (9500432, "ENG", [("Demand that Moscow share its findings", 60, ["type = relation which = SOV value = -10"] + path_cmds),
                          ("Congratulate Moscow", 40, ["type = relation which = SOV value = 20"])]),
        (9500433, "USA", [("A victory for mankind", ["type = relation which = SOV value = 10"])])):
        E += g.event(eid, "The Soviets Have Won in Siberia",
            "Moscow announces that the Siberian enemy has been annihilated. Rumours speak of Red Army soldiers "
            "who no longer feel pain, and of alien machines being shipped west by rail.", opts, country=tag)
    return E

# Purging a town costs 2 dissent instead of 3 once the Great Purge is over (a cowed country and a free
# hand for the NKVD) AND the USSR prepared in some way: the army warned, the meteorologists heeded, or
# Sorokin's sanitary protocols. The Purge waits while the Hive is at war, so only an early (pre-1937)
# Purge unlocks this.
CHEAP_PURGE = ("AND = { flag = res_great_purge OR = { flag = res_army_prepared flag = res_forewarned "
               "flag = res_sanitary_protocols } }")

QUARANTINE, SERUM = 95310, 95320
THRALL0 = 9520000          # 9520000+province: the Hive raises Thralls from an abandoned town

def infection_options(tag, p, extra_abandon=(), purge_cmds=None, serum_cost=25):
    """The three answers to an outbreak. Abandon is always on the table (and is action a, so the AI
    always has a valid pick); Purge needs Quarantine Protocols; Inoculate needs Inhibitor Serum
    Trials, keeps the town and costs only money."""
    purge_cmds = purge_cmds or ["type = manpowerpool value = -10", "type = dissent value = 2"]
    return [
        ("Abandon it to the Hive", 20, list(extra_abandon) + [
            f"type = secedeprovince which = {C} value = {p}", "type = dissent value = 1",
            f"type = event which = {THRALL0 + p} where = {C} when = 1"]),
        ("Purge the infected", 40, purge_cmds, [f"technology = {QUARANTINE}"]),
        ("Inoculate the survivors", 60, [f"type = money value = -{serum_cost}"], [f"technology = {SERUM}"]),
    ]

def infection_events(g, sov_provinces, adjacency):
    import story
    """The Hive converts behind the lines: any Soviet province bordering Chimeran-held land can
    be lost to infection. One event per province (DH events fire once)."""
    E = []
    for n, p in enumerate(sorted(sov_provinces)):
        near = [q for q in adjacency.get(p, []) if q != p]
        # Tower sites can only be taken by force: abandoning one with troops inside let them walk
        # straight back in and kill the newly arrived Angel.
        if not near or p in [t for t, _ in TOWERS]:
            continue
        nm = g_name(p)
        E += g.event(9501000 + n, f"Infection at {nm}",
            f"Refugees from the front have brought the virus to {nm}. Whole districts are turning. "
            "The local commander asks for orders.",
            infection_options("SOV", p, story.garrisons_in(p),
                ["type = manpowerpool value = -25",
                 f"trigger = {{ NOT = {{ {CHEAP_PURGE} }} }} type = dissent value = 3",
                 f"trigger = {{ {CHEAP_PURGE} }} type = dissent value = 2"], serum_cost=40),
            country="SOV", trigger=[war("SOV"), f"owned = {{ province = {p} data = SOV }}",
                                    f"NOT = {{ {ctl(p)} }}", any_of(*[ctl(q) for q in near])],
            date=(1, "january", 1937), offset=60, deathdate=DEATH)
    return E

def thrall_events(g, provinces):
    """A town given up to the Hive does not stay empty: its people are marched to the conversion
    centres and come back as a Thrall militia division."""
    E = []
    for p in sorted(provinces):
        nm = g_name(p)
        E += g.event(THRALL0 + p, f"The Thralls of {nm}",
            f"The townsfolk of {nm} have been processed. They shamble out of the conversion centre in "
            "columns, armed with whatever the Hive could spare.",
            [("More bodies for the Hive", [f"type = addcore which = {p}",
                                          f'type = add_corps which = "Thralls of {nm}" value = land where = {p}',
                                          f'type = add_division which = "Thrall Horde of {nm}" value = militia when = 10'])],
            country=C)
    return E

# Where the Hive goes after the Soviet Union, and who might own each region by then (owners at start
# plus anyone likely to have conquered it). One event per (province, tag): the 'owned' trigger means
# only the current owner's version can fire, so a province changing hands is still covered.
SPREAD = {
    "Finland": "FIN SOV", "Baltic States": "EST LAT LIT POL SOV GER", "Poland": "POL GER SOV LIT CZE",
    "Romania": "ROM SOV HUN BUL", "Czechoslovakia": "CZE GER HUN POL", "Hungary": "HUN GER ROM CZE YUG",
    "Austria": "AUS GER ITA", "Germany": "GER POL FRA CZE LIT", "Balkan": "YUG BUL GRE ALB ROM ITA TUR GER",
    "Anatolia": "TUR GRE SOV", "Persia": "PER SOV ENG", "Afghanistan": "AFG SOV ENG",
    "Benelux": "HOL BEL LUX GER", "France": "FRA GER ITA", "Denmark": "DEN GER", "Switzerland": "SCH GER ITA FRA",
    "Italy": "ITA GER", "Norway": "NOR GER SWE", "Sweden": "SWE GER FIN", "Korea": "JAP",
    "China": "MON MAN CHI CHC SIK CXB CSX JAP", "Krasnoyarsk": "TAN SOV",
}
CHINA_REACH = 4            # only the part of China within this many provinces of the Soviet border

def spread_provinces(sov_provinces, adjacency):
    import cordon
    from collections import deque
    sov = set(sov_provinces) | {story_ground_zero()}
    dist, q = {p: 0 for p in sov}, deque(sov)
    while q:
        x = q.popleft()
        for y in adjacency.get(x, []):
            if y not in dist and y in cordon.PROV:
                dist[y] = dist[x] + 1; q.append(y)
    out = []
    for p, (nm, area, region) in sorted(cordon.PROV.items()):
        if p in sov or region not in SPREAD: continue
        if region == "China" and dist.get(p, 99) > CHINA_REACH: continue
        out.append((p, SPREAD[region].split()))
    return out

def story_ground_zero():
    import story
    return story.GROUND_ZERO

FIRST_CONTACT0 = 9509900

def foreign_infection_events(g, sov_provinces, adjacency):
    """The virus doesn't stop at the Soviet border. Same three answers as in the USSR; the techs
    that unlock Purge and Inoculate reach each country through a first-contact event."""
    import cordon
    E, tags, n = [], [], 0
    land = lambda q: q in cordon.PROV
    for p, owners in spread_provinces(sov_provinces, adjacency):
        near = [q for q in adjacency.get(p, []) if q != p and land(q)]
        if not near: continue
        nm = g_name(p)
        for t in owners:
            if t not in tags and t != "SOV": tags.append(t)
            E += g.event(9510000 + n, f"Infection at {nm}",
                f"The virus has crossed into {nm}. Refugees, soldiers and the dead are all carrying it now, "
                "and the town is turning street by street.",
                infection_options(t, p), country=t,
                trigger=[war(t), f"owned = {{ province = {p} data = {t} }}", f"NOT = {{ {ctl(p)} }}",
                         any_of(*[ctl(q) for q in near])],
                date=(1, "january", 1937), offset=60, deathdate=DEATH, text_id=f"RESINF{p}")
            n += 1
    assert 9510000 + n < 9520000, n
    for i, t in enumerate(tags):
        E += g.event(FIRST_CONTACT0 + i, "The Russian Papers",
            "Our first battles with the Chimera have taught us what the Soviets learned too late: the "
            "enemy's real weapon is the virus. Moscow's quarantine manuals and serum notes, smuggled out "
            "through refugees and prisoners, are now on our ministers' desks.",
            [("Begin quarantine research", [f"type = activate which = {QUARANTINE}", f"type = activate which = {SERUM}",
                                            "type = activate which = 95330", f"type = gain_tech which = {QUARANTINE}"])],
            country=t, trigger=[war(t), f"NOT = {{ flag = res_alert_{t} }}"],
            date=(1, "january", 1934), offset=15, deathdate=DEATH)
    assert FIRST_CONTACT0 + len(tags) < 9510000
    return E + don_alert_events(g, tags)

# The Don alert: once the Hive reaches the Don (about Moscow's longitude), Eastern Europe is warned.
# If Britain passed Sorokin's letter to Porton Down, London circulates real science; otherwise rumours.
DON = [654, 653, 655, 659, 649, 644]     # Voronezh, Pavlovsk, Uryupinsk, Kalach, Kamensk, Rostov
ALERTED = "POL ROM FIN EST LAT LIT CZE HUN TUR GER".split()
DON_ALERT0 = 9509800                      # +i: London version   +50+i: rumour version

def don_alert_events(g, contact_tags):
    E = []
    reached = any_of(*[ctl(p) for p in DON], ctl(P["moscow"]), "flag = res_stavka")
    techs = ["type = activate which = 95310", "type = activate which = 95320", "type = activate which = 95330"]
    for i, t in enumerate(ALERTED):
        common = [reached, f"NOT = {{ {war(t)} }}", f"NOT = {{ event = {FIRST_CONTACT0 + contact_tags.index(t)} }}"]
        heed = techs + [f"type = setflag which = res_alert_{t}"]
        E += g.event(DON_ALERT0 + i, "Word from London",
            "The Chimera have reached the Don. The British government has quietly circulated to every capital "
            "east of the Rhine a dossier from its laboratory at Porton Down: the Siberian infection, how it "
            "spreads, how a town can be sealed, and what a serum might do. The dossier is based on the work "
            "of a Soviet scientist who wrote to Cambridge years ago, when nobody believed him.",
            [("Put our laboratories on it at once", 90, heed + ["type = gain_tech which = 95310"]),
             ("British scaremongering. File it.", 10, [])],
            country=t, trigger=common + ["flag = res_porton_down"],
            date=(1, "january", 1936), offset=15, deathdate=DEATH, text_id="RES_DON_LONDON")
        E += g.event(DON_ALERT0 + 50 + i, "The Don Has Fallen",
            "The Chimera have reached the Don. What crosses our eastern border now is rumour: Red Army "
            "deserters who speak of soldiers who rise again, train crews who will not say what they saw "
            "east of Voronezh, and a Soviet press that has gone entirely silent. Nobody in the West has studied "
            "this enemy, but our doctors can at least start.",
            [("Heed the warning", 80, heed),
             ("Bolshevik propaganda", 20, [])],
            country=t, trigger=common + ["NOT = { flag = res_porton_down }", f"NOT = {{ event = {DON_ALERT0 + i} }}"],
            date=(1, "january", 1936), offset=15, deathdate=DEATH, text_id="RES_DON_RUMOUR")
    assert DON_ALERT0 + 50 + len(ALERTED) < FIRST_CONTACT0
    return E

def occupation_events(g, sov_provinces, capital=572):
    """Occupied Soviet land becomes Hive land. There is no peace with the Hive, so occupied provinces
    would otherwise stay Soviet-owned forever: no infrastructure repair, no manpower, no resources,
    and supply crawling back to Norilsk. 9503000+n: the USSR writes the province off;
    9504000+n: the Hive rebuilds its roads (infrastructure +40)."""
    E = []
    for n, p in enumerate(sorted(sov_provinces)):
        if p == capital:
            continue
        nm = g_name(p)
        E += g.event(9503000 + n, f"The Dead Zone at {nm}",
            f"There is nothing left at {nm} to liberate. The Hive has torn down the old town and is building something of its own.",
            [("Strike it from the map", [f"type = secedeprovince which = {C} value = {p}", f"type = trigger which = {9504000 + n}"])],
            country="SOV", trigger=[war("SOV"), f"owned = {{ province = {p} data = SOV }}", ctl(p)],
            date=(1, "january", 1937), offset=30, deathdate=DEATH, text_id=None)
        E += g.event(9504000 + n, f"The Hive Builds at {nm}",
            "Menials lay down roads of black metal and power conduits. Supplies now flow to the front.",
            [("The Hive grows", hive_builds_cmds(p))],
            country=C)
    return E

def hive_builds_cmds(p):
    """Shared by every 'The Hive Builds' event: roads, and a core (Hive land now: no more revolts).
    Hybrid armies come from the regional Processing milestones (milestones.py), not from single towns."""
    return [f"type = construct which = infrastructure where = {p} value = 40", "type = manpowerpool value = 5",
            f"type = addcore which = {p}"]

# the Hive moves its heart west as it advances, so supply doesn't crawl back to Norilsk
CAPITALS = [(9500745, 1156), (9500746, 1142), (9500747, 1151), (9500748, 672), (9500749, 572)]

def capital_events(g):
    E = []
    for eid, p in CAPITALS:
        E += g.event(eid, f"The Hive Moves West: {g_name(p)}",
            f"A new heart is growing at {g_name(p)}. Conversion chambers, power conduits and spire silos follow it west.",
            [("The Hive moves", [f"type = capital which = {p}", f"type = construct which = infrastructure where = {p} value = 30",
                                 f"type = setflag which = res_hive_capital_{p}"])],
            # once-only guard: the log shows these being run again and again
            country=C, trigger=[f"owned = {{ province = {p} data = {C} }}", ctl(p), f"NOT = {{ flag = res_hive_capital_{p} }}"],
            date=(1, "january", 1934), offset=14, deathdate=DEATH)
    return E

# Losing Norilsk used to cripple the Hive: nearly all its IC is there, it is the capital (unless the heart has
# already moved west), and the battle leaves it at 10 infrastructure. Three cycles of wound and regrowth.
# where the capital goes: the westernmost of these the Hive owns and holds (the heart always moves west)
HEART_EXILE = [572, 672, 1131, 1151, 1142, 1148, 1156, 1162]   # Moscow, Kazan, Ufa, Sverdlovsk, Novosibirsk, Tomsk, Krasnoyarsk, Irkutsk
HEART_CYCLES = 3                  # story.HEART_GUARD_CYCLES must be HEART_CYCLES + 1
HEART0 = 9500780                  # +2k: wounded, +2k+1: regrows

def heart_events(g):
    import story
    gz = story.GROUND_ZERO
    held = lambda p: f"owned = {{ province = {p} data = {C} }} {ctl(p)}"
    exile = []
    for k, p in enumerate(HEART_EXILE):
        cond = " ".join([held(p)] + [f"NOT = {{ {held(q)} }}" for q in HEART_EXILE[:k]])
        exile += [f"trigger = {{ {cond} }} type = capital which = {p}",
                  f"trigger = {{ {cond} }} type = setflag which = res_heart_exile"]
    # the pre-war conversions also built IC at Norilsk (story.CONVERSION_IC each, flagged res_heart_conv_n)
    conv_ic = lambda sign: [f"trigger = {{ flag = res_heart_conv_{n} }} type = construct which = ic where = {gz} "
                            f"value = {sign * story.CONVERSION_IC}" for n in range(len(story.QUIET))]
    nowhere = " ".join(f"NOT = {{ AND = {{ {held(p)} }} }}" for p in HEART_EXILE)
    E = []
    for k in range(HEART_CYCLES):
        wid, rid = HEART0 + 2 * k, HEART0 + 2 * k + 1
        after = [f"event = {HEART0 + 2 * k - 1}"] if k else ["flag = res_outbreak"]
        E += g.event(wid, "The Heart Is Wounded",
            "The humans are inside Norilsk. As the heart was cut off, the conversion chambers died with it: what the "
            "invaders have found is a city of cold organic vats they can neither run nor understand. The Hive's will "
            "must flow from another place until the heart is retaken.",
            # the Hive Heart's factories go dark rather than falling into human hands; Regrows gives them back
            [("Endure", exile + conv_ic(-1) + [f"type = construct which = ic where = {gz} value = -{story.HIVE_HEART_IC}",
                                 "type = supplies value = 3000", "type = oilpool value = 500"])],
            country=C, trigger=after + [f"exists = {C}", f"NOT = {{ {ctl(gz)} }}"],
            date=(1, "january", 1934), offset=1, deathdate=DEATH, text_id="RES_HEART_WOUNDED")
        E += g.event(rid, "The Heart Regrows",
            "Norilsk is ours again. Menials are already clearing the rubble, the first conduits are pulsing and the "
            "vats are warm again. The heart will beat again.",
            # the capital only comes home if the Hive holds none of the western hubs
            [("The Hive heals", story.wake_heart_guard(k + 1) + [f"trigger = {{ flag = res_heart_exile {nowhere} }} type = capital which = {gz}",
                                 "type = clrflag which = res_heart_exile",
                                 f"type = construct which = ic where = {gz} value = {story.HIVE_HEART_IC}",
                                 *conv_ic(+1),
                                 f"type = construct which = infrastructure where = {gz} value = 40",
                                 "type = supplies value = 5000", "type = oilpool value = 1000"])],
            country=C, trigger=[f"event = {wid}", ctl(gz)],
            date=(1, "january", 1934), offset=1, deathdate=DEATH, text_id="RES_HEART_REGROWS")
    return E

# Chimeran towers (lore: Angels live in the towers and hold the hive mind together; when the London
# tower fell, every Chimera in Britain died within minutes). One tower per region of Russia.
TOWERS = [(1155, "Krasnoyarsk"), (1142, "Novosibirsk"), (1162, "Irkutsk"), (1148, "Tomsk"), (1151, "Urals"),
          (1131, "Eastern Russia"), (672, "Northern Russia"), (572, "Russia"), (617, "Ukraine"), (599, "Belarus"),
          (1103, "Central Asia"), (504, "Kazakstan"), (1190, "Far East Siberia"), (713, "Kaukasus"),
          (663, "Southern Russia")]

# The tower network powers the Hive (lore: the towers channel its power). Each tower carries part of its industry,
# so the Hive's IC grows and moves west as it advances, and goes dark when a tower falls.
TOWER_IC = 5

def tower_events(g):
    E = []
    for i, (p, region) in enumerate(TOWERS):
        nm = g_name(p)
        E += g.event(9505000 + i, f"A Tower Rises at {nm}",
            f"The Hive has unearthed something beneath {nm}: a tower of black metal, older than mankind. "
            f"An Angel has taken up residence inside, and the Chimera of the whole {region} region answer to it.",
            # every tower gets a garrison of its own, so a band of partisans can't walk in and kill the Angel
            [("The Angel watches", [f"type = setflag which = res_tower_{p}", "type = manpowerpool value = 50",
                                    # wake the two dormant, locked guards from the scenario (they can never be moved away)
                                    *[f"type = activate_division which = 19500 value = {95900 + 2 * TOWER_PROVINCES.index(p) + j} where = {p} when = 0"
                                      for j in range(2)],
                                    f"type = construct which = land_fort where = {p} value = 3",
                                    f"type = construct which = ic where = {p} value = {TOWER_IC}",
                                    f"type = construct which = infrastructure where = {p} value = 20"])],
            country=C, trigger=[f"owned = {{ province = {p} data = {C} }}", ctl(p), f"NOT = {{ flag = res_tower_{p} }}"],
            date=(1, "january", 1933), offset=14, deathdate=DEATH)
        E += g.event(9505100 + i, f"The Tower at {nm} Has Fallen",
            f"Human soldiers have broken into the tower at {nm} and killed the Angel inside. Across the {region} "
            "region the Chimera are collapsing where they stand, their link to the hive mind severed.",
            # Hand back only the Hive's own provinces in the region, one by one, so land held by anyone else
            # (the buffer states above all) is never touched. Buffer-state provinces go to them if they exist.
            [("The link is severed", __import__("cordon").tower_release(region) + [
                                      "type = manpowerpool value = -300", f"type = setflag which = res_tower_fallen_{p}",
                                      # the tower's factories die with the Angel: nothing for the captor to take
                                      f"type = construct which = ic where = {p} value = -{TOWER_IC}",
                                      f"type = trigger which = {9505200 + i}"])],
            country=C, trigger=[f"exists = {C}", f"flag = res_tower_{p}", f"NOT = {{ {ctl(p)} }}", "atwar = yes",
                                f"NOT = {{ flag = res_tower_fallen_{p} }}"],
            date=(1, "january", 1933), offset=3, deathdate=DEATH)
        E += g.event(9505200 + i, f"The Angel of {nm} Is Dead",
            f"Our soldiers report that every creature around {nm} simply fell down and died when the tower burned. "
            "We have found the enemy's weakness.",
            # the region went to the USSR; Moscow passes the buffer states' provinces on to them.
            # (This has to be a Soviet event: secedeprovince only hands over the executing country's own land.)
            [("Burn every tower", ["type = dissent value = -5", "type = manpowerpool value = 50",
                                   "type = setflag which = res_tower_secret"])],
            country="SOV")
    return E

TOWER_PROVINCES = [p for p, _ in TOWERS]

# Hybrid wiki: "Hybrids are quick to learn the methods of their adversaries. They had already displayed
# expertise in British Army tactics by 1951." Twice a year the Hive steals a tech from each enemy it fights.
LEARN_FROM = ["SOV", "GER", "ENG", "FRA", "POL", "JAP", "ITA", "USA", "ROM", "FIN", "TUR", "CHI", "PER"]

def learning_events(g):
    E = []
    n = 0
    for year in range(1937, 1964):
        for month in ("january", "july"):
            E += g.event(9506000 + n, "The Hive Learns",
                "Captured officers, field manuals and the converted minds of human soldiers: the Hive absorbs "
                "the methods of every army it fights.",
                [("Adapt", [f"trigger = {{ {war(t)} }} type = steal_tech which = {t}" for t in LEARN_FROM])],
                country=C, trigger=[f"exists = {C}", "atwar = yes"],
                date=(1, month, year), offset=10, deathdate=(28, month, year), text_id=9506000)
            n += 1
    return E

def g_name(p):
    import story
    return story.ADJNAME[p]

def build(g, path_cmds, sov_provinces, adjacency):
    g.write("db/events/USSR.txt", patch_ussr(os.path.join(g.SRC, "USSR.txt")))
    g.write("db/events/res_breakout.txt", events(g, path_cmds) + junta_event(g) + sorokin_checkpoint_event(g))
    g.write("db/ministers/ministers_SOV_res.csv", junta_ministers_csv())
    g.write("db/events/res_cloven.txt", cloven_events(g, path_cmds))
    g.write("db/events/res_occupation.txt",
            ["#########################################################################",
             "#  RESISTANCE MOD - Occupation: Soviet land the Hive controls becomes Hive land",
             "#  9500745-749 capital moves   9503000+ the USSR writes provinces off   9504000+ the Hive builds",
             "#########################################################################", ""]
            + capital_events(g) + heart_events(g) + occupation_events(g, sov_provinces))
    import milestones
    g.write("db/events/res_processing.txt", milestones.events(g))
    import burrowers
    g.write("db/events/res_burrowers.txt", burrowers.events(g))
    g.write("db/events/res_towers.txt",
            ["#########################################################################",
             "#  RESISTANCE MOD - Chimeran towers and Angels",
             "#  9505000+ a tower rises   9505100+ a tower falls (region collapses)   9505200+ Soviet news",
             "#########################################################################", ""] + tower_events(g)
            + ["", "# The Hive Learns (9506000+): twice a year, steal a tech from each enemy at war with the Hive", ""]
            + learning_events(g))
    g.write("db/events/res_infection.txt",
            ["#########################################################################",
             "#  RESISTANCE MOD - Infection behind the lines (9501000+): one per Soviet province",
             "#########################################################################", ""]
            + infection_events(g, sov_provinces, adjacency)
            + ["", "# The Thralls (9520000+province): the Hive raises a militia division in every town abandoned to it", ""]
            + thrall_events(g, set(sov_provinces) | {p for p, _ in spread_provinces(sov_provinces, adjacency)}))
    g.write("db/events/res_infection_abroad.txt",
            ["#########################################################################",
             "#  RESISTANCE MOD - The virus crosses the border",
             "#  9509900+ first contact (quarantine techs unlocked)   9510000+ infection outside the USSR",
             "#########################################################################", ""]
            + foreign_infection_events(g, sov_provinces, adjacency))
    import cordon, story
    g.write("db/events/res_cordon.txt", cordon.events(g, sov_provinces, adjacency, story.garrisons_in))
    import refugees
    g.write("db/events/res_refugees.txt", refugees.events(g))
    # revolt.txt is UTF-8 with CRLF: append raw bytes rather than going through g.write (latin-1)
    raw = open(os.path.join(g.SRC, "revolt.txt"), "rb").read().rstrip()
    out = os.path.join(g.OUT, "db/revolt.txt")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "wb") as f:
        f.write(raw + "\r\n".join(cordon.revolt_entries(sov_provinces)).encode("ascii") + b"\r\n")
