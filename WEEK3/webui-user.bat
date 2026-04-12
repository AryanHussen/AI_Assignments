@echo off
setlocal
title Koya University AI Project - A* Pathfinder

echo =======================================================
echo   A* Manhattan Pathfinder: Automated Setup & Launch
echo =======================================================

:: STEP 1: Check for Python (Updated to use 'py')
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python 3.12+.
    pause
    exit /b
)

:: STEP 2: Check for Node.js
node -v >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed. Please install Node.js LTS.
    pause
    exit /b
)

echo.
echo [1/3] Preparing Backend (Member 1 Logic)...
echo -------------------------------------------------------
cd backend
:: Using 'py -m pip' ensures libraries go to your specific Python 3.14 version
py -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [WARNING] Failed to install backend requirements.
)

echo.
echo [2/3] Preparing Frontend (Member 2 & 3 UI)...
echo -------------------------------------------------------
cd ../frontend
call npm install
if %errorlevel% neq 0 (
    echo [WARNING] Failed to install frontend packages.
)

echo.
echo [3/3] Launching Project...
echo -------------------------------------------------------
:: Start the Backend using 'py' so Port 8000 actually opens
start "A* Pathfinder Backend" /min cmd /k "cd ../backend && py -m uvicorn main:app --reload --port 8000"

echo Starting Frontend Interface...
npm start

pause