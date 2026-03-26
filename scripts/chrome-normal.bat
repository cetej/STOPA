@echo off
REM Restartuje Chrome bez remote debugging (normalni rezim)

taskkill /F /IM chrome.exe >nul 2>&1
timeout /t 2 /nobreak >nul
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --restore-last-session
echo Chrome restarted in normal mode (no debugging)
