@echo off
cd /d "%~dp0"

echo Stopping AoETallyScript...
taskkill /F /FI "WINDOWTITLE eq AoETallyScript" /T >nul 2>&1
echo Done.
pause
