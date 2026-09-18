@echo off
chcp 65001 >nul
title Camera Port Studio
cd /d "%~dp0"

if not exist "venv\Scripts\activate.bat" (
    echo [!] Виртуальное окружение не найдено. Создаю...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

echo.
echo ========================================
echo   Camera Port Studio запускается...
echo   Браузер откроется автоматически
echo ========================================
echo.

streamlit run app.py --server.headless false

pause
