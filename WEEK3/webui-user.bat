@echo off
setlocal
title Koya University AI Project - A* Pathfinder (Robust Edition)

echo =======================================================
echo   A* Manhattan Pathfinder: Automated Setup & Launch
echo =======================================================

:: STEP 1: Check for Python
python --version >nul 2>&1
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
echo [1/3] Preparing Backend...
cd backend
python -m pip install -r requirements.txt 
if %errorlevel% neq 0 echo [WARNING] Backend install failed. Check internet.

echo.
echo [2/3] Preparing Frontend (Fixing Potential Hangs)...
cd ../frontend

:: --- THE FIX FOR STUCK INSTALLS ---
:: Resetting the npm registry and clearing cache to prevent "idealTree" hangs.
call npm config set registry https://registry.npmjs.org/
if exist "package-lock.json" del /f /q "package-lock.json"

echo Running npm install... (This may take a few minutes)
call npm install --no-audit --no-fund
if %errorlevel% neq 0 (
    echo [RETRY] Attempting forced clean install...
    call npm cache clean --force
    call npm install
)

echo.
echo [3/3] Launching Project...
start "A* Backend" /min cmd /k "cd ../backend && python -m uvicorn main:app --reload --port 8000" 

echo Starting Frontend...
npm start 
pause
