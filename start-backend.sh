#!/bin/bash

echo "Starting Photo Organiser Backend..."
echo ""

cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt --quiet
echo ""

echo "Starting Flask server..."
echo "Backend will run on http://localhost:5000"
echo ""
python app.py

