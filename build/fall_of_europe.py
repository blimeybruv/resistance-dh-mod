"""The Fall of Europe (1933 scenario): Paris falls, France fights on from Algiers, Britain braces for the
Channel, and the Hive comes across it: Burrowers under it (burrowers.py), Dropships over it, Hunters against
the fleet, then Spire batteries on every foothold, shelling the English towns next door.

Vanilla DH Full's armistice and Vichy chain (france.txt) only fires when GERMANY or ITALY holds Paris, and the
British surrender chain (UK.txt) only when Britain is at war with GER/SOV/JAP/ITA. The Hive is neither, so
they would stay quiet anyway; the events below still sleep them, in case Germany is alive and retakes Paris.

Event ids (9590000+):
  9590000-009  Act 1  Paris falls, the government sails for Algiers, the fleet, Dunkirk
  9590010-019  Act 2  the Channel Front (Britain), Hunters over Scapa Flow and the Channel
  9590020-039  Act 3  Dropship landings (one per target, two waves) and the Home Guard
  9590040-049         the Hive turns on London (AI), the London Tower
  9590100+i           Spire batteries come ashore at a foothold (UK province i)
  9590200+i           Spire strike on a British-held province next to a foothold
  9590300+i           the barrage goes on (30 days later, if the town still stands)
  9590500-509  Act 4  London falls, the Crown to Ottawa
"""
C = "UA0"
DEATH = (29, "december", 1963)
ID0 = 9590000
SPIRES, DROPSHIPS, HUNTERS = 95140, 95150, 95170
ALGIERS, ORAN, PARIS, LONDON = 727, 728, 55, 29

# Hybrid models by Hive tech (as burrowers.py / milestones.py)
BEST = [("technology = 95060", 20), ("technology = 95040 NOT = { technology = 95060 }", 19),
        ("NOT = { technology = 95040 }", 18)]

# mainland Britain (Lerwick and Stornoway are islands: no Spire strikes reach them from a foothold)
UK = [5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
# the Channel coast is in range of batteries across the water (Calais and Dunkirk to Dover, as in 1940)
ACROSS = {26: [49, 51]}

# Dropship landings: (target, launch shores (any), divisions per wave, Home Guard woken in (province, unit id))
# The Home Guard is vanilla DH Full's own: 18 dormant, locked garrison divisions with artillery in the UK's 1933
# file (unit type 12700, ids 10001-10018). Nothing in the uploaded event files wakes them; the drops do.
HG = 12700
DROPS = [
    (26, [49, 51, 50], 3, [(29, 10001), (29, 10002), (29, 10003), (28, 10004), (28, 10005), (27, 10006)]),  # Dover
    (27, [45, 43, 44], 3, [(19, 10007), (19, 10008), (28, 10009), (28, 10010), (20, 10011), (20, 10012)]),  # Portsmouth
    (25, [122, 125, 123], 2, [(16, 10013), (16, 10014), (29, 10015), (29, 10016), (18, 10017), (18, 10018)]),  # Norwich
]
WAVE_GAP = 45
DROP_COST = 30                       # manpower per wave

# dormant Hive units in chimera.inc (unit id type 19500)
SPIRE_ID0 = 96000                    # + UK index: "Spire Battery of X" (Hybrid Brood with a Spire Launcher brigade)
LONDON_GUARD = [(96100, "London Tower Brood", "infantry", 18), (96101, "London Tower Thralls", "militia", 10)]
SPIRE_BRIGADE = 14                   # artillery model 14, Spire Launcher Battery (units.ARTILLERY)

# the Hive's British campaign (AI targets once the first foothold is taken)
BRITAIN_TARGETS = [(29, 250), (26, 150), (27, 150), (28, 140), (24, 130), (25, 120), (19, 110), (17, 110),
                   (18, 100), (16, 100), (13, 90), (12, 90), (11, 80), (5, 80)]
CHANNEL_TARGETS = [(49, 200), (51, 200), (45, 150), (43, 140), (37, 120), (125, 120), (122, 120), (26, 100)]

VANILLA_VICHY = [2002004, 2001001, 2002005, 2003001, 2002006, 2003002, 2002007, 2006022, 2003003, 2002008,
                 2002031, 2001003, 2002009, 2001004, 2002011, 2002090, 2002091]
VANILLA_UK_SURRENDER = [2001040, 2001041, 2001042, 2001095]

def ctl(p, tag=C): return f"control = {{ province = {p} data = {tag} }}"
def any_of(*xs): return "OR = { " + " ".join(xs) + " }"
def war(a, b=C): return f"war = {{ country = {a} country = {b} }}"

def name(p):
    import breakout
    return breakout.g_name(p)

def spire_id(p): return SPIRE_ID0 + UK.index(p)

def neighbours(p):
    import story
    return [q for q in story.ADJ.get(p, []) if q in UK and q != p]

def dormant_units(tag):
    """Dormant divisions for the patched country files. None: the Home Guard is vanilla's."""
    return ""

def dormant_hive():
    """Lines for chimera.inc: one Spire battery per British province, and the London Tower's guard."""
    import story
    L = []
    for p in UK:
        L.append(f'   landdivision = {{ dormant = yes id = {{ type = {story.UNIT_TYPE} id = {spire_id(p)} }} '
                 f'name = "Spire Battery of {name(p)}" type = infantry model = 18 '
                 f'extra = artillery brigade_model = {SPIRE_BRIGADE} }}')
    for uid, nm, typ, model in LONDON_GUARD:
        L.append(f'   landdivision = {{ dormant = yes id = {{ type = {story.UNIT_TYPE} id = {uid} }} '
                 f'name = "{nm}" type = {typ} model = {model} locked = yes }}')
    return L

def ai_files():
    import ai
    return {"switch/UA0_channel.ai": lambda: ai.chimera_switch("to the Channel coast", CHANNEL_TARGETS),
            "switch/UA0_britain.ai": lambda: ai.chimera_switch("the conquest of Britain", BRITAIN_TARGETS)}

# ------------------------------------------------------------------------------------------------ Act 1
def act1(g):
    E = []
    sleep = [f"type = sleepevent which = {e}" for e in VANILLA_VICHY]
    E += g.event(ID0, "Paris Is Silent",
        "The last broadcast from the Eiffel Tower ended in the middle of a sentence. Paris has fallen to the Hive. "
        "There will be no armistice: there is no one on the other side to sign one. The Council of Ministers, "
        "meeting in a requisitioned schoolhouse outside Tours, has voted to carry the Republic across the "
        "Mediterranean and fight on from Algiers with the Empire behind it.",
        [("The government sails for Algiers", sleep + [
            f"type = capital which = {ALGIERS}", "type = dissent value = 8", "type = manpowerpool value = 40",
            "type = domestic which = defense_lobby value = 1", "type = setflag which = res_fra_algiers",
            f"type = event which = {ID0 + 1} where = ENG when = 1", f"type = event which = {ID0 + 3} where = FRA when = 5",
            f"trigger = {{ {ctl(ORAN, 'FRA')} }} type = event which = {ID0 + 4} where = FRA when = 10"])],
        country="FRA", trigger=["exists = FRA", ctl(PARIS), war("FRA"), ctl(ALGIERS, "FRA")],
        date=(1, "january", 1937), offset=3, deathdate=DEATH, picture="res_paris_falls")
    E += g.event(ID0 + 1, "France Fights On",
        "The French government has reached Algiers. It has refused to treat with the Hive and asks only for "
        "ships, guns and time. Whatever happens on the Continent, Britain will not stand alone.",
        [("We stand with France", ["type = relation which = FRA value = 50",
            f"trigger = {{ exists = FRA NOT = {{ alliance = {{ country = ENG country = FRA }} }} }} type = alliance which = FRA"])],
        country="ENG")
    E += g.event(ID0 + 3, "L'Appel d'Alger",
        "From Radio Alger, the Minister of War speaks to every Frenchman still in France, in the colonies and "
        "abroad: France has lost a battle, but France has not lost the war. The tirailleurs of Algeria, Senegal "
        "and Morocco are already marching to the ports.",
        [("Vive la France!", ["type = manpowerpool value = 60", "type = dissent value = -5",
                              "type = domestic which = interventionism value = 1"])],
        country="FRA", picture="res_paris_falls")
    E += g.event(ID0 + 4, "The Fleet Sails for Mers-el-Kebir",
        "The Marine Nationale steamed out of Toulon and Brest as the Hive reached the coast. Admiral Darlan "
        "asks where the fleet should go: to Mers-el-Kebir, under the government's own hand, or to Portsmouth "
        "and Admiralty command, where it can guard the Channel.",
        [("To Mers-el-Kebir", 70, ["type = dissent value = -2", "type = setflag which = res_fra_fleet_africa",
                                   f"type = construct which = coastal_fort where = {ORAN} value = 1"]),
         ("To Portsmouth", 30, ["type = relation which = ENG value = 30", "type = setflag which = res_fra_fleet_channel",
                                f"type = event which = {ID0 + 5} where = ENG when = 3"])],
        country="FRA")
    E += g.event(ID0 + 5, "The French Fleet at Portsmouth",
        "French battleships and destroyers are anchored at Spithead under the tricolour. Their crews will fight "
        "beside the Home Fleet in the Channel.",
        [("Welcome them", ["type = escort_pool value = 20", "type = relation which = FRA value = 20"])],
        country="ENG")
    E += g.event(ID0 + 6, "The Little Ships",
        "The Hive has broken through in Flanders and the armies are falling back on Dunkirk. The Admiralty has "
        "called for every boat that can cross the Channel: ferries, trawlers, lifeboats and pleasure steamers.",
        [("Every boat that floats", 70, ["type = manpowerpool value = 40", "type = dissent value = -3",
                                         "type = escort_pool value = -5"]),
         ("Hold Dunkirk", 30, [f"trigger = {{ {any_of(ctl(51, 'ENG'), ctl(51, 'FRA'))} }} type = construct which = land_fort where = 51 value = 2",
                               "type = dissent value = 2"])],
        country="ENG", trigger=["exists = ENG", war("ENG"), any_of(ctl(52), ctl(116), ctl(50)),
                                any_of(ctl(51, "ENG"), ctl(51, "FRA"), ctl(51, "BEL"))],
        date=(1, "january", 1937), offset=3, deathdate=DEATH, picture="res_little_ships")
    return E

# ------------------------------------------------------------------------------------------------ Act 2
def act2(g):
    E = []
    E += g.event(ID0 + 10, "The Channel Front",
        "Twenty-one miles of water are all that stand between the Hive and England. The War Cabinet orders the "
        "south and east coasts fortified: pillboxes on the beaches, the piers blown, the road signs taken down.",
        [("Fortify the coast", 70, [f"type = sleepevent which = {e}" for e in VANILLA_UK_SURRENDER] +
            ["type = money value = -100"] +
            [f"trigger = {{ {ctl(p, 'ENG')} }} type = construct which = coastal_fort where = {p} value = 1" for p in (26, 27, 25, 15, 23)]),
         ("Trust the Royal Navy", 30, [f"type = sleepevent which = {e}" for e in VANILLA_UK_SURRENDER] +
            ["type = escort_pool value = 10"])],
        country="ENG", trigger=["exists = ENG", "flag = res_stage_9500756"],
        date=(1, "january", 1937), offset=5, deathdate=DEATH)
    E += g.event(ID0 + 11, "Operation Pied Piper",
        "The children are leaving the cities: labels on their coats, gas masks in cardboard boxes, a sandwich "
        "each for the train. Some will go to the Welsh hills, some much further.",
        [("To the countryside", 60, ["type = dissent value = -2", "type = manpowerpool value = -5"]),
         ("Across the Atlantic, to Canada", 40, ["type = dissent value = -4", "type = escort_pool value = -5",
                                                  "type = relation which = CAN value = 20"])],
        country="ENG", trigger=["exists = ENG", f"event = {{ id = {ID0 + 10} days = 20 }}"],
        date=(1, "january", 1937), offset=5, deathdate=DEATH)
    E += g.event(ID0 + 12, "Hunters Sent to Sea",
        "The Hunter Dropships are ready. The Hive has learnt that the humans' fleets are their last wall. "
        "The swarm will go after their anchorages: the Channel ports, and the great base at Scapa Flow.",
        [("Hunt", ["type = setflag which = res_hunters_at_sea"])],
        country=C, trigger=[f"technology = {HUNTERS}", "flag = res_stage_9500756"],
        date=(1, "january", 1940), offset=10, deathdate=DEATH)
    E += g.event(ID0 + 13, "Hunters over Scapa Flow",
        "They came in low out of the North Sea at dusk. Hunter Dropships struck the Home Fleet at its moorings in "
        "Scapa Flow. The boom defences are torn and the oil tanks at Lyness are burning.",
        [("Move the fleet south, to Rosyth", 50, [f"type = construct which = naval_base where = 5 value = -1",
            f"trigger = {{ {ctl(12, 'ENG')} }} type = construct which = naval_base where = 12 value = 1", "type = escort_pool value = -5"]),
         ("Stand and fight", 50, [f"type = construct which = naval_base where = 5 value = -1", "type = money value = -60",
            f"type = construct which = anti_air where = 5 value = 2", "type = escort_pool value = -10"])],
        country="ENG", trigger=["exists = ENG", war("ENG"), "flag = res_hunters_at_sea", ctl(5, "ENG")],
        date=(1, "january", 1940), offset=20, deathdate=DEATH, picture="res_scapa")
    E += g.event(ID0 + 14, "Hunters in the Channel",
        "Convoys in the Channel are being torn apart by Hunter Dropships striking out of the low cloud. The "
        "colliers to London have stopped running.",
        [("Convoys by night", 60, ["type = escort_pool value = -8", "type = supplies value = -300"]),
         ("Close the Channel to shipping", 40, ["type = supplies value = -800", "type = dissent value = 2"])],
        country="ENG", trigger=["exists = ENG", war("ENG"), "flag = res_hunters_at_sea", any_of(ctl(49), ctl(45), ctl(51))],
        date=(1, "january", 1940), offset=20, deathdate=DEATH, picture="res_scapa")
    E += g.event(ID0 + 15, "Spire Launchers on the Channel",
        "Spire launchers are being dug in along the cliffs above Calais. From there, the Hive can reach the English coast.",
        [("Bombard", ["type = setflag which = res_spire_channel"])],
        country=C, trigger=[f"technology = {SPIRES}", "flag = res_stage_9500756", any_of(ctl(49), ctl(51))],
        date=(1, "january", 1937), offset=10, deathdate=DEATH)
    return E

# ------------------------------------------------------------------------------------------------ Act 3
def act3(g):
    E = []
    for d, (target, shores, size, guards) in enumerate(DROPS):
        base = ID0 + 20 + 4 * d
        nm = name(target)
        launch = any_of(*[ctl(s) for s in shores])
        for k in range(2):
            # the first wave needs a British-held target; the second also reinforces a foothold already taken
            gate = f"{launch} {ctl(target, 'ENG')}" if k == 0 else f"{launch} {any_of(ctl(target, 'ENG'), ctl(target))}"
            army = [f"trigger = {{ {gate} }} type = manpowerpool value = -{DROP_COST}",
                    f'trigger = {{ {gate} }} type = add_corps which = "{nm} Drop Brood {"I" * (k + 1)}" value = land where = {target}']
            for i in range(size):
                army += [f'trigger = {{ {gate} {tc} }} type = add_division which = "{["I", "II", "III", "IV"][i]} {nm} Drop Brood'
                         f'{" II" if k else ""}" value = infantry when = {m}' for tc, m in BEST]
            army.append(f"trigger = {{ {gate} }} type = event which = {base + 2 + k} where = ENG when = 0")
            if k == 0:
                army.append(f"type = event which = {base + 1} where = {C} when = {WAVE_GAP}")
            E += g.event(base + k, f"The {nm} Dropships" if k == 0 else f"The Second Wave over {nm}",
                f"Dropships are lifting off from the coast in their hundreds and heading out over the water for {nm}. "
                "Each one carries a Hybrid brood packed into its belly. They will come down on the English fields."
                if k == 0 else f"The Dropships are crossing again. A second brood is coming down at {nm}.",
                [("Launch", army)], country=C,
                trigger=[f"technology = {DROPSHIPS}", "flag = res_stage_9500756", war("ENG"), launch, ctl(target, "ENG")]
                if k == 0 else None,
                date=(1, "january", 1938) if k == 0 else None, offset=15 if k == 0 else None,
                deathdate=DEATH if k == 0 else None, picture="res_channel",
                text_id=f"RES_DROP_{d}_{k}")
            wake = [f"trigger = {{ {ctl(p, 'ENG')} }} type = activate_division which = {HG} value = {uid} where = {p} when = 0"
                    for p, uid in guards]
            E += g.event(base + 2 + k, f"Dropships over {nm}",
                f"The church bells are ringing across {nm}: the signal that the invasion has begun. Dropships are coming "
                "down in the fields and Hybrids are spilling out of them."
                + (" The Home Guard is turning out." if k == 0 else " They are back, and there are more of them."),
                [("Ring the bells. Turn out the Home Guard", 80, (wake if k == 0 else []) + ["type = dissent value = 2"]),
                 ("Counterattack with everything we have", 20, ["type = supplies value = -400", "type = dissent value = 1"])],
                country="ENG", picture="res_channel", text_id=f"RES_DROP_WARN_{d}_{k}")
    # the Hive's war in Britain: a foothold changes its targets
    feet = any_of(*[ctl(p) for p in UK])
    E += g.event(ID0 + 40, "A Foothold in England",
        "The Hive stands on English soil. Its swarms will march on London.",
        [("Onward to London", ["type = setflag which = res_uk_foothold", "type = manpowerpool value = 100",
                               'trigger = { ai = yes } type = ai which = "switch/UA0_britain.ai"'])],
        country=C, trigger=[f"exists = {C}", feet], date=(1, "january", 1937), offset=3, deathdate=DEATH)
    E += g.event(ID0 + 41, "The Enemy Is in England",
        "Hybrids are on English soil for the first time. Spire launchers are being brought up behind them.",
        [("We shall fight on the beaches", ["type = dissent value = 3", "type = manpowerpool value = 50",
                                            "type = domestic which = defense_lobby value = 1"])],
        country="ENG", trigger=["exists = ENG", feet], date=(1, "january", 1937), offset=3, deathdate=DEATH)
    # Spire batteries on every foothold
    for i, p in enumerate(UK):
        nm = name(p)
        E += g.event(ID0 + 100 + i, f"Spire Batteries at {nm}",
            f"Menials are clearing firing pits at {nm}. Spire launchers are coming up behind the broods, "
            "aimed at the next English town.",
            [("Emplace them", [f"type = activate_division which = 19500 value = {spire_id(p)} where = {p} when = 0",
                               "type = setflag which = res_uk_foothold"])],
            country=C, trigger=[ctl(p), f"technology = {SPIRES}"],
            date=(1, "january", 1937), offset=5, deathdate=DEATH, text_id=f"RES_SPIRE_BATT_{p}")
    # Spire strikes on British towns next to a foothold (or across the Channel from the Calais batteries)
    for i, p in enumerate(UK):
        nm = name(p)
        near = [ctl(q) for q in neighbours(p)]
        sources = [f"AND = {{ flag = res_uk_foothold {any_of(*near)} }}"] if near else []
        sources += [f"AND = {{ flag = res_spire_channel {ctl(q)} }}" for q in ACROSS.get(p, [])]
        if not sources:
            continue
        big = p == LONDON
        hit = [f"type = construct which = land_fort where = {p} value = -1",
               f"type = construct which = anti_air where = {p} value = -1",
               f"type = dissent value = {3 if big else 1}",
               f"type = event which = {ID0 + 300 + i} where = ENG when = 30"]
        E += g.event(ID0 + 200 + i, f"Spire Strike on {nm}",
            f"Spires are falling on {nm}. The bolts come down out of the sky, bury themselves in the streets and then "
            "split open, and whatever is inside crawls out among the rubble. The ARP wardens cannot keep up."
            + (" The Houses of Parliament have been hit." if big else ""),
            [("Evacuate the town", 60, hit + ["type = manpowerpool value = -3", "type = dissent value = 1"]),
             ("Hold every street", 40, hit + [f"type = manpowerpool value = -{12 if big else 6}"])],
            country="ENG", trigger=["exists = ENG", war("ENG"), ctl(p, "ENG"), any_of(*sources)],
            date=(1, "january", 1937), offset=7, deathdate=DEATH, picture="res_spire_strike",
            text_id=f"RES_SPIRE_STRIKE_{p}")
        follow = [f"trigger = {{ {ctl(p, 'ENG')} }} {c}" for c in
                  (f"type = construct which = land_fort where = {p} value = -1", "type = supplies value = -200",
                   f"type = manpowerpool value = -{6 if big else 3}")]
        E += g.event(ID0 + 300 + i, f"The Barrage Goes On at {nm}",
            f"The Spires have not stopped falling on {nm}. Whole streets are gone.",
            [("Endure", follow)], country="ENG", picture="res_spire_strike", text_id=f"RES_SPIRE_AGAIN_{p}")
    return E

# ------------------------------------------------------------------------------------------------ Act 4
def act4(g):
    E = []
    seat = [12, 11, 36, 6, 7]                  # Edinburgh, Glasgow, Belfast, Inverness, Aberdeen
    move = []
    for n, p in enumerate(seat):
        before = " ".join(f"NOT = {{ {ctl(q, 'ENG')} }}" for q in seat[:n])
        move.append(f"trigger = {{ {ctl(p, 'ENG')} {before} }} type = capital which = {p}")
    E += g.event(ID0 + 500, "London Burns",
        "London has fallen. The Hive is in Whitehall and the Spires are still falling on the East End. The King and "
        "the Cabinet left by night. Part of the government will carry on in the north. The Crown, the gold and the "
        "Admiralty's codebooks are crossing the Atlantic to Ottawa.",
        [("The government carries on", move + ["type = dissent value = 10", "type = manpowerpool value = 30",
            "trigger = { exists = CAN } type = event which = 9590501 where = CAN when = 7",
            "trigger = { exists = USA } type = event which = 9590502 where = USA when = 3"])],
        country="ENG", trigger=["exists = ENG", ctl(LONDON)],
        date=(1, "january", 1937), offset=2, deathdate=DEATH, picture="res_london_burns")
    E += g.event(ID0 + 501, "The Crown Comes to Ottawa",
        "The King has landed at Halifax with the Royal Family and the Bank of England's gold. Ottawa is now the "
        "seat of the Crown, and Canada stands at the head of what is left of the Empire.",
        [("God save the King", ["type = manpowerpool value = 80", "type = dissent value = -3",
                                "type = relation which = ENG value = 50", "type = domestic which = interventionism value = 2",
                                "type = money value = 300"])],
        country="CAN", picture="res_london_burns")
    E += g.event(ID0 + 502, "London Has Fallen",
        "London has fallen to the Hive. Britain's government is in exile and the King is in Canada. The Atlantic is "
        "now all that lies between the Hive and the United States.",
        [("Send everything we can spare", 60, ["type = domestic which = interventionism value = 2",
                                               "type = relation which = CAN value = 30", "type = relation which = ENG value = 30"]),
         ("Look to our own shores", 40, ["type = domestic which = defense_lobby value = 2"])],
        country="USA")
    wake = [f"type = activate_division which = 19500 value = {uid} where = {LONDON} when = 0" for uid, *_ in LONDON_GUARD]
    E += g.event(ID0 + 45, "A Tower over London",
        "A tower is growing out of the ruins of the City of London. It stands taller than St Paul's dome, and it is "
        "still rising.",
        [("Raise the tower", wake + ["type = manpowerpool value = 150",
                                     f"type = construct which = anti_air where = {LONDON} value = 3"])],
        country=C, trigger=[f"exists = {C}", ctl(LONDON), f"event = {{ id = {ID0 + 500} days = 60 }}"],
        date=(1, "january", 1937), offset=10, deathdate=DEATH, picture="res_london_tower")
    return E

def events(g):
    E = ["#########################################################################",
         "#  RESISTANCE MOD - The Fall of Europe: France, the Channel and Britain (9590000+)",
         "#########################################################################", ""]
    E += act1(g) + act2(g) + act3(g) + act4(g)
    assert max(ID0 + 300 + len(UK), ID0 + 510) < 9600000
    return E
