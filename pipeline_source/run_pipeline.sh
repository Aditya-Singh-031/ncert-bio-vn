#!/usr/bin/env bash
set -e; cd "$(dirname "$0")/src"
SPEC=../specs/ch8_s82_demo.json
python3 validate.py $SPEC ../source/ch8_spans.json   # Gate: schema + evidence
python3 -c "import json;from render import render;d=json.load(open('$SPEC'));[render(s,f'../assets/{s[\"scene_id\"]}.png') for s in d['scenes']]"
python3 audio.py >/dev/null                           # cached TTS
python3 gen_renpy.py $SPEC
(cd ../renpy-8.5.3-sdk && ./renpy.sh ../build/bio_demo lint)
python3 qa.py
