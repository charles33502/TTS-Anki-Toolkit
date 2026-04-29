@echo off
setlocal

REM Move to the folder where this BAT file is located
cd /d "%~dp0"

set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
set "SCRIPT=%~dp0toeic_listen_choice_tts_abcd.py"
set "INPUT=%~dp0toeic_listen_questions_abcd.txt"

if not exist "%PYTHON_EXE%" (
    echo [ERROR] Cannot find .venv Python:
    echo %PYTHON_EXE%
    echo.
    echo Please make sure this file is in the same folder as .venv
    pause
    exit /b 1
)

if not exist "%SCRIPT%" (
    echo [ERROR] Cannot find script:
    echo %SCRIPT%
    echo.
    echo Please put toeic_listen_choice_tts_abcd.py in the same folder as this BAT file.
    pause
    exit /b 1
)

if not exist "%INPUT%" (
    echo [ERROR] Cannot find input file:
    echo %INPUT%
    echo.
    echo Please put toeic_listen_questions_abcd.txt in the same folder as this BAT file.
    pause
    exit /b 1
)

echo Using Python:
echo %PYTHON_EXE%
echo.

echo Checking edge-tts...
"%PYTHON_EXE%" -m pip show edge-tts >nul 2>nul
if errorlevel 1 (
    echo Installing edge-tts...
    "%PYTHON_EXE%" -m pip install edge-tts
    if errorlevel 1 (
        echo [ERROR] Failed to install edge-tts.
        pause
        exit /b 1
    )
)

echo.
echo Running TOEIC ABCD TTS...
"%PYTHON_EXE%" "%SCRIPT%"

echo.
echo Done.
pause
