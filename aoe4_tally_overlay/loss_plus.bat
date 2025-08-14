@echo off
cd /d %~dp0
PowerShell -WindowStyle Hidden -Command "Start-Process '..\\python.exe' -ArgumentList 'adjust_session.py loss+' -WorkingDirectory '%~dp0'-WindowStyle Hidden"
