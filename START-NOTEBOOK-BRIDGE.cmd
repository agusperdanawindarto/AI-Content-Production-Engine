@echo off
cd /d "%~dp0"
if not exist tmp mkdir tmp
set "TEMP=%CD%\tmp"
set "TMP=%TEMP%"
set "PYTHONDONTWRITEBYTECODE=1"
python -B notebook_bridge.py
pause
