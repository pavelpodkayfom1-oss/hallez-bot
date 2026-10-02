@echo off
chcp 65001 > nul
title Hallez FAMQ Discord Bot

echo ============================================================
echo        ⚜️ ЗАПУСК DISCORD БОТА HALLEZ FAMQ (Majestic RP) ⚜️
echo ============================================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ОШИБКА] Python не найден в системе!
    echo Установите Python 3.10 или новее с python.org и включите "Add Python to PATH".
    pause
    exit /b
)

if not exist ".venv" (
    echo [*] Создаю виртуальное окружение .venv...
    python -m venv .venv
)

echo [*] Установка зависимостей...
.venv\Scripts\python.exe -m pip install --upgrade pip >nul 2>&1
.venv\Scripts\pip.exe install -r requirements.txt

if not exist ".env" (
    echo [ВНИМАНИЕ] Заполните токен в файле .env!
    pause
    exit /b
)

echo [*] Запуск бота Hallez FAMQ...
.venv\Scripts\python.exe main.py
pause
