# Resistance mod for Darkest Hour Full: notes for AI agents

The mod is generated, not hand-edited. Python in build/ reads vanilla DH Full files from src/ and writes the finished mod to mod/. Never edit mod/; change the generators and rebuild.

## Build
- python3 build/import_vanilla.py "<DH Full 1.05.2 folder>" copies the vanilla files into src/ (they aren't in the repo).
- sh build/package.sh N builds and zips. Number builds upward and add a "## Changes in vN" section at the top of build/README_RESISTANCE.md.
- Requirements: Python 3, Pillow, numpy.
- build/validate.py runs during the build and must pass. It checks event ids, commands against vanilla usage, provinces and text.

## Layout
- gen.py: the entry point. Techs, units, text, pictures.
- One module per story arc: story.py (outbreak, scenario, Soviet events), breakout.py, cordon.py, burrowers.py, refugees.py, milestones.py, fall_of_europe.py, and others.
- ai.py: AI switch files.
- units.py, hive_research.py: Chimeran units and the tech plan.
- src/assets/: the mod's own art, copied as-is. src/tech_raw/: tech picture originals, rendered by tech_pictures.py.

## Rules
- Event ids: the mod uses 9500000-9599999. Check free ranges before adding (fall_of_europe uses 9590000+).
- Read build/DH_FACTS.md before relying on any engine behaviour. Record new assumptions there with a way to test them in game.
- Art formats: build/ASSETS.md and DH_FACTS.md. All BMPs are 24-bit. Tech pictures 344x266, unit pictures 192x104, event pictures 400x116 via the banner mask, portraits 36x50, research team pictures 96x96.
- Country tag UA0 is the Chimera. UA1 and UA2 are buffer states. Free France in DH Full is U01.
- Event text is in plain English, with no semicolons in event text.
