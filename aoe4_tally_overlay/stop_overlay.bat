@echo off
cd /d "%~dp0"
setlocal enabledelayedexpansion

if exist overlay.pid (
    set /p PID=<overlay.pid
    taskkill /PID !PID! /F >nul 2>&1
    del overlay.pid
)

endlocal
