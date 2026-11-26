@echo off
cd /d "%~dp0"
if /I not "%~d0"=="D:" (echo Copy folder to D: first.& exit /b 1)
if not exist tmp mkdir tmp
set "TEMP=%CD%\tmp"
set "TMP=%TEMP%"
set "PIP_CACHE_DIR=%TEMP%\pip-cache"
python -B -m pip install --no-cache-dir --target "%CD%\vendor\piper" -r requirements-voice.txt
if errorlevel 1 exit /b 1
powershell -NoProfile -File "%CD%\download-voice.ps1"
if errorlevel 1 exit /b 1
python -B studio_services.py --voice
pause
