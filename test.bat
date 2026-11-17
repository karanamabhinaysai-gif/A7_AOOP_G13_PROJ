@echo off
setlocal
echo ========================================================
echo Building and Running Automated Unit & Invariant Tests
echo ========================================================

set SCRIPT_DIR=%~dp0
set BIN_DIR=%SCRIPT_DIR%bin
if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"

dir /s /b "%SCRIPT_DIR%src\main\java\*.java" > "%SCRIPT_DIR%sources.txt"
dir /s /b "%SCRIPT_DIR%src\test\java\*.java" >> "%SCRIPT_DIR%sources.txt"
javac -encoding UTF-8 -d "%BIN_DIR%" @"%SCRIPT_DIR%sources.txt"
if %errorlevel% neq 0 (
    echo [ERROR] Test compilation failed!
    del "%SCRIPT_DIR%sources.txt"
    exit /b %errorlevel%
)
del "%SCRIPT_DIR%sources.txt"

echo Test compilation successful. Executing Test Suites...
echo.
java "-Dfile.encoding=UTF-8" -cp "%BIN_DIR%" com.bookmyshow.BookingSystemTests
endlocal
