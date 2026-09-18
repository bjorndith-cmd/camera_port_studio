@echo off
chcp 65001 >nul
title Build Camera Port Studio EXE
cd /d "%~dp0"

echo ========================================
echo  Сборка EXE (PyInstaller)
echo ========================================
echo.

if not exist "venv\Scripts\activate.bat" (
    echo Создаю venv...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo Устанавливаю зависимости...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo Собираю EXE (это может занять 1-3 минуты)...
echo.

pyinstaller --noconfirm --onefile --console ^
  --name "CameraPortStudio" ^
  --add-data "generator;generator" ^
  --hidden-import=streamlit ^
  --hidden-import=generator.module_builder ^
  --collect-all streamlit ^
  --collect-all PIL ^
  app.py

echo.
if exist "dist\CameraPortStudio.exe" (
    echo [OK] Готово: dist\CameraPortStudio.exe
    echo.
    echo Внимание: Streamlit в onefile-режиме работает, но при первом запуске
    echo может потребоваться время на распаковку. Альтернатива — просто
    echo использовать run.bat (рекомендуется).
) else (
    echo [ОШИБКА] EXE не создан. Смотрите вывод выше.
)

pause
