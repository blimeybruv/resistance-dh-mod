@echo off
rem Pulls the errors, the Resistance events and the last 300 lines (where a crash happens) out of savedebug.txt.
rem Double-click it in the mod folder, or drag a savedebug.txt onto it. Run it BEFORE restarting the game after a crash.
set "LOG=%~1"
if "%LOG%"=="" set "LOG=%~dp0..\..\savedebug.txt"
if not exist "%LOG%" (echo savedebug.txt not found at "%LOG%" - drag it onto this file instead.& pause & exit /b)
set "OUT=%~dp0resistance_log.txt"
echo ===== ERRORS AND MOD EVENTS =====> "%OUT%"
findstr /i /c:"ERROR" /c:"Critical" /c:"STRING WANTED" /c:"Executing event 950" "%LOG%" >> "%OUT%"
echo.>> "%OUT%"
echo ===== LAST 300 LINES =====>> "%OUT%"
powershell -NoProfile -Command "Get-Content -LiteralPath $env:LOG -Tail 300" >> "%OUT%"
echo Written to "%OUT%"
pause
