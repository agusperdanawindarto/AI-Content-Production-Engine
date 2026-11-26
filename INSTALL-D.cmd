@echo off
cd /d "%~dp0"
if /I not "%~d0"=="D:" (echo Copy this folder to D: first.& exit /b 1)
if not exist tmp mkdir tmp
set "TEMP=%CD%\tmp"
set "TMP=%TEMP%"
set "PIP_CACHE_DIR=%TEMP%\pip-cache"
python -B -m pip install --no-cache-dir --target "%CD%\vendor" -r requirements.txt
if errorlevel 1 exit /b 1
python -B -c "import sys;sys.path.insert(0,'vendor');import PIL,imageio_ffmpeg;print('Dependencies OK')"
pause
