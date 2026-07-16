@echo off
py -m pip install -r requirements.txt
py scripts\build.py
py scripts\validate.py dist
cd dist
py -m http.server 8000
