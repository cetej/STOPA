@echo off
REM Restartuje Chrome s remote debugging portem
REM Chrome automaticky obnovi vsechny taby

taskkill /F /IM chrome.exe >nul 2>&1
timeout /t 2 /nobreak >nul
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --restore-last-session
echo Chrome restarted with remote debugging on port 9222
