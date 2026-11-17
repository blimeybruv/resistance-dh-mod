# Resistance mod: art the mod needs

Until art arrives, the mod uses existing DH pictures (`news_paper` for events and borrowed tech and team pictures). Once a file exists, I switch the mod over to its name. The names below are suggestions; use any names you like and tell me.

## Format rules (from your savedebug.txt)

- **24-bit BMP only.** DH rejects 32-bit BMPs with "Unsupported image bit count (32)". Most image generators and editors save 32-bit with alpha by default, so export as 24-bit.
- **Size:** match an existing vanilla file of the same kind exactly. Open any vanilla file in the folder below and copy its pixel size.
- Some DH graphics use a magenta or black background as transparency. Check a vanilla example of each type.

## Priority 1: identity

Done: flags and shields for `UA1` (Siberian Cordon Administration) and `UA2` (Far Eastern Republic), drawn by `build/flags.py`.


Done: the Chimera flag and shield (option 1: navy and amber with the Spire), in `gfx/map/flags/flag_ua0.bmp` and `gfx/map/shields/shield_ua0.bmp`.


| What | File | Folder (check against vanilla) | Notes |
|---|---|---|---|
| Minister portraits | done (v25), see Priority 5 | `gfx/interface/pics/` | |
| Leader portraits | 5, one per clone tier | `gfx/interface/pics/` | The Overmind, Hive Node, Swarm Node (land), Spire Node (air), Deep Node (sea). |

## Priority 2: event pictures (most visible to players)

One picture can serve several events. Suggested names and subjects:

| Picture name | Used by | Subject |
|---|---|---|
| `res_closed_zone` | The Closed Zone, The Expedition Has Not Returned | Snowy taiga, NKVD checkpoint, barbed wire, warning signs |
| `res_falls_silent` | the four "Falls Silent" events | Empty Siberian village, black tower in the forest |
| `res_hive_heart` | The Hive Heart, conversions, surges | Chimeran conversion chambers / tower interior |
| `res_outbreak` | The Outbreak, Krasnoyarsk Falls Silent | Swarm of creatures pouring out of a forest at night |
| `res_soviet_decision` | the four Soviet decisions | Soviet officers over a map; Volga fortifications |
| `res_foreign_news` | Refugees on the Amur, Abwehr Reports, The Siberian Question, Strange News from Russia, The Fall of Russia | 1930s newspaper front page about Siberia |
| `res_fall_of_moscow` | Moscow in Peril, The Fall of Moscow, The Soviet Union Is No More | The Kremlin under a dark sky, towers on the horizon |
| `res_breakout` | the seven breakout stages | Creatures advancing across a European plain |
| `res_armistice` | Armistice in the West, Berlin Offers an Armistice | Officers from both sides shaking hands in a railway carriage |
| `res_chimera_here` | The Chimera Are Here (33 nations) | Soldiers and civilians mobilising, recruitment poster |
| `res_research` | the captured-tech unlock events | Scientists dissecting a creature, lab with captured weapons |

## Priority 3: tech pictures

**Style (v104):** every tech picture is laid into DH's own tech template: monochrome print, aged paper, torn edge, paperclip. Send the plain picture at any size; the build does the rest. It works best when the picture is mid-toned and evenly lit, like a 1930s press photo or engraving, rather than a dark night scene. Machine techs can instead be blueprints, which keep their blue.

**Official art in use (replace before a public release):** 95230 Deployable Shield Studies (the Resistance 3 shield drone notebook page); 95110 Bio-mechanical Engineering (the Longlegs leg notebook page). Found art, source not recorded: 95010, 95030, 95140 and 95310 (the four Chimeran virus dossier pages); check who made them before any release.

**Done (v70):** all 23 techs of the Strains, Chimeran Engineering, Captured Chimeran Arms, Chimeran Pathology and Anti-Chimeran Warfare columns, as `gfx/interface/tech/<id>.bmp` (344x266, 24-bit). A tech switches to its own picture as soon as `<id>.bmp` exists.

**Done (v86):** the 10 Hive Warfare and remaining Engineering techs (95170, 95180, 95510–95580). Every tech in the mod now has its own picture.

All remixes requested in v86 are done (v87 to v90).

## Priority 4: unit model pictures

Your infantry set shows the pattern to follow. Each model gets two 24-bit BMPs, in both a Chimera-only and a generic version (the generic one is the fallback for anyone else who obtains the model, for example a Cloven USSR):

- **Icon:** 67x44, with the year in the corner. Files: `UA0_model_<type>_<model>.bmp` and `model_<type>_<model>.bmp`.
- **Illustration:** 192x104. Files: `ill_div_UA0_<type>_<model>.bmp` and `ill_div_<type>_<model>.bmp`.

For brigades and aircraft, copy the size and naming of a vanilla file of the same kind. The type numbers below come from `models.csv`. The super-heavy armour unit file says 35 in its header, but `models.csv` uses 9, so check a vanilla super-heavy picture's file name before naming.

### Done (in the mod)

| Unit | Type / model | Year | Notes |
|---|---|---|---|
| Hybrid Swarm | infantry 0 / 18 | 1933 | replaced in v76: varied-poses remix (crouch, stride, kneel), heat-sink packs, dead forest |
| Advanced Hybrid Swarm | infantry 0 / 19 | 1942 | armoured; replaced in v74 by the six-eyed remix (cylindrical towers, onion-dome ruins) |
| Steelhead Swarm | infantry 0 / 20 | 1950 | replaced in v76: armoured domes, eyes set in, ribbed canisters, snowy ruined city |

### Done in art batch 2 (v69)

Leaper Swarm I and II (cavalry 1 / 15–16), Angel Nexus (HQ 10 / 6), Chimeran Fighter I and II (interceptor 13 / 17–18), Dropship 'Buzzard' (CAS 17 / 7, replaced in v82 by the strafing-run picture), Chimeran Battleship (strategic bomber 14 / 10). Brigades: Stalkers and Goliaths (super-heavy 9 / 2–3), Titans (heavy 8 / 6, replaced in v79 by the arm-cannon Titan), Widowmakers (medium 29 / 11), Spire Launcher Battery (artillery 1 / 14, replaced in v81), AA Turrets (anti-air 11 / 7). Each has the UA0 and the generic version.

The batch drew the Angel Nexus as HQ 0–5. In the mod it is HQ model **6**, so its files were installed as `10_6`. HQ 0–5 are the human headquarters, and generic files for them would replace every country's HQ pictures.

**Done (v72):** Thrall Horde (militia 11 / 10), made from your first Grok picture with the batch 2 frame, bars and year layout.

**Done (v73, v77):** the Cloven. Cloven I (model 18) is the uniformed red-star squad. Cloven II (19) is the half-feral shirtless squad (v77). Cloven III (20) is the ragged mixed squad (v78). Originally: (the USSR's infantry models 18–20, Cloven Rifle Division I–III), as Soviet-only pictures (`ill_div_SOV_0_<m>`, `SOV_model_0_<m>`). They show for the USSR in place of the generic Hybrid pictures.

### Units still needed

None: since v76 every Chimeran unit has its own picture. The Hunter Dropship (naval bomber 16 / 9) came last.

### Not in the mod yet (art could come first)

| Unit | Notes |
|---|---|
| Hybrid Gen IV (around 1955) | An optional fourth step in the infantry chain. Canon's later military Chimera include Ravagers, Brawlers and Longlegs, which would mainly matter for the 1951 scenario. |
| Feral Chimera and the Cloven | For the planned third faction in the 1951 scenario: Grims, feral Leapers and Cloven cannibals in gas masks. |

## Priority 4b: map sprites

**Done (v67):** the Hybrid infantry sprite (stand, walk and fire, 8 directions) in `gfx/map/units`, at levels L-1 to L-4. The UA0 row of `db/country.csv` now uses UA0 as its sprite nationality.

**Still needed, if other Chimeran units show no counter on the map:** sprites for militia (Thralls), cavalry (Leapers), HQ (Angel Nexus) and the armour and air units. Until then, I can make UA0 copies of the Soviet `.spr` files that point at the Soviet bitmaps. The `.spr` names follow `T-<TYPE> A-<WALK|FIRE|STAND> C-UA0 L-<n> [D-<dir>].spr`.

## Priority 5: portraits (ministers, leaders, research teams)

Name each file exactly as in the **File** column, as a 24-bit BMP. For the size, copy any vanilla minister, leader or team picture, and send me the files: I'll put them where DH looks for that kind of picture. The generator uses a portrait as soon as the file exists, and keeps the placeholder until then. So you can send them one at a time, and nothing breaks if some are missing.

The Hive has no individuals, so these are portraits of functions and organs rather than faces. A consistent frame helps them read as a set: a dark background, the subject lit from below in amber, and the same crop for each.

### Ministers: done (v25)

All ten are in the mod, in `gfx/interface/pics/`. They are 36x50 with a 1px white frame. Leaders use the same folder and size. Research teams use the same folder but are larger: 96x96 with a 1px white frame (fixed in v103).

### Minister list

| File | Post | Name | Suggested picture |
|---|---|---|---|
| M1500001 | Head of State | The Hive | The Tunguska tower seen from below, its peak glowing |
| M1500002 | Head of Government | The Hive Mind | An Angel: pale, eyeless head and floating body, the psychic leader caste |
| M1500003 | Foreign Minister | The Silence | Checkpoint 14 abandoned in snow, the phone hanging off the hook (ties to the prelude) |
| M1500004 | Minister of Armament | Conversion Chambers | A conversion cocoon with a human shape still visible inside |
| M1500005 | Minister of Security | The Choir | A row of Hybrids standing perfectly still, heads tilted the same way |
| M1500006 | Head of Military Intelligence | The Watchers | Six amber eyes in darkness, nothing else |
| M1500007 | Chief of Staff | The Overmind | The inside of a tower: a glowing core with cabling running into it |
| M1500008 | Chief of Army | Swarm Coordinator | A Steelhead or armoured Hybrid at the head of a column |
| M1500009 | Chief of Navy | Deep Spawn | A large shape under Arctic ice, lit faintly from beneath |
| M1500010 | Chief of Air Force | Spire Coordinator | A cluster of Spires in flight, or a dropship against the sky |

### Leaders and research teams: done (v87)

### Leaders (generals, shown in unit and leader lists)

| File | Name | Type |
|---|---|---|
| L1500101 | The Overmind (8 clones, field marshals) | land |
| L1500109 | Hive Node (16 clones, generals) | land |
| L1500125 | Swarm Node (24 clones, lieutenant generals) | land |
| L1500149 | Spire Node (4 clones) | air |
| L1500153 | Deep Node | navy |

The generals are clones, so each tier shares one portrait: five pictures in all.

### Research teams (optional: they currently borrow vanilla pictures)

| File | Team | Suggested picture |
|---|---|---|
| T1500201 | Conversion Chambers | conversion pods in rows |
| T1500202 | Tunguska Core | the crash site or a glowing crystal core |
| T1500203 | Bio-Engineering Spawn | half-grown creature in a growth sac |
| T1500204 | Swarm Instinct | Leapers flowing over a ridge |
| T1500205 | Tower Builders | a tower half built, scaffolded with organic ribbing |
| T1500251 | Sorokin Laboratory (USSR; also used by Britain's Sorokin Group) | a Tomsk laboratory, specimen jars, a pathologist at a microscope |
| T1500261 | Russian Emigre Institute (UK, refugees) | émigré scientists in a borrowed Cambridge lab |
| T1500262 | Kharkov Physics Circle (USA, refugees) | blackboards of equations, a cyclotron |
| T1500263 | Harbin Medical Mission (Japan, refugees) | a field hospital in Harbin |
| T1500264 | Odessa Naturalists (South Africa, refugees) | naturalists with specimen cases on a Cape Town quay |

## Priority 6: event pictures

Added (v98): `res_menials` for The Hive Harvest and The Hive Builds. Done (v100): `res_exodus`. Done (v102): `res_exodus_sea` for the 58 ship events.

Every event in the mod currently uses the vanilla newspaper picture. Each event now has a picture name reserved, as in the tables below. To add one, save a 24-bit BMP with that name and send it to me. The mod's events use `style = 2` (newspaper header), so pictures are 400x116, with the green frame used in your first batch.

Done (v27): res_conversion, res_silent_town, res_salvage, res_specimens, res_tower_falls, res_chimera_here, res_surge, res_tower_rises. The generator switches an event to its picture as soon as the file exists, and keeps the newspaper until then. One picture covers every event in its group.

### Events already in the mod, in the order a Soviet player sees them most

| Picture | Events | Count | Suggested picture |
|---|---|---|---|
| res_conversion | Infection behind the lines, city conversions | 316 | conversion cocoons in a town street, a Hybrid standing over them |
| res_silent_town | Towns falling silent, Dead Zones | 286 | empty frozen town, doors open, telegraph wires down |
| res_salvage | Chimeran weapons recovered, lessons from the front | 86 | Soviet engineers around a captured Chimeran rifle on a workbench |
| res_specimens | Chimeran specimens recovered | 43 | a dissected Hybrid on a lab table under lamps |
| res_tower_falls | A tower falls, an Angel dies, Soviet victory | 34 | a tower collapsing in smoke, Red Army soldiers in the foreground |
| res_chimera_here | The Chimera reach a new country | 33 | a European village at dusk, figures in the fog beyond the church |
| res_surge | The Hive surges, breakout stages | 25 | a swarm of Hybrids and Leapers pouring across snow |
| res_tower_rises | A tower rises | 15 | a tower rising over a captured Soviet city |
| res_fall_of_moscow | Moscow in peril, the fall of the Soviet Union and Russia | 8 | the Kremlin under a red-black sky, a tower behind it |
| res_cloven | The Cloven programme | 4 | Red Army soldiers in gas masks, eyes glowing behind the lenses |
| res_armistice | Germany and the eastern horror, Berlin's armistice | 4 | German and Soviet officers at a field table, both looking east |
| res_foreign_aid | Appeals to the world, aid from Britain and America | 5 | crates and lorries being unloaded at Murmansk docks |
| res_quarantine_line | The Ural and Volga lines | 2 | soldiers digging trenches in snow, barbed wire, searchlights |
| res_lost_expedition | The lost expedition, the Academy expedition | 3 | an abandoned camp in the taiga, tents torn, sledges overturned |
| res_closed_zone | The OGPU file, the Krasnoyarsk secretary | 2 | a stamped secret file on a desk, a map of Siberia with a red circle |
| res_exodus | The Evenki exodus, refugees on the Amur | 2 | reindeer herders and sledges fleeing across the tundra |
| res_checkpoint | Checkpoint 14 | 1 | the same hut as The Silence's portrait, from further away |
| res_early_winter | Winter comes early | 1 | a frozen village in a blizzard in October |
| res_outbreak | The Outbreak at Krasnoyarsk | 1 | Krasnoyarsk burning at night, shapes in the streets |
| res_evacuation | Evacuate Siberian industry | 1 | factory machinery on flatcars, a train heading west |
| res_scorched_earth | Scorched earth in Siberia | 1 | a village set alight by retreating troops |
| res_ued | The United European Defence | 1 | European flags around a conference table, a map of Russia |
| res_hive_stirs | The Hive stirs, builds, wages war | 3 | the Tunguska crater glowing at night |
| res_hive_evolves | Chimeran evolution, the Hive learns | 69 | growth vats, half-formed creatures (seen by Chimera players only) |
| res_hive_heart | Hive Heart, the Hive moves, the Hive builds | 287 | the inside of the Hive: ribbed organic halls, amber light (seen by Chimera players only) |
| res_dropship | The Army of … (Processing armies), done v82 | 26 | Hybrids pouring out of a landed Dropship |
| res_harvest | The monthly Hive Harvest | 369 | land being stripped by Chimeran machines (seen by Chimera players only) |
| res_exodus | Refugee corridors: transit, receivers, camps, closings (v60) | about 180 | refugee columns on a railway line, a crowded quayside |
| res_foreign_aid | Don alert ("Word from London"), "The Russian Papers" (v60) | about 30 | a dossier stamped PORTON DOWN, a map of the Don |

Since v60 several new groups reuse pictures that already exist: Processing armies use `res_conversion`, Thrall and Burrower events use `res_surge` and `res_chimera_here`, and Dead Zones use `res_silent_town`. A dedicated picture for any of them is optional.

The three foreign intelligence reports (Abwehr, the Siberian Question, Strange News from Russia) keep the newspaper, which suits them.

### Events still to be written: pictures done (v83)

All seven are in `gfx/events_pics` as framed banners, ready for when the events are written.

| Picture | For | Status |
|---|---|---|
| res_peace | The peace path: Europe unites against the east | done (remix v84) |
| res_channel | The Hive reaches the Channel; the invasion of Britain (1951) | done (redo v85: three Dropships over the sea towards the cliffs, container slung beneath. They read a little like jets, with tailfins and rear exhaust. An optional touch-up would be "remove the tailfins and the rear engine flames; lift comes from four amber booster ports underneath".) |
| res_morning_star | Operation Morning Star (1951) | done; optional remix without the 1944 invasion stripes |
| res_angel | Angel sightings, psychic events | done: the winged figure stays, as a psychic projection seen by humans (the real Angel is the spiked, many-limbed creature) |
| res_inhibitor | Inhibitor serum breakthroughs | done; already used by the Cloven programme events |
| res_feral | Feral Chimera and Grims | done |
| res_london_tower | A tower in London (1951) | done |

## Interface skin: done (v27)

The Chimera skin is in `gfx/SKINS/UA0/` (sidebar, top bar, full-screen panels). Only a player playing the Chimera sees it.

## Priority 7: buffer-state ministers (generic Russian portraits): done (v91)

These are fictional officials, so generic period faces suit them best: men in 1930s Soviet tunics, or suits for the civilians. As with the Hive, the mod uses a portrait as soon as a file with its name exists. The size is 36x50, like your Chimera ministers.

| Siberian Cordon Administration | File | Far Eastern Republic | File |
|---|---|---|---|
| Pavel Dorokhov (Head of State) | M1500301 | Aleksandr Varnavin (Head of State, old partisan) | M1500321 |
| Ivan Sedykh | M1500302 | Boris Lisitsyn (former general) | M1500322 |
| Arkady Lamin | M1500303 | Konstantin Ushakov | M1500323 |
| Grigory Shcherbak | M1500304 | Lev Pankratov | M1500324 |
| Viktor Bulatov (security, NKVD) | M1500305 | Dmitri Zolotov | M1500325 |
| Semyon Ryabov | M1500306 | Andrei Melnikov | M1500326 |
| Nikolai Ostapenko | M1500307 | Vasily Gorelov | M1500327 |
| Fyodor Kazantsev | M1500308 | Timofei Kuzmin | M1500328 |
| Yakov Belousov | M1500309 | Ilya Starostin | M1500329 |
| Mikhail Trusov | M1500310 | Oleg Ponomarev | M1500330 |

## About AI-generated and derived art

For your own copy, anything goes. If you release the mod publicly, Resistance's art and screenshots belong to Sony / Insomniac. Art copied from or trained on them (including a LoRA trained on official art) is more likely to cause takedown trouble than original art made in a similar 1950s alt-history style. Fan mods usually get away with it, but original art is the safer route for a public release.
