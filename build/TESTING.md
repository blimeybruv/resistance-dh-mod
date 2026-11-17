# Testing the mod quickly

## 1. The log

Double-click `resistance_log.bat` in the mod folder after a session (or drag a `savedebug.txt` onto it).
It writes `resistance_log.txt` next to itself: errors, critical errors, STRING WANTED, every mod event,
and the last 300 lines of the log, which is where a crash shows. After a crash, run it before starting the
game again, because DH overwrites savedebug.txt on launch. Send that file instead of the full savedebug.txt.

## 2. Firing events directly

HoI2-family games have a console that can fire an event by number (`event <id>`), so you don't have to
play to 1938 to test something. Check that DH Full has it (open the console and try `event 9500500` on day one).
If it works, these are the events worth firing on their own:

| Event | Fire as | What should happen |
|---|---|---|
| 9500500 | SOV | The Closed Zone (start of the prelude) |
| 9500490 | SOV | Sorokin writes abroad (choose "Leave him" to test the lab and the British letter) |
| 9500492 / 9500493 | SOV | The NKVD report / the military intelligence report |
| 9500530 | UA0 | The Outbreak: war, Krasnoyarsk falls (9500531 follows) |
| 9500554 | SOV | Abandon the East: two buffer states, 39 provinces, cores removed |
| 9500703 | SOV | The Fall of Moscow; 10 days later The Kremlin Is Silent (9500710) |
| 9500420 | SOV | The Cloven Programme: Tunguska Strain becomes researchable |
| 9500430 | SOV | The Hive Is Destroyed: Chimeran Engineering opens |
| 9590000 | FRA | Paris Is Silent: capital to Algiers, Vichy chain slept (check event 2002008 never fires) |
| 9590020 | UA0 | The Dover Dropships: a Drop Brood appears at Dover (needs Calais/Dunkirk/Amiens held) |
| 9590022 | ENG | Dropships over Dover: six vanilla Home Guard divisions wake around London, Oxford, Portsmouth |
| 9590120 | UA0 | Spire Batteries at Dover: a Spire Battery division appears there (index 20 = Dover) |
| 9590223 | ENG | Spire Strike on London: forts and AA drop; the barrage repeats 30 days later |
| 9590500 | ENG | London Burns: capital moves north, Canada and the USA react |

Events fired by hand skip their triggers, so check the *results* (land, ministers, techs), not whether
they would have fired on their own.

## 3. Release checklist

The release notes list which assumptions a version relies on (see `DH_FACTS.md`, "Assumed").
Each one says how to check it; a playtest that settles one moves it to "Confirmed".
