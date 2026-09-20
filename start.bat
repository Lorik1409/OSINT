DOS
@echo off
title OSINT - OSINT TOOL
cd /d "%~dp0"
python osint.py
if errorlevel 1 (
    echo.
    echo OSINT konnte nicht gestartet werden.
    pause
)