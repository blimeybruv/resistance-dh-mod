#!/bin/sh
# Build, validate and package: sh build/package.sh 54
set -e
cd "$(dirname "$0")/.."
rm -rf mod
python3 -I build/tech_pictures.py src
python3 -I build/gen.py src mod
cp build/README_RESISTANCE.md build/ASSETS.md build/DH_FACTS.md build/TESTING.md build/resistance_log.bat \
   build/*.py build/dh_facts.json build/provinces.json build/adjacency.json mod/
rm -f "resistance_mod_v$1.zip"
(cd mod && zip -qr "../resistance_mod_v$1.zip" .)
ls -la "resistance_mod_v$1.zip"
