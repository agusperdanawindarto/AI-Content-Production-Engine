@echo off
cd /d "%~dp0"
if not exist tmp mkdir tmp
set "TEMP=%CD%\tmp"
set "TMP=%TEMP%"
set "PYTHONDONTWRITEBYTECODE=1"
start "" http://127.0.0.1:8899/
python -B app.py
pause
