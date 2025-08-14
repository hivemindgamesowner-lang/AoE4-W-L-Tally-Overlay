@echo off
cd /d "%~dp0"
setlocal enabledelayedexpansion

for /f %%a in ('PowerShell -Command "Start-Process -FilePath 'python' -ArgumentList 'main.py' -WorkingDirectory '%CD%' -WindowStyle Hidden -PassThru | Select-Object -ExpandProperty Id"') do (
    set PID=%%a
    echo !PID! > overlay.pid
)
endlocal
