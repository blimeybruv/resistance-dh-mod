"""Generates the Resistance mod files for Darkest Hour Full 1.05.

All tech, event and localisation data lives in the tables below so the
whole module can be regenerated after any change.  Output uses CRLF line
endings like the vanilla files.
"""
import os, re, sys

SRC = sys.argv[1]   # folder with vanilla secret_weapons_tech.txt and country.csv
OUT = sys.argv[2]   # mod output folder

CHIMERA = "UA0"     # spare tag from country.csv
LANGS = 10          # text columns in localisation csv before the closing X

# ---------------------------------------------------------------- techs
# (id, key, name, year, picture, required, [(component name, type, difficulty)], [effect commands])
CHIMERA_STRAINS = [
    (95010, "STRAIN_1", "Tunguska Strain", 1908, "DH1010", [],
     [("Primary Infection Vector", "chemistry", 3), ("Cellular Rewriting", "chemistry", 3),
      ("Host Integration", "training", 3), ("Hive Signalling", "electronics", 3),
      ("First Hybrid Generation", "general_equipment", 3)],
     [# the infantry unit type came from the human 1870 infantry tech, which the Hive no longer has
      "type = activate_unit_type which = infantry", "type = new_model which = infantry value = 18",
      # cooling implants: the Hive suffers in hot climates until the Apex Strain
      "type = desert_attack which = infantry value = -3", "type = desert_defense which = infantry value = -3",
      "type = desert_attack which = cavalry value = -3", "type = desert_defense which = cavalry value = -3",
      "type = toughness which = militia value = -2",
      "type = defensiveness which = militia value = -1",
      "type = manpower which = infantry when = on_upgrade value = -0.2"]),
    (95020, "STRAIN_2", "Adaptive Strain", 1936, "DH1020", [95010],
     [("Thermal Adaptation", "chemistry", 5), ("Accelerated Metabolism", "chemistry", 5),
      ("Spined Carapace", "general_equipment", 5), ("Pack Instinct", "small_unit_tactics", 5),
      ("Second Hybrid Generation", "training", 5)],
     ["type = activate_unit_type which = cavalry",
      "type = new_model which = cavalry value = 15",
      "type = activate_unit_type which = medium_armor",
      "type = new_model which = medium_armor value = 11",
      "type = soft_attack which = infantry value = 1",
      "type = soft_attack which = militia value = 1"]),
    (95030, "STRAIN_3", "Rapid Conversion", 1939, "14080", [95020],
     [("Conversion Pods", "chemistry", 6), ("Cocoon Chambers", "industrial_engineering", 6),
      ("Mass Host Processing", "management", 6), ("Gestation Acceleration", "chemistry", 6),
      ("Conversion Centre Network", "management", 6)],
     ["type = manpower which = infantry when = on_upgrade value = -0.2",
      "type = manpower which = militia when = on_upgrade value = -0.2"]),
    (95040, "STRAIN_4", "Advanced Hybrids", 1942, "DH1020", [95030],
     [("Augmented Musculature", "chemistry", 7), ("Integrated Weapon Grafts", "general_equipment", 7),
      ("Thermal Vision", "electronics", 7), ("Coordinated Swarming", "large_unit_tactics", 7),
      ("Third Hybrid Generation", "training", 7)],
     ["type = new_model which = infantry value = 19",
      "type = defensiveness which = militia value = -1"]),
    (95050, "STRAIN_5", "Heavy Hybrid Breeds", 1946, "DH1010", [95040],
     [("Heavy Carapace", "chemistry", 8), ("Grafted Cannons", "artillery", 8),
      ("Shock Troop Breeding", "training", 8), ("Regenerative Tissue", "chemistry", 8),
      ("Brute Generation", "general_equipment", 8)],
     ["type = new_model which = cavalry value = 16",
      "type = activate_unit_type which = heavy_armor",
      "type = new_model which = heavy_armor value = 6",
      "type = hard_attack which = infantry value = 1"]),
    (95060, "STRAIN_6", "Apex Strain", 1950, "14080", [95050],
     [("Perfected Conversion", "chemistry", 9), ("Hive Mind Uplink", "electronics", 9),
      ("Apex Predator Instincts", "small_unit_tactics", 9), ("Total Adaptation", "chemistry", 9),
      ("Final Hybrid Generation", "training", 9)],
     ["type = new_model which = infantry value = 20",
      # heat-adapted strains (canon: from 1951 the Chimera no longer need cooling implants)
      "type = desert_attack which = infantry value = 3", "type = desert_defense which = infantry value = 3",
      "type = desert_attack which = cavalry value = 3", "type = desert_defense which = cavalry value = 3",
      "type = defensiveness which = infantry value = -1"]),
]

CHIMERA_ENGINEERING = [
    (95110, "ENG_1", "Bio-mechanical Engineering", 1937, "DH7600", [95010],
     [("Living Armour Plating", "mechanics", 5), ("Organic Power Cells", "chemistry", 5),
      ("Walker Locomotion", "vehicle_engineering", 5), ("Neural Control Links", "electronics", 5),
      ("Bio-mechanical Trials", "vehicle_engineering", 5)],
     ["type = activate_unit_type which = super_heavy_armor",
      "type = new_model which = super_heavy_armor value = 2"]),
    (95120, "ENG_2", "Stalker Walkers", 1941, "Dh7610", [95110],
     [("Tripod Chassis", "vehicle_engineering", 7), ("Plasma Cannon Mount", "artillery", 7),
      ("Armoured Brain Case", "mechanics", 7), ("Hunter-Killer Routines", "electronics", 7),
      ("Stalker Field Trials", "vehicle_engineering", 7)],
     ["type = soft_attack which = super_heavy_armor value = 2",
      "type = hard_attack which = super_heavy_armor value = 2"]),
    (95130, "ENG_3", "Goliath Walkers", 1946, "Dh7610", [95120],
     [("Colossal Frame", "vehicle_engineering", 9), ("Massive Bio-reactor", "chemistry", 9),
      ("Siege Armament", "artillery", 9), ("Self-Repairing Hide", "mechanics", 9),
      ("Goliath Gestation", "vehicle_engineering", 9)],
     ["type = new_model which = super_heavy_armor value = 3",
      "type = scrap_model which = super_heavy_armor value = 2"]),
    (95140, "ENG_4", "Spire Launchers", 1936, "7100", [95110],
     [("Spire Projectiles", "rocketry", 6), ("Ballistic Seeding", "mathematics", 6),
      ("Impact Infection Pods", "chemistry", 6), ("Launch Organs", "rocketry", 6),
      ("Spire Bombardment Trials", "artillery", 6)],
     ["type = soft_attack which = artillery value = 2",
      "type = activate_unit_type which = artillery", "type = new_model which = artillery value = 14"]),
    (95150, "ENG_5", "Dropships and Fighters", 1938, "7010", [95110],
     [("Anti-gravity Lift", "aeronautics", 8), ("Armoured Hull Growth", "mechanics", 8),
      ("Transport Containers", "management", 8), ("Plasma Cannon", "artillery", 8),
      ("Flight Trials", "aeronautics", 8)],
     ["type = activate_unit_type which = interceptor", "type = new_model which = interceptor value = 17",
      "type = activate_unit_type which = cas", "type = new_model which = cas value = 7"]),
    (95160, "ENG_6", "The Chimeran Fleet", 1950, "7200", [95150],
     [("Tower-core Reactors", "nuclear_physics", 10), ("Hangar Decks", "aeronautics", 10),
      ("Energy Lances", "electronics", 10), ("Spire Silos", "rocketry", 10),
      ("Fleet Command Angels", "management", 10)],
     ["type = activate_unit_type which = strategic_bomber", "type = new_model which = strategic_bomber value = 10",
      "type = new_model which = interceptor value = 18"]),
    (95170, "ENG_7", "Sea Hunters", 1940, "7010", [95150],
     [("Hull Sealing", "aeronautics", 7), ("Wave-skimming Flight", "aeronautics", 7), ("Surface Sensing", "electronics", 7),
      ("Ship-killing Charges", "munitions", 7), ("Strike Broods", "training", 7)],
     # the Hive's air doctrines are locked, so this tech grants the anti-shipping missions itself
     ["type = activate_unit_type which = naval_bomber", "type = new_model which = naval_bomber value = 9",
      "type = enable_task which = naval_strike", "type = enable_task which = port_strike",
      "type = task_efficiency which = naval_strike value = 0.50", "type = task_efficiency which = port_strike value = 0.30"]),
    # the Burrower (lore: Chimeran tunnelling machine): no effect of its own; the crossing events check for it
    (95180, "ENG_8", "Burrowers", 1944, "Dh7610", [95120],
     [("Boring Organisms", "mechanics", 8), ("Tunnel Shoring", "industrial_engineering", 8), ("Seabed Navigation", "electronics", 8),
      ("Pressure Membranes", "chemistry", 8), ("Burrow Broods", "training", 8)],
     []),
]

HUMAN_ARMS = [
    (95210, "ARMS_1", "Recovered Chimeran Weapons", 1936, "DH1010", [],
     [("Specimen Recovery Teams", "management", 6), ("Alien Mechanism Analysis", "mechanics", 6),
      ("Power Source Studies", "chemistry", 6), ("Field Testing", "general_equipment", 6),
      ("Weapons Evaluation Reports", "training", 6)],
     ["type = soft_attack which = infantry value = 1"]),
    (95220, "ARMS_2", "Reverse-Engineered Rifles", 1940, "DH1020", [95210],
     [("Penetrating Rounds", "munitions", 7), ("Captured Power Cells", "chemistry", 7),
      ("Rifle Production Line", "industrial_engineering", 7), ("Sight Adaptation", "electronics", 7),
      ("Troop Conversion Training", "training", 7)],
     ["type = soft_attack which = infantry value = 2",
      "type = soft_attack which = militia value = 2",
      "type = hard_attack which = infantry value = 1",   # penetrating rounds
      # alien parts are scarce and hand-fitted: like vanilla's equipment techs, better kit costs more to build
      "type = build_cost which = infantry when = on_upgrade where = relative value = 5",
      "type = build_cost which = militia when = on_upgrade where = relative value = 5"]),
    (95230, "ARMS_3", "Deployable Shield Studies", 1943, "14080", [95220],
     [("Energy Barrier Theory", "electronics", 8), ("Portable Emitters", "electronics", 8),
      ("Shield Power Cells", "chemistry", 8), ("Defensive Drill", "training", 8),
      ("Shield Field Trials", "general_equipment", 8)],
     ["type = defensiveness which = infantry value = -2",
      "type = build_cost which = infantry when = on_upgrade where = relative value = 5"]),
    (95240, "ARMS_4", "Chimeran Alloy Armour", 1947, "DH7600", [95230],
     [("Alloy Metallurgy", "chemistry", 9), ("Composite Plating", "mechanics", 9),
      ("Hull Retrofit", "vehicle_engineering", 9), ("Heat Treatment", "industrial_engineering", 9),
      ("Armour Proving Trials", "vehicle_engineering", 9)],
     ["type = toughness which = armor value = -2",
      "type = defensiveness which = armor value = -2",
      "type = build_cost which = armor when = on_upgrade where = relative value = 10"]),
]

HUMAN_PATHOLOGY = [
    (95310, "PATH_1", "Quarantine Protocols", 1934, "16000", [],
     [("Infection Identification", "rt_user_1", 5), ("Cordon Procedures", "management", 5),
      ("Decontamination Stations", "rt_user_1", 5), ("Civilian Screening", "management", 5),
      ("Quarantine Drills", "training", 5)],
     ["type = defensiveness which = garrison value = -1",
      "type = defensiveness which = militia value = -1"]),
    (95320, "PATH_2", "Inhibitor Serum Trials", 1941, "16000", [95310],
     [("Virus Isolation", "rt_user_1", 8), ("Inhibitor Synthesis", "rt_user_1", 8),
      ("Dosage Trials", "rt_user_1", 8), ("Field Injectors", "general_equipment", 8),
      ("Frontline Inoculation", "training", 8)],
     ["type = toughness which = infantry value = -1"]),
    (95330, "PATH_3", "Mass Inoculation", 1947, "16000", [95320],
     [("Serum Mass Production", "rt_user_1", 9), ("Cold Chain Logistics", "management", 9),
      ("Booster Regimens", "rt_user_1", 9), ("Army-wide Programme", "management", 9),
      ("Civil Defence Inoculation", "training", 9)],
     ["type = toughness which = infantry value = -1",
      "type = toughness which = militia value = -1"]),
]

HUMAN_DOCTRINE = [
    (95410, "DOC_1", "Anti-Hybrid Tactics", 1935, "7240", [],
     [("Threat Recognition", "training", 5), ("Close Quarters Drill", "small_unit_tactics", 5),
      ("Fire Discipline", "training", 5), ("Strongpoint Defence", "small_unit_tactics", 5),
      ("After-action Analysis", "management", 5)],
     ["type = defensiveness which = infantry value = -1"]),
    (95420, "DOC_2", "Flamethrower Assault Teams", 1939, "7240", [95410],
     [("Portable Flamethrowers", "chemistry", 6), ("Incendiary Fuel Mixes", "chemistry", 6),
      ("Assault Team Training", "training", 6), ("Nest Clearing Drill", "small_unit_tactics", 6),
      ("Combined Flame Tactics", "combined_arms_focus", 6)],
     ["type = soft_attack which = engineer value = 2"]),
    (95430, "DOC_3", "Scorched Earth Doctrine", 1944, "7240", [95420],
     [("Denial Planning", "management", 7), ("Demolition Stockpiles", "munitions", 7),
      ("Fighting Withdrawal", "large_unit_tactics", 7), ("Rearguard Training", "training", 7),
      ("Evacuation Corridors", "management", 7)],
     ["type = toughness which = infantry value = -1",
      "type = toughness which = garrison value = -1"]),
    (95440, "DOC_4", "Tower Demolition Teams", 1950, "7240", [95430],
     [("Tower Structural Analysis", "mathematics", 8), ("Shaped Demolition Charges", "munitions", 8),
      ("Infiltration Training", "small_unit_tactics", 8), ("Cooling Network Sabotage", "chemistry", 8),
      ("Raid Rehearsals", "training", 8)],
     ["type = hard_attack which = engineer value = 1"]),
]

# Hive Warfare: a Chimera-only land doctrine line, in the empty column at x=346 of the land
# doctrine screen. Effect commands are all copied from vanilla doctrines.
DOCTRINE = [
    # requires the Tunguska Strain (event-gated, Chimera only) so no human nation can research it
    (95510, "HIVE_1", "Hive Mind Coordination", 1908, "DH6500", [95010],
     [("Telepathic Command Links", "centralized_execution", 3), ("Shared Senses", "infantry_focus", 3),
      ("Instant Orders", "management", 3), ("No Retreat Instinct", "individual_courage", 3),
      ("Hive Drill", "training", 3)],
     ["type = max_organization which = land value = 6", "type = delay value = -8",
      # The human doctrine trunk the Hive starts with leaves it at 75% attack and 25% ground defence efficiency.
      # The Hive is lopsided on purpose: full attack efficiency and fearless from the start, but poor at
      # holding ground (ground_def_eff is set, not added; it rises only through Hive Warfare and never to 100%).
      "type = task_efficiency which = attack value = 0.25", "type = task_efficiency which = support_attack value = 0.25",
      "type = morale which = land value = 10", "type = ground_def_eff value = 0.40",
      # Angel Nexus HQ. Here, not on the Tunguska Strain, because the Cloven programme gives the USSR that tech.
      "type = activate_unit_type which = hq", "type = new_model which = hq value = 6"]),
    (95520, "HIVE_2", "Swarm Assault", 1936, "DH6510", [95510],
     [("Massed Charges", "infantry_focus", 6), ("Encirclement Instinct", "maneuver_tactics", 6),
      ("Leaper Screens", "small_unit_tactics", 6), ("Relentless Pressure", "large_unit_tactics", 6),
      ("Swarm Exercises", "training", 6)],
     ["type = plain_attack which = land value = 8", "type = forest_attack which = land value = 6",
      "type = urban_attack which = land value = 6", "type = breakthrough value = 5"]),
    (95530, "HIVE_3", "Overwhelming Numbers", 1939, "DH6530", [95520],
     [("Conversion Replacements", "medicine", 7), ("Expendable Thralls", "large_unit_focus", 7),
      ("Wave Tactics", "large_unit_tactics", 7), ("Fearless Advance", "individual_courage", 7),
      ("Endless Hordes", "training", 7)],
     ["type = max_organization which = land value = 4", "type = morale which = land value = 5",
      "type = ground_def_eff value = 0.50",
      # Thralls improve with the Hive, not with the human militia line
      "type = soft_attack which = militia value = 2", "type = defensiveness which = militia value = -2"]),
    (95540, "HIVE_4", "Siege of the Cities", 1942, "DH6550", [95530],
     [("Concussion Barrages", "artillery", 8), ("Spire Saturation", "rocketry", 8),
      ("Goliath Escorts", "combined_arms_focus", 8), ("Tunnelling Menials", "static_defense_tactics", 8),
      ("Siege Drill", "training", 8)],
     ["type = fort_attack which = land value = 10", "type = urban_attack which = land value = 6",
      "type = ground_def_eff value = 0.55"]),
    (95550, "HIVE_5", "Primarchs and Overseers", 1950, "DH6500", [95540],
     [("Primarch Caste", "centralized_execution", 9), ("Overseer Caste", "decentralized_execution", 9),
      ("Redundant Command", "management", 9), ("Human Tactics Assimilated", "combined_arms_focus", 9),
      ("Command Reform", "training", 9)],
     ["type = max_organization which = land value = 8", "type = morale which = land value = 5",
      "type = hq_supply_eff value = 3", "type = ground_def_eff value = 0.65",
      "type = soft_attack which = militia value = 2", "type = toughness which = militia value = -2"]),
    # Innate, known from the start (Hive-only: needs Hive Mind). Replaces the human lines the Hive has no use for
    # (agriculture, medicine, hospitals) and sets the doctrine-page levers to a lopsided Chimeran profile.
    (95560, "HIVE_6", "Hive Physiology", 1908, "DH6500", [95510],
     [("Biomass Reclamation", "chemistry", 3), ("Tissue Regrowth", "chemistry", 3),
      ("Cold Adaptation", "training", 3), ("Swarm Instinct", "small_unit_tactics", 3),
      ("Aerial Brood Coordination", "electronics", 3)],
     [# the dead are reclaimed, the converted swell the ranks, bodies regrow and shrug off the cold
      "type = trickleback_mod value = 20", "type = relative_manpower value = 10",
      "type = attrition_mod value = 10", "type = repair_mod value = 20",
      "type = industrial_modifier which = supplies value = 10", "type = industrial_modifier which = total value = 5",
      # the swarm surrounds and storms; it does not counterattack or ambush any better than men
      "type = assault value = 5", "type = encirclement value = 3",
      # Dropships are made for ground attack; the Battleships come late, so strategic bombing stays weak
      "type = task_efficiency which = ground_attack value = 0.50", "type = task_efficiency which = interdiction value = 0.40",
      "type = task_efficiency which = air_superiority value = 0.40",
      "type = task_efficiency which = strategic_bombardment value = 0.15"]),
    # The Hive's own Thralls and AA, instead of the human infantry and AA brigade lines (which also brought
    # garrisons, military police and human AA). Hive-only, known from the start.
    (95570, "HIVE_7", "Thrall Conversion", 1908, "DH1010", [95510],
     [("Host Subjugation", "chemistry", 3), ("Neural Suppression", "chemistry", 3), ("Herding", "training", 3),
      ("Crude Armament", "general_equipment", 3), ("Expendable Masses", "management", 3)],
     ["type = activate_unit_type which = militia", "type = new_model which = militia value = 10",
      # the same conversions yield the Menials, the worker caste: engineer brigades for river crossings
      "type = activate_unit_type which = engineer", "type = new_model which = engineer value = 8"]),
    (95580, "HIVE_8", "Chimeran Air Defence", 1908, "2800", [95510],
     [("Spore Flak", "artillery", 3), ("Bio-luminescent Tracking", "electronics", 3), ("Turret Grafting", "mechanics", 3),
      ("Hive Sky-watch", "electronics", 3), ("Flak Broods", "training", 3)],
     ["type = activate_unit_type which = anti_air", "type = new_model which = anti_air value = 7"]),
]
DOCTRINE_X, DOCTRINE_LABEL_Y, DOCTRINE_MARKER_Y, DOCTRINE_FIRST_Y = 351, 3, 20, 37
# Vanilla boxes moved to make room: Leading by Task (6590) and Leading by Orders (6580)
# sit side by side (vanilla rows use a 110 px pitch) instead of 140 px apart.
MOVED_TECHS = {6590: 128, 6580: 238}

def build_doctrine_band():
    loc("TECH_CAT_RES_HIVE", "Hive Warfare (Hive only)")
    out = ["", "  ##########################################################",
           "  # RESISTANCE MOD - Hive Warfare (Chimera only)", "  ##########################################################",
           "  label =", "  { tag      = TECH_CAT_RES_HIVE", f"    position = {{ x = {DOCTRINE_X} y = {DOCTRINE_LABEL_Y} }}", "  }",
           "  event =", "  { id         = 9500003", f"    position   = {{ x = {DOCTRINE_X} y = {DOCTRINE_MARKER_Y} }}",
           f"    technology = {DOCTRINE[1][0]}", "  }"]
    for i, t in enumerate(DOCTRINE):
        out += tech_block(DOCTRINE_X, DOCTRINE_FIRST_Y + i * STEP, t)
    return out

def move_techs(txt, moves):
    for tid, x in moves.items():
        txt, n = re.subn(rf"(id\s*=\s*{tid}\b.*?position\s*=\s*\{{\s*x\s*=\s*)\d+", rf"\g<1>{x}", txt, count=1, flags=re.S)
        assert n == 1, tid
    return txt

def insert_band(src, band, moves=None):
    txt = open(src, encoding="latin-1").read().replace("\r\n", "\n")
    if moves: txt = move_techs(txt, moves)
    cut = txt.rstrip().rfind("}")          # closing brace of the technology block
    return (txt[:cut].rstrip() + "\n" + "\n".join(band) + "\n}\n").split("\n")

# Layout: free band at the bottom of the secret weapons screen
COLUMNS = [  # (x, label key, label text, techs, activating event)
    (24,  "TECH_CAT_RES_STRAINS",     "Chimeran Strains", CHIMERA_STRAINS,     9500001),
    (160, "TECH_CAT_RES_ENGINEERING", "Chimeran Engineering", CHIMERA_ENGINEERING, 9500002),
    (296, "TECH_CAT_RES_ARMS",        "Captured Chimeran Arms", HUMAN_ARMS,         9500101),
    (432, "TECH_CAT_RES_PATHOLOGY",   "Chimeran Pathology",    HUMAN_PATHOLOGY,     9500201),
    (552, "TECH_CAT_RES_DOCTRINE",    "Anti-Chimeran Warfare", HUMAN_DOCTRINE,      9500301),
]
LABEL_Y, MARKER_Y, FIRST_Y, STEP = 338, 352, 370, 17

# Nations that get the captured-tech line once they fight the Chimera
HUMAN_NATIONS = ["SOV", "ENG", "FRA", "GER", "USA", "ITA", "POL", "JAP", "FIN", "ROM",
                 "CHI", "TUR", "PER", "MON", "EST", "LAT", "LIT", "CZE", "HUN", "SWE",
                 "NOR", "DEN", "HOL", "BEL", "SPA", "AUS", "YUG", "BUL", "GRE", "CAN",
                 "AFG", "MAN", "TAN", "SIK", "UPE", "ALB", "LUX", "IRE", "POR", "SPR", "SCH", "VIC", "U01"]

# Chimera evolution schedule: (event id, tech id, date)
EVOLUTION = [(9500011, 95020, (1, "march", 1936)), (9500012, 95110, (1, "june", 1937)),
             (9500013, 95030, (1, "january", 1939)), (9500014, 95140, (1, "september", 1936)),
             (9500015, 95120, (1, "march", 1941)), (9500016, 95040, (1, "may", 1942)),
             (9500017, 95050, (1, "february", 1946)), (9500018, 95130, (1, "october", 1946)),
             (9500019, 95060, (1, "april", 1950)),
             (9500020, 95150, (1, "june", 1938)), (9500021, 95160, (1, "march", 1950)),
             (9500022, 95520, (1, "september", 1936)), (9500023, 95530, (1, "june", 1939)),
             (9500024, 95540, (1, "september", 1942)), (9500025, 95550, (1, "january", 1950))]
EVOLUTION_NAMES = {}

text = {}  # localisation key -> English

def loc(key, value):
    text[key] = value
    return key

SHORT = {95010: "Tunguska Strain", 95020: "Adaptive Strain", 95030: "Rapid Conversion", 95040: "Adv. Hybrids",
         95050: "Heavy Hybrids", 95060: "Apex Strain", 95110: "Bio-mechanics", 95120: "Stalkers",
         95130: "Goliaths", 95510: "Hive Mind", 95520: "Swarm Assault", 95530: "Overwhelming Nos.",
         95540: "City Sieges", 95550: "Primarchs", 95150: "Dropships", 95160: "Chimeran Fleet", 95140: "Spire Launchers", 95210: "Chimeran Arms", 95220: "Rev.-Eng. Rifles",
         95230: "Shield Studies", 95240: "Chimeran Alloy", 95310: "Quarantine", 95320: "Inhibitor Serum",
         95330: "Inoculation", 95410: "Anti-Hybrid Tactics", 95420: "Flame Teams", 95430: "Scorched Earth",
         95440: "Tower Demolition", 95560: "Hive Physiology", 95570: "Thrall Conversion", 95580: "Chimeran Air Defence", 95170: "Sea Hunters", 95180: "Burrowers"}

# Activating a unit type also makes its model 0 (the 1870/1918 human version) buildable. After every
# activate_unit_type in a Chimeran tech, scrap model 0 again - but only for the Hive: every human country knows
# the 1870 infantry tech (1010), which the Hive no longer has, so a Cloven USSR keeps its own models.
HIVE_ONLY = "NOT = { technology = 1010 }"

def drop_model_zero(effects):
    out = []
    for e in effects:
        out.append(e)
        m = re.match(r"type = activate_unit_type which = (\w+)$", e.strip())
        if m and f"type = new_model which = {m.group(1)} value = 0" not in effects:
            out.append(f"trigger = {{ {HIVE_ONLY} }} type = scrap_model which = {m.group(1)} value = 0")
    return out

def tech_block(x, y, t):
    tid, key, name, year, pic, req, comps, effects = t
    # the mod's own tech picture (src/assets/gfx/interface/tech/<id>.bmp) replaces the borrowed vanilla one
    if os.path.exists(os.path.join(SRC, "assets", "gfx", "interface", "tech", f"{tid}.bmp")):
        pic = str(tid)
    n = loc(f"TECH_APP_RES_{key}_NAME", name)
    loc(f"SHORT_TECH_APP_RES_{key}_NAME", SHORT[tid])   # label shown in the tree box
    lines = ["  # " + name, "  application =", f"  {{ id        = {tid}", f"    name      = {n}", "",
             f"    position  = {{ x = {x} y = {y} }}", f'\tpicture   = "{pic}"', f"    year      = {year}"]
    for i, (cname, ctype, diff) in enumerate(comps, 1):
        ck = loc(f"TECH_CMP_RES_{key}_{i}_NAME", cname)
        dt = " double_time = yes" if i == 5 else ""
        lines.append(f"    # {cname}")
        lines.append(f"    component = {{ id = {tid + i} name = {ck} type = {ctype}{dt} difficulty = {diff} }}")
    lines.append(f"    required  = {{ {' '.join(map(str, req))} }}")
    lines.append("    effects =")
    lines.append("    { " + "\n      ".join(f"command = {{ {e} }}" for e in drop_model_zero(effects)))
    lines.append("    }")
    lines.append("  }")
    return lines

def build_tech_band():
    out = ["", "  ##########################################################",
           "  # RESISTANCE MOD - Chimeran technology band", "  ##########################################################"]
    for x, lkey, ltext, techs, ev in COLUMNS:
        loc(lkey, ltext)
        out += ["  label =", f"  {{ tag      = {lkey}", f"    position = {{ x = {x} y = {LABEL_Y} }}", "  }"]
        out += ["  event =", f"  {{ id         = {ev}", f"    position   = {{ x = {x} y = {MARKER_Y} }}",
                f"    technology = {techs[0][0]}", "  }"]
        for i, t in enumerate(techs):
            out += tech_block(x, FIRST_Y + i * STEP, t)
    return out

def write(path, lines):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", newline="\r\n", encoding="latin-1") as f:
        f.write("\n".join(lines) + "\n")

# Event pictures: (first id, last id, picture). A custom picture is used once a BMP with that
# name exists in src/assets (gfx/events_pics/); until then the vanilla picture stays.
EVENT_PICS = [
    # Menials, the worker caste, at work in a captured town: The Hive Harvest and The Hive Builds
    (9502000, 9502999, "res_menials"), (9504000, 9504999, "res_menials"), (9508500, 9508999, "res_menials"),
    (9500001, 9500003, "res_hive_stirs"),      (9500011, 9500025, "res_hive_evolves"),
    (9500101, 9500143, "res_salvage"),         (9500201, 9500243, "res_specimens"),
    (9500301, 9500343, "res_salvage"),
    (9500420, 9500424, "res_cloven"),          (9500430, 9500433, "res_tower_falls"),
    (9500490, 9500490, "res_specimens"),       (9500554, 9500554, "res_evacuation"),
    (9507000, 9507999, "res_conversion"),      (9508000, 9508499, "res_silent_town"),
    (9508500, 9508999, "res_hive_heart"),       (9500492, 9500493, "res_closed_zone"),
    (9500496, 9500496, "res_early_winter"),
    (9500500, 9500500, "res_closed_zone"),     (9500501, 9500501, "res_lost_expedition"),
    (9500502, 9500502, "res_checkpoint"),      (9500503, 9500503, "res_exodus"),
    (9500504, 9500505, "res_lost_expedition"), (9500506, 9500506, "res_early_winter"),
    (9500507, 9500507, "res_closed_zone"),
    (9500510, 9500513, "res_silent_town"),     (9500520, 9500523, "res_conversion"),
    (9500530, 9500530, "res_outbreak"),        (9500531, 9500531, "res_silent_town"),
    (9500540, 9500540, "res_exodus"),
    (9500550, 9500550, "res_quarantine_line"), (9500551, 9500551, "res_evacuation"),
    (9500552, 9500552, "res_scorched_earth"),  (9500553, 9500553, "res_foreign_aid"),
    (9500560, 9500563, "res_foreign_aid"),     (9500570, 9500573, "res_surge"),
    (9500580, 9500589, "res_conversion"),      (9500600, 9500600, "res_hive_heart"),
    (9500700, 9500700, "res_surge"),           (9500701, 9500701, "res_quarantine_line"),
    (9500702, 9500709, "res_fall_of_moscow"),  (9500740, 9500741, "res_surge"),
    (9500745, 9500749, "res_hive_heart"),      (9500750, 9500756, "res_surge"),
    (9500760, 9500763, "res_armistice"),       (9500770, 9500770, "res_ued"),
    (9500800, 9500832, "res_chimera_here"),    (9500850, 9500860, "res_surge"),
    (9500900, 9500919, "res_conversion"),      (9501000, 9501999, "res_conversion"),
    (9535010, 9535099, "res_silent_town"),     (9530000, 9535999, "res_exodus"),
    (9570000, 9579999, "res_conversion"),     (9580000, 9589999, "res_chimera_here"),
    (9509800, 9509899, "res_chimera_here"),    (9509900, 9509999, "res_specimens"),     (9510000, 9519999, "res_conversion"),
    (9520000, 9529999, "res_surge"),
    (9502000, 9502999, "res_harvest"),         (9503000, 9503999, "res_silent_town"),
    (9504000, 9504999, "res_hive_heart"),      (9505000, 9505099, "res_tower_rises"),
    (9505100, 9505299, "res_tower_falls"),     (9506000, 9506999, "res_hive_evolves"),
]

def event_picture(eid, default):
    import people, milestones
    # an event that names its own res_ picture uses it once the file exists; otherwise its range picture
    if default.startswith("res_"):
        if people.pic(default, None):
            return default
        default = "news_paper"
    # "The Army of ..." (milestones, ID0 + 10r + 1): the Hybrid army leaving a Dropship
    if milestones.ID0 <= eid < milestones.ID0 + 10 * len(milestones.REGIONS) and eid % 10 == 1:
        return people.pic("res_dropship", default)
    # the Cloven programme's decision and its result: the serum itself
    if eid in (9500420, 9500424):
        return people.pic("res_inhibitor", default)
    for lo, hi, pic in EVENT_PICS:
        if lo <= eid <= hi:
            return people.pic(pic, default)
    return default

def event(eid, name, desc, actions, country=None, trigger=None, date=None, offset=None,
          invention=False, persistent=False, picture="news_paper", decision=None,
          decision_trigger=None, deathdate=None, text_id=None):
    """actions: list of (name, [commands]) or (name, ai_chance, [commands])."""
    tid = text_id or eid          # events can share one set of text keys
    nk = loc(f"EVT_{tid}_NAME", name)
    dk = loc(f"EVT_{tid}_DESC", desc)
    L = ["event = {", f"\tid = {eid}", "\trandom = no"]
    if country: L.append(f"\tcountry = {country}")
    if invention: L.append("\tinvention = yes")
    if persistent: L.append("\tpersistent = yes")
    L.append("")
    for block, cond in (("decision", decision), ("decision_trigger", decision_trigger)):
        if cond is not None:
            L += [f"\t{block} = {{"] + [f"\t\t{t}" for t in cond] + ["\t}"]
    if trigger is not None:
        L += ["\ttrigger = {"] + [f"\t\t{t}" for t in trigger] + ["\t}"]
    else:
        L.append("\t# Triggered by another event")
    L.append("")
    L += [f'\tname = "{nk}"', f'\tdesc = "{dk}"', "\tstyle = 2", f'\tpicture = "{event_picture(eid, picture)}"', ""]
    # DH months have 30 days numbered 0-29: clamp any calendar day 30/31
    if date: date = (min(date[0], 29),) + tuple(date[1:])
    if deathdate: deathdate = (min(deathdate[0], 29),) + tuple(deathdate[1:])
    if date:
        d, m, y = date
        L.append(f"\tdate = {{ day = {d} month = {m} year = {y} }}")
        if offset: L.append(f"\toffset = {offset}")
    if date and not deathdate:
        deathdate = (29, "december", 1963)   # DH requires a deathdate whenever offset is used
    if deathdate:
        d, m, y = deathdate
        L.append(f"\tdeathdate = {{ day = {d} month = {m} year = {y} }}")
    if date or deathdate: L.append("")
    # A 4th tuple element is an action trigger: the option is only shown (and selectable) while it
    # holds (DH dev diary 13). Such events use the plain "action = {" form from the diary's examples.
    gated = any(len(a) == 4 for a in actions)
    for letter, act in zip("abcd", actions):
        if len(act) == 4: aname, ai, cmds, atrig = act
        elif len(act) == 3: (aname, ai, cmds), atrig = act, None
        else: aname, ai, cmds, atrig = act[0], None, act[1], None
        ak = loc(f"ACTION_{tid}_{letter.upper()}", aname)
        L.append("\taction = {" if gated else f"\taction_{letter} = {{")
        if atrig: L.append("\t\ttrigger = { " + " ".join(atrig) + " }")
        L.append(f'\t\tname = "{ak}"')
        if ai is not None: L.append(f"\t\tai_chance = {ai}")
        L += [f"\t\tcommand = {{ {c} }}" for c in cmds]
        L.append("\t}")
    L += ["}", ""]
    return L

def all_ids(cols):
    return [t[0] for _, _, _, techs, _ in cols for t in techs]

def build_events():
    E = ["#########################################################################",
         "#  RESISTANCE MOD - Chimeran technology events",
         "#  9500001-002    unlock Chimeran trees for the Chimera",
         "#  9500003        unlock the Hive Warfare doctrines for the Chimera",
         "#  9500011-025    Chimeran evolution (grants techs on a schedule)",
         "#  95001xx/2xx/3xx unlock the arms/pathology/doctrine trees when a nation fights the Chimera",
         "#########################################################################", ""]
    for col, title in zip(COLUMNS[:2], ["The Hive Stirs", "The Hive Builds"]):
        x, _, ltext, techs, ev = col
        E += event(ev, title,
                   "Beneath the Siberian taiga, the thing that fell at Tunguska has learned to remake living flesh in its own image.",
                   [("The Hive grows", [f"type = activate which = {t[0]}" for t in techs if t[0] != 95010])],
                   country=CHIMERA, date=(1, "january", 1933), offset=1,
                   # not an invention event: those fire for every country, which leaked these trees to the USSR
                   trigger=["technology = 95010", f"NOT = {{ is_tech_active = {techs[1][0]} }}"])
    E += event(9500003, "The Hive Wages War",
               "The Hive does not train its soldiers. It simply knows, and every Hybrid knows with it.",
               [("The Hive commands", [f"type = activate which = {t[0]}" for t in DOCTRINE[1:]])],
               country=CHIMERA, date=(1, "january", 1933), offset=1,
               trigger=["technology = 95010", f"NOT = {{ is_tech_active = {DOCTRINE[1][0]} }}"])
    for eid, tid, date in EVOLUTION:
        tname = EVOLUTION_NAMES.get(tid) or next(t[2] for c in COLUMNS[:2] + [(0, 0, 0, DOCTRINE, 0)] for t in c[3] if t[0] == tid)
        E += event(eid, f"Chimeran Evolution: {tname}",
                   f"The Hive has adapted again. Its forces now benefit from {tname}.",
                   [("The Hive adapts", [f"type = gain_tech which = {tid}"])],
                   country=CHIMERA, date=date, offset=30,
                   trigger=[f"exists = {CHIMERA}", f"NOT = {{ technology = {tid} }}"])
    blurbs = {
        9500101: ("Chimeran Weapons Recovered", "Our troops have recovered strange weapons from the battlefield. Engineers believe they can be studied and copied."),
        9500201: ("Chimeran Specimens Recovered", "Bodies recovered from the front show a virus that rewrites living tissue. Our doctors must learn how it spreads, or we will all be consumed."),
        9500301: ("Lessons from the Front", "Our officers are compiling hard lessons about how the creatures fight. The old manuals are useless against this enemy."),
    }
    for x, _, ltext, techs, base in COLUMNS[2:]:
        title, desc = blurbs[base]
        for n, tag in enumerate(HUMAN_NATIONS):
            E += event(base + n, title, desc,
                       [("Begin the programme", [f"type = activate which = {t[0]}" for t in techs])],
                       country=tag, date=(1, "january", 1933), offset=3,
                       trigger=[f"war = {{ country = {tag} country = {CHIMERA} }}",
                                f"NOT = {{ is_tech_active = {techs[0][0]} }}"])
    return E

def copy_assets():
    """Art made for the mod (flags, unit pictures) lives in SRC/assets and is copied as-is."""
    import shutil
    a = os.path.join(SRC, "assets")
    if os.path.isdir(a):
        shutil.copytree(a, OUT, dirs_exist_ok=True)

def main():
    sw = open(os.path.join(SRC, "secret_weapons_tech.txt"), encoding="latin-1").read().replace("\r\n", "\n")
    cut = sw.rstrip().rfind("}")          # closing brace of the technology block
    band = "\n".join(build_tech_band())
    write("db/tech/secret_weapons_tech.txt", (sw[:cut].rstrip() + "\n" + band + "\n}\n").split("\n"))

    write("db/tech/land_doctrines_tech.txt", insert_band(os.path.join(SRC, "land_doctrines_tech.txt"), build_doctrine_band(), MOVED_TECHS))
    write("db/events/res_chimeran_tech.txt", build_events())

    # country.csv: give the spare tag a dark colour and its own map sprites (column 4, Army Nationality Sprite:
    # gfx/map/units/T-<type> ... C-UA0 ...). Columns 5-7 (model nationality) must stay empty: filling them crashed v47.
    rows = open(os.path.join(SRC, "country.csv"), encoding="latin-1").read().replace("\r\n", "\n").rstrip("\n").split("\n")
    rows = [f"{CHIMERA};Black;SOV;{CHIMERA};;;;X" if r.startswith(CHIMERA + ";") else r for r in rows]
    import cordon      # the buffer states east of the Yenisei use Soviet sprites and models
    tag_of = lambda r: r.split(";", 1)[0]
    rows = [f"{tag_of(r)};{cordon.COLOURS[tag_of(r)]};SOV;SOV;;;;X" if tag_of(r) in cordon.COLOURS else r
            for r in rows]
    write("config/country.csv", rows)
    write("db/country.csv", rows)        # DH reads map colours from db/country.csv


def write_text():
    import people
    people.scan_assets(SRC)
    loc(CHIMERA, "Chimera")
    # model names belong in models.csv (your de-duplicated copy, with the Chimera rows added)
    write("config/models.csv", people.insert_rows(os.path.join(SRC, "models.csv"), people.model_names(CHIMERA)))
    write("config/mods.csv", people.mods_csv(os.path.join(SRC, "mods.csv"), text))
    import units
    units.build(sys.modules[__name__])
    tn = os.path.join(SRC, "tech_names.csv")
    if os.path.exists(tn):   # tech screen text is read from tech_names.csv, not mods.csv
        rows = people.insert_rows(tn, {k: v for k, v in text.items() if k.startswith(("TECH_", "SHORT_TECH_"))})
        # research component rt_user_1 becomes Chimeran Biology (only Sorokin's team has it among the humans)
        rows = [("RT_USER_1;" + ";".join(["Chimeran Biology"] * 8) + ";;;X") if r.startswith("RT_USER_1;") else r for r in rows]
        write("config/tech_names.csv", rows)
    un = os.path.join(SRC, "unit_names.csv")
    if os.path.exists(un):   # generic model names: without them other countries see STRING_WANTED
        write("config/unit_names.csv", people.insert_rows(un, units.generic_names()))
    for kind in people.HIVE_NAMES:
        write(f"db/{kind}.csv", people.names_csv(os.path.join(SRC, f"{kind}.csv"), kind, CHIMERA))
    write("db/ministers/ministers_UA0.csv", people.ministers_csv())
    write("db/leaders/chimera.csv", people.leaders_csv())
    import cordon
    write("db/leaders/cordon.csv", cordon.leaders_csv())
    write("db/leaders.txt", people.append_list(os.path.join(SRC, "leaders.txt"), "chimera.csv") + ["cordon.csv"])
    for t in (cordon.UA1, cordon.UA2):
        write(f"db/ministers/ministers_{t}.csv", cordon.ministers_csv(t))
    write("db/tech/teams/teams_UA0.csv", people.teams_csv())
    write("db/tech/teams/teams_SOV_res.csv", people.sov_teams_csv())
    teams = people.append_list(os.path.join(SRC, "teams.txt"), "teams_UA0.csv")
    import refugees
    extra = ["teams_SOV_res.csv"]
    for fn, rows in refugees.team_csvs().items():
        write(f"db/tech/teams/{fn}", rows)
        extra.append(fn)
    write("db/teams.txt", teams[:-1] + extra + teams[-1:] if teams[-1].startswith("#") else teams + extra)
    write("db/ministers.txt", people.append_list(os.path.join(SRC, "ministers.txt"), "ministers_UA0.csv")
          + ["ministers_UA1.csv", "ministers_UA2.csv", "ministers_SOV_res.csv"])
    print(f"techs: {len(all_ids(COLUMNS))}  loc keys: {len(text)}")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import story, people
people.scan_assets(SRC)
main()
copy_assets()
story.build(sys.modules[__name__])
write_text()

# build checks: refuse to finish a build that contains a mistake we have already shipped once
import validate
errs, warns, n = validate.run(OUT)
print(f"validate: {n} events checked, {len(errs)} errors, {len(warns)} warnings")
for w in warns: print("  warning", w)
if errs:
    for e in errs: print("  ERROR  ", e)
    sys.exit("build failed validation")
