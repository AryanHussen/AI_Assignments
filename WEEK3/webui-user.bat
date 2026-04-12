@echo off
setlocal
title Koya University AI Project - A* Pathfinder

echo =======================================================
echo   A* Manhattan Pathfinder: Automated Setup & Launch
echo =======================================================

:: STEP 1: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b
)

:: STEP 2: Check for Node.js
node -v >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed or not in PATH.
    pause
    exit /b
)

echo.
echo [1/3] Preparing Backend (Member 1 Logic)...
echo -------------------------------------------------------
cd backend
:: Install libraries from requirements.txt (fastapi, uvicorn)
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [WARNING] Failed to install backend requirements. Check your internet.
)

echo.
echo [2/3] Preparing Frontend (Member 2 & 3 UI)...
echo -------------------------------------------------------
cd ../frontend
:: npm install recreates node_modules based on package.json
call npm install
if %errorlevel% neq 0 (
    echo [WARNING] Failed to install frontend packages.
)

echo.
echo [3/3] Launching Project...
echo -------------------------------------------------------
:: Start the Backend in a separate minimized window
start "A* Pathfinder Backend" /min cmd /k "cd ../backend && python -m uvicorn main:app --reload --port 8000"

echo Starting Frontend Interface...
:: Start the Frontend in the current window
npm start

pause
