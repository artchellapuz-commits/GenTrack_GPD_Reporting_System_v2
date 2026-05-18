@echo off
cd /d "%~dp0"
title NPC Reporting System Runner
color 0B

echo ========================================
echo NPC Reporting System - Startup Script
echo ========================================
echo.

echo [1/3] Starting Backend Server (Django)...
start "NPC Backend" cmd /k "START_BACKEND.bat"
timeout /t 5 /nobreak >nul

echo [2/3] Starting Frontend Server (Vue.js)...
start "NPC Frontend" cmd /k "START_FRONTEND.bat"

echo.
echo ========================================
echo System Starting...
echo ========================================
echo.
echo Backend running on:  http://localhost:8000
echo Frontend running on: http://localhost:3000
echo.
echo [3/3] Please wait 10 seconds for both servers to fully initialize...
timeout /t 10 /nobreak >nul

echo Opening the application in your default web browser...
start http://localhost:3000

echo.
echo ========================================
echo System is now running!
echo Do not close the two command prompt windows that opened.
echo Close them only when you want to stop the system.
echo ========================================
echo.
pause
