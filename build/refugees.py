"""Refugee corridors: an advance wave of (mostly healthy) refugees flees ahead of the Hive, west through
Europe to Britain and America, south through Turkey and Spain to Africa and Madagascar, and east through
Manchuria and China to Japan and America. Transit countries can let them pass or hold them in camps;
receivers can admit them or turn the ships away. When the mainland falls, the ships stop coming.

Event ids:
  9530000+   stage events (one per stage and country: transit or receiver)
  9531000+i  the camps (follow-up for a transit country holding refugees)
  9532000+i  the camps are overrun (UA0 raises Thralls from the inmates)
  9533000+i  the infected among the refugees (receiver admitted them without Quarantine Protocols)
  9534000+i  the emigre institute disbands (temporary research team goes back to sleep)
  9535000+   Madagascar settlement and the closing events
"""
C = "UA0"
DEATH = (29, "december", 1963)
QUARANTINE = 95310

def ctl(p): return f"control = {{ province = {p} data = {C} }}"
def any_ctl(*ps): return "OR = { " + " ".join(ctl(p) for p in ps) + " }"
def all_ctl(*ps): return "AND = { " + " ".join(ctl(p) for p in ps) + " }"

DON = [654, 653, 655, 659, 649, 644]
TANANARIVE, TAMATAVE = 1001, 1002

# where each country holds its camps (its capital; for a fallen haven the camp falls with it)
CAMP = {"POL": 232, "LAT": 264, "EST": 270, "LIT": 262, "FIN": 525, "ROM": 316, "GER": 163, "CZE": 207,
        "HUN": 284, "AUS": 195, "DEN": 294, "HOL": 122, "BEL": 116, "FRA": 55, "YUG": 338, "BUL": 321,
        "GRE": 377, "TUR": 1075, "SCH": 392, "ITA": 419, "SPR": 460, "SPA": 460, "POR": 476,
        "MAN": 1208, "MON": 1124, "CHI": 1337, "CHC": 1259, "UA2": 1169}
# havens: refugees are only sent while the haven's capital is free
HAVEN_CAPITAL = {"SWE": 2159, "TUR": 1075, "SPR": 460, "SPA": 460, "EGY": 787}

# temporary research teams brought by the refugees: (receiver, stage key, team id, name, picture, skill, specs)
TEAMS = [
    ("ENG", "W3", 1500261, "Russian Emigre Institute", "T10504", 6, ["rt_user_1", "medicine", "chemistry", "mathematics"]),
    ("USA", "W3", 1500262, "Kharkov Physics Circle", "T13507", 7, ["nuclear_physics", "mathematics", "electronics", "rocketry"]),
    ("JAP", "E2", 1500263, "Harbin Medical Mission", "T10510", 5, ["rt_user_1", "medicine", "chemistry"]),
    ("SAF", "W4", 1500264, "Odessa Naturalists", "T10504", 5, ["rt_user_1", "medicine", "chemistry"]),
]
TEAM_YEARS = 2                       # the institutes disband after this long (no money, no lab)

URALS = "event = 9500700"
DON_OR_MOSCOW = "OR = { " + " ".join(ctl(p) for p in DON + [572]) + " flag = res_stavka }"

# (key, corridor, title, condition, transit tags, receiver tags, manpower per admission, text)
STAGES = [
    ("W1", "west", "Flight from the Urals", URALS, "POL LAT EST LIT FIN ROM", "ENG USA CAN SWE", 4,
     "The first trains from beyond the Urals have reached our border: engineers, doctors and party families "
     "who saw what was coming and had the means to run. Most of them are healthy. All of them are afraid."),
    ("W2", "west", "Exodus from the Don", DON_OR_MOSCOW, "POL LAT EST LIT FIN ROM GER CZE HUN",
     "ENG USA CAN SWE TUR SPR SPA", 6,
     "With the Chimera on the Don the trickle has become a flood. Whole factories have been abandoned, their "
     "workers walking west along the railway lines with what they can carry."),
    ("W3", "west", "The Vistula Crossings", any_ctl(232, 264, 316, 525),
     "GER CZE HUN AUS DEN HOL BEL FRA YUG BUL GRE", "ENG USA CAN SWE TUR SPR SPA", 8,
     "The Hive is across the old Soviet border. Poles, Balts and Romanians are joining the Russians on the "
     "roads, and every port from Danzig to Constanta is full of people trying to buy a passage."),
    ("W4", "west", "The Road to the Sea", any_ctl(163, 195, 207, 284),
     "HOL BEL FRA SCH ITA SPR SPA TUR", "ENG USA CAN EGY SAF MAD", 8,
     "Central Europe is falling. The columns now stretch from the Rhine to the Channel ports and south over "
     "the Alps and the Pyrenees towards Africa."),
    ("W5", "west", "The Last Ports", any_ctl(55, 122, 116), "SPR SPA POR TUR", "ENG USA CAN EGY SAF MAD", 10,
     "Paris and the Low Countries are gone. What is left of Europe's refugees is crowded into Lisbon, Cadiz, "
     "Gibraltar and Istanbul, waiting for ships that come less often each week."),
    ("E1", "east", "Down the Amur", ctl(1162), "UA2 MAN MON CHI", "JAP USA", 4,
     "Irkutsk has fallen. Russians, Buryats and Chinese traders are fleeing down the Amur and across the "
     "Mongolian steppe towards Harbin and the sea."),
    ("E2", "east", "The Harbin Trains", any_ctl(1199, 1191, 1124), "MAN CHI CHC MON", "JAP USA AST", 6,
     "The Chimera are in Manchuria. Every train south from Harbin is packed to the roofs, and the "
     "quaysides at Dairen and Port Arthur are a city of tents."),
    ("E3", "east", "The Treaty Ports", any_ctl(1247, 1214, 1219), "CHI CHC", "JAP USA AST ENG", 8,
     "Peking and Mukden are lost. Millions are moving south through China, and the treaty ports are "
     "chartering anything that floats."),
]

CLOSINGS = [
    # (id offset, title, condition, receivers, text)
    (10, "No More Ships from Europe", all_ctl(55, 49, 45, 122, 460, 348), "ENG USA CAN",
     "The harbour masters report no arrivals from the Continent this week, or the week before. The last "
     "ship to reach us came out of Gibraltar with half its passengers dead of thirst. No more refugees "
     "are arriving. There is no one left to send them."),
    (20, "The Southern Routes Close", all_ctl(348, 409), "SAF EGY MAD",
     "Gibraltar and the Bosporus are in the Hive's hands. The refugee camps on our coast are full, and "
     "will stay that way: no more refugees are arriving."),
    (30, "The Last Junks", all_ctl(1338, 1241, 1328, 1369), "JAP USA AST",
     "Shanghai, Tientsin, Tsingtao and Canton have fallen silent. Fishing boats still drift ashore now and "
     "then, empty. No more refugees are arriving."),
]
MAD_OWNERS = "FRA ENG SAF".split()
SEA = "res_exodus_sea"     # the ships: receivers, the infected, Madagascar and the closings (land side: res_exodus)        # whoever holds Madagascar runs the settlement

def provname(p):
    import story
    return story.ADJNAME[p]

def team_csvs():
    """One small teams file per receiver; the teams start in 1964 so they only appear when woken."""
    out = {}
    hdr = lambda t: f"{t};Name;Pic Name;Skill;Start Year;End Year;" + ";".join(f"Speciality{i}" for i in range(1, 33)) + ";x"
    import people
    for tag, _, tid, nm, pic, sk, specs in TEAMS:
        pic = people.pic(f"T{tid}", pic)
        cells = specs + [""] * (32 - len(specs))
        out.setdefault(tag, [hdr(tag)]).append(f"{tid};{nm};{pic};{sk};1964;1964;" + ";".join(cells) + ";x")
    # Sorokin's group, if Britain takes him in after Moscow falls (breakout.sorokin_checkpoint_event)
    import people
    out.setdefault("ENG", [hdr("ENG")]).append(
        f"1500265;Sorokin Group;{people.pic('T1500251', 'T10504')};6;1964;1964;rt_user_1;medicine;chemistry;mathematics"
        + ";" * 28 + ";x")
    return {f"teams_{t}_res.csv": rows for t, rows in out.items()}

def events(g):
    E = ["#########################################################################",
         "#  RESISTANCE MOD - Refugee corridors (see refugees.py for the id ranges)",
         "#########################################################################", ""]
    camp_tags = sorted({t for s in STAGES for t in s[4].split()})
    recv_tags = sorted({t for s in STAGES for t in s[5].split() if t != "MAD"} | set(MAD_OWNERS))
    n = 0

    def alive(t):
        conds = [f"exists = {t}"]
        if t in HAVEN_CAPITAL: conds.append(f"NOT = {{ {ctl(HAVEN_CAPITAL[t])} }}")
        elif t in CAMP: conds.append(f"NOT = {{ {ctl(CAMP[t])} }}")
        return conds

    for key, corridor, title, cond, transit, recv, mp, text in STAGES:
        for t in transit.split():
            i = camp_tags.index(t)
            E += g.event(9530000 + n, title,
                text + " They want to go on. Our ministers would rather they did not stay, but turning back "
                "people who are running from the Chimera is not something a government can be seen to do. "
                "We can let them through, or hold them in camps and put the able-bodied to work.",
                [("Let them pass", 60, ["type = money value = -5", "type = dissent value = 1"]),
                 ("Hold them in camps", 40, ["type = money value = -25", "type = dissent value = 2",
                     "type = manpowerpool value = 10", f"type = setflag which = res_camps_{t}",
                     f"type = event which = {9531000 + i} where = {t} when = 90"])],
                country=t, trigger=[cond] + alive(t), date=(1, "january", 1934), offset=15,
                deathdate=DEATH, text_id=f"RES_REFUGEE_TRANSIT_{key}")
            n += 1
        for t in recv.split():
            owners = MAD_OWNERS if t == "MAD" else [t]
            for o in owners:
                ri = recv_tags.index(o)
                admit = [f"type = manpowerpool value = {mp}", "type = money value = -15", "type = dissent value = 1",
                         f"type = setflag which = res_refuge_{o}",
                         f"trigger = {{ NOT = {{ technology = {QUARANTINE} }} }} type = event which = {9533000 + ri} where = {o} when = 30"]
                for tt, tk, tid, *_ in TEAMS:
                    if tt == o and tk == key:
                        admit += [f"type = waketeam which = {tid}",
                                  f"type = event which = {9534000 + ri} where = {o} when = {360 * TEAM_YEARS}"]
                trig = [cond] + (alive(o) if t != "MAD" else [f"exists = {o}"])
                if t == "MAD":
                    trig += [f"owned = {{ province = {TANANARIVE} data = {o} }}", "flag = res_madagascar"]
                    head = (f"Ships for Madagascar: {title}",
                            "More refugee ships have been routed to the Madagascar settlement. " + text)
                    tid_ = f"RES_REFUGEE_MAD_{key}"
                else:
                    head = (f"Refugees: {title}", text + " Ships carrying them are now arriving in our ports.")
                    tid_ = f"RES_REFUGEE_RECV_{key}"
                E += g.event(9530000 + n, head[0], head[1],
                    [("Admit them", 70, admit), ("Turn the ships away", 30, [])],
                    country=o, trigger=trig, date=(1, "january", 1934), offset=15,
                    deathdate=DEATH, text_id=tid_, picture=SEA)
                n += 1
    assert n < 1000, n

    for i, t in enumerate(camp_tags):
        E += g.event(9531000 + i, "The Camps",
            "The refugee camps are overcrowded and underfed. The labour battalions are useful, but the "
            "camps cost money every month, and the doctors are worried about typhus and worse.",
            [("Keep them behind the wire", 50, ["type = money value = -15", "type = dissent value = 1",
                 f"trigger = {{ NOT = {{ technology = {QUARANTINE} }} }} type = dissent value = 2"]),
             ("Open the gates and send them on", 50, [f"type = clrflag which = res_camps_{t}",
                 "type = manpowerpool value = -5"])],
            country=t, text_id="RES_CAMPS")    # fired 90 days after the camps open; no trigger of its own
        p = CAMP[t]
        nm = provname(p)
        E += g.event(9532000 + i, f"The Camps at {nm}",
            f"The refugee camps at {nm} were still full when our swarms arrived. Nobody had opened the gates.",
            [("More bodies for the Hive", [f"type = clrflag which = res_camps_{t}",
                f'type = add_corps which = "Camp Thralls of {nm}" value = land where = {p}',
                f'type = add_division which = "Camp Horde of {nm} I" value = militia when = 10',
                f'type = add_division which = "Camp Horde of {nm} II" value = militia when = 10'])],
            country=C, trigger=[f"flag = res_camps_{t}", ctl(p)],
            date=(1, "january", 1934), offset=15, deathdate=DEATH)

    for i, t in enumerate(recv_tags):
        E += g.event(9533000 + i, "The Infected Among the Refugees",
            "Several of the new arrivals have turned in the reception centres. We had no screening in "
            "place. The papers are calling for the camps to be closed and the ships sunk.",
            [("Round up the sick", ["type = dissent value = 2", "type = manpowerpool value = -3"])],
            country=t, text_id="RES_INFECTED", picture=SEA)
        if any(tt == t for tt, *_ in TEAMS):
            tid = next(tid for tt, _, tid, *_ in TEAMS if tt == t)
            E += g.event(9534000 + i, "The Emigre Institute Disbands",
                "The refugee scientists have scattered: some to universities, some to industry, some simply "
                "worn out. What they knew is in our files now.",
                [("Thank them for their service", [f"type = sleepteam which = {tid}"])], country=t,
                text_id=f"RES_TEAM_END_{t}")

    for j, o in enumerate(MAD_OWNERS):
        E += g.event(9535000 + j, "The Madagascar Settlement",
            "The Colonial Office proposes to make Madagascar the clearing house for Europe's refugees: a long "
            "way from the Hive, with land, a port at Tamatave and room to build. Tananarive would become one "
            "of the great cities of what is left of the free world.",
            [("Found the settlement", 90, ["type = setflag which = res_madagascar", "type = money value = -40",
                f"type = province_keypoints which = {TANANARIVE} value = 5",
                f"type = construct which = infrastructure where = {TANANARIVE} value = 20",
                f"type = construct which = infrastructure where = {TAMATAVE} value = 20",
                "type = manpowerpool value = 10"]),
             ("We cannot take them", 10, [])],
            country=o, trigger=[STAGES[3][3], f"owned = {{ province = {TANANARIVE} data = {o} }}",
                                "NOT = { flag = res_madagascar }"],
            date=(1, "january", 1934), offset=30, deathdate=DEATH, text_id="RES_MADAGASCAR", picture=SEA)

    for off, title, cond, recv, text in CLOSINGS:
        k = 0
        for t in recv.split():
            for o in (MAD_OWNERS if t == "MAD" else [t]):
                if t == "MAD" and o in recv.split(): continue      # already told as a receiver
                extra = ([f"owned = {{ province = {TANANARIVE} data = {o} }}", "flag = res_madagascar"]
                         if t == "MAD" else [f"flag = res_refuge_{o}"])
                E += g.event(9535000 + off + k, title, text, [("Close the reception centres", [])], country=o,
                    trigger=[cond, f"exists = {o}"] + extra, date=(1, "january", 1934), offset=30,
                    deathdate=DEATH, text_id=f"RES_CLOSE_{off}")
                k += 1
            assert k < 10
    return E
