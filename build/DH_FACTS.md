# What we know about DH Full, and how we know it

Rule: nothing goes into the mod as a fact unless it is in the **Confirmed** table. Anything used from
the **Assumed** table is listed in the release notes as "check in game", and moves up once a playtest settles it.
`validate.py` enforces the parts that can be checked automatically (`dh_facts.json` holds its lists).

## Confirmed

| Fact | How we know |
|---|---|
| Months run day 0–29; day 30/31 is an error | savedebug error, v31 |
| An AI file's unit mix (land + air + naval) must add to exactly 100 | savedebug error, v31 |
| Defensiveness, toughness and air defence are **vulnerabilities**: lower is better. Brigades lower them with negative values | DH text ("Defensive / Offensive / Air Vulnerability"); vanilla militia and cavalry values; your observation, v50 |
| `gain_tech` gives a blueprint, not the tech | your observation, v35 |
| A tech in a tree `event` box can't be researched until an event `activate`s it | design of vanilla secret weapons; Hive Mind leak, v28 |
| `invention = yes` events fire for every country | Tunguska Strain leak to the USSR |
| `secedeprovince` only hands over the executing country's own provinces; `secederegion` / `secedearea` take any owner's | buffer-state bug, v46–v47 |
| A province that is another country's core can be handed straight back to it; capitals are exempt | buffer-state bug; your observation, v49 |
| A country can only be released (`independence`) if `db/revolt.txt` defines it | savedebug list of revolt tags, v40 |
| Map colours come from `db/country.csv`; `config/country.csv` alone does nothing for colour | your observation, v48 |
| In `country.csv`, filling the three "model nationality" columns crashes the game at setup | crash, v47 → v48 |
| Minister personalities must match DH's names; an unknown one is a critical error (the minister falls back to generic) | 'Armored Spearhead Doctrine', v45 |
| Ministers/teams files can be split: a second file for the same tag works | `teams_SOV_res.csv` (Sorokin), `ministers_SOV_res.csv` |
| Every new model needs a generic name in `config/unit_names.csv`, or other countries see STRING_WANTED | savedebug model list, v50 |
| `add_corps` / `add_division` / `build_division` create units by event | vanilla Japan, Manchukuo, AI files |
| `province_keypoints which = PROV value = N` changes a province's VP (relative) | vanilla USSR.txt (Odessa, Omsk) |
| `action = { trigger = { ... } name = ... }`: an option shown only while its trigger holds | DH dev diary 13 (documented; first used in v59, not yet seen in game) |
| `type = event which = ID where = TAG when = DAYS` schedules an event | vanilla North Strike and AI files |
| Dormant divisions in a scenario file (`landdivision = { dormant = yes … locked = yes }`) can be woken in a province by `activate_division which = TYPE value = ID where = PROV when = 0` | vanilla UK Home Guard; vanilla AI files |
| `max_strength`, `locked = yes`, `extra = police` on scenario divisions | vanilla `united_kingdom.inc`, militia.txt |
| `rt_user_1` … `rt_user_60` research components, renamed via `RT_USER_n` | DH dev diary #18, tech_names.csv |
| Events may use command-level triggers: `command = { trigger = { … } type = … }` | vanilla USSR.txt |
| Flags (`setflag`) are global; `local_setflag` is per country | vanilla AI files |
| `type = trigger` on a vanilla event that has its own date/trigger does not force it to fire | early Purge, your observation, v55 |
| DH's savedebug "Executing event" lines are not literal firings (they list non-existent tags too) | 25 MB log, v47 |
| Air map sprites (vanilla T-FIGHTER): 108x108 frames x19, origin ~55,86 = shadow centre; palette index 0 magenta, index 1 shadow (cyan in the file); STAND + 8 WALK + 8 FIRE, L-1 only | vanilla ENG fighter files, v119 |
| 24-bit BMPs only; flags 700×18 (25 frames on pure green), shields 176×70, minister and leader portraits 36×50, research team pictures 96×96 (1px white frame), event pictures 400×116 for `style = 2` | savedebug errors; your art packs |

## Assumed (check in game)

| Assumption | Used by | How to check |
|---|---|---|
| `energypool`, `metalpool`, `rarematerialspool` add resources | Hive Harvest (monthly) | Play as UA0 and watch the stockpiles on the 1st of a month |
| `waketeam` brings in a team whose start year (1964) hasn't come | Émigré research teams (refugees) | As ENG, admit refugees at the Vistula stage; check the research teams list |
| An action with its own `trigger` is hidden while the trigger fails | Infection options (Purge, Inoculate) | Get an infection event before researching Quarantine Protocols; only Abandon should show |
| `lost_national = { country = X value = N }`: N looks like a percentage of national provinces lost (vanilla uses 10 and 35) | Cloven decision (removed v59) | - |
| `add_division` can create a model the country can't build yet (SOV infantry model 18) | Cloven decision | Take the decision; look for the Cloven Rifle Divisions |
| `deactivate` from an event locks any tech for that country, not just doctrines | Hive research lock (The Hive Heart) | As UA0, open the Infantry or Armour tab: only Chimeran and economic techs should be researchable |
| `steal_tech` can still hand over a tech the thief has deactivated | The Hive Learns | Watch for "The Hive Learns" as UA0 at war; check whether a human tech appears |
| Techs listed in a scenario's `techapps` count as known, with their models, without being researched | Hive starting techs (65) | As UA0 at start, Tribal Warfare should already show as known |
| `scrap_model` from an event removes a model from the build list | Hive start (human HQ, garrison, police, AA) | As UA0, open production: no HQ-1, garrison, MP or human AA brigade |
| A single event option may hold hundreds of commands (now split into 50s to be safe) | Hive research lock | If the lock works now but didn't in the 734-command version, record the cap |
| `activate_unit_type` also makes model 0 of that type buildable | seen: Infantry 1870 and Militia 1870 for the Hive (v59) | - |
| A tech effect `command = { trigger = {...} ... }` is checked against the researching country | model-0 scrap in Chimeran techs (vanilla does this in land doctrines) | As UA0, no 1870 models; as a Cloven USSR, nothing lost |
| For aircraft, `surfacedefence` and `airdefence` are vulnerabilities (lower is better) | human interceptor.txt 30 -> 3, strategic_bomber.txt 30 -> 8 | - |
| A dormant division line may carry a brigade (`extra = artillery brigade_model = N`) | vanilla UK Home Guard (1933 file) | - |
| `activate_division` can wake vanilla's UK Home Guard (type 12700, ids 10001-10018) in a chosen province | Dropships over Dover/Portsmouth/Norwich (v126) | Fire 9590022 as ENG, choose "Ring the bells" |
| Negative `construct` works for `anti_air` and `naval_base`, not only `land_fort` | Spire strikes, Hunters over Scapa Flow (v126) | Fire 9590223 as ENG (London); check its forts and AA |
| A dormant UA0 Hybrid division with a Spire Launcher brigade (artillery model 14) wakes correctly | Spire batteries (v126) | As UA0, take Dover; check the Spire Battery of Dover |
| `add_corps` can create a unit in a province an enemy controls | Burrowers | Watch the first wave surface at the far shore |
| `enable_task` works as a tech effect outside the air doctrines | Sea Hunters | As UA0 with Sea Hunters, a Hunter Dropship should offer Naval Strike |
| `garrison = { country = X province = P type = land size = N }` is true with at least N divisions (it can't see brigades) | DH dev diary 11; forum | Ural Line: move a division out of a line province and watch the decision grey out |
| A dormant scenario division may use a model its country hasn't researched | Okha coastal militia (SOV militia model 4) | Trigger Tremors under the Tatar Strait as SOV |
| `event = { id = X days = N }` is true once event X fired at least N days ago | Cloven Madness (180 days), Evacuation window (NOT ... 90 days) | Krasnoyarsk falls; the evacuation decision should vanish about three months later |
| A unit type with no sprite for its country's sprite nationality falls back gracefully | UA0 sprite nationality = UA0, infantry sprites only (v67) | Look at Thrall, Leaper and HQ counters on the map as UA0 |
| Each sprite level (L-n) needs its own .spr | Hybrid sprite copied to L-1..L-4 | Check Gen. I-III Hybrids all show the new sprite |
| A minister can be appointed by event before his start year, or only after | Kremlin junta (start year 1936) | Fire 9500710; check the cabinet |
| `removecore` on a Soviet core stops the hand-back to the USSR | Abandon the East, v49 | Fire 9500554; hover a released province a week later |
| `independence` + `make_puppet` on a tag with only `revolt.txt` cores creates the state | Abandon the East | Fire 9500554 |
| AI switch files only change the settings they list | Soviet "hold the Urals" switches | Play another country; watch where the Red Army stands in 1937 |
| A dormant division woken by `activate_division` stays locked, even for a country that didn't exist at its definition | Tower guards (v58) | When a tower rises, try to move one of its Sentinel Nodes |
| `sleepteam` works on a team whose start year hasn't come yet | Refusing the Academy (Sorokin) | Refuse the expedition; look for the Sorokin Laboratory in 1934 |
