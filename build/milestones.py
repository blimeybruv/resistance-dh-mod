"""The Processing: when the Hive holds all the key cities of a region, its people are fed into the
conversion centres and, two months later, a Hybrid army marches out. One milestone per region, in the
USSR and beyond, instead of a division per town.

Event ids, per region index r:  9570000 + 10r      The Processing of X (UA0)
                                9570000 + 10r + 1  the army emerges (UA0)
                                9570000 + 10r + 2+ the news reaches X's owners
"""
C = "UA0"
DEATH = (29, "december", 1963)
ID0 = 9570000
ARMY_DELAY = 60
SPAWN_TRIES = 3                  # the army appears in the first of the first three cities the Hive still holds
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]

# (name, key cities (first = where the army appears), Hybrid divisions, who hears of it)
REGIONS = [
    ("Western Siberia", [1142, 1148, 1138, 1140, 1144, 1156], 5, "SOV"),
    ("the Baikal", [1162, 1167, 1169, 1165, 1179], 4, "SOV UA1 UA2"),
    ("the Far East", [1190, 1191, 1176, 1196], 3, "SOV UA2 JAP"),
    ("the Urals", [1151, 1132, 1131, 687, 1134], 5, "SOV"),
    ("the Volga", [672, 668, 680, 669, 663], 6, "SOV"),
    ("Central Russia", [572, 553, 584, 604, 542], 8, "SOV"),
    ("the Ukraine", [617, 636, 626, 632, 644], 6, "SOV"),
    ("Byelorussia", [599, 590, 601], 3, "SOV"),
    ("the Caucasus", [713, 709, 702, 691, 706], 4, "SOV TUR PER"),
    ("Central Asia", [1103, 504, 1107, 503, 1114], 3, "SOV"),
    ("Manchuria", [1199, 1208, 1214, 1219, 1205], 6, "MAN JAP CHI"),
    ("Mongolia", [1124, 1120], 2, "MON"),
    ("Korea", [1228, 1232], 3, "JAP"),
    ("North China", [1247, 1241, 1252, 1330], 6, "CHI CHC JAP"),
    ("Finland", [525, 527, 524, 531], 3, "FIN SWE"),
    ("the Baltic States", [264, 270, 262], 3, "EST LAT LIT"),
    ("Poland", [232, 235, 242, 224, 258], 6, "POL GER"),
    ("Romania", [316, 297, 288], 4, "ROM"),
    ("Central Europe", [207, 284, 195, 208], 5, "CZE HUN AUS GER"),
    ("Germany", [163, 154, 179, 131, 167, 181], 8, "GER"),
    ("the Balkans", [338, 321, 377, 352], 5, "YUG BUL GRE"),
    ("Turkey", [409, 1075, 1077], 4, "TUR"),
    ("Persia", [1085, 1083], 3, "PER"),
    ("France and the Low Countries", [55, 85, 89, 116, 122], 8, "FRA BEL HOL ENG"),
    ("Italy", [419, 407, 421], 5, "ITA"),
    ("Scandinavia", [2159, 483, 294, 2152], 4, "SWE NOR DEN"),
]

def ctl(p): return f"control = {{ province = {p} data = {C} }}"

def events(g):
    import breakout
    E = ["#########################################################################",
         "#  RESISTANCE MOD - The Processing: a Hybrid army for every region the Hive takes (9570000+)",
         "#########################################################################", ""]
    best = [("technology = 95060", 20), ("technology = 95040 NOT = { technology = 95060 }", 19),
            ("NOT = { technology = 95040 }", 18)]
    for r, (name, cities, size, audience) in enumerate(REGIONS):
        base = ID0 + 10 * r
        tags = audience.split()
        assert len(tags) <= 8
        short = name[4:] if name.startswith("the ") else name          # "the Baikal" -> "Baikal" for unit names
        news = [f"trigger = {{ exists = {t} }} type = event which = {base + 2 + i} where = {t} when = 1"
                for i, t in enumerate(tags)]
        E += g.event(base, f"The Processing of {name}",
            f"Every city of {name} is ours. The menials are herding the survivors towards the conversion centres, "
            "and the centres are working day and night. In two months they will give the Hive a new army.",
            [("Process them all", [f"type = event which = {base + 1} where = {C} when = {ARMY_DELAY}",
                                   "type = manpowerpool value = 20"] + news)],
            country=C, trigger=[ctl(p) for p in cities], date=(1, "january", 1934), offset=30, deathdate=DEATH)

        # the army appears in the first key city the Hive still holds (of the first few); none held, no army
        spawn = cities[:SPAWN_TRIES]
        army = []
        for k, p in enumerate(spawn):
            cond = " ".join([ctl(p)] + [f"NOT = {{ {ctl(q)} }}" for q in spawn[:k]])
            nm = breakout.g_name(p)
            army.append(f'trigger = {{ {cond} }} type = add_corps which = "Army of {name}" value = land where = {p}')
            army.append(f'trigger = {{ {cond} technology = 95510 }} type = add_division which = "{short} Nexus" value = hq when = 6')
            for d in range(size):
                for tcond, m in best:
                    army.append(f'trigger = {{ {cond} {tcond} }} type = add_division which = '
                                f'"{ROMAN[d]} {short} Brood" value = infantry when = {m}')
        E += g.event(base + 1, f"The Army of {name}",
            f"The conversion centres of {name} have emptied. What marches out of them is a full Hybrid army, "
            "and it already knows where the next cities are.",
            [("Onward", army)], country=C)

        for i, t in enumerate(tags):
            E += g.event(base + 2 + i, f"The Processing of {name}",
                f"Reconnaissance flights over {name} report the same thing everywhere: long columns of civilians "
                "being herded into the Chimeran towers and conversion centres. Nobody is coming out. Our "
                "intelligence officers estimate that within two months the enemy will have a new army.",
                [("God help them", [])], country=t, text_id=f"RES_PROCESSING_NEWS_{r}")
    assert ID0 + 10 * len(REGIONS) < 9580000
    return E
