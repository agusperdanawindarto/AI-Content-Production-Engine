@echo off
cd /d "%~dp0"
set "TEMP=%CD%\tmp"
set "TMP=%TEMP%"
set "PIP_CACHE_DIR=%TEMP%\pip-cache"
set "HF_HOME=%CD%\vendor\asr-cache"
set "PYTHONDONTWRITEBYTECODE=1"
python -B -m pip install --no-cache-dir --target "%CD%\vendor\asr" faster-whisper==1.2.1
if errorlevel 1 exit /b 1
set "PYTHONPATH=%CD%\vendor\asr"
python -B -c "from faster_whisper import WhisperModel; WhisperModel('base',device='cpu',compute_type='int8',download_root=r'%CD%\vendor\asr-cache',cpu_threads=4,num_workers=1)"
pause
