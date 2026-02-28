@echo off
chcp 65001 >nul 2>&1
net session >nul 2>&1
if %errorlevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0cleanup_c_drive_en.ps1"
pause
