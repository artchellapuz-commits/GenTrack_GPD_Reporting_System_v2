@echo off
echo ========================================
echo   RESTARTING DJANGO SERVER
echo ========================================
echo.
echo Stopping any running Django servers...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *runserver*" 2>nul
timeout /t 2 /nobreak >nul
echo.
echo Starting Django server...
echo.
python manage.py runserver
