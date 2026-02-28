@echo off
setlocal

echo Checking Python environment...
python -m pip install -r requirements.txt

echo.
echo Building executable with PyInstaller...
python -m PyInstaller ^
    --name="Windows_Cleaner" ^
    --windowed ^
    --onefile ^
    --uac-admin ^
    --icon="assets/icon.ico" ^
    --add-data="assets/icon.ico;assets" ^
    app/main.py

echo.
echo Build complete. Check the 'dist' folder.
pause
