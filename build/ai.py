"""Module 4: AI files.  The Chimera get a full AI built from DH Full's minor_default.ai
with aggressive settings; partial 'switch' files retarget them (and the Soviet AI) as the
story advances, the same way vanilla uses ai/switch/*.ai."""
import os, re
from breakout_towers import TOWER_PROVINCES

C = "UA0"

def sub(s, pattern, repl, count=1):
    new, n = re.subn(pattern, repl, s, count=count, flags=re.M)
    assert n, f"pattern not found: {pattern}"
    return new

def block(s, name, body):
    """Replace a top-level 'name = { ... }' block (balanced braces)."""
    m = re.search(rf"^{name}\s*=\s*\{{", s, re.M)
    assert m, name
    i, depth = m.end(), 1
    while depth:
        depth += {"{": 1, "}": -1}.get(s[i], 0); i += 1
    return s[:m.start()] + f"{name} = {{\n{body}\n}}" + s[i:]

def targets(provs):
    return "\n".join(f"\t{p} = {v}" for p, v in provs)

# Chimeran advance targets per phase: (province, priority)
SIBERIA = [(1156, 150), (1142, 140), (1148, 130), (1162, 120), (1138, 110), (1157, 100), (1144, 100), (1167, 90), (1169, 80)]
URALS = [(1151, 150), (1132, 150), (1131, 140), (687, 130), (1128, 120), (1134, 110), (1103, 90), (504, 80)]
RUSSIA = [(672, 150), (668, 140), (680, 140), (572, 200), (553, 160), (663, 120), (669, 110), (677, 110), (636, 100), (617, 120), (599, 110), (713, 90)]
EUROPE = [(232, 200), (316, 150), (163, 200), (195, 140), (207, 140), (284, 130), (525, 100), (264, 100), (167, 120), (184, 110)]
WEST = [(55, 200), (116, 150), (122, 140), (419, 120), (49, 150), (51, 150), (392, 80), (338, 100)]

def chimera_ai(src):
    s = open(src, encoding="latin-1").read().replace("\r\n", "\n")
    s = sub(s, r"^# Minor 1936 AI File by Lothos", "# The Chimera (UA0) - Resistance mod. Based on minor_default.ai by Lothos")
    s = sub(s, r"^max_front_ratio = .*", "max_front_ratio = 3.0")
    s = sub(s, r"^max_garrison_prop = .*", "max_garrison_prop = 0.05")
    s = sub(s, r"^min_garrison_prop = .*", "min_garrison_prop = 0.0")
    s = sub(s, r"^neutrality = .*", "neutrality = 0")
    s = sub(s, r"^war = .*", "war = 0 # wars are declared by events only\nferocity = yes\ndesperation = 0.0")
    s = sub(s, r"^upgrading = .*", "upgrading = 0.50")
    s = sub(s, r"^reinforcement = .*", "reinforcement = 0.50")
    s = sub(s, r"^strat_redeploy_threshold = .*", "strat_redeploy_threshold = 15")
    s = sub(s, r"^exp_force_ratio = .*", "exp_force_ratio = 0.0")
    s = block(s, "target", targets(SIBERIA))
    # construction: keep building factories even at war (conversion chambers)
    s = sub(s, r"^\tmax_factor = 0\.00", "\tmax_factor = 0.40")
    s = sub(s, r"^\tic_at_war = no", "\tic_at_war = yes")
    s = sub(s, r"^\tforce_ic_until = 1935", "\tforce_ic_until = 1937")
    s = sub(s, r"^\tic_end_year = 1935", "\tic_end_year = 1964")
    # army: swarms of Hybrids and thralls, Stalkers/Leviathans as brigades
    s = sub(s, r"^\tinfantry \t\t= 100", "\tinfantry \t\t= 46")   # land 82 + air 18 = 100 (DH checks the sum)
    s = sub(s, r"^\tcavalry \t\t= 0", "\tcavalry \t\t= 17")   # Leaper swarms
    s = sub(s, r"^\tnaval_bomber \t= 0", "\tnaval_bomber \t= 3")    # Hunter Dropships (from 1940)
    s = sub(s, r"^\tmilitia \t\t= 0", "\tmilitia \t\t= 16")
    s = sub(s, r"^\tartillery \t\t\t= 35", "\tartillery \t\t\t= 30")
    s = sub(s, r"^\tinterceptor \t= 0", "\tinterceptor \t= 10")       # Chimeran Fighters (from 1938)
    s = sub(s, r"^\tcas \t\t\t= 0", "\tcas \t\t\t= 5")                 # Dropships
    s = sub(s, r"^\tstrategic_bomber = 0", "\tstrategic_bomber = 3")    # Chimeran Battleships (from 1950)
    s = sub(s, r"^\tair_base = no", "\tair_base = yes")
    s = sub(s, r"^\tair_base_provs = \{ \}", "\tair_base_provs = { " + " ".join(map(str, TOWER_PROVINCES)) + " }")
    s = sub(s, r"^\tsuper_heavy_armor \t= 0", "\tsuper_heavy_armor \t= 20")   # Stalkers, Goliaths
    s = sub(s, r"^\tmedium_armor \t\t\t= 0", "\tmedium_armor \t\t\t= 15")         # Widowmakers
    s = sub(s, r"^\theavy_armor \t\t= 0", "\theavy_armor \t\t= 15")                # Titans
    s = sub(s, r"^\tsecret_weapons \t= 0", "\tsecret_weapons \t= 8")
    s = sub(s, r"^\tanti_air \t\t\t= 0", "\tanti_air \t\t\t= 20")
    s = sub(s, r"^\tland_doctrines \t= 8", "\tland_doctrines \t= 4")
    s = sub(s, r"^\t\t# Regular Infantry\n", "\t\t# Chimeran Strains and Engineering\n"
            "\t\t95010 95020 95030 95040 95050 95060 95110 95120 95130 95140\n\t\t# Regular Infantry\n")
    s = sub(s, r"^\tcapital\t\t\t= 40", "\tcapital\t\t\t= 10")
    # guard the towers: losing one collapses a whole region
    s = sub(s, r"^\tprovince_priorities = \{\t\}", "\tprovince_priorities = {\n" + targets([(p, 150) for p in TOWER_PROVINCES]) + "\n\t}")
    s = sub(s, r"^\twar_target\t\t= 50", "\twar_target\t\t= 0")
    # front: relentless, attacks at poor odds, never withdraws, accepts losses
    for key, val in (("recklessness", "3"), ("reserve_prop", "0.05"), ("panic_ratio_vs_ai", "2.5"),
                     ("base_attack_odds", "0.9"), ("min_attack_odds", "0.7"),
                     ("max_attack_odds", "2.0"), ("reinforce_odds", "1.0"), ("withdraw_odds", "0.1")):
        s = sub(s, rf"^(\t{key}\s*=\s*)[0-9.]+", rf"\g<1>{val}")
    return s.split("\n")

def buffer_ai(src, title, key_provinces):
    """The buffer states east of the Yenisei: dig in, hold the cities and the railway, never start wars,
    build cheap infantry and militia. Based on minor_default.ai, like the Chimera's own file."""
    s = open(src, encoding="latin-1").read().replace("\r\n", "\n")
    s = sub(s, r"^# Minor 1936 AI File by Lothos", f"# {title} - Resistance mod. Based on minor_default.ai by Lothos")
    s = sub(s, r"^max_front_ratio = .*", "max_front_ratio = 2.0")
    s = sub(s, r"^max_garrison_prop = .*", "max_garrison_prop = 0.20")
    s = sub(s, r"^war = .*", "war = 0 # buffer states never start wars")
    s = sub(s, r"^\tinfantry \t\t= 100", "\tinfantry \t\t= 60")
    s = sub(s, r"^\tmilitia \t\t= 0", "\tmilitia \t\t= 40")
    s = sub(s, r"^\tcapital\t\t\t= 40", "\tcapital\t\t\t= 60")
    s = sub(s, r"^\tprovince_priorities = \{\t\}", "\tprovince_priorities = {\n" + targets(key_provinces) + "\n\t}")
    for key, val in (("recklessness", "0"), ("withdraw_odds", "0.4")):
        s = sub(s, rf"^(\t{key}\s*=\s*)[0-9.]+", rf"\g<1>{val}")
    return s.split("\n")

# key cities and railway junctions (province, priority)
CORDON_KEYS = [(1162, 200), (1169, 150), (1148, 140), (1157, 120), (1165, 100), (1166, 100), (1167, 100), (1179, 100), (1069, 80)]
FER_KEYS = [(1191, 200), (1190, 180), (1176, 140), (1196, 120), (1189, 80)]

def switch(title, body_lines):
    return [f"# Resistance mod switch AI: {title}", "# Partial AI file - only the listed settings change (as in vanilla ai/switch files)", ""] + body_lines

def chimera_switch(title, provs):
    return switch(f"Chimera - {title}", ["target = {", targets(provs), "}"])

def sov_switch(title, lines, defend):
    return switch(f"USSR - {title}", lines + ["target = {", targets([(p, 120) for p in TOWER_PROVINCES]), "}"] + [
        "garrison = {", "\tdefend_overseas_beaches = no", "\tcapital\t\t= 60", "\tprovince_priorities = {",
        targets(defend), "\t}", "\tkey_point_prio_mult = 3", "}"])

SOV_URALS_DEFENCE = [(1151, 150), (1132, 150), (1131, 120), (687, 120), (1128, 100), (1134, 100), (1138, 80), (572, 150), (553, 120)]
SOV_VOLGA_DEFENCE = [(672, 150), (668, 150), (680, 150), (669, 120), (663, 120), (677, 120), (572, 200), (553, 150)]
SOV_FRONT = ["max_front_ratio = 3.0", "strat_redeploy_threshold = 20", "front = {", "\trecklessness = 1",
             "\treserve_prop = 0.3", "\treinforce_odds = 1.4", "\twithdraw_odds = 0.3", "}"]

FILES = {
    "switch/UA0_urals.ai": lambda: chimera_switch("onto the Urals", URALS),
    "switch/UA0_russia.ai": lambda: chimera_switch("into European Russia", RUSSIA),
    "switch/UA0_europe.ai": lambda: chimera_switch("into Central Europe", EUROPE),
    "switch/UA0_west.ai": lambda: chimera_switch("into Western Europe", WEST),
    "switch/SOV_siberian_front.ai": lambda: sov_switch("hold the Urals", SOV_FRONT, SOV_URALS_DEFENCE),
    "switch/SOV_volga_line.ai": lambda: sov_switch("hold the Volga", SOV_FRONT, SOV_VOLGA_DEFENCE),
}

def cmd(path):
    return f'trigger = {{ ai = yes }} type = ai which = "{path}"'

def build(g):
    g.write("ai/chimera.ai", chimera_ai(os.path.join(g.SRC, "minor_default.ai")))
    g.write("ai/res_cordon.ai", buffer_ai(os.path.join(g.SRC, "minor_default.ai"), "Siberian Cordon Administration (UA1)", CORDON_KEYS))
    g.write("ai/res_fer.ai", buffer_ai(os.path.join(g.SRC, "minor_default.ai"), "Far Eastern Republic (UA2)", FER_KEYS))
    import fall_of_europe
    for path, make in list(FILES.items()) + list(fall_of_europe.ai_files().items()):
        g.write("ai/" + path, make())
