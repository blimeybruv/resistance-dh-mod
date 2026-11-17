"""The abandoned East (option B, v36): when Krasnoyarsk falls the USSR may give up everything east of the
Yenisei to two Soviet-backed buffer states, as Moscow did in 1920 with the Far Eastern Republic.

  UA1  Siberian Cordon Administration  - North/South Krasnoyarsk, Irkutsk, Yakutsk     (capital Irkutsk)
  UA2  Far Eastern Republic            - Zabaikalye, Amur, Khabarovsk, Primorye,
                                         Kamchatka, Magadan                              (capital Vladivostok)

Both are created as Soviet puppets at war with the Hive. Their provinces stop sending infection events to
Moscow; they get AI-only infection and occupation events of their own. If the Hive is destroyed, Moscow
takes them back.

  9500554       Decision: Abandon the East (SOV)
  9500555/556   founding events (UA1 / UA2)
  9500557       Return to the Union (SOV)
  9500565       The Yenisei Question (SOV): opens the decision six months into the war
  9507000+      infection in the buffer states        9508000+ occupation   9508500+ the Hive builds
"""
import json, os

UA1, UA2 = "UA1", "UA2"
C = "UA0"
ROOT = os.path.dirname(os.path.abspath(__file__))
PROV = {int(k): v for k, v in json.load(open(os.path.join(ROOT, "provinces.json"))).items()}   # id -> [name, area, region]

AREA_OWNER = {"North Krasnoyarsk": UA1, "South Krasnoyarsk": UA1, "Irkutsk": UA1, "Yakutsk": UA1,
              "Zabaikalye": UA1, "Amur": UA2, "Khabarovsk": UA2, "Primorski": UA2, "Kamchatka": UA2, "Magadan": UA2}
# Tayshet and Cheremkhovo sit on the railway between Krasnoyarsk and Irkutsk, west of Lake Baikal:
# they belong with Irkutsk, not with the Far Eastern Republic beyond the lake.
# Tomsk and Salekhard (west of the Yenisei) too, and the whole Zabaikalye area (Ulan-Ude, Chita, Borzya): Chita
# sits on the railway back to Moscow, while the Republic's Pacific provinces hang on a corridor the Hive can cut,
# so the Republic is governed from Vladivostok, not Chita.
PROVINCE_OWNER = {1069: UA1, 1166: UA1, 1148: UA1, 1152: UA1}
CAPITAL = {UA1: 1162, UA2: 1191}            # Irkutsk, Vladivostok
NAMES = {UA1: ("Siberian Cordon Administration", "Siberian"), UA2: ("Far Eastern Republic", "Far Eastern")}
COLOURS = {UA1: "LightGreen", UA2: "DarkOrange"}
GROUND_ZERO = 1155
DEATH = (29, "december", 1963)

def owner_of(p):
    return PROVINCE_OWNER.get(p) or AREA_OWNER.get(PROV.get(p, [None, None])[1])

def zone(sov_provinces):
    """{tag: [provinces]} for Soviet-owned provinces east of the Yenisei (capital first)."""
    z = {UA1: [], UA2: []}
    for p in sorted(sov_provinces):
        owner = owner_of(p)
        if owner and p != GROUND_ZERO:
            z[owner].append(p)
    for t in z:
        z[t].sort(key=lambda p: p != CAPITAL[t])
    return z

def revolt_entries(sov_provinces):
    """db/revolt.txt entries: DH can only release a country defined there. Both need just one of their
    provinces in Soviet hands (min = 1), and only the USSR can release them."""
    z = zone(sov_provinces)
    L = ["", "", "# RESISTANCE MOD - buffer states east of the Yenisei (released by the decision 'Abandon the East')"]
    for t in (UA1, UA2):
        L += [f"{t} = {{ # {NAMES[t][0]}",
              "\tdate = { day = 0 month = january year = 1933 }",
              "\texpirydate = { day = 29 month = december year = 1964 }",
              "\tminimum = { " + " ".join(map(str, z[t])) + " }",
              "\tmin = 1",
              f"\tcapital = {CAPITAL[t]}",
              "\tcountry = { SOV }",
              "\trevolt = no",
              "\tliberate = no",
              f"\tintrinsic_gov_type = {'stalinist' if t == UA1 else 'leninist'}",
              "}"]
    return L

def ctl(p, tag=C): return f"control = {{ province = {p} data = {tag} }}"
def owned(p, tag): return f"owned = {{ province = {p} data = {tag} }}"
def war(a, b=C): return f"war = {{ country = {a} country = {b} }}"

def tower_release(region_name):
    """Commands for the Hive's tower-fall event: every Hive-owned province in the region goes to its buffer
    state (if that exists) or else to the USSR. secedeprovince only moves the executing country's own land,
    so nobody else's provinces can be swept up the way secederegion did."""
    L = []
    for p in sorted(q for q in PROV if PROV[q][2] == region_name and q != GROUND_ZERO):
        mine = f"owned = {{ province = {p} data = {C} }}"
        o = owner_of(p)
        if o:
            L.append(f"trigger = {{ {mine} exists = {o} }} type = secedeprovince which = {o} value = {p}")
            L.append(f"trigger = {{ {mine} NOT = {{ exists = {o} }} exists = SOV }} type = secedeprovince which = SOV value = {p}")
        else:
            L.append(f"trigger = {{ {mine} exists = SOV }} type = secedeprovince which = SOV value = {p}")
    return L

def tower_overrides(region_name):
    """After a tower falls its region goes to the USSR; inside the buffer states the land goes to them instead."""
    return [f"trigger = {{ exists = {owner_of(p)} owned = {{ province = {p} data = SOV }} }} type = secedeprovince which = {owner_of(p)} value = {p}"
            for p in sorted(PROV) if PROV[p][2] == region_name and owner_of(p) and p != GROUND_ZERO]

def events(g, sov_provinces, adjacency, garrisons_in):
    z = zone(sov_provinces)
    E = ["#########################################################################",
         "#  RESISTANCE MOD - The abandoned East: buffer states east of the Yenisei",
         "#  9500554 decision  9500555-556 founding  9500557 Return to the Union",
         "#  9507000+ infection  9508000+ occupation  9508500+ the Hive builds",
         "#########################################################################", ""]
    for t, (nm, adj) in NAMES.items():
        g.loc(t, nm); g.loc(f"{t}_ADJ", adj)

    # Available once Krasnoyarsk falls, or six months into the war (9500565), whichever comes first; after
    # that, retaking Krasnoyarsk no longer hides it.
    cond = ["flag = res_outbreak", war("SOV"), "NOT = { flag = res_east_abandoned }",
            f"OR = {{ {ctl(1156)} flag = res_yenisei_question }}"]
    cmds = ["type = setflag which = res_east_abandoned", "type = dissent value = 5"]
    for t in (UA1, UA2):
        provs = z[t]
        # the cordon garrisons in the zone pass out of Soviet hands with it
        cmds += [c for p in provs for c in garrisons_in(p)]
        # Moscow gives up its claim: while the provinces stay Soviet cores, DH hands them straight back to the
        # USSR (a province an ally controls reverts to the ally whose core it is). Capitals were exempt, which
        # is why only Irkutsk and Chita stayed. Return to the Union restores the cores.
        cmds += [f"type = removecore which = {p}" for p in provs]
        # release and puppet it (it is defined in db/revolt.txt, like vanilla's Soviet Poland U32),
        # then hand over anything the release left behind
        cmds += [f"type = independence which = {t} value = 1", f"type = make_puppet which = {t}"]
        cmds += [f"trigger = {{ {owned(p, 'SOV')} control = {{ province = {p} data = SOV }} }} "
                 f"type = secedeprovince which = {t} value = {p}" for p in provs]
        # the Soviet divisions handed over to the new state's army
        cmds += [f"type = remove_division which = {SOV_UNIT_TYPE} value = {sid}"
                 for _, _, divs in ARMIES[t] for _, _, sid in divs]
        cmds.append(f"type = trigger which = {9500555 if t == UA1 else 9500556}")
    E += g.event(9500554, "Decision: Abandon the East",
        "The line of the Yenisei cannot be held by Moscow alone. The Politburo proposes to "
        "do what it did in 1920: hand everything east of the river to Soviet-backed buffer states. A Siberian Cordon "
        "Administration will hold Irkutsk and Yakutia, and a new Far Eastern Republic will hold the Amur and the "
        "Pacific coast. They will fight the Hive with Soviet advisers and Soviet rifles, and their losses will "
        "not be ours. Their armies will be built from ours: four Siberian rifle divisions from Novosibirsk go to the "
        "Cordon with the Chita garrison, and the Khabarovsk and Vladivostok garrisons of the Far Eastern Front go to the Republic.",
        [("Abandon the East", 60, cmds), ("Not one step back", 40, ["type = setflag which = res_east_abandoned"])],
        # the AI ('trigger') still waits for Krasnoyarsk to fall, as before
        country="SOV", decision=cond, decision_trigger=cond, trigger=cond[:3] + [ctl(1156)],
        date=(1, "january", 1937), offset=7, deathdate=DEATH)

    E += g.event(9500565, "The Yenisei Question",
        "Six months into the war, the General Staff has delivered its appreciation of the eastern front. Every "
        "division sent beyond the Yenisei is a division not defending the Urals, and the Trans-Siberian cannot "
        "supply both. Gosplan's old 1920 file on the Far Eastern Republic has been taken out of the archive.",
        [("Put the plans before the Politburo", ["type = setflag which = res_yenisei_question"])],
        country="SOV")

    # Vanilla's Soviet-Japanese border incidents (hoi2.txt 24 Lake Khasan, July-Sept 1938; 22 Nomonhan, May 1939)
    # only check that Japan and the USSR are at peace. Put them to sleep when Japan is fighting the Hive or the
    # Hive holds that border (Vladivostok; Choibalsan, facing Khalkhin Gol).
    for eid, vanilla, prov, title, text, last in (
        (9500591, 24, 1191, "No Border at Lake Khasan",
         "Our Korea Army wanted to test the Soviets on the hills above Lake Khasan. There are no Soviets there "
         "to test any more, only the Chimera.", (20, "september", 1938)),
        (9500592, 22, 1120, "No Border at Khalkhin Gol",
         "The Kwantung Army's plans for the Khalkhin Gol frontier are void. Whatever holds the far bank of the "
         "river now, it is not the Red Army.", (29, "august", 1939))):
        E += g.event(eid, title, text, [("Turn to the real enemy", [f"type = sleepevent which = {vanilla}"])],
            country="JAP", trigger=["exists = JAP", f"OR = {{ {war('JAP')} {ctl(prov)} }}"],
            date=(1, "january", 1933), offset=3, deathdate=last)

    SLOTS = ["headofstate", "headofgovernment", "foreignminister", "armamentminister", "ministerofsecurity",
             "ministerofintelligence", "chiefofstaff", "chiefofarmy", "chiefofnavy", "chiefofair"]
    for eid, t, text in [
        (9500555, UA1, "The Siberian Cordon Administration has taken over the cities of the Angara and the Lena. "
                       "Its first decree is the same as Moscow's last: hold the line."),
        (9500556, UA2, "The Far Eastern Republic has been proclaimed again, this time in Vladivostok, fifteen years after it was "
                       "folded into the Union. Its people know exactly why Moscow has brought it back.")]:
        cab = [f"type = {slot} which = {minister_id(t, i)}" for i, slot in enumerate(SLOTS, 1)]
        cores = [f"type = addcore which = {p}" for p in z[t]]          # the state's own core provinces
        army = []
        for corps, where, divs in ARMIES[t]:
            # spawn in the first town of the list the new state actually holds; a town the Hive has taken
            # (or none held at all) spawns nothing, rather than a corps that walks into an empty Hive town
            for cond, p in first_held([where] + FALLBACK[where], t):
                army.append(f'trigger = {{ {cond} }} type = add_corps which = "{corps}" value = land where = {p}')
                army += [f'trigger = {{ {cond} }} type = add_division which = "{d}" value = {kind}' for d, kind, _ in divs]
        E += g.event(eid, f"The {NAMES[t][0]}", text,
            [("Hold the line", [f"trigger = {{ {cond} }} type = capital which = {p}"
                                for cond, p in first_held([CAPITAL[t]] + FALLBACK[CAPITAL[t]], t)]
                               + [f"type = war which = {C}",
                                "type = manpowerpool value = 150", "type = supplies value = 3000",
                                "type = relation which = SOV value = 200", "type = setflag which = res_" + t.lower() + "_founded",
                                f"type = event which = {9500558 if t == UA1 else 9500559} where = {t} when = 7",
                                # front-line states: mobilised, with their own defensive AI
                                "type = set_domestic which = professional_army value = 8",
                                f'trigger = {{ ai = yes }} type = ai which = "{"res_cordon.ai" if t == UA1 else "res_fer.ai"}"']
                               + cab + cores + army)],
            country=t)

    # a week or so later: who they are
    E += g.event(9500558, "Who Holds the Cordon",
        "For eleven years the men of the Special Cordon Directorate were told they were guarding an anthrax "
        "quarantine. They buried patrols that came back wrong, burned villages that went quiet, and signed oaths "
        "never to speak of either. Now Moscow has handed them everything east of the Yenisei and called it a state. "
        "Chairman Pavel Dorokhov, who ran the Krasnoyarsk section of the cordon until the night it fell, has made "
        "only one change: the checkpoints face west as well as north. Nobody leaves who has not been examined.",
        [("We were the cordon. We still are.", ["type = dissent value = -2", "type = manpowerpool value = 25"])],
        country=UA1)                                   # scheduled by the founding event, 7 days on
    E += g.event(9500559, "The Republic Remembers",
        "In 1920 Lenin created the Far Eastern Republic to keep the Japanese at arm's length, and in 1922 its "
        "People's Revolutionary Army stormed Volochayevka in forty degrees of frost and drove the last "
        "interventionists into the sea. Then the Republic folded itself into the Union and was forgotten by everyone "
        "but the men who fought for it. They are old now, but they are the only government the Amur has ever trusted. "
        "Chairman Aleksandr Varnavin, a partisan of the Amur, has called up the veterans' associations and the "
        "Ussuri Cossacks alike. The old red and blue flag flies over the station again.",
        [("Remember Volochayevka", ["type = dissent value = -3", "type = manpowerpool value = 40"])],
        country=UA2)

    # Japan hears about it - only a Japan that chose the North Strike (DH Full 1330120019 sets JAP_NorthStrategy)
    E += g.event(9500564, "A Republic on the Amur",
        "Moscow has abandoned its own Far East. A revived Far Eastern Republic, the same buffer state the Bolsheviks "
        "used to see off our expedition in 1922, now holds Vladivostok, Khabarovsk and the Amur with a few old "
        "partisans and whatever the Red Army left behind. Whatever is consuming Siberia is coming this way. The "
        "North Strike Group says the moment it has argued for since the Five Ministers conference has come: take "
        "the Maritime Province and the Amur now, and hold the line against the creatures on our terms, not Moscow's.",
        [("Strike now, while Russia is on its knees", 55, [f"type = war which = {UA2}", "type = setflag which = res_jap_north",
                                                            "type = domestic which = interventionism value = 1",
                                                            "type = belligerence which = JAP value = 5"]),
         ("Mass the Kwantung Army on the Amur first", 35, [f"type = relation which = {UA2} value = -100",
                                                           "type = relation which = SOV value = -30",
                                                           "type = domestic which = defense_lobby value = 1",
                                                           "type = setflag which = res_jap_north"]),
         ("Let the Russians and the creatures bleed each other", 10, [f"type = relation which = {UA2} value = 20"])],
        country="JAP", trigger=[f"exists = {UA2}", "flag = res_ua2_founded",
                                "OR = { flag = JAP_NorthStrategy local_flag = NorthStrike }",
                                f"NOT = {{ war = {{ country = JAP country = {UA2} }} }}"],
        date=(1, "january", 1937), offset=14, deathdate=DEATH)

    E += g.event(9500557, "Return to the Union",
        "The Hive is gone. The Siberian Cordon Administration and the Far Eastern Republic have done what they were "
        "created to do, and the Politburo has decided that they will now cease to exist.",
        [("Welcome them home", [f"type = addcore which = {p}" for t in (UA1, UA2) for p in z[t]] + [
                                f"trigger = {{ exists = {UA1} }} type = inherit which = {UA1}",
                                f"trigger = {{ exists = {UA2} }} type = inherit which = {UA2}",
                                "type = dissent value = -5"])],
        country="SOV", trigger=[f"NOT = {{ exists = {C} }}", f"OR = {{ exists = {UA1} exists = {UA2} }}"],
        date=(1, "january", 1937), offset=14, deathdate=DEATH)

    n = 0
    import breakout
    towers = {p for p, _ in breakout.TOWERS}
    for t in (UA1, UA2):
        for p in z[t]:
            nm = PROV[p][0]
            near = [q for q in adjacency.get(p, []) if q != p]
            if near and p not in towers:
                E += g.event(9507000 + n, f"Infection at {nm}",
                    f"The virus has reached {nm}. The {NAMES[t][1]} authorities must purge the town or abandon it.",
                    breakout.infection_options(t, p),
                    country=t, trigger=[war(t), owned(p, t), f"NOT = {{ {ctl(p)} }}",
                                        "OR = { " + " ".join(ctl(q) for q in near) + " }"],
                    date=(1, "january", 1937), offset=60, deathdate=DEATH)
            E += g.event(9508000 + n, f"The Dead Zone at {nm}",
                f"There is nothing left at {nm} to liberate.",
                [("Strike it from the map", [f"type = secedeprovince which = {C} value = {p}",
                                             f"type = trigger which = {9508500 + n}"])],
                country=t, trigger=[war(t), owned(p, t), ctl(p)],
                date=(1, "january", 1937), offset=30, deathdate=DEATH)
            E += g.event(9508500 + n, f"The Hive Builds at {nm}",
                "Menials lay down roads of black metal and power conduits. Supplies now flow to the front.",
                [("The Hive grows", breakout.hive_builds_cmds(p))],
                country=C)
            n += 1
    return E

# ---------------------------------------------------------------- people
BASE = 1500000
MINISTER_POSTS = ["Head of State", "Head of Government", "Foreign Minister", "Minister of Armament",
                  "Minister of Security", "Head of Military Intelligence", "Chief of Staff", "Chief of Army",
                  "Chief of Navy", "Chief of Air Force"]
# fictional officials
MINISTERS = {
    UA1: ["Pavel Dorokhov", "Ivan Sedykh", "Arkady Lamin", "Grigory Shcherbak", "Viktor Bulatov",
          "Semyon Ryabov", "Nikolai Ostapenko", "Fyodor Kazantsev", "Yakov Belousov", "Mikhail Trusov"],
    UA2: ["Aleksandr Varnavin", "Boris Lisitsyn", "Konstantin Ushakov", "Lev Pankratov", "Dmitri Zolotov",
          "Andrei Melnikov", "Vasily Gorelov", "Timofei Kuzmin", "Ilya Starostin", "Oleg Ponomarev"],
}
LEADERS = {UA1: [("Fyodor Kazantsev", 1, 4, 3), ("Grigory Avdeyev", 2, 3, 2), ("Pyotr Lomakin", 3, 3, 2)],
           UA2: [("Timofei Kuzmin", 1, 4, 3), ("Sergei Rudakov", 2, 3, 2), ("Ivan Shadrin", 3, 3, 2)]}

PERSONALITIES = {
    UA1: ["Ruthless Powermonger", "Silent Workhorse", "Iron-fisted Brute", "Infantry Proponent", "Prince of Terror",
          "Logistics Specialist", "School of Defense", "Elastic Defense Doctrine", "Base Control Doctrine",
          "Army Aviation Doctrine"],
    UA2: ["Popular Figurehead", "Old General", "Great Compromiser", "Resource Industrialist", "Crime Fighter",
          "Political Specialist", "School of Maneuver", "Elastic Defense Doctrine", "Base Control Doctrine",
          "Army Aviation Doctrine"],
}
IDEOLOGY = {UA1: "ST", UA2: "LE"}          # Stalinist / Leninist

def minister_id(t, i):
    return BASE + (300 if t == UA1 else 320) + i

def ministers_csv(t):
    import people
    L = [f"{t};Ruling Cabinet - Start;Name;Start Year;End Year;Retirement Year;Ideology;Personality;Loyalty;Picturename;X",
         ";Replacements;;;;;;;;;X"]
    for i, (post, nm, pers) in enumerate(zip(MINISTER_POSTS, MINISTERS[t], PERSONALITIES[t]), 1):
        mid = minister_id(t, i)
        L.append(f"{mid};{post};{nm};1930;1964;1999;{IDEOLOGY[t]};{pers};High;{people.pic(f'M{mid}', 'unknownminister')};X")
    return L

# where a corps (or the capital) goes if its home town is not held when the state is founded
FALLBACK = {1162: [1165, 1179, 1166],          # Irkutsk -> Bratsk, Yakutsk, Cheremkhovo
            1169: [1167, 1162],                # Chita -> Ulan-Ude, Irkutsk
            1190: [1176, 1191, 1189],          # Khabarovsk -> Blagoveshchensk, Vladivostok, Nikolayevsk
            1191: [1196, 1190, 1189]}          # Vladivostok -> Nikolsk-Ussuriysky, Khabarovsk, Nikolayevsk

def first_held(cands, t):
    """[(trigger, province)]: exactly one trigger holds, for the first candidate t controls (none if it holds none)."""
    out = []
    for k, p in enumerate(cands):
        conds = [f"control = {{ province = {p} data = {t} }}"] + \
                [f"NOT = {{ control = {{ province = {q} data = {t} }} }}" for q in cands[:k]]
        out.append((" ".join(conds), p))
    return out

# starting armies (DH add_corps / add_division, as vanilla Japan does for Mengkukuo)
# Each new division takes over a Soviet one (quid pro quo): the decision removes the Soviet division with this
# scenario id (type 10848, soviet union.inc), wherever it is by then, and the founding event raises its successor.
SOV_UNIT_TYPE = 10848
ARMIES = {
    UA1: [("Special Cordon Corps", 1162, [("1st Cordon Rifle Division", "infantry", 234),      # 73rd Rifle, Novosibirsk
                                         ("2nd Cordon Rifle Division", "infantry", 235),      # 78th Rifle
                                         ("Angara Militia", "militia", 236),                  # 94th Rifle
                                         ("Irkutsk Workers' Militia", "militia", 238)]),      # 109th Rifle
          ("Transbaikal Group", 1169, [("1st Transbaikal Rifle Division", "infantry", 243),      # 36th Rifle, Chita
                                       ("Chita Workers' Militia", "militia", 244)])],            # 57th Rifle, Chita
    UA2: [("People's Revolutionary Army", 1190, [("Amur Rifle Division", "infantry", 252),     # 12th Rifle, Khabarovsk
                                                ("Amur Partisan Detachments", "militia", 253),        # 21st Rifle, Khabarovsk
                                                ("Ussuri Cossack Division", "cavalry", 257)]),        # 8th Far Eastern Cavalry
          ("Primorye Group", 1191, [("Pacific Rifle Division", "infantry", 263),               # 1st Kolkhoz Rifle, Vladivostok
                                    ("Vladivostok Workers' Militia", "militia", 264)])],       # 2nd Kolkhoz Rifle
}

def leaders_csv():
    L = ["Name;ID;Country;Rank 3 Year;Rank 2 Year;Rank 1 Year;Rank 0 Year;Ideal Rank;Max Skill;Traits;Skill;"
         "Experience;Loyalty;Type;Picture;Start Year;End Year;Retirement Year;x"]
    import people
    i = 400
    for t in (UA1, UA2):
        for nm, rank, mx, sk in LEADERS[t]:
            i += 1
            # a general who also sits in the cabinet (the Chief of Army) shares his minister portrait
            pic = "unknownleader"
            if nm in MINISTERS[t]:
                pic = people.pic(f"M{minister_id(t, MINISTERS[t].index(nm) + 1)}", pic)
            r = [1930 if k >= rank else 1990 for k in (3, 2, 1, 0)]
            L.append(f"{nm};{BASE + i};{t};{r[0]};{r[1]};{r[2]};{r[3]};{rank};{mx};0;{sk};0;5;0;{pic};1930;1964;1999;x")
    return L
