@echo off
cd /d "%~dp0"
if /I not "%~d0"=="D:" (echo Copy folder to D: first.& exit /b 1)
if not exist tmp mkdir tmp
set "TEMP=%CD%\tmp"
set "TMP=%TEMP%"
set "npm_config_cache=%TEMP%\npm-cache"
if not exist vendor mkdir vendor
if not exist vendor\siwc-devkit\.git git clone https://github.com/openai/sign-in-with-chatgpt-devkit.git vendor\siwc-devkit
if errorlevel 1 exit /b 1
pushd vendor\siwc-devkit
git checkout 0a36fefeb913055c8c7a1a29b63d82b96b2e841a
if errorlevel 1 goto fail
call npm ci --ignore-scripts --workspace @siwc/local --include-workspace-root
if errorlevel 1 goto fail
call npm audit fix --ignore-scripts --workspace @siwc/local --include-workspace-root
call npm audit --omit=dev --workspace @siwc/local --audit-level=high
if errorlevel 1 goto fail
call npm run build -w @siwc/local
if errorlevel 1 goto fail
popd
node chatgpt-plan.mjs selftest
pause
exit /b 0
:fail
popd
echo GPT SDK installation failed. Do not sign in until fixed.
pause
exit /b 1
