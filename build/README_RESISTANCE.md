# Resistance: Darkest Hour Full 1.05 mod

Modules 1 (Chimeran technology), 2 (the Chimera country and the Siberian outbreak) and 3 (the Soviet collapse and the breakout into Europe).

## Files

| File | What it does |
|---|---|
| `scenarios/resistance_1933.eug` | A new scenario, "Resistance: The Fall of Europe (1933)". It's a copy of the 1933 Grand Campaign with the Chimera added. The vanilla 1933 scenario is untouched. |
| `scenarios/resistance_1933/chimera.inc` | The Chimera (`UA0`). They start in Norilsk (province 1155) with a full cabinet and 6 broods: 30 Hybrid swarms (infantry) and 12 thrall divisions (militia). |
| `scenarios/resistance_1933/soviet union.inc` | The vanilla Soviet file, except that the USSR no longer owns or controls 1155. It stays a Soviet core. |
| `db/events/res_1933_outbreak.txt` | 50 story events and decisions (listed below). |
| `db/events/res_breakout.txt` | 81 events: the Soviet collapse, the seven breakout stages, the WWII interplay, nations attacked by the Hive, late Hive surges and city conversions. |
| `db/events/USSR.txt` | The vanilla Soviet events with one change: the two "Transfer of Industry to Siberia" decisions (2007042, 2007043) are blocked while the USSR is at war with the Chimera, so factories don't get moved into Hive territory. Other scenarios are unaffected because UA0 never exists in them. |
| `db/events/res_chimeran_tech.txt` | 90 events that unlock the tech trees and grant the Chimera's evolution techs on schedule. |
| `db/tech/secret_weapons_tech.txt` | The vanilla file plus the 21 Chimeran and anti-Chimeran techs. |
| `db/ministers/ministers_UA0.csv` + `db/ministers.txt` | The Hive's cabinet. All ten posts are functions of the Hive rather than people. IDs 1500001–010. `ministers.txt` is your list (rebuilt from `savedebug.txt`) with `ministers_UA0.csv` added. If you'd rather keep your own file, just add that one line to the end of it. |
| `db/leaders/chimera.csv` + `db/leaders.txt` | 10 Hive Node commanders (8 land, 1 air, 1 naval). IDs 1500101–110. `leaders.txt` is your list with `chimera.csv` added at the end. |
| `db/tech/teams/teams_UA0.csv` + `db/teams.txt` | 5 research teams, such as the Conversion Chambers and the Tunguska Core. IDs 1500201–205. `teams.txt` is your list with `teams_UA0.csv` added. |
| `ai/chimera.ai` | The Chimera's AI, built from DH Full's `minor_default.ai`: it attacks at poor odds, rarely withdraws, keeps almost no garrisons, builds factories at war, and builds 70% Hybrids and 30% thralls with artillery and Stalker brigades. Its research favours the Chimeran techs. |
| `ai/switch/*.ai` | Partial AI files that events load as the story advances, like vanilla's `ai/switch` files. The Chimera retarget from Siberia to the Urals, then European Russia, Central Europe and Western Europe. The Soviet AI switches to defending the Urals, then the Volga. |
| `config/mods.csv` | Your vanilla `mods.csv` with all the mod's English text added before `#EOF`, including the country name "Chimera". DH loads this file last, so it's the right place for mod text. |
| `db/unitnames.csv`, `armynames.csv`, `airnames.csv`, `navynames.csv` | Vanilla names lists with the Chimera's names added at the end (see v11). |
| `db/units/divisions/*.txt`, `db/units/brigades/*.txt` | Vanilla unit files with the Chimeran models appended (see v15, v16, v20 and v21). |
| `db/tech/land_doctrines_tech.txt` | Vanilla land doctrines with the Hive Warfare line added (see v21). |
| `config/country.csv` | `UA0` set to black, with Soviet sprites. |
| `gen.py`, `story.py`, `people.py`, `breakout.py`, `ai.py`, `units.py`, `adjacency.json` | Rebuild everything from the vanilla files: `python gen.py <vanilla_src> <out>`. Edit the tables in these scripts rather than the output. |

The scenario loads both event files itself, so `db/events.txt` doesn't need editing.

IDs 1500001–1505000 are reserved for the Chimera. Your ID spreadsheet shows no tag using them.

## Timeline (war path: vanilla WWII events run as normal)

| Date | Event |
|---|---|
| Start | **The Hive Heart.** The Chimera get factories (IC) and infrastructure in Norilsk. A Soviet–Chimera non-aggression pact runs until January 1937, so the Soviet AI doesn't attack early. |
| Start + 2 days | **The Closed Zone**, then the 1933–34 prelude chain (see v22). Either choice in The Closed Zone unlocks the USSR's Pathology column early. |
| Aug 1934 – Jun 1936 | **Settlements fall silent:** Ust-Kut, Bratsk, Nyurba, Bodaybo. Each one borders land the Chimera already hold. Choose: (a) extend the cordon, or (b) send the Red Army in, which costs manpower and dissent but gives pathology research. The province goes to the Chimera either way, and they gain manpower and IC. |
| Feb 1937 | **The Outbreak.** The Chimera declare war, Krasnoyarsk falls, and the USSR chooses between declaring the Siberian Emergency (+200 manpower, +5 dissent) and hiding the truth. Japan, Germany, Britain and the USA each get a reaction event. |
| From Feb 1937 | **Soviet decisions:** the Ural Quarantine Line (forts), Evacuate Siberian Industry (factories move west of the Volga), Scorched Earth (destroy infrastructure in the Hive's path) and Appeal to the World (Britain and the USA can send aid). Appeal to the World isn't available if the USSR chose to hide the truth. |
| June 1938–41 | **Hive surges:** manpower and IC for the Chimera every June. |
| Novosibirsk/Omsk fall | **The Hive Looks West.** The Chimera AI retargets to the Urals. |
| Sverdlovsk/Chelyabinsk fall | **Beyond the Urals.** The Chimera AI retargets to the Volga and Moscow. |
| Urals fall | **The Urals Have Fallen** (Sverdlovsk or Chelyabinsk). This unlocks the **Volga Line** decision: forts at Kazan, Kuybyshev, Saratov, Stalingrad, Gorky and Yaroslavl. |
| Volga crossed | **Moscow in Peril.** Stalin stays, or the government moves to Leningrad. |
| Moscow falls | **The Fall of Moscow.** Fight on from Leningrad, or scatter as partisans. Germany gets **The Eastern Horror**: build the Ostwall (forts on its eastern border) or strike Russia while it bleeds. |
| Moscow and Leningrad fall | **The Soviet Union Is No More.** Britain, France, Germany and the USA each get a "Fall of Russia" event. |
| Breakout stages | Each stage fires when the Hive takes one of its trigger cities and declares war on everyone in the next ring: **East** (Irkutsk/Chita: Mongolia, Tuva, Manchukuo); **South** (Tashkent/Alma-Ata/Ashkhabad: Persia, Afghanistan, Xinjiang); **Caucasus** (Baku/Tbilisi: Turkey, Persia); **Borderlands** (Moscow/Leningrad/Minsk/Kiev: Finland, the Baltic states, Poland, Romania and any German Reichskommissariats); **Heart of Europe** (Warsaw/Bucharest: Germany, Hungary, Czechoslovakia, Austria, Yugoslavia, Bulgaria, Scandinavia); **The West** (Berlin/Vienna/Prague: France, Vichy, Free France, the Low Countries, Switzerland, Italy, Greece, Albania); **The Channel** (Paris or a Channel/Low Countries port: Britain, Ireland, Portugal, Spain). |
| WWII interplay | If Germany is fighting both the Hive and Britain or France, it can offer an **armistice in the West**. Britain and France each decide whether to make peace. |
| Under attack | Every nation the Hive attacks gets **The Chimera Are Here**: +50 manpower, +2 dissent, defence lobby +1. |
| 1942–52 | **Late Hive surges:** 300 to 800 manpower each June. |
| Any time | **City conversions:** manpower bonus when the Chimera take Krasnoyarsk, Novosibirsk, Tomsk, Omsk, Irkutsk, Ulan-Ude, Sverdlovsk, Chelyabinsk, Ufa or Nizhny Tagil (+50 manpower), or 20 major Russian and European cities from Moscow to Paris (+100 manpower). |

## Things to check in game

- **Province IDs** come from `DH_Province_List.pdf`, which matches DH Full's Soviet file. The `Province.csv` you sent numbers provinces differently, so don't copy it into the mod.
- **Ground zero** is Norilsk (1155). If the Tunguska river is in a different province on your map, change `GROUND_ZERO` in `story.py`.
- **Confirmed** from your files: `gain_tech`, `secedeprovince`, `war = {}`, decisions, `construct which = ic/infrastructure`, and the column layouts of `mods.csv`, the ministers, leaders and teams files.
- **Not confirmed:**
  - `construct which = land_fort` (Ural Quarantine Line)
  - `soft_attack` (tech effects)
- **Minister ideology.** The ministers use ideology `FA`, copied from the U99 template, which has the Hive running as an authoritarian state.
- **Text check.** The generator rejects any text that contains characters `mods.csv` forbids (`#`, `;`, `%`, double quotes, backslash).
- **Flag.** The Chimera flag and shield ship with the mod (v23).
- **Debugging.** If something misbehaves, set extra debug logs to level 2 in `settings.cfg`. DH then writes errors to `savedebug.txt`, which you can send me.

## Balance knobs (first pass, expect to tune after playtesting)

The constants at the top of `story.py` (`HIVE_ARMIES`, `SWARMS_PER_ARMY`, `THRALLS_PER_ARMY`, `HIVE_HEART_IC`) set the starting Hive. The manpower numbers live in the event tables in `story.py` and `breakout.py`. The 1933 Soviet army is huge, so the Hive starts with 42 divisions and 20 IC. Whether the AI uses them aggressively depends on its AI file. Since v7 the Chimera use their own `ai/chimera.ai`.

## Changes in v126

**The Fall of Europe arc** (new `fall_of_europe.py`, `db/events/res_fall_of_europe.txt`, ids 9590000+, 102 events).

- **Vanilla flavour.** DH Full's armistice/Vichy chain only fires when Germany or Italy holds Paris, and the British surrender chain only when Britain is at war with GER/SOV/JAP/ITA. So neither fires against the Hive. The Paris event still sleeps 17 Vichy/Free France events, and the Channel Front sleeps the 4 British surrender events, in case Germany survives and takes Paris back.
- **Act 1, France.**
  - *Paris Is Silent* (FRA): the capital moves to Algiers; +40 manpower, +8 dissent.
  - *France Fights On* (ENG): alliance with France.
  - *L'Appel d'Alger* (FRA): +60 colonial manpower, -5 dissent.
  - *The Fleet Sails for Mers-el-Kebir* (FRA): keep the fleet in Africa, or send it to Portsmouth (+20 British escorts).
  - *The Little Ships* (ENG): the Dunkirk evacuation, when the Hive breaks through in Flanders.
- **Act 2, the Channel Front.** Fires on the existing "The Channel" stage (9500756), which now also switches the Hive AI to the Channel coast (`switch/UA0_channel.ai`).
  - Coastal forts at Dover, Portsmouth, Norwich, Hull and Plymouth.
  - Operation Pied Piper.
  - With Sea Hunters (95170): *Hunters over Scapa Flow*, where the naval base is damaged and the fleet moves to Rosyth or stands and fights, and *Hunters in the Channel*, which costs convoys or supplies.
  - With Spire Launchers (95140) and Calais or Dunkirk held: the Calais batteries can reach Dover.
- **Act 3, the invasion.**
  - **Dropships** (scripted, no AI or transports needed). With Dropships (95150), the Hive drops broods at Dover (from the Pas de Calais), Portsmouth (from Normandy) and Norwich (from Holland). Each drop has a second wave 45 days later; the second wave also reinforces a foothold already taken. Each wave costs 30 manpower.
  - **The Home Guard.** Britain answers each drop by ringing the bells, which wakes **vanilla DH Full's own Home Guard**: 18 dormant garrison-plus-artillery divisions already in the UK 1933 file, which no uploaded event wakes. Six are woken around each landing.
  - **A Foothold in England.** The Hive switches to `switch/UA0_britain.ai`, with London the top target. Britain gets *We shall fight on the beaches*.
  - **Spire batteries.** Every British province the Hive takes (with 95140) gets a *Spire Battery of X* division: a Hybrid Brood carrying a Spire Launcher brigade. DH has no event command that adds a brigade to an existing division, so the battery arrives as a new unit in the captured province.
  - **Spire strikes.** Every British-held province next to a foothold is shelled, as is Dover from Calais. A strike costs a land fort, an AA level and manpower and adds dissent; London is hit harder. 30 days later *The Barrage Goes On* hits again if the town still stands. 24 provinces are covered.
- **Act 4.**
  - *London Burns*: the government moves north to Edinburgh, Glasgow, Belfast, Inverness or Aberdeen, whichever is still held.
  - *The Crown Comes to Ottawa* (CAN): +80 manpower and money.
  - *London Has Fallen* (USA).
  - 60 days later, *A Tower over London* (UA0, res_london_tower), with two locked guard divisions.
- **Pictures.** Dropship events use res_channel. New picture names fall back to news_paper until the art exists: `res_paris_falls`, `res_little_ships`, `res_scapa`, `res_spire_strike`, `res_london_burns`.

## Changes in v125

- **Hybrid sprite switched to variant H** (the Resistance 3 look): warm tan skin, a red sash at the waist, legs armoured in reddish-brown plate with lighter knee pads and shin guards, and bare clawed feet. G (gunmetal Advanced Hybrid armour) stays in the script as an alternative.

## Changes in v124

- **Hybrid sprite now in Advanced Hybrid armour** (variant G): a smooth dark-gunmetal breastplate with a lit top edge and a centre ridge, matching gunmetal knee pads and greaves with dark soles, over brown trousers. Variant H (Resistance 3 look: tan skin, red sash, legs armoured in reddish-brown plate, bare clawed feet) is in the script as an alternative.

## Changes in v123

- **Hybrid sprite uniform reworked** (variant D in `build/infantry_sprite.py`):
  - bare grey-tan chest, no straps;
  - opaque dark brown trousers with gentle shading, so the leg shape no longer shows through;
  - grey knee pads, and black boots up to the knee as the darkest part of the figure;
  - the crotch is no longer painted as part of the rifle;
  - the alien's eye spots are painted out of the front view.

  Variants A to E are kept in the script (`HYBRID_VARIANT=E` is the same without knee pads).

## Changes in v122

- **Fix: the Hybrid's rifle was drawn solid black in v121.** The repaint had lost the step that colours it. The rifle is back to gunmetal with its original highlights.

## Changes in v121

- **Hybrid sprite repainted**: a bare grey-tan chest with two dark harness straps crossing it (instead of a solid black torso band), a belt at the waist, and continuous charcoal trousers into dark boots (instead of brown legs below dark hips).

## Changes in v120

- **New Hybrid infantry map sprite**, repainted from Darkest Hour's own alien infantry set (`C-ALI`) by `build/infantry_sprite.py`. It keeps the vanilla animation exactly (stand, walk and fire in 8 directions, the original frame counts and anchor points) and repaints it:
  - grey-tan skin, a dark harness and brown trousers;
  - amber eyes and two cooling towers with amber vents behind the shoulders;
  - the white firing beam is now amber Bullseye fire.

  All four Hybrid model levels use it. The previous Grok sprite is kept in `src/sprite_src/hybrid_grok_r3/`. Not yet tested in game.

## Changes in v119

- **Chimeran fighter map sprite** (`T-FIGHTER C-UA0 L-1`): a compact gunmetal teardrop hull with short swept scythe wings, amber leading-edge veins, a cockpit band at the blunt nose and twin amber engine glows at the tail. Firing frames add twin amber bolts. It is drawn by `build/fighter_sprite.py` to the vanilla fighter conventions: 108x108 frames x19, near top-down view, a half-size flat shadow in palette slot 1 at the anchor, and the same scale as the vanilla Spitfire. Not yet tested in game.

## Changes in v118

- **Apex Strain (95060) has a new picture**: a pencil study sheet of the six-eyed, heavily armoured apex breed, with a head study and a spine cross-section, the callouts hand-lettered in sepia ink.

## Changes in v117

- **Heavy Hybrid Breeds (95050) has a new picture**: a pencil study sheet of a hulking, unarmed heavy breed, with a head study and a muscle-fibre sketch, the callouts hand-lettered in sepia ink.

## Changes in v116

- **Advanced Hybrids (95040) has a new picture**: a pencil study sheet of an armoured Advanced Hybrid, with a head study and an armour cross-section. Its callouts are hand-lettered in sepia ink: jaw, fused plates, grown armour, toes, cooling vanes ("will not survive without them"), drum-fed rifle, binocular eyes, three-layer plate.
- `build/annotate.py` adds handwritten notes to a study sheet's empty callout circles, using the open-licence Caveat font in `build/fonts/`.

## Changes in v115

- **Dropship (transport plane) unit picture replaced**: a long armoured Dropship with ribbed troop bays, Hybrids deploying beneath it. The old strafing-run picture fitted an attack plane more than a transport.

## Changes in v114

- **AA turret brigade picture replaced**: a single Chimeran AA mount firing, with a Hybrid crewman on each side, in the same warm sepia as the other brigade pictures.

## Changes in v113

- **Hybrid map sprite updated (r3)**: grey-tan skin, black chest harness, brown trousers, the three amber cooling towers on the back, a ridged skull and a chunky Bullseye. It covers all animations (stand, walk and fire in eight directions). The L-2 to L-4 sprite files point at the same bitmaps, so every Hybrid model gets the new look.

## Changes in v112

- **Four tech pictures are now dossier pages** on the Chimeran virus, pinned whole into the vintage template:
  - Tunguska Strain (95010): Stage 3, the full Hybrid.
  - Rapid Conversion (95030): Stage 2, the 72-hour mutation.
  - Spire Launchers (95140): the Crawler Spire attack.
  - Quarantine Protocols (95310): the Chimera bite.
- **The build now pins portrait-shaped originals whole** (a notebook page, a dossier sheet) on the template's paper instead of cropping them. The replaced originals are kept in `src/tech_raw_old/`.

## Changes in v111

- **"Carriers Among the Refugees" renamed "The Infected Among the Refugees"**, so it doesn't suggest the Carrier strain (the floating Chimera that ferry the infected to conversion centres). The event itself is unchanged.

## Changes in v110

- **Bio-mechanical Engineering (95110)** now uses the Longlegs notebook page from the game: the mechanically enhanced knee joint with its muscle and bone notes, cropped to the joint. This is official art, so it is on the list of pictures to replace before a public release.

## Changes in v109

- **Bio-mechanical Engineering (95110) has a new picture**: a sepia technical sketch of a Chimeran bio-mechanical assembly, flesh and tendons growing through a ribbed metal housing between two growth vats.

## Changes in v108

- **Deployable Shield Studies (95230)**: back to the v106 crop of the notebook page, the labelled shield drone diagram (v107 had used the other page by mistake).

## Changes in v106

- **Deployable Shield Studies (95230) has a new picture**: a researcher's notebook page sketching a captured shield drone and its "shield generator core". This is official Resistance art: fine for your own copy, but replace it before any public release (see the note on derived art in ASSETS.md).

## Changes in v105

- **Recovered Chimeran Weapons (95210) has a new picture**: an exploded, numbered parts drawing of a captured Bullseye, as an engineering plate in the vintage template.

## Changes in v104

- **All 33 tech pictures in the vanilla DH style**: each is now a faded monochrome print on aged paper with a torn edge and a paperclip, using the official "Blank Tech Picture Template" from DH's Modding documentation. They now sit alongside the human techs instead of standing out as colour paintings.
- **This is now part of the build.** The originals are kept untouched in `src/tech_raw/<id>.jpg/png`. `build/tech_pictures.py` turns them into the template on every build: it crops to 344x266, lifts dark scenes, converts to greyscale and overlays at about 55% on the paper. A new picture only has to be dropped in as `<id>.jpg`. Ids listed in `KEEP_COLOUR` keep their own colour (for blueprints).

## Changes in v103

- **Research team pictures fixed**: they were made at minister size (36x50) and showed tiny in the research screen. All ten (the five Chimeran teams, the Sorokin Laboratory and the four refugee teams) are now 96x96 with a 1px white frame, the size of vanilla team pictures, recropped from your originals.

## Changes in v102

- **New event picture `res_exodus_sea`**: refugee ships unloading at a dusk quay, with officials checking papers and a masked doctor examining a child. It is used on the 58 ship events: receivers, Madagascar and carriers among the refugees.

## Changes in v101

- **Refugee pictures split, ready for the sea picture**: the ship events (receivers admitting or turning away ships, Madagascar, carriers among the refugees, 58 events) will use `res_exodus_sea` as soon as it exists. Until then they keep `res_exodus`. The trains, transit and camps stay on `res_exodus`.

## Changes in v100

- **New event picture `res_exodus`**: refugees from Russia crowding a snowy railway platform at dusk, climbing into goods wagons while a border guard checks papers. It covers the whole refugee chain (transit, camps, ships, Madagascar, closings) and the earlier exodus events.

## Changes in v99

- **New Chimeran brigade: Menial Labour Gangs** (engineer, model 8). Menials are the unarmed worker caste; attached to a division they give the usual engineer bonus for river crossings. They need no horses, trucks or fuel. **Thrall Conversion** unlocks them, so the Hive has them from the start, and the human engineer line stays locked.
- The Menial picture is now also the brigade picture.

## Changes in v98

- **New event picture `res_menials`**: Menials, the Chimera's unarmed worker caste, tearing down a Siberian town and laying glowing conduit plates under a growing tower. It replaces the newspaper on The Hive Harvest and The Hive Builds (about 690 events, seen when playing the Hive).

## Changes in v97

- **AA turret brigade picture replaced**: a battery of three Chimeran AA mounts on clawed bases firing amber tracers at a Soviet biplane, instead of the tracked human-style flak gun.

## Changes in v96

- **Widowmaker brigade picture replaced**: a living, armoured spider-like Chimera spitting amber acid over an infantry line, instead of the metal walkers with guns. The Widowmaker is a creature, the Chimera's answer to the battle tank.

## Changes in v95

- **All 20 buffer-state portraits recropped** from your full-size masters, with the same framing for every face: the whole head with a little room above it, centred, shoulders at the bottom. They replace both the clipped first crops and the zoomed v93 fixes.

## Changes in v94

- **`res_conversion` replaced**: three Hybrids in a converted factory between rows of glowing conversion pods, each with a human shape inside. This picture appears on about 3,000 events, the most of any.

## Changes in v93

- **Five buffer-state portraits reframed** (Dorokhov, Ryabov, Trusov, Lisitsyn, Pankratov): the full-head versions, zoomed in so the face still fills the frame. The other fifteen keep their first versions.

## Changes in v92

- **Goliaths redrawn closer to the official design**: heavy armoured legs, a spined back and a gun-studded head. The Goliath brigade picture and Siege of the Cities now show the same machine.

## Changes in v91

- **Buffer-state minister portraits**: all 20 ministers of the Siberian Cordon Administration and the Far Eastern Republic.
- **Kazantsev and Kuzmin**, each his state's Chief of Army and senior general, now use their minister portrait in the leader list too.

## Changes in v90

- **Hive Mind Coordination remixed**: an Angel floating in a ruined Gothic hall, with amber threads running to a ring of kneeling Hybrids. The blue is gone, so every Hive Warfare picture now shares the amber palette.

## Changes in v89

- **`res_channel` replaced again**: three Dropships with rotor ducts and troop containers over the Channel at night, the White Cliffs on the left with searchlights and flak bursts. The whole fleet fits the banner.
- **Primarchs and Overseers**: the commander now has no cape and is directing the swarm with a raised arm.

## Changes in v88

- **Primarchs and Overseers remixed**: a Chimeran commander on a ridge above the swarm, with an Overseer drone lighting the plain.

## Changes in v87

- **Leader portraits**: the five clone tiers (Overmind, Hive Node, Swarm Node, Spire Node, Deep Node).
- **Research team portraits**: all five Chimeran teams, the Sorokin Laboratory (and Britain's Sorokin Group), and the four refugee teams. The refugee teams now use their own pictures.
- **Swarm Assault and Siege of the Cities remixed**: unarmed Leapers ahead of the Hybrid line, and real tripod Goliaths over a burning city.

## Changes in v86

- **Ten new tech pictures**: Sea Hunters, Burrowers and the eight Hive Warfare techs (Hive Mind Coordination to Chimeran Air Defence). Every tech in the mod now has its own picture.

## Changes in v85

- **`res_channel` replaced** by your Dover redo: three Dropships crossing towards the White Cliffs, the lead one carrying a troop container. The whole fleet fits the banner.

## Changes in v84

- **`res_peace` replaced** by your remix: a civilian signing between two Soviet marshals under a map of Russia, seen over a delegate's shoulder.
- **`res_angel` kept as it is.** The event is about Angel sightings, and a psychic projection that looks like an angel to human eyes fits that, even though real Angels look nothing like it.

## Changes in v83

- **Seven new event pictures** from your batch, converted to the 400×116 framed banner: `res_angel`, `res_channel`, `res_feral`, `res_inhibitor`, `res_london_tower`, `res_morning_star` and `res_peace`.
  - Six are for events not yet written (the 1951 scenario, the peace path, the Feral faction) and switch on automatically when those events use these names.
  - `res_inhibitor` (the glowing serum) is used now, by "Decision: The Cloven Programme" and "The First Cloven".
  - Optional remix for `res_morning_star`: the invasion stripes are a 1944 marking.

## Changes in v82

- **New Dropship 'Buzzard' pictures** (CAS 17 / 7), UA0 and generic: a compact armoured shuttle on a strafing run over Soviet trenches, troop container slung beneath, searchlights and plasma cannon firing. The icon is now labelled "38", the model's actual year (batch 2 said "44"), with an "8" built from the existing "3".
- **New event picture `res_dropship`**: Hybrids pouring out of a landed Dropship. It is used by the 26 "The Army of …" events, where a Processing army appears.

## Changes in v81

- **New Spire Launcher Battery picture** (artillery brigade 1 / 14), UA0 and generic: tracked multi-tube launchers firing a Spire, with Hybrid crews in the mud.

## Changes in v80

- **Cloven III picture updated** to your glowing-eyes version of the mixed squad: amber eyes and lenses tie the Cloven back to the serum.

## Changes in v79

- **New Titan brigade picture** (heavy armour 8 / 6), UA0 and generic: an armoured six-eyed giant firing its arm cannon, with Hybrids behind it in ruined factories. Brigades have no per-model icon in DH, so this is the unit-details picture only.

## Changes in v78

- **Cloven III pictures** (the USSR's infantry model 20, Soviet only): a mixed squad of greatcoats and bare torsos, different gas masks, a pan-magazine machine gunner and a man dragging a wounded comrade. The three Cloven models now each look different: uniformed, half-feral, and ragged mixed.

## Changes in v77

- **Cloven II pictures** (the USSR's infantry model 19, Soviet only): the half-feral Cloven, gaunt and shirtless in braces and gas masks, with Mosins, in a dead forest. Cloven I keeps the uniformed red-star squad, and Cloven III shares that picture until a mixed-squad remix arrives.

## Changes in v76

- **Hunter Dropship pictures** (naval bomber 16 / 9, "40"), UA0 and generic: an armoured, insect-like Dropship skimming the waves past a burning cargo ship. Every Chimeran unit now has its own picture.
- **New Steelhead Swarm pictures** (infantry 0 / 20, "50"): armoured domes with the eyes set in, ribbed canisters, heavy Bullseyes, a snowy ruined city.
- **Gen I Hybrid Swarm (0 / 18) updated** to the varied-poses remix: crouching, striding, kneeling to reload.
- The previous pictures are kept outside the mod.

## Changes in v75

- **New Hybrid Swarm (Gen I, infantry 0 / 18) pictures**, from your remix: gaunt converted soldiers in rags and harness, with finned heat-sink packs, six-eyed faces and Bullseyes, in a dead forest.
- **Advanced Hybrid Swarm (0 / 19) updated** to your varied-mouths version.
- Both are in UA0 and generic versions. The previous pictures are kept outside the mod.

## Changes in v74

- **New Advanced Hybrid Swarm pictures** (infantry 0 / 19, 1942), both UA0 and generic, from your remix: six-eyed armoured Hybrids with cylindrical cooling towers and Bullseyes, in a ruined Russian city with onion domes. The previous pictures are kept outside the mod in `art_old/` in my workspace, in case you want them back.

## Changes in v73

- **Cloven pictures.** The USSR's Cloven Rifle Divisions (infantry models 18–20, the Hybrid models under their Soviet name) now have their own Soviet-only unit and production pictures: a gas-masked Red Army squad with red-star ushankas in a ruined city. DH prefers a country's own picture to the generic one, so the Chimera keep their Hybrid pictures. The icons carry the same years as the Hybrid models (33, 42, 50).

## Changes in v72

- **Thrall Horde model pictures** (militia 11 / 10): a unit-detail picture and a production icon marked "33", each in a UA0 and a generic version. They are made from your first Grok image, using batch 2's frame, green bars and year digits. Of the Chimeran units, only the Hunter Dropship is now without a picture.

## Changes in v71

- **`ASSETS.md` brought up to date.** It records the art added since v60 as done: the Hybrid map sprite, the batch 2 unit pictures and the 23 tech pictures. It lists what is still needed: 10 tech pictures, the Thrall Horde and Hunter Dropship model pictures, and map sprites for the other unit types. It also lists the refugee and Sorokin research teams, and the event groups added since v60. No change to the mod itself.

## Changes in v70

- **Tech pictures for the Chimeran trees** (`gfx/interface/tech/<id>.bmp`, 344×266 like vanilla): the Strains, Chimeran Engineering, Captured Chimeran Arms, Chimeran Pathology and Anti-Chimeran Warfare techs, 23 in all. A tech uses its own picture whenever `src/assets` has one, otherwise the borrowed vanilla picture. Still on vanilla pictures: the Hive Warfare doctrines (95510–95580), Sea Hunters (95170) and Burrowers (95180).

## Changes in v69

- **Model pictures for the rest of the Chimeran army** (art batch 2), in `gfx/interface/models`: unit-detail pictures and production icons.
  - Divisions: Leaper Swarm I and II (cavalry 15–16), Angel Nexus (HQ 6), Chimeran Fighter I and II (13_17–18), Dropship (CAS 7), Battleship (strategic bomber 10).
  - Brigades: Stalkers and Goliaths (super-heavy 2–3), Titans (heavy 6), Widowmakers (medium 11), Spire Launcher Battery (artillery 14), AA Turrets (AA 7).
  - Each has a UA0 picture plus a generic one. DH Full has no picture for these model numbers, all of which come right after vanilla's last model, and the national picture only shows if a generic one exists.
  - The batch drew the Angel Nexus as HQ models 0–5. In the mod it is model 6, so its pictures are installed as 10_6. The generic HQ 0–5 files are left out, since they would replace every country's HQ pictures.
  - The batch's text lines are not used: the mod already writes these model names.

## Changes in v68

- **Coastal militia for every Burrower landing.** The scenario now includes patched copies of DH Full's 1933 files for the USA, Japan, the UK and Spain. Each has dormant, locked militia added just before the country block's closing brace, the way vanilla adds the British Home Guard. "Tremors under …" can then raise:
  - USA: Nome (Bering Strait).
  - Japan: Sapporo (La Pérouse), Nagasaki (Tsushima), and Okha (Tatar Strait), if Japan has taken northern Sakhalin.
  - UK: Dover (the Channel).
  - Spain: Tangier (Gibraltar), which is Spanish in 1933.
  - USSR: Okha, as before.
  - Militia models follow each country's 1933 file: 3 for the USA, UK and Spain, 4 for Japan and the USSR. The rest of each file is unchanged. France and the Far Eastern Republic have none: France doesn't hold Tangier in 1933, and the Republic has no scenario file.

## Changes in v67

- **Chimeran map sprite for infantry.** The Hybrid sprite set is in `gfx/map/units` and `gfx/palette`: stand, walk and fire in eight directions, at sprite level L-1, with copies at L-2 to L-4 that use the same bitmaps.
  - The UA0 row of `db/country.csv` now has UA0 as its Army Nationality Sprite (was SOV). The three model nationality columns stay empty, since filling those crashed v47.
  - **To check:** UA0 militia, cavalry, HQ, armour and aircraft now also look for UA0 sprites, and none exist yet. If they show no sprite, show a wrong one, or the game crashes, the fix is UA0 copies of the Soviet sprite definitions for those types.

## Changes in v66

- **Vanilla Soviet-Japanese border incidents sleep when the border is the Hive's.** Two new Japanese events put the vanilla ones to sleep (`sleepevent`), so the incidents no longer fire over land the Chimera hold. Each fires if Japan is at war with the Hive or the Hive holds the border province:
  - "No Border at Lake Khasan" (9500591) sleeps Lake Khasan (hoi2.txt 24). Border province: Vladivostok.
  - "No Border at Khalkhin Gol" (9500592) sleeps Nomonhan (hoi2.txt 22). Border province: Choibalsan.

## Changes in v65

- **Evacuate Siberian Industry is a 90-day window.** It opens when Krasnoyarsk falls ("Krasnoyarsk Falls Silent", 9500531) and lapses 90 days later. It no longer depends on holding Tomsk. Each factory still only moves if the USSR holds its town: Novosibirsk, Kemerovo, Kuznetsk and Barnaul.

## Changes in v64

- **The Ural Quarantine Line no longer needs the Combat Engineer tech.** The USSR always has it. The decision now needs only the war and a Soviet division in every line province the USSR holds. The forts go up 42 days later where a division still stands.

## Changes in v63

- **The Ural Quarantine Line no longer costs money.** It still needs the engineer tech and a division in every line province, and still takes 42 days.
- **The buffer-state borders are redrawn.**
  - **Siberian Cordon Administration** gains Tomsk, Salekhard and the whole Zabaikalye area (Ulan-Ude, Chita, Borzya). Chita sits on the railway back to Moscow.
  - **Far Eastern Republic** is now the Amur, Khabarovsk, Primorye, Magadan and Kamchatka. Its capital is Vladivostok, not Chita, so its Pacific provinces aren't cut off from their capital when the Hive closes the Chita corridor.
  - **Armies:** the Cordon gets a second corps, the Transbaikal Group at Chita (from the 36th and 57th Rifle Divisions). The People's Revolutionary Army now forms at Khabarovsk, from the 12th and 21st Rifle Divisions and the 8th Far Eastern Cavalry Division. The Primorye Group at Vladivostok is unchanged.
  - The decision and founding texts, the fallback spawn towns and both buffer AIs' target lists are updated to match.

## Changes in v62

- **Burrow warnings: a locked coastal militia instead of a fort.** "Tremors under …" no longer builds a land fort; players can build those normally.
  - Where a dormant unit exists, *Raise a coastal militia* costs 10 money and 100 supplies and wakes a locked militia division at the landing province. Like the tower guards, it is a dormant division in that country's scenario file.
  - So far only the USSR has one: Coastal Militia of Tatar Strait, at Okha, militia model 4. Other defenders only get "Nothing can dig that far" until their scenario files are added.
- **The Ural Quarantine Line takes troops, engineers and time.**
  - It costs 600 money (was 150) and needs the 1911 Combat Engineer Brigade tech.
  - It needs a Soviet division in every line province the USSR holds. DH's `garrison` trigger counts divisions but can't see brigades, so the engineer tech stands in for the sappers.
  - The forts (+2) go up 42 days later, in "The Ural Line Is Complete" (9500590), only in provinces the USSR still holds with a division in them.

## Changes in v61

- **The Burrower warning's emergency fort is dear.** "Tremors under …" now costs 200 money (was 50) for +1 land fort (was +2) at the landing province. It's instant, so it shouldn't be cheaper than building one. Each crossing warns only once, so there are at most six such forts in a game.

## Changes in v60

v60 collects every interim v59 build sent while these changes were made. From v60 on, each build gets its own number.

- **Infection outbreaks have three answers, gated by research.** The options are shown only when their tech is known, using DH's action-level triggers.
  - **Abandon it to the Hive** is always available. The town secedes to the Chimera, with dissent +1.
  - **Purge the infected** needs Quarantine Protocols (95310). It costs the same as before:
    - Soviet: manpower −25 and dissent +3, or +2 with the Purge and preparation.
    - Others: manpower −10, dissent +2.
  - **Inoculate the survivors** needs Inhibitor Serum Trials (95320). It costs money only (40 for the USSR, 25 for anyone else) and keeps the town without dissent.
- **Abandoned towns become Thralls.** One day after a town is abandoned, the Chimera raise a Thrall militia division there (9520000 + province ID, model 10).
- **The virus crosses the border.** Infection events now cover provinces outside the USSR along the Hive's path: Finland, the Baltics, Poland, Romania, Central Europe, Germany, the Balkans, Turkey, Persia, Afghanistan, the Low Countries, France, Denmark, Switzerland, Italy, Scandinavia, Korea, Tuva, and China within four provinces of the Soviet border.
  - Each province has one event per likely owner (start owner plus plausible conquerors). Only the current owner's event can fire, and only while at war with the Hive next to Hive-held land (`res_infection_abroad.txt`, 9510000+).
- **"The Russian Papers" (9509900+).** The first time a country is at war with the Hive, the quarantine techs are unlocked for it and it gets a Quarantine Protocols blueprint. Without this, foreign countries could never research the gated options.
- **The Don alert (9509800+).** When the Hive takes a Don province (Voronezh, Pavlovsk, Uryupinsk, Kalach, Kamensk or Rostov), or Moscow falls, Poland, Romania, Finland, the Baltic states, Czechoslovakia, Hungary, Turkey and Germany are warned before the Hive reaches them.
  - **If Britain passed Sorokin's letter to Porton Down** (new flag `res_porton_down`), "Word from London" unlocks the quarantine techs and gives a Quarantine Protocols blueprint.
  - **Otherwise,** "The Don Has Fallen" unlocks the techs only.
  - **Either way,** the country can dismiss the warning. "The Russian Papers" then still fires when its war with the Hive starts. A country that heeded the warning skips it.
- **Refugee corridors (`res_refugees.txt`, 9530000+).** An advance wave of mostly healthy refugees flees ahead of the Hive in stages tied to its progress.
  - **West, five stages:** the Urals, then the Don or Moscow, then Warsaw, Riga, Bucharest or Helsinki, then Berlin, Vienna, Prague or Budapest, then Paris or the Low Countries.
  - **East, three stages:** Irkutsk, then Harbin, Vladivostok or Ulaanbaatar, then Peking, Mukden or Port Arthur.
  - **Transit countries** choose to *Let them pass* (money −5, dissent +1) or *Hold them in camps* (money −25, dissent +2, manpower +10).
    - Camps get a follow-up after 90 days: keep holding them (more money and dissent, worse without Quarantine Protocols) or open the gates.
    - If the Hive takes a camp's capital while it is still full, the Hive raises two Thrall divisions there.
  - **Receivers** choose to *Admit them* (manpower +4 to +10, money −15, dissent +1) or *Turn the ships away*.
    - Receivers are Britain, the USA, Canada, Japan and Australia, plus Sweden, Turkey, Spain and Egypt while their capitals hold, and South Africa.
    - Admitting refugees without Quarantine Protocols brings a "Carriers Among the Refugees" event 30 days later.
  - **Spain and Turkey** start as havens and become transit routes to Africa as the Hive moves west.
  - **Émigré research teams** come with some admissions: Britain at stage 3 of the western route, the USA also at stage 3, Japan at stage 2 of the eastern route, South Africa at stage 4 of the western route. Each team is woken with `waketeam` and put back to sleep after two years.
  - **The Madagascar Settlement.** Once Central Europe falls, whoever holds Madagascar can found a refugee settlement: Tananarive gets +5 VP (`province_keypoints`), +20 infrastructure there and at Tamatave, and manpower. Later refugee ships are routed there.
  - **Closings.** Every country that admitted refugees gets a final "no more refugees are arriving" event when its route is cut:
    - Britain, the USA and Canada: the Channel ports plus Madrid and Gibraltar fall.
    - South Africa, Egypt and Madagascar: Gibraltar and Istanbul fall.
    - Japan, the USA and Australia: Shanghai, Tientsin, Tsingtao and Canton fall.
- **Sorokin escapes to Britain.** When the Kremlin falls silent (9500710), the Sorokin Laboratory leaves Soviet service (`sleepteam`), unless he was silenced or the Academy expedition was refused.
  - 45 days later Britain gets "A Name at the Checkpoint" (9500498 if it knows him from the Barentsburg letter, 9500499 if not). A refugee checkpoint has flagged him and handed him to the British legation.
  - *Fly him to Porton Down* wakes the Sorokin Group as a British research team. It also unlocks the quarantine techs and gives a blueprint: Quarantine Protocols, or Inhibitor Serum Trials if Britain already has Quarantine Protocols.
- **Abandon the East opens six months into the war.** Before, retaking Krasnoyarsk hid the decision again. "The Outbreak" now schedules "The Yenisei Question" (9500565) for the USSR 180 days later. From then on the decision is available whether or not Krasnoyarsk is held. It also opens earlier if Krasnoyarsk falls first. The Soviet AI still only takes it once Krasnoyarsk is in Hive hands.
- **Buffer-state armies spawn only in towns the state holds.** Before, founding the Far Eastern Republic after Chita had fallen dropped a division into Hive-held Chita. Each corps and its divisions are now guarded with `control`, and if the home town isn't held the corps moves down a fallback list:
  - Irkutsk → Bratsk → Yakutsk → Cheremkhovo
  - Chita → Blagoveshchensk → Khabarovsk → Vladivostok
  - Vladivostok → Nikolsk-Ussuriysky → Khabarovsk → Nikolayevsk
  - If none is held, the corps doesn't spawn. The capital follows the same lists.
- **Evacuate Siberian Industry opens when Krasnoyarsk is lost and closes when Tomsk falls.** It can be taken once "Krasnoyarsk Falls Silent" (9500531) has fired, so retaking the city doesn't hide it again. It disappears while the Hive holds Tomsk. Before, it was shown while the USSR held Novosibirsk and could only be taken after Tomsk fell.
- **Hive land becomes Hive core.** "The Hive Builds" (after a Dead Zone event, in the USSR and the buffer states) and "The Thralls of …" (after a town is abandoned to infection) now add the province as a UA0 core. That ends revolts in Hive-held provinces. The old owner keeps its core, so a counter-attack can still take the province back.
- **The Hive Heart is guarded.** Norilsk has three dormant, locked divisions (Heart Sentinels I and II, and the Heart Brood Hybrids) that "The Outbreak" wakes in place. Like the tower guards, they can never be moved away, so taking Norilsk always means beating a garrison.
- **The Processing: Hybrid armies by region (`res_processing.txt`, 9570000+).** When the Hive holds all the key cities of a region, "The Processing of …" fires.
  - Sixty days later "The Army of …" appears in the first key city it still holds. It has an Angel Nexus HQ (once the Hive has Hive Mind) and 2–8 Hybrid divisions of the best model, depending on the region's size.
  - The region's owners get a news event: "Nobody is coming out."
  - There are 26 regions:
    - Inside the USSR: Western Siberia, the Baikal, the Far East, the Urals, the Volga, Central Russia, the Ukraine, Byelorussia, the Caucasus, Central Asia.
    - Asia and the Middle East: Manchuria, Mongolia, Korea, North China, Turkey, Persia.
    - Europe: Finland, the Baltic States, Poland, Romania, Central Europe, Germany, the Balkans, France and the Low Countries, Italy, Scandinavia.
  - This replaces the per-town Hybrid conversions and the Dead Zones outside the USSR, which tried out earlier in v59 came to about 3,000 events. The Soviet and buffer-state Dead Zones remain, for ownership, supply and the new Hive cores. The per-town Thrall militia from abandoned towns also remains.
- **Losing Norilsk no longer cripples the Hive for good.** Up to three cycles of two events:
  - **"The Heart Is Wounded"** (9500780+): when Norilsk falls, its 30 Hive Heart IC goes dark. It is removed, so the captor gets no Chimeran factories and the Hive has nothing to rebuild. Also, the Hive's capital moves to the westernmost of Moscow, Kazan, Ufa, Sverdlovsk, Novosibirsk, Tomsk, Krasnoyarsk and Irkutsk that it owns and holds. The Hive also gets 3,000 supplies and 500 oil.
  - **"The Heart Regrows"**: when it retakes Norilsk, a fresh locked Heart guard wakes there: two Sentinels and a Brood, from a separate dormant set for each cycle (95953–95961). The 30 IC returns intact, Norilsk gets +40 infrastructure, and the Hive gets 5,000 supplies and 1,000 oil. The capital only returns to Norilsk if the Hive holds none of those cities.
- **Fix: "Seize the alien technology" now works.** Every Chimeran Engineering tech needs Tunguska Strain (95010), and "The Hive Is Destroyed" gave only its blueprint without making it researchable. The whole tree stayed locked. 95010 is now activated as well.
- **Fix: the Cloven.** "Decision: The Cloven Programme" no longer requires `lost_national` 5, which a USSR holding the line never reached. It no longer hands out free units either.
  - Taking it lends 10 IC from Moscow (or Leningrad, or Kazan, whichever the USSR holds first) to the programme.
  - Ninety days later, "The First Cloven" (9500424) returns the IC and creates two Cloven Rifle Divisions (model 18) in a Special Corps Cloven, at Sverdlovsk, Kazan or Moscow.
  - Building more still needs Tunguska Strain, which the decision unlocks.
- **Buffer-state armies are taken from the Red Army.** "Abandon the East" now removes one Soviet division (scenario type 10848) for each division the new states raise:
  - The Cordon takes the 73rd, 78th, 94th and 109th Rifle Divisions (Novosibirsk).
  - The People's Revolutionary Army takes the 36th and 57th Rifle Divisions (Chita) and the 8th Far Eastern Cavalry Division (Khabarovsk).
  - The Primorye Group takes the 1st and 2nd Kolkhoz Rifle Divisions (Vladivostok).
  - The decision text says so. A division already destroyed can't be removed, so its successor comes free.
- **The tower network carries the Hive's industry.** The Hive Heart at Norilsk now starts with 30 IC instead of 50. Every tower that rises adds 5 IC in its province: 15 towers, so up to 75 more for a Hive that conquers the USSR. Norilsk's own tower makes 35 there at the start.
  - When a tower falls its 5 IC goes dark: it is removed, so the captor gets nothing. The Heart's 30 IC goes dark and returns with "The Heart Is Wounded" and "The Heart Regrows", as before.
  - Early on Norilsk is still the jugular. Later the Hive has to be taken apart tower by tower.
- **The Hive researches only its own trees, plus economic improvements** (`hive_research.py`, built from DH Full's tech files).
  - **Known from the start (65 techs):**
    - The land doctrine trunk up to "20th Century military concept", so no more researching Tribal Warfare. The Hive's doctrine branch is Hive Warfare.
    - Mobilization (strategic redeployment).
    - The early air doctrines that give Dropships ground attack and interdiction, and Battleships installation strikes and strategic bombing.
    - Construction engineering, logistics up to Rear Area Supply Dumps, and industry, mining, oil and hospital techs up to 1936.
  - **Still researchable (46):** later industry, production, construction, logistics, repair and hospital techs. An improvement is only allowed if everything it requires is known or allowed.
  - **Deactivated by "The Hive Heart" (734):** every other human tech, using DH Full's doctrine-exclusivity command `deactivate`. That covers weapons, vehicles, aircraft, ships, radar, codes, nuclear and rocket research, and the human land, air and naval doctrine branches. Human weapons now only reach the Hive through "The Hive Learns" (`steal_tech`).
- **Captured Chimeran equipment costs IC to build, and does more.** The costs work like DH Full's own equipment techs, using `build_cost … when = on_upgrade where = relative`:
  - Reverse-Engineered Rifles (95220): infantry and militia soft attack +2 (was +1), infantry hard attack +1 (new). Costs +5% infantry and militia.
  - Deployable Shield Studies (95230): infantry defensiveness −2 (was −1; lower is better). Costs +5% infantry.
  - Chimeran Alloy Armour (95240): armour toughness and defensiveness −2 each (was −1). Costs +10% armour.
  - Recovered Chimeran Weapons (95210) stays free. It is the evaluation step, not production kit.
- **The Hive can no longer build human units.** "The Hive Heart" scraps human HQ models 0–5, garrison 0–5, military police 0–1 and AA brigades 0–2. It had picked these up from its starting infantry, anti-air and doctrine techs. What is left is its own Angel Nexus HQ, Thralls, Hybrids and Chimeran AA Turrets.
- **The guards are Chimeran.** Each tower's two dormant, locked guards are now a Hybrid Brood and a Thrall Horde ("Norilsk Brood", "Norilsk Thralls"), not two human 1938 garrisons. The Heart guard is two Heart Thralls and a Heart Brood. Being locked, they don't need to be garrisons.
- **The research lock runs in batches.** The 734 deactivations are split into 15 events of 50 (9500610–9500624), fired by "The Hive Heart", in case DH caps the number of commands in one option.
- **The Hive's starting techs are listed in prerequisite order,** each after the techs it requires (Tribal Warfare first). In numeric order, Modern Agriculture came before Early Agriculture, and DH may skip a starting tech whose requirements it hasn't read yet. **Check in a new game:** the Chimera's Land Doctrine tab should show Tribal Warfare through "20th Century military concept" as researched, and the Industry tab its 1910–1936 techs.
- **A lopsided Chimeran doctrine.** The human doctrine trunk the Hive starts with left it at 75% attack and 25% ground defence efficiency. Hive Warfare now sets these on purpose:
  - **Hive Mind Coordination (known from the start):** attack and support-attack efficiency +25% (back to 100%), morale +10, ground defence efficiency set to 40%.
  - Overwhelming Numbers sets ground defence efficiency to 50%, Siege of the Cities to 55%, Primarchs and Overseers to 65%. It never reaches the human 100%: the swarm hits hard and doesn't break, but holds ground poorly.
- **No agriculture for the Hive.** The agriculture line (Early Agriculture Research to Modern Agricultural Production) is locked, not known or researchable. 
- **Hive Physiology (95560), a Chimeran tech on the Land Doctrine page.** It is Hive-only, known from the start and requires Hive Mind. It replaces the human lines the Hive has no use for (agriculture, medicine and hospitals are now locked) and sets the levers to a lopsided profile:
  - **The body:** trickleback +20, manpower growth +10, attrition +10, repair +20, supplies production +10%, industrial efficiency +5%.
  - **The swarm:** assault +5, encirclement +3.
  - **The air:** ground attack +50% (25% → 75%), interdiction +40%, air superiority +40% (10% → 50%), strategic bombardment +15% (10% → 25%).
  - **Unchanged on purpose:** ground defence efficiency (Hive Warfare raises it slowly), counterattack, ambush, research speed, radar.
- **Fix: Hive Mind is no longer open to the USSR.** The Cloven decision and "Seize the alien technology" unlock Tunguska Strain, which Hive Mind requires. Both now deactivate Hive Mind and Hive Physiology for the USSR, keeping the Angel Nexus HQ and Thrall Hordes out of Soviet hands.
- **Thralls and AA come from the Hive's own techs.** The human infantry line (1870–1942) and the AA brigade techs are no longer known or researchable for the Hive. They brought garrisons, military police and human AA into its build list, and blocked its militia from improving.
  - **Thrall Conversion (95570)** and **Chimeran Air Defence (95580)** are new Hive-only techs in the Hive Warfare column, known from the start. They give the militia (Thrall Horde, model 10) and AA brigade (AA Turrets, model 7) units.
  - The infantry unit type now comes from Tunguska Strain, beside the Hybrids. The AA Turrets moved off it, since the Cloven USSR can get that tech.
  - Thralls improve through Hive Warfare: Overwhelming Numbers gives militia soft attack +2 and defensiveness −2; Primarchs gives soft attack +2 and toughness −2. Lower is better for both.
  - Static anti-air is known to 1942 (Interwar to 2480), with 1945, 1948 and 1956 still researchable.
  - The Cloven and "Seize the alien technology" also lock the two new techs for the USSR.
  - The Hive now starts with 42 human techs, 36 are researchable, and 767 are locked.
- **Fix: no 1870 infantry or militia for the Hive.** Activating a unit type also makes its model 0 (the 1870/1918 human version) buildable. Every Chimeran tech that activates a unit type now scraps model 0 straight afterwards:
  - Tunguska Strain, Thrall Conversion, Chimeran Air Defence and Hive Mind (infantry, militia, AA, HQ).
  - Adaptive Strain and the later Strains (cavalry, medium, heavy and super-heavy armour).
  - Engineering (artillery, fighters, Dropships, Battleships).
  The scrap is limited to countries without the 1870 infantry tech, which every human country has, so a Cloven USSR keeps its own models. "The Hive Heart" also scraps infantry and militia model 0 at game start, as a backup.
- **Sea Hunters (95170, Chimeran Engineering, 1940):** the Hunter Dropship, a Chimeran naval bomber (model 9). The Hive's human air doctrines are locked, so the tech grants the naval strike and port strike missions itself, at +50% and +30%. The Hive AI builds them (3% of its mix, from Leapers). The USSR gets the tech too after "Seize the alien technology".
- **The Burrowers (95180, Chimeran Engineering, 1944; `res_burrowers.txt`, 9580000+).** The Hive has no ships. Once it knows Burrowers and holds a shore, it tunnels under the strait:
  - **The crossings:** Anadyr → Nome, Nikolayevsk → Okha (Sakhalin), Toyohara → Sapporo, Busan → Nagasaki, Calais → Dover, and Gibraltar → Tangier.
  - **Digging** costs 40 manpower and declares war on whoever holds the far shore. That country gets "Tremors under …" and can fortify the landing (−50 money, +2 land fort; changed in v61).
  - **Two waves** of three Hybrid divisions (best model) break out on the far side 60 and 150 days later, but only while the Hive still holds the near shore.
  - **Caveat:** DH has no supply line under a strait, so the bridgehead fights out of supply until it takes enough ground.
- **Fix: Chimeran aircraft vulnerabilities.** For aircraft, `surfacedefence` and `airdefence` are vulnerabilities too: the human interceptor goes from 30 to 3 over the tree. The Dropship goes from 8/20 to 4/10, better armoured than human close air support as the lore says. The Battleship goes from 12/40 to 2/6. The Fighters were already right.

## Changes in v58

- **Tower guards are locked in place.** Units created by `add_division` can't be locked, so the guards now follow vanilla's UK Home Guard pattern. The Chimera scenario file holds 30 dormant, locked garrison divisions (Sentinel Nodes, two per tower). Each tower-rise event wakes its pair in the tower province with `activate_division`. Locked units can't be moved by the AI or a player, so a tower is never left empty.

## Changes in v57

- **Tower guards.** When a tower rises, the Hive raises two garrison divisions there (superseded in v58 by locked guards).
- **The State Defence Committee fires on its own** once the USSR has lost 3% of its home provinces to the Hive. It used to be a decision, which was easy to forget, and it only ever helped (-2 dissent).

## Changes in v56

- **Once-only guards** on the Hive's capital moves, tower rises and tower falls. Your log shows these events being run over and over. Each now sets a flag and won't run again, so a tower can't rise twice (stacking forts and manpower) or fall twice.
- **`resistance_log.bat`** now also copies every mod event (not just two ranges) and the **last 300 lines** of the log, which is where a crash shows. Run it before restarting the game, since DH overwrites savedebug.txt on launch.

## Changes in v55

- **Fix: the early Purge didn't happen.** *The Organs Move First* fired vanilla event 2007025 with `trigger`, but that event has its own date and chance conditions and evidently still applied them, so nothing happened. The mod now has its own **The Great Purge** event (9500497). It carries out exactly the same 163 commands as vanilla's (arrests, ministers, HQs removed, generals put to sleep, +30 dissent for a human player) and then puts vanilla 2007025 to sleep so the Purge can't happen twice.
- **Purge flag:** both Purge events now set the flag `res_great_purge`. Everything that asks "has the Purge happened?" checks that flag: the postponement notice, the cheaper town purges, and which generals form the Kremlin junta.

## Changes in v54: build checks

No gameplay changes.
- **Build checks.** `validate.py` runs at the end of every build and stops the build on any mistake that has reached a playtest before:
  - day 30/31 dates
  - AI unit mixes that don't add to 100
  - unknown or rejected minister personalities
  - missing model names (STRING_WANTED)
  - missing text keys or pictures
  - duplicate event IDs
  - event commands never seen in vanilla
  - bad province IDs
  - ministers, garrisons or event files referred to but never defined
- **`DH_FACTS.md`** records what is confirmed about DH Full (and how) against what is only assumed. Each assumption says how to check it in game.
- **`TESTING.md`**: firing events from the console, and the key event IDs to test.
- **`resistance_log.bat`**: double-click it, or drag a savedebug.txt onto it, to get a small `resistance_log.txt` with just the errors and the main story events.

## Changes in v53

- **Reverts most of v52.** Chimeran Engineering is open to the USSR again, but only through *The Hive Is Destroyed*. Its "Seize the alien technology" option now also *activates* the whole Engineering line (without that, the blueprint couldn't be researched). The Soviet "Captured" brigade names are back, and the column is no longer labelled "(Hive only)". There is still no Cloven route to Chimeran Engineering.

## Changes in v52

- **Chimeran Engineering is Hive-only.** *The Hive Is Destroyed* no longer gives the USSR Bio-mechanics, so no human nation can reach Stalkers, Goliaths, Titans, Widowmakers, Spire Launchers, dropships or the Chimeran fleet. The Soviet "Captured" and "Tamed" brigade names are gone, and the column is labelled "(Hive only)" again. The Cloven route to Chimeran *infantry* (the Strains) is unchanged.

## Changes in v51: the Cloven

- **The Cloven programme gives the Red Army Chimeran infantry.** *Decision: The Cloven Programme* now also *activates* the Tunguska Strain for the USSR. In DH, `gain_tech` only hands over a blueprint, so the USSR could not research the tech the decision gave it. *Expand the Cloven Divisions* does the same for the next two strains.
- **Fix:** v37 had put the Angel Nexus HQ, the Thrall Horde and the removal of the human 1942 infantry and militia on the Tunguska Strain. Through the Cloven, that would have handed the Red Army Angels and taken away its own infantry. These effects now sit on Hive Mind Coordination, the Hive's starting doctrine, which no human nation can reach.

## Changes in v50: vulnerability, not toughness

- **The big one.** In DH Full, defensiveness, toughness and air defence are vulnerabilities: the game labels them Defensive, Offensive and Air Vulnerability, and lower is better. The mod treated them as strengths, so every Chimeran unit was *more* vulnerable than its human counterpart, and every "+toughness" tech made units worse. Fixed:
  - **Hybrids** (defensiveness / toughness / air): Gen I 30/34/12, Advanced 27/31/11, Steelhead 24/28/10. Human infantry is 35/40.
  - **Leapers:** Gen I 24/30/8, Gen II 20/24/7. Horse cavalry is 22/28/7.
  - **Angel Nexus HQ:** 12/12/5.
  - **Brigades** now *reduce* vulnerability: Stalkers -3, Goliaths -6, Titans -5, Widowmakers -3. AA turrets lower air vulnerability by 4.
  - **All 15 toughness and defensiveness tech bonuses** (Chimeran and human) now subtract instead of add.
- **No more STRING_WANTED.** The mod now ships `config/unit_names.csv` with generic names for every new model. Countries without their own name for a model, such as the USSR for the Angel Nexus or the Thrall Horde, showed STRING_WANTED.
- **Tech screen:** the Hive Warfare doctrine column is labelled "(Hive only)". The Strains line stays open to the USSR through the Cloven programme.

## Changes in v49

- **Fix: the buffer states' provinces went back to the USSR.** While those provinces stayed Soviet cores, DH handed any that Soviet troops controlled straight back to the USSR (the misc.txt rule that passes controlled provinces to an ally whose cores they are). Capitals are exempt, which is why only Irkutsk and Chita stayed. *Abandon the East* now removes the Soviet cores before the release (`removecore`), and *Return to the Union* adds them back (`addcore`).

## Changes in v48

- **Fix: crash to desktop when loading the scenario** (v47). The crash came just after the `revolt.txt` check, as DH began setting up the countries. That is the first time it reads `db/country.csv`, which v47 had just added. The rows for UA1 and UA2 filled the three "model nationality" columns with `SOV`, which no vanilla row does. They are now empty, like every other row. If the game still crashes, delete `db/country.csv` from the mod folder. That restores v46 behaviour: no crash, but yellow map colours.

## Changes in v47

- **Tower falls no longer sweep up other countries' land.** The Hive's tower-fall event used to hand its whole region to the USSR (`secederegion`), which also took the buffer states' provinces. It now hands over only the Hive's own provinces, one by one: to the Siberian Cordon or the Far Eastern Republic inside their zones if they exist, otherwise to the USSR. No other country's land is touched.
- **Map colours:** the colour rows are now also written to `db/country.csv`, which is where DH reads map colours. The Chimera should be black, the Cordon light green and the Republic dark orange. Start a new game to see them.

## Changes in v46

- **Fix: the buffer states lost their land to the USSR.** When a tower in their territory fell (Irkutsk, Khabarovsk or Krasnoyarsk), the Hive's event handed the whole region to the USSR. The follow-up commands meant to pass the buffer states' provinces back ran as the Hive's event, and `secedeprovince` only hands over the executing country's own land, so they did nothing. Capitals survived because a region secession can't take a capital. The handovers now run in the Soviet news event (*The Angel of X Is Dead*), where Moscow owns the land.
- **The buffer states now hold their provinces as cores** (`addcore` in their founding events).

## Changes in v45

- **Fix:** DH rejected the minister personality "Armored Spearhead Doctrine" (critical error on launch). Yakir now uses Decisive Battle Doctrine and Timoshenko uses Elastic Defense Doctrine. Both are already accepted elsewhere in the mod.

## Changes in v44: the Kremlin is silent

- **New event, The Kremlin Is Silent** (9500710). It fires 10 days after the Fall of Moscow, whichever option you chose. Stalin's evacuation train never arrives, and Stalin, the Politburo and the commissars go missing (they are put to sleep). A State Defence Council of generals takes every ministry. Effects: +5 dissent, democratic -1, defence lobby +2.
- **Who takes over depends on the Great Purge:**
  - **After the Purge:** Voroshilov, Shaposhnikov, Vasilevsky, Kulik, Golikov, Proskurov, Zhukov, Timoshenko, Kuznetsov and Novikov.
  - **If the Purge never happened** (it is postponed during the Hive war): the old guard it would have killed. Tukhachevsky becomes head of state, with Egorov, Voroshilov, Uborevich, Gamarnik, Berzin, Shaposhnikov, Yakir, Orlov and Alksnis.
- **The junta ministers** are in `db/ministers/ministers_SOV_res.csv`. They reuse each man's existing DH portrait, from his minister or leader entry.

## Changes in v43: AI for the buffer states

- **AI files:** `ai/res_cordon.ai` (UA1) and `ai/res_fer.ai` (UA2), built from `minor_default.ai` like the Chimera's. They never start wars, dig in (recklessness 0), and build infantry and militia (60/40). They hold their capitals, railway junctions and ports first: Irkutsk, Kansk, Bratsk, Cheremkhovo and Yakutsk for the Cordon; Chita, Vladivostok, Khabarovsk, Blagoveshchensk and Ulan-Ude for the Republic. The founding events load these files when the AI runs the state.
- **Mobilisation:** both states are set to general mobilisation (professional army slider 8) when founded. DH Full's own mobilisation AI events only cover the tags they list, which doesn't include these two.

## Changes in v42

- **Japan's reaction now needs the North Strike.** *A Republic on the Amur* fires only for a Japan that took the North Strike at the Five Ministers conference (DH Full event 1330120019 sets the flag `JAP_NorthStrategy`). That Japan usually strikes at once (AI 55%), and otherwise masses on the Amur.
- **The national events** are now scheduled exactly 7 days after founding, using DH's delayed event command (`type = event ... where = TAG when = 7`), instead of being left to the event trigger.

## Changes in v41: the buffer states come alive

- **Cabinets:** both states install their own cabinet on founding. The ministers have fitting personalities and the right ideology: the Cordon is Stalinist, and the Far Eastern Republic is Leninist, like the 1920 original. Each minister has a reserved portrait name (see ASSETS.md, Priority 7).
- **Starting armies** (added with `add_corps` / `add_division`, as vanilla Japan does for Mengkukuo):
  - **Special Cordon Corps** at Irkutsk: two rifle divisions and two militias.
  - **People's Revolutionary Army** at Chita: a rifle division, Amur partisans and Ussuri Cossacks.
  - **Primorye Group** at Vladivostok: a rifle division and the workers' militia.
- **National events** about a week after founding:
  - *Who Holds the Cordon* (UA1): the cordon men who guarded the "anthrax quarantine".
  - *The Republic Remembers* (UA2): Volochayevka, 1922, and the old partisans.
- **Japan's reaction, *A Republic on the Amur*.** The Kwantung Army sees the road north open. Japan can prepare, which sets `res_jap_north` and sours relations, strike at once, or let the Russians and the creatures bleed each other.
- **Fixed:** the two states' ministers used the code for social liberal instead of Stalinist or Leninist.

## Changes in v40

- **Fix: "Abandon the East" did nothing.** DH can only release a country that `db/revolt.txt` defines, and UA1 and UA2 weren't in it. The mod now ships DH Full's `revolt.txt` with two entries added. Each state needs only one of its provinces in Soviet hands (`min = 1`), and only the USSR can release them. The decision now releases each state, makes it a puppet and hands over the rest of its provinces, the same order vanilla uses for Soviet Poland.

## Changes in v39

- **Siberian Cordon Administration flag and shield** (`flag_ua1.bmp`, `shield_ua1.bmp`): a red field inside a broad white border (the cordon), with a gold shield and an upright sword after the security troops' badge. Drawn by `build/flags.py`.

## Changes in v38

- **Far Eastern Republic flag and shield** (`flag_ua2.bmp`, `shield_ua2.bmp`), drawn pixel by pixel at DH's own sizes: red, with a square blue canton bearing Д В Р. The flag strip reuses the cloth shape of the 25 frames of the Chimera flag. `build/flags.py` makes them.

## Changes in v37: Angels and Thralls

- **Angel Nexus HQ** (HQ model 6). It is as fast as the Hybrids, burns no fuel and carries no horses or vehicles. Every Hive army starts with one, six in all.
- **Thrall Horde** (militia model 10): cheap converted humans. They replace the human 1945 militia model in the Hive's starting armies.
- **The Tunguska Strain** now unlocks both. It also removes the human 1942 infantry and the old militia from the Chimera's build list.

## Changes in v36: the abandoned East

- **New decision, Abandon the East.** It becomes available once the Hive holds Krasnoyarsk. It costs +5 dissent and hands everything east of the Yenisei to two Soviet puppet states, created at war with the Hive:
  - **Siberian Cordon Administration** (`UA1`, capital Irkutsk): Krasnoyarsk east of the river, Irkutsk with Tayshet and Cheremkhovo, and Yakutia.
  - **Far Eastern Republic** (`UA2`, capital Chita, as in 1920-22): Transbaikalia, the Amur, Khabarovsk, Primorye, Kamchatka and Magadan.
- **What happens on release:** each state gets 150 manpower and 3,000 supplies. The cordon garrisons inside the zone are disbanded, since they would otherwise be stranded in a foreign country.
- **Infection and occupation:** both states get their own AI-only infection events (9507000+) and occupation events (9508000+). Moscow no longer gets infection events for those provinces.
- **Tower sites:** when the tower at Krasnoyarsk, Irkutsk or Khabarovsk falls, the provinces in the buffer states go back to them, not to Moscow.
- **Return to the Union:** if the Hive is destroyed, the USSR takes both states back and gets -5 dissent.

## Changes in v35

- **The dissent cut is reworked.** Purging an infected town costs 2 dissent instead of 3 once both of these are true:
  - **The Great Purge has happened.** It can't happen during the war, so it has to come before 1937, either early through the NKVD or by vanilla chance in 1936.
  - **The USSR prepared in at least one way:** the army was warned by military intelligence, the meteorologists' warning was heeded, or Sorokin was spared.

  The Inhibitor Serum requirement is gone, because DH won't let anyone research a tech more than about two years early.
- **Research component** renamed back to Chimeran Biology.

## Changes in v34

- **The sanitary dissent cut** (purging a town costs 2 dissent instead of 3) now needs Inhibitor Serum Trials as well as Sorokin spared. Quarantine Protocols comes free with the Academy expedition, so it was no real hurdle.
- **Chimeran Biology** (`rt_user_1`) is now the main component of the pathology line: 2 of 5 components in Quarantine Protocols, 3 in Inhibitor Serum Trials and 2 in Mass Inoculation. Sorokin's laboratory is now the obvious team for them.
- **No more horses:** the Chimera no longer start with human field artillery, which was drawn by horses. Spire Launchers now evolve in September 1936 instead of 1939, so the Hive has artillery before the outbreak.
- **OGPU and NKVD names follow the real dates.** The OGPU ran the secret police until July 1934, when it was folded into the NKVD.
  - The 1933-34 events use the OGPU: the Closed Zone file (now from the Secret Operational Directorate), the expeditions, and the interception of Sorokin's letters.
  - The December 1935 report comes from the NKVD's Main Directorate of State Security, or from the Intelligence Directorate of the RKKA General Staff.
  - The cordon garrisons no longer carry an NKVD prefix, since they exist from 1933.

## Changes in v33: command and air

- **Clone commanders:** the Hive now has 53 leaders, in tiers of identical clones.
  - 8 × The Overmind (field marshals, skill 4)
  - 16 × Hive Node (generals, skill 3)
  - 24 × Swarm Node (lieutenant generals, skill 2)
  - 4 × Spire Node (air)
  - 1 × Deep Node (navy)
  Before this the Hive had no field marshals at all and only eight land leaders, so its armies ran into the command limit.
- **Earlier fighters:** Dropships and Fighters now evolve in June 1938 instead of 1944, and the tech requires Bio-mechanics instead of Stalkers.
- **Chimera AI air mix:** interceptor weight is up from 6 to 10. The land weights drop to infantry 46, Leapers 20 and thralls 16, so the total is still 100.

## Changes in v32

- **Checkpoint 14:** choosing "Replace the garrison" now keeps the post's division, manned by fresh men. Only pulling the cordon back removes it.
- **Cordon strengths:** the five small posts (Checkpoint 14, Ust-Kut, Bratsk, Nyurba and Bodaybo) are capped at 5%, about 500 men. The five detachments stay at 15%, about 1,500 men.
- **Military police:** every cordon garrison has a police brigade (Police 1921), the NKVD's own troops. They are good at suppressing partisans, and they add to the numbers shown.
- **Locked garrisons:** the cordon units are locked in place (`locked = yes`), like DH's Hong Kong and Singapore garrisons. A locked unit can't retreat, so it is lost with its province when that province is handed to the Hive: Krasnoyarsk at the outbreak, or any province abandoned to infection.

## Changes in v31: load errors fixed

- **Chimera AI:** the unit mix now adds up to exactly 100, as DH requires. Land is 86 (infantry 48, Leapers 22, thralls 16) and air is 14 (fighters 6, dropships 5, battleships 3).
- **Event dates:** no event date uses day 30 or 31 any more, because DH months only run from 0 to 29. The event helper clamps them.

## Changes in v30

- **Cordon garrisons** are capped at 15% (`max_strength = 15`), so they no longer refill.
- **Meteorologists:** if you kept them measuring in 1933, they warn you in late November 1936 that the cold front is heading for Krasnoyarsk. Alerting the Siberian District costs 500 supplies and 5 manpower. At the outbreak it gives +50 manpower and 2 less dissent.
- **Tower sites can no longer be lost to infection.** Abandoning one while troops were inside let them walk back in and kill the newly risen Angel. The Hive now has to take tower provinces by force.

## Changes in v29: the NKVD, Sorokin and the Purge

- **Cover-up choices** now feed the NKVD: sealing the zone, refusing the Academy, detaining the Evenki, blaming the weather, removing the Krasnoyarsk secretary, and silencing Sorokin. Three or more and the NKVD takes the lead.
- **A report on the Closed Zone arrives in December 1935.** It collates every pre-1936 sign into one inference: either nothing, or something very bad by about mid-1937. Who sends it depends on your choices so far:
  - **The NKVD** (three or more cover-ups): let the Organs proceed and the Great Purge comes early, in spring 1936, before the Hive. Restraining them costs +3 dissent.
  - **Military intelligence** (fewer than three): you can prepare the Siberian District quietly for 2,000 supplies and 10 manpower. At the outbreak that gives +100 manpower and Anti-Hybrid Tactics.
- **The Great Officer Purge waits** while the Hive is at war with the USSR. A notice event says so. It can still come once the Hive is beaten.
- **Academician Sorokin:** if the Academy expedition went in, one survivor leaks the truth through Barentsburg on Spitsbergen. His letter reaches Britain either way.
  - **Silence him:** a cover-up. Britain only gets rumours.
  - **Spare him:** +3 dissent. In return the **Sorokin Laboratory** research team joins the USSR, and Britain gets Quarantine Protocols. **Sanitary protocols** also cut the dissent for purging an infected town from 3 to 2.
- **New research component "Chimeran Biology"** (`rt_user_1`). It appears in the Captured Pathology techs. Among Soviet teams, only the Sorokin Laboratory has it.
- **NKVD cordon garrisons** at 15% strength guard the Closed Zone in 1933. Checkpoint 14 and the four quiet-spread posts vanish with their events.

## Changes in v28: land doctrine fixes

- **Hive Mind Coordination** now requires the Tunguska Strain, which only the Chimera can get. Other nations, including the USSR, could research it before.
- **Leading by Task and Leading by Orders** now sit side by side. The Hive Warfare column moved right, so it no longer covers Leading by Orders.

## Changes in v27: event pictures and interface skin

- **Event pictures:** the eight most-seen groups now have their own picture: conversion, silent towns, salvage, specimens, towers rising and falling, the Chimera arriving, and surges. That covers 838 of the 1,605 events. The rest still show the newspaper until their pictures arrive.
- **Interface skin:** the Chimera skin is in `gfx/SKINS/UA0/` and shows only when playing UA0.
- **Folder fix:** the event picture folder is `gfx/events_pics/`. Earlier notes said `event_pics`.

## Changes in v26: event picture slots

- **Picture names:** every event now has a picture name reserved, grouped into 26 pictures (`res_conversion`, `res_silent_town` and so on).
- **Automatic switch:** an event shows its picture as soon as a BMP with that name is in `src/assets/gfx/events_pics/`. Until then it keeps the vanilla newspaper.
- **The list** of pictures, with suggested subjects, is in `ASSETS.md`, Priority 6.

## Changes in v25: the Hive's cabinet

- **Minister portraits:** all ten are in the mod, in `gfx/interface/pics/M1500001-M1500010.bmp`.
- **Minister personalities:** each one fits its post. Spellings come from DH Full's own personality list.
  - The Hive: Ruthless Powermonger
  - The Hive Mind: Silent Workhorse
  - The Silence: Iron-fisted Brute
  - Conversion Chambers: Infantry Proponent
  - The Choir: Prince of Terror
  - The Watchers: Technical Specialist
  - The Overmind: School of Mass Combat
  - Swarm Coordinator: Decisive Battle Doctrine
  - Deep Spawn: Indirect Approach Doctrine
  - Spire Coordinator: Army Aviation Doctrine

## Changes in v24: portrait slots

- **Portrait names:** every Chimera minister, leader and research team now has a reserved picture name (`M1500001`, `L1500101`, `T1500201` and so on).
- **Automatic switch:** the generator uses a custom portrait as soon as a file with that name is in `src/assets`. Until then it keeps the vanilla placeholder.
- **The list** of portraits, with suggested pictures, is in `ASSETS.md`, Priority 5.

## Changes in v23: first art

- **Chimera flag:** option 1 (navy and amber stripes with the Spire), in `gfx/map/flags/flag_ua0.bmp` and `gfx/map/shields/shield_ua0.bmp`.
- **Infantry pictures:** icons and illustrations for Hybrid Swarm (1933), Advanced Hybrid Swarm (1942) and Steelhead Swarm (1950), in `gfx/interface/models/`. Each comes as a `UA0_` version and a generic version.
- **The generator** now copies anything in `src/assets/` into the mod unchanged.
- **`ASSETS.md`** lists every Chimeran unit and brigade that still needs art, with type and model numbers.

## Changes in v22: the 1933–34 prelude

The opening is now a staggered chain told from inside a cover-up that has run since 1926. Until July 1934 the secret police is the OGPU, as it was historically.

| Date | Event | Choices |
|---|---|---|
| March 1933 | **The Closed Zone** (rewritten). The Lubyanka file: an "anthrax quarantine" since 1926, villages emptied, patrols coming back with too many eyes, a burned 1927 vaccine trial at Tomsk, and a cordon of 30,000 men that moves south every spring. | Seal it tighter, or send an OGPU expedition (which never returns). |
| May 1933 | **Checkpoint 14 Does Not Report.** A cordon post on the Yenisei is found empty, the stove still warm. | Re-garrison (−5 manpower), or pull the cordon back (+1 dissent). |
| July 1933 | **The Evenki Exodus.** Herders cross the cordon at night, telling of shamans turned into demons (canon Evenki lore). | Detain them (+1 dissent), or resettle them in Kazakhstan (+2 manpower). |
| September 1933 | **The Academy Asks for Permission** to visit the 1908 impact site. | Refuse (+1 dissent), or allow it under escort. If allowed, **The Academy Expedition Returns** with samples: 2 of 11 scientists survive and the USSR gains the Quarantine Protocols tech. |
| October 1933 | **Winter Comes Early.** The Yenisei freezes in October; the cold comes from the Zone (canon: the Chimera cool their surroundings). | Blame the weather, or keep measuring. |
| February 1934 | **The Krasnoyarsk Secretary Asks Questions.** | Remove him (−1 dissent), or tell him the truth (+10 manpower, and +50 more manpower when the Outbreak comes). |

From August 1934 the quiet-spread events (Ust-Kut, Bratsk and so on) follow as before. Most of the prelude events only fire before the outbreak.

## Changes in v21: Hive Warfare doctrine and no more horses

**Hive Warfare** is a Chimera-only land doctrine line in the empty column (x=346) of the land doctrine screen. It's locked behind event 9500003 and only opens for a country that owns the Tunguska Strain. Every effect command is copied from vanilla doctrines.

| Tech | Year | Effects | Lore |
|---|---|---|---|
| Hive Mind Coordination (95510) | start | land max org +6, delay −8 | hive-mind command |
| Swarm Assault (95520) | 1936 | plain +8, forest +6, urban +6 attack, breakthrough +5 | Hybrids in packs "almost unstoppable" |
| Overwhelming Numbers (95530) | 1939 | land max org +4, morale +5 | numbers and conversion |
| Siege of the Cities (95540) | 1942 | fort +10, urban +6 attack | Goliath siege batteries, Spires |
| Primarchs and Overseers (95550) | 1950 | land max org +8, morale +5, HQ supply efficiency +3 | canon's 1951 command reform under Daedalus |

The Chimera start with 95510. The rest arrive through evolution events 9500022–025, so they don't depend on research.

**No more horses.** Unit equipment lists come from the vanilla models, and the Chimera were still using vanilla artillery and AA brigades, which list horses. They now have their own brigade models:

| Brigade | Model | Unlocked by | Stats | Human comparison |
|---|---|---|---|---|
| Chimeran AA Turrets | anti-air 7 | Tunguska Strain | air attack 6, no fuel | 1956 human AA brigade: air attack 6 |
| Spire Launcher Battery | artillery 14 | Spire Launchers (1939) | soft 9, hard 3, no fuel | 1955 human artillery: soft 9, hard 3 |

Both list only manpower as equipment. Thralls still use vanilla militia models, which list horses. Sending `db/units/divisions/militia.txt` would let me give them a Chimeran model too.

## Changes in v20: the Hybrid page and the Chimeran air fleet

**Hybrids.** The wiki says a second heart and an enlarged brain stem let them "function despite massive trauma", that their fire is inaccurate, and that "Hybrids that gang together are almost unstoppable". Hybrid models now favour toughness over firepower and are cheap to mass:

| Model | Soft attack | Toughness | Cost | Build time | Manpower |
|---|---|---|---|---|---|
| Hybrid Swarm (1933) | 16 | 54 | 4 | 220 | 9 |
| Advanced Hybrid Swarm (1942) | 19 | 58 | 4 | 220 | 9 |
| Steelhead Swarm (1950) | 22 | 62 | 4 | 220 | 9 |

Human 1942 infantry, for comparison: soft attack 13, toughness 40, cost 5, build time 290, manpower 13.

**The Hive Learns** (9506000+, in `res_towers.txt`). Hybrids "are quick to learn the methods of their adversaries". Twice a year from 1937, the Hive steals one tech from each major power it's at war with, using vanilla's `steal_tech` command.

**The Chimeran air fleet.** Two new Chimeran Engineering techs fill the last two rows of that column. None of the aircraft use fuel.

| Tech | Year | Unlocks | Key stats | Human comparison |
|---|---|---|---|---|
| Dropships and Fighters (95150) | 1944 | Chimeran Fighter (interceptor 17) | air attack 11, speed 950, air defence 6 | 1944 human jet: air attack 9, speed 850, air defence 5 |
| | | Dropship 'Buzzard' (CAS 7) | soft 6, hard 4, air defence 20 | 1948 human CAS: soft 6, hard 6, air defence 8 |
| The Chimeran Fleet (95160) | 1950 | Chimeran Battleship (strategic bomber 10) | strategic 14, soft 8, air attack 6, air defence 40, speed 300, range 6000 | 1958 human intercontinental bomber: strategic 14, air defence 8, speed 800 |
| | | Chimeran Fighter II (interceptor 18) | air attack 14, speed 1200 | 1950 human interceptor: air attack 11, speed 1100 |

- **Lore basis:** fighters "could easily take on modern day fighter planes, particularly the F-86 Sabre"; dropships are "better armoured than equivalent human aircraft"; battleships are as large as the towers and carry Spire missiles and hundreds of fighters.
- **Delivery:** both techs reach the Chimera through evolution events (9500020 in June 1944, 9500021 in March 1950).
- **AI:** builds interceptors 6, CAS 5, strategic bombers 3, and builds air bases at the tower cities.
- **Names:** `models.csv` names the new aircraft for the Chimera, and as "Captured …" for a Cloven USSR.

## Changes in v19: towers and Angels (lore from the Angel, Goliath and Operation Morning Star pages)

In the lore, Angels hold the hive mind together from inside the Chimeran towers. When the London tower fell, every Chimera in Britain died within minutes, and that was humanity's first victory. `db/events/res_towers.txt` brings this into the 1933 scenario. There is one tower per Soviet region: Norilsk (the Hive Heart), Novosibirsk, Irkutsk, Tomsk, Sverdlovsk, Ufa, Kazan, Moscow, Kiev, Minsk, Tashkent, Alma-Ata, Khabarovsk, Baku and Stalingrad.

- **A Tower Rises** (9505000+): when the Hive owns a tower city, an Angel moves in. The city gets a level-3 fort and +20 infrastructure, and the Hive +50 manpower.
- **The Tower Has Fallen** (9505100+): if an enemy takes a tower province, the Hive cedes **every province it owns in that region** back to the USSR and loses 300 manpower. The USSR gets "The Angel Is Dead" (−5 dissent, +50 manpower).
- **AI:** the Chimera AI gives the towers top garrison priority. The Soviet AI's Urals and Volga switch files now target them.
- **HQ divisions:** Chimera HQs are named "Angel Nexus" (models.csv, HQ unit type 10), and the HQ names list now reads "1st–30th Angel Nexus".

Each tower can rise and fall once. This gives a human player a real way to win other than grinding: punch through to a tower and the whole region collapses.

## Changes in v18: why the Hive stalled in 1940 (supply and occupation)

- **Occupied land becomes Hive land.** `db/events/res_occupation.txt`: when the Hive controls a Soviet province, a Soviet event (checked every 30 days) cedes it to the Chimera, so it doesn't stay Soviet-owned until a peace that never comes. A matching Chimera event then builds +40 infrastructure there and adds a little manpower. Moscow is excluded while it's the Soviet capital. Before this, conquered provinces stayed Soviet-owned, so the Hive couldn't repair their infrastructure (wrecked by Scorched Earth and the fighting) and got no manpower, factories or resources from them.
- **The capital moves west.** DH traces supply back to the capital, which was Norilsk in the Arctic. The capital now moves to Krasnoyarsk, Novosibirsk, Sverdlovsk, Kazan and finally Moscow as the Hive comes to own each one (+30 infrastructure at each new capital).
- **Harvest.** Monthly manpower is up from 20 to 60 and supplies from 1000 to 1500, before the yearly multipliers. This makes up for losses of around a million men.

## Changes in v17: lore from the Chimera, Chimeran War and Stalker wiki pages

- **Stalkers are anti-aircraft walkers.** The intel describes a "mobile heavy weapons platform" with an AA autocannon, a missile pod and an anti-personnel gun, saying that "a single Stalker can make friendly air support over a battlefield impossible". The Stalker brigade now has air attack 6 (the 1956 human AA brigade has 6), with soft 6, hard 6, def +1, tough +1 and speed cap 8. This is the lore answer to massed CAS.
- **Goliaths are siege batteries.** They're the walkers that crushed the German armour on the Oder: soft 16, hard 16, def +2, tough +2, speed cap 5.
- **Heat weakness.** Chimeran metabolism needs cooling implants, and before 1951 the Chimera can't cope with heat. Hybrids and Leapers now get −3 desert attack and −3 desert defence from the Tunguska Strain, removed by the Apex Strain (1950), matching the canon heat-adapted strains of 1951. `desert_defense` is a vanilla command; `desert_attack` is assumed by analogy.
- **The Cloven, closer to canon.** In canon, Malikov's 1927 vaccine turned almost 90% of the inoculated soldiers into feral cannibals by 1930, which left Russia defenceless.
  - **Cloven Madness** now costs −150 manpower and +3 dissent (isolate them), or +8 dissent (unleash them).
  - Unleashing them leads to **The Cloven Desert** (9500423), 120 days later: −200 manpower and +5 dissent (hunt them down), or +10 dissent (let them roam).
  - The Cloven Red Army is still possible, but it's a gamble.
- **The United European Defence** (9500770). When the Hive breaks out of Russia, Britain can form the UED, allying with every European nation it isn't at war with (France, the Low Countries, Poland, Czechoslovakia, Scandinavia, Switzerland, Austria, Germany, Italy). The alternative is "Britain will look after Britain" (canon's Avalon One refugee policy), which sets a flag for later events.

## Changes in v16: units checked against Resistance lore

- **Stalkers:** the lore says they're slower than human vehicles and less armoured than a human tank, but heavily armed. They're now speed cap 6 (was 8), toughness −2 and defence 0 (were +2/+2), with the same soft 8 / hard 10.
- **Goliaths:** the giant walkers now hit harder (soft 14, hard 18) and are even slower (speed cap 5).
- **Titans (new):** giant Chimera carrying Stalker-grade guns, protected by thick hide rather than armour. Heavy-armour brigade model 6, unlocked by Heavy Hybrid Breeds (1946): soft 6, hard 6, def +1, tough +1, no fuel. The human 1945 heavy tank brigade is soft 3, hard 6, def/tough −4, fuel 4.6.
- **Widowmakers (new):** the Fall of Man "main battle tank" strain. Medium-armour brigade model 11, unlocked by Adaptive Strain (1936): soft 6, hard 5, speed cap 10, no fuel. The human 1948 medium tank brigade is soft 6, hard 4, fuel 3.3.
- **Hybrid generations renamed** after the Fall of Man strains: Hybrid Swarm (1933), Advanced Hybrid Swarm (1942), Steelhead Swarm (1950).
- **Leapers stay** as fast, fragile swarm cavalry. In lore they were bred to hunt down hiding humans, and later went feral.
- **AI brigade mix:** Stalkers/Goliaths 20, Titans 15, Widowmakers 15, plus artillery and AA.

## Changes in v15: Chimeran unit models

DH's unit stats in `db/units` are shared by every country, so the Chimera get **new models appended to three unit types**. Only Chimeran techs unlock them, plus the Cloven decisions for the USSR. All of them use **no fuel** and little supply.

| Unit | Model | Unlocked by | Key stats | Human comparison |
|---|---|---|---|---|
| Hybrid Swarm Gen. I | infantry 18 | Tunguska Strain (start) | soft 18, hard 5, def 45, tough 50, org 40, morale 60, airdef 18, speed 7 | 1942 infantry: 13 / 4 / 35 / 40 / 30 / 30 / 14 / 6 |
| Hybrid Swarm Gen. II | infantry 19 | Advanced Hybrids (1942) | 21 / 7 / 48 / 54 / 45 / 65 | 1951 infantry: 14 / 6 / 35 / 40 / 30 / 30 |
| Hybrid Swarm Gen. III | infantry 20 | Apex Strain (1950) | 24 / 9 / 52 / 58 / 50 / 70 | 1962 infantry: 16 / 7 / 35 / 40 / 30 / 30 |
| Leaper Swarm Gen. I | cavalry 15 | Adaptive Strain (1936) | speed 12, soft 16, def 25, tough 30, org 40, morale 60 | 1942 mech cavalry: speed 23, soft 15, def 20, tough 26, 7.5 fuel |
| Leaper Swarm Gen. II | cavalry 16 | Heavy Hybrid Breeds (1946) | speed 13, soft 20, hard 4, def 28, tough 34 | |
| Stalkers | super-heavy armour 2 | Bio-mechanical Engineering (1937) | soft 8, hard 10, org +10, supply 0.6 | best human super-heavy (1944): soft 7, hard 10, supply 4.6, fuel 5 |
| Goliaths | super-heavy armour 3 | Goliath Walkers (1946; was "Leviathan Class") | soft 12, hard 16, def +4, tough +4, org +15 | |

- **Strains.** Now that the models carry the strength, the strains' flat bonuses are modest again (+1 here and there). The unconfirmed `air_defense` command is gone.
- **Human infantry evolution events** (Hybrid Generation II–VII) are removed. Human infantry models now sit below the Hybrid models.
- **AI build mix:** 55% Hybrid infantry, 25% Leaper cavalry, 20% thralls, with Stalker/Goliath, artillery and AA brigades.
- **Names.** `models.csv` names the new models for the Chimera and, for the Cloven, the USSR ("Cloven Rifle Division", "Cloven Shock Division", "Captured Stalkers"). Super-heavy armour is brigade 9 in `models.csv`. The unit file's header says 35, but `models.csv` uses 35 for super-heavy artillery.
- **To edit the stats:** change the tables in `units.py` and rebuild.
- **Not yet checked in game:** whether DH accepts extra models on a unit type. If it refuses, `savedebug.txt` will say so.

## Changes in v14: the Cloven

`db/events/res_cloven.txt` covers what happens if the USSR holds the Hive, or destroys it.

- **Decision: The Cloven Programme.** Available to the USSR while it's at war with the Chimera and has researched Inhibitor Serum Trials (95320). The USSR gains the Hive's own **Tunguska Strain**, so its infantry gets the same bonuses as the Hybrids. Cost: −30 manpower and +3 dissent.
- **Cloven Madness**, 180 days later. Isolate them (−50 manpower, −2 dissent) or unleash them (+4 dissent).
- **Decision: Expand the Cloven Divisions.** Needs Mass Inoculation (95330). The USSR gains **Adaptive Strain** and **Rapid Conversion**, the latter making infantry cheaper in manpower. Cost: +4 dissent and −50 manpower.
- **The Hive Is Destroyed.** Fires if the Chimera cease to exist after the outbreak. The USSR either seizes the alien technology (Bio-mechanical Engineering, so Soviet Stalkers, plus the Tunguska Strain and the pathology trees) or burns it all (−10 dissent). Germany, Britain and the USA each react.

All the strains boost infantry and militia, so a Cloven Red Army turned on Germany is the "alien-influenced Red Army" play.

## Changes in v13 (the Hive ran out of resources)

- **The Hive Harvest.** `db/events/res_harvest.txt` has 369 monthly events, April 1933 to December 1963. Each one gives the Chimera energy 5000, metal 2500, rare materials 1250, oil 400, supplies 1000 and manpower 20, scaled up over time: ×2 from 1937, ×3 from 1942, ×4 from 1947. Each month also adds a bonus while the Hive controls Sverdlovsk, Chelyabinsk, Novosibirsk, Moscow, Leningrad, Kiev, Warsaw, Berlin or Paris. All the events share one text entry. The amounts are in `HARVEST_BASE`, `HARVEST_TIERS` and `HARVEST_BONUS` in `story.py`.
- **Starting stockpile.** The Chimera now start with energy 40000, metal 20000, rare materials 10000, oil 5000 and supplies 10000, enough to run the Hive Heart's 50 IC until the harvests take over.
- **Unconfirmed commands.** `oilpool` is used by vanilla. `energypool`, `metalpool` and `rarematerialspool` follow the same naming but are unconfirmed, so check `savedebug.txt` for unknown-command errors.

## Changes in v12 (the Red Army still won)

- **Infection behind the lines.** `db/events/res_infection.txt` has 282 events, one per Soviet province. When the USSR is at war with the Chimera and the Hive controls a neighbouring province, the province can be lost to infection. Each province is checked every 60 days. The USSR either abandons it to the Hive or purges it (−25 manpower, +3 dissent). Each event fires at most once per province. This is how the Hive is meant to win: it converts behind the lines rather than only beating the Red Army in the field.
- **Economy.** The Hive Heart now gives 50 IC (was 20). The Chimera start with 600 manpower (was 150), and each quiet-spread conversion gives +50 manpower and +3 IC.
- **Anti-air.** The Chimera start with static and brigade anti-air techs, and the AI builds AA brigades (20%), so massed CAS no longer flies unopposed.
- **Strains.** The Tunguska Strain is now +4 toughness, +3 defence, +2 soft attack and +2 air defence for Hybrids, and +3 toughness and +2 defence for thralls. Adaptive Strain and Advanced Hybrids went up too.
- **Unconfirmed commands.** `soft_attack` and `air_defense` don't appear in any vanilla file I've seen. If `savedebug.txt` reports an unknown command, or the tech tooltip shows no effect, tell me and I'll swap them.

## Changes in v11

- **Chimera names lists.** `db/unitnames.csv`, `armynames.csv`, `airnames.csv` and `navynames.csv` are your vanilla files with Chimera lists added at the end: 300 Hybrid Swarms, 200 Thrall Hordes, 30 Hive Overminds (HQ), 50 Sentinel Nodes (garrison), 100 Hive Broods (armies), 20 Spire Flights and 20 Deep Spawns. Divisions the Chimera AI builds now get proper names. The starting army uses names from these lists ("1st Hive Brood", "1st Hybrid Swarm", "1st Thrall Horde"...), which also stops the "not found in names list" notices in savedebug.txt.
- `config/unit_names.csv` holds the generic unit-type names ("Infantry", "Militia"...) shared by every country, so the mod leaves it alone.

## Changes in v10

- **Tech tree labels.** DH Full gives every tech a second, short label (`SHORT_TECH_APP_..._NAME`), which is the text in the tree boxes. The mod's 21 techs now have short labels as well, which was probably the remaining UNKNOWN_STRING.
- **Chimera unit names.** `config/models.csv` (your de-duplicated copy) now names the Chimera's models: infantry models 11–17 are "Hybrid Swarm Gen. I–VII", lining up with the Hybrid Generation evolution events; militia 6–9 are "Converted Thralls Gen. I–IV"; artillery brigades are "Spire Launchers"; heavy and super-heavy armour brigades are "Stalkers and Leviathans". The unit-type numbers (0 = infantry, 11 = militia, 9 = super-heavy) are inferred from savedebug.txt and `models.csv`, so if a name doesn't appear in game, tell me which.
- **Artillery.** The Chimera now start with WWI field artillery (2290–2920), so the AI can actually build the Spire Launcher brigades it wants.

## Changes in v9

- **Tech names.** The 131 tech strings are now in `config/tech_names.csv` (your file with the mod's rows added before `#EOF`), so the tech screen should show real names instead of UNKNOWN_STRING.
- **The Hive is a decade ahead.** In 1933 Hybrids are 1942-level infantry (model 11) and thralls 1942-level militia (model 6). Evolution then hands out the 1945, 1948, 1951, 1954, 1958 and 1962 infantry techs in 1936, 1939, 1942, 1945, 1948 and 1951, so the Chimera stay 10–14 years ahead. The strain bonuses come on top.

## Changes in v8 (from your first SOV playtest)

- **Chimeran techs leaking to the USSR.** The tree-unlock events were "invention" events, which DH checks for every country, so the USSR (and probably everyone else) got the Chimeran trees. They're now ordinary country events. The Chimera trees only unlock for a country that owns the Tunguska Strain, which only `UA0` starts with. The captured-tech trees unlock per nation when that nation is at war with the Chimera. Old saves keep the leaked techs; start a new game.
- **The Hive was too weak.** Hybrids now start at infantry model 8 and thralls at militia model 4, the same level as the 1933 Red Army, instead of 1922 models. The evolution schedule also hands the Chimera the next five infantry techs (1936, 1939, 1942, 1945, 1948), so they keep pace. The strain bonuses are roughly doubled.
- **State Defense Committee.** The vanilla event (2007041) is blocked while the USSR is fighting the Chimera. A Chimera version, "The State Defence Committee" (9500709), replaces it with the same effect: Stalin takes over as head of government.
- **Tech names showing UNKNOWN_STRING.** Not fixed yet. The tech screen seems to read only `config/tech_names.csv`. The generator now adds the 131 tech strings (tech names, component names and column labels) to that file automatically once it has a copy.

## Changes in v7

- **AI files:** the Chimera have their own AI (`ai/chimera.ai`), plus six switch files that move both the Chimera and the Soviet AI on as the war progresses. The `.inc` now sets `ai = "chimera.ai"`.
- **`ASSETS.md`:** the art the mod needs, with formats and subjects.

## Changes in v6

- Module 3: the Soviet collapse, the breakout stages and the WWII interplay (see the timeline).
- The starting Hive is much bigger (42 divisions, 20 IC).
- 13 more nations can unlock the captured Chimeran tech trees, including Afghanistan, Manchukuo, Vichy and Free France.

## Changes in v5

- **"Critical error: illegal id-type 95000".** The Chimera's units now use id type 19500, which is in the same range as other countries' types (Britain uses 12700, the USSR 10848). Their unit numbers start at 95001, so they can't collide with another country's units.

## Changes in v4 (from the first savedebug.txt)

- **Missing deathdates.** Every dated event now has a deathdate. DH requires one whenever `offset` is used, and 14 events were missing it.
- **Chimera ministers.** These were rejected as invalid because `ministers_UA0.csv` wasn't in `db/ministers.txt`. It is now.
- **Teams list.** `teams.txt` now goes in `db/`, matching where you moved it.
- **Quiet spread.** Surgut doesn't border Norilsk, so it would have been a cut-off enclave. Bratsk replaces it. The generator now checks every province the Chimera are handed against the real adjacency map from your log (`adjacency.json`).
- **Confirmed by the log:** the tech file, both event files and all the text in `mods.csv` load cleanly. The game found every text key and reported no unknown commands.

## Coming next

- What the Chimera do after Siberia: the Urals, Central Asia, then westwards into Europe, timed against WWII.
- The peace path: a second scenario, with WWII events blocked by a `res_peace` flag.
- Soviet survival goals (evacuation and holding the Urals) and a Chimera AI file.
