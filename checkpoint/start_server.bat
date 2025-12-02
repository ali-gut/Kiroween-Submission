@echo off
title Witch Chat Server
cls
echo ========================================
echo        WITCH CHAT SERVER
echo ========================================
echo.
echo [1/2] Installing dependencies...
pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo     Dependencies installed successfully!
echo.
echo [2/2] Starting server on port 5500...
echo.
echo ========================================
echo   Server running at: http://localhost:5500
echo   Client app: http://localhost:5500/clientapp/client.html
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.
python -m http.server 5500
pause