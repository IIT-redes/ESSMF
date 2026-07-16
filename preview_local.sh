#!/usr/bin/env bash
set -e
python3 -m pip install -r requirements.txt
python3 scripts/build.py
python3 scripts/validate.py dist
cd dist
python3 -m http.server 8000
