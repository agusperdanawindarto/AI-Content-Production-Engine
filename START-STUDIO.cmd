@echo off
cd /d "%~dp0"
if not exist tmp mkdir tmp
set "TEMP=%CD%\tmp"
set "TMP=%TEMP%"
set "PYTHONDONTWRITEBYTECODE=1"
if exist make-icon.py if not exist studio.ico python -B make-icon.py
if exist UPDATE-DESKTOP.ps1 powershell -NoProfile -File "%CD%\UPDATE-DESKTOP.ps1"
powershell -NoProfile -Command "try { $r=Invoke-RestMethod http://127.0.0.1:8899/health -TimeoutSec 2; if($r.ok){exit 0} } catch {}; exit 1"
if not errorlevel 1 (start "" http://127.0.0.1:8899/ & exit /b 0)
python -B app.py --open
pause
