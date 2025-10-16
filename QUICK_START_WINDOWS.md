# Quick Start Guide for Windows

The easiest way to run the Photo Organiser on Windows.

## Prerequisites

Make sure you have installed:
- Python 3.8+ ([Download here](https://www.python.org/downloads/))
- Node.js 14+ ([Download here](https://nodejs.org/))

## Running the Application

### Option 1: Use the Startup Scripts (Easiest)

1. **Start the Backend**:
   - Double-click `start-backend.bat`
   - A terminal window will open with the backend server
   - Keep this window open

2. **Start the Frontend**:
   - Double-click `start-frontend.bat`
   - A new terminal window will open
   - Your browser will automatically open to http://localhost:3000

That's it! The application is now running.

### Option 2: Manual Setup

If you prefer manual setup or the scripts don't work:

**Terminal 1 (Backend):**
```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Terminal 2 (Frontend):**
```cmd
cd frontend
npm install
npm start
```

## Troubleshooting

### Python not recognized
- Make sure Python is added to PATH during installation
- Restart your terminal/command prompt
- Or use full path: `C:\Python39\python.exe` (adjust for your version)

### npm not recognized
- Make sure Node.js is installed
- Restart your terminal/command prompt
- Check installation: `node --version`

### Port already in use
- Close any other applications using ports 5000 or 3000
- Or change the port in the application files

### Backend won't start
- Make sure you're running Python 3.8 or higher
- Try: `python --version` or `python3 --version`
- Delete the `venv` folder and try again

### Frontend won't start
- Delete `node_modules` folder
- Delete `package-lock.json` file
- Run `npm install` again

## Stopping the Application

1. Go to each terminal window
2. Press `Ctrl + C`
3. Close the terminal windows

## First Time Setup

The first time you run the scripts, they will:
- Create a Python virtual environment (backend)
- Install all Python dependencies (backend)
- Install all Node.js dependencies (frontend)
- This may take 2-5 minutes

Subsequent runs will be much faster!

## Testing

Once both servers are running:

1. Open http://localhost:3000 in your browser
2. Click "Create Album"
3. Create an album called "Test Album"
4. Click on the album
5. Upload some photos (PNG or JPEG)
6. Check the `backend\uploads\album_1\` folder to see compressed images

## Getting Help

If you encounter issues:
1. Check the terminal windows for error messages
2. Read the full `README.md` for detailed documentation
3. See `TESTING_GUIDE.md` for comprehensive testing steps
4. Check `SETUP_GUIDE.md` for detailed setup instructions

## What's Next?

- Try uploading different image formats (PNG, JPEG, HEIC)
- Create multiple albums
- Check file size compression in the uploads folder
- Test the responsive design by resizing your browser

Enjoy organizing your photos! 📸

