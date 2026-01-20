@echo off
echo ==========================================
echo   Physician Notetaker - One-Click Setup
echo ==========================================
echo.
echo [1/3] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies.
    pause
    exit /b %errorlevel%
)

echo.
echo [2/3] Downloading NLP models...
python -m spacy download en_core_web_sm
if %errorlevel% neq 0 (
    echo Error: Failed to download basic model.
    pause
    exit /b %errorlevel%
)

echo.
echo [3/3] Setup Complete!
echo You can now run 'run_app.bat' to start the system.
echo.
pause
