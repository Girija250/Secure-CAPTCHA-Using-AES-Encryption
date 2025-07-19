@echo off
echo ---------------------------
echo Secure CAPTCHA Login System
echo ---------------------------

REM (Optional) Activate virtual environment if you have one
REM call venv\Scripts\activate

echo Installing required Python packages...
pip install flask cryptography captcha >nul 2>&1

REM Check if encryption key exists
IF NOT EXIST "encryption_key.key" (
    echo Generating AES key...
    python generate_key.py
)

echo Starting Flask server...
python app.py

pause
