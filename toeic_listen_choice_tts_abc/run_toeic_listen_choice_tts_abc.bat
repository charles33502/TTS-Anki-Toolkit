@echo off
setlocal
cd /d "%~dp0"

set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
set "SCRIPT=%~dp0toeic_listen_choice_tts_abc.py"
set "INPUT=%~dp0toeic_listen_questions_abc.txt"

echo ========================================
echo TOEIC Choice TTS Generator - venv version
echo ========================================
echo.

if not exist "%PYTHON_EXE%" goto NO_VENV
if not exist "%SCRIPT%" goto NO_SCRIPT
if not exist "%INPUT%" goto MAKE_SAMPLE

goto RUN

:NO_VENV
echo ERROR: Cannot find .venv Python:
echo %PYTHON_EXE%
echo.
echo Please create venv first:
echo python -m venv .venv
echo .venv\Scripts\python.exe -m pip install edge-tts
pause
exit /b 1

:NO_SCRIPT
echo ERROR: Cannot find toeic_listen_choice_tts.py
echo Put this bat file in the same folder as toeic_listen_choice_tts.py
pause
exit /b 1

:MAKE_SAMPLE
echo INFO: Cannot find toeic_listen_questions_abc.txt. Creating a sample file...
> "%INPUT%" echo The company is planning to recruit more staff, is it not?
>> "%INPUT%" echo.
>> "%INPUT%" echo ^(A^) No, they are not included.
>> "%INPUT%" echo ^(B^) Yes, two and a half will be enough.
>> "%INPUT%" echo ^(C^) Absolutely, that is our top priority.
echo.
echo Created toeic_listen_questions_abc.txt.
echo Edit toeic_listen_questions_abc.txt, then run this bat again.
pause
exit /b 0

:RUN
echo [1/2] Checking edge-tts in .venv...
"%PYTHON_EXE%" -m pip show edge-tts >nul 2>nul
if errorlevel 1 goto INSTALL_EDGE_TTS
goto EXEC_SCRIPT

:INSTALL_EDGE_TTS
echo Installing edge-tts into .venv...
"%PYTHON_EXE%" -m pip install edge-tts
if errorlevel 1 goto INSTALL_FAIL
goto EXEC_SCRIPT

:INSTALL_FAIL
echo ERROR: Failed to install edge-tts.
pause
exit /b 1

:EXEC_SCRIPT
echo.
echo [2/2] Running toeic_listen_choice_tts.py...
"%PYTHON_EXE%" "%SCRIPT%"
if errorlevel 1 goto SCRIPT_FAIL
echo.
echo Done. Audio files are in the output folder.
pause
exit /b 0

:SCRIPT_FAIL
echo.
echo ERROR: Script failed.
pause
exit /b 1
