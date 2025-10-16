# Quick Setup Guide

Follow these steps to get your Photo Organiser app running locally.

## Step 1: Install Prerequisites

Make sure you have the following installed:
- Python 3.8 or higher
- Node.js 14 or higher
- npm (comes with Node.js)

## Step 2: Backend Setup

Open a terminal/command prompt and navigate to the project root:

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
# For Windows:
python -m venv venv
venv\Scripts\activate

# For macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Frontend Setup

Open a **new** terminal/command prompt window and navigate to the project root:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

## Step 4: Start the Application

### Terminal 1 - Backend:
```bash
cd backend
# Activate venv if not already active
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
python app.py
```
✅ Backend running at http://localhost:5000

### Terminal 2 - Frontend:
```bash
cd frontend
npm start
```
✅ Frontend will open automatically at http://localhost:3000

## Step 5: Test the Application

1. **Create an Album**:
   - Click "Create Album" button
   - Enter name: "My First Album"
   - Enter description: "Testing the app"
   - Click Create

2. **Upload Photos**:
   - Click on the album you just created
   - Drag and drop some photos or click to select
   - Wait for upload to complete

3. **Verify Compression**:
   - Navigate to `backend/uploads/album_1/` folder
   - Check that images are smaller than originals

## Common Issues

### Backend won't start
- Make sure you activated the virtual environment
- Check that all dependencies are installed: `pip list`
- Try reinstalling: `pip install -r requirements.txt --force-reinstall`

### Frontend won't start
- Delete `node_modules` folder
- Delete `package-lock.json`
- Run `npm install` again
- Try `npm start` again

### Cannot connect to backend
- Make sure backend is running on port 5000
- Check for any firewall blocking localhost connections
- Open http://localhost:5000/albums in browser to test backend directly

### Images won't upload
- Check browser console for errors (F12)
- Verify file format (PNG, JPEG, HEIC only)
- Check backend terminal for error messages

## Testing Checklist

- [ ] Create multiple albums
- [ ] Edit an album
- [ ] Delete an album
- [ ] Upload PNG images
- [ ] Upload JPEG images
- [ ] Upload HEIC images (if available)
- [ ] Upload multiple images at once
- [ ] Delete a photo
- [ ] Navigate back and forth between views
- [ ] Check compressed file sizes in uploads folder

## Next Steps

Once everything is working:
1. Try uploading large images (>5MB) to test compression
2. Create multiple albums with different photos
3. Test on mobile device by accessing from phone browser (use your computer's IP address instead of localhost)

Enjoy organizing your photos! 📸

