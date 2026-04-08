@echo off
REM Start Managed Agents Service for STOPA
REM Loads ANTHROPIC_API_KEY from DANE/.env

cd /d "%~dp0"

REM Load API key from DANE/.env if not already set
if "%ANTHROPIC_API_KEY%"=="" (
    for /f "tokens=1,* delims==" %%a in ('findstr "ANTHROPIC_API_KEY" "C:\Users\stock\Documents\000_NGM\DANE\.env"') do set "%%a=%%b"
)

if "%ANTHROPIC_API_KEY%"=="" (
    echo ERROR: ANTHROPIC_API_KEY not found
    exit /b 1
)

echo Starting Managed Agents Service on :9100...
python scripts/managed_agents.py
