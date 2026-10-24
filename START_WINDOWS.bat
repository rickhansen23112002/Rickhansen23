@echo off
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
 echo Installeer Python 3 via python.org en probeer opnieuw.
 pause
 exit /b 1
)
start "" http://localhost:18761
py -3 -m http.server 18761 --bind 127.0.0.1
pause
