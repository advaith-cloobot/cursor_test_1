@echo off
echo Starting Photo Organiser Frontend...
echo.

cd frontend

if not exist node_modules (
    echo Installing dependencies...
    call npm install
    echo.
)

echo Starting React development server...
echo Frontend will open at http://localhost:3000
echo.
call npm start

