@echo off
echo Starting Photo Organiser Backend...
echo.

cd backend

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt --quiet
echo.

echo Starting Flask server...
echo Backend will run on http://localhost:5000
echo.
python app.py

