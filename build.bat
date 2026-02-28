@echo off
setlocal

echo Checking Python environment...
python -m pip install -r requirements.txt

echo Cleaning old build files...
if exist build rd /s /q build
if exist dist rd /s /q dist
if exist Windows_Cleaner.spec del /q Windows_Cleaner.spec

echo.
echo Building executable with PyInstaller...
python -m PyInstaller ^
    --name="Windows_Cleaner" ^
    --windowed ^
    --onefile ^
    --uac-admin ^
    --icon="assets/icon.ico" ^
    --add-data="assets;assets" ^
    --exclude-module numpy ^
    --exclude-module pandas ^
    --exclude-module matplotlib ^
    --exclude-module notebook ^
    --clean ^
    app/main.py

echo.
echo Build complete. Check the 'dist' folder.
echo.
echo [TIPS] If start failed, please try to disable Antivirus software temporarily.
pause
