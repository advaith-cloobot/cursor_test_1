#!/bin/bash

echo "Starting Photo Organiser Frontend..."
echo ""

cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
    echo ""
fi

echo "Starting React development server..."
echo "Frontend will open at http://localhost:3000"
echo ""
npm start

