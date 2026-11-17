@echo off
setlocal
echo ========================================================
echo Building and Running BookMyShow-style Booking System
echo ========================================================

set SCRIPT_DIR=%~dp0
set BIN_DIR=%SCRIPT_DIR%bin
if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"

where javac >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] javac compiler not found in PATH!
    exit /b 1
)

echo Compiling Java source files...
dir /s /b "%SCRIPT_DIR%src\main\java\*.java" > "%SCRIPT_DIR%sources.txt"
javac -encoding UTF-8 -d "%BIN_DIR%" @"%SCRIPT_DIR%sources.txt"
if %errorlevel% neq 0 (
    echo [ERROR] Compilation failed!
    del "%SCRIPT_DIR%sources.txt"
    exit /b %errorlevel%
)
del "%SCRIPT_DIR%sources.txt"

echo Compilation successful. Launching Main Application...
echo.
java "-Dfile.encoding=UTF-8" -cp "%BIN_DIR%" com.bookmyshow.app.Main
endlocal
