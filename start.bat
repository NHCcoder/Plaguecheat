@echo off
setlocal

REM Define the path to the executable
set EXE_PATH=cs2-dumper.exe

REM Check if cs2.exe is running
tasklist /FI "IMAGENAME eq cs2.exe" 2>NUL | find /I /N "cs2.exe" >NUL
if "%ERRORLEVEL%"=="0" (
    echo cs2.exe is running.
) else (
    echo cs2.exe is not running.
    pause
    exit /b 1
)

REM Check if the executable exists
if not exist "%EXE_PATH%" (
    echo Executable %EXE_PATH% not found.
    pause
    exit /b 1
)

REM Run the executable
echo Running %EXE_PATH%...
"%EXE_PATH%"

REM Check if the executable ran successfully
if %ERRORLEVEL% equ 0 (
    echo Offset dumper ran successfully.
) else (
    echo There was an error running the executable.
    pause
    exit /b 1
)

REM Navigate to the directory and activate conda environment
cd "..\quantico"
call activate quantico

REM Copy the Local URL to the clipboard
echo http://localhost:8501 | clip

REM Run the Streamlit app
streamlit run app.py --server.headless true

pause
endlocal