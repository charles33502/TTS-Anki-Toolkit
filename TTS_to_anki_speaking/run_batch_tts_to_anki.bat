@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo   Batch TTS to Anki (.venv)
echo ========================================
echo.

set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"

if not exist "%PYTHON_EXE%" (
    echo [錯誤] 找不到 .venv 的 Python：
    echo %PYTHON_EXE%
    pause
    exit /b 1
)

echo [1/4] 升級 pip...
"%PYTHON_EXE%" -m pip install --upgrade pip

echo.
echo [2/4] 檢查並安裝 edge-tts...
"%PYTHON_EXE%" -m pip show edge-tts >nul 2>nul
if errorlevel 1 (
    "%PYTHON_EXE%" -m pip install edge-tts
    if errorlevel 1 (
        echo [錯誤] edge-tts 安裝失敗。
        pause
        exit /b 1
    )
)

echo.
echo [3/4] 執行 Python 腳本...
"%PYTHON_EXE%" batch_tts_to_anki.py
if errorlevel 1 (
    echo.
    echo [錯誤] 腳本執行失敗。
    pause
    exit /b 1
)

echo.
echo [4/4] 完成
pause