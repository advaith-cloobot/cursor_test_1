# Photo Organiser

A modern web-based photo organizer application with React frontend and Python Flask backend. Manage your photo albums with ease, featuring automatic image compression and support for multiple image formats including HEIC.

## Features

- 📁 **Album Management**: Create, edit, and delete photo albums
- 📸 **Photo Upload**: Upload photos in PNG, JPEG, and HEIC formats
- 🗜️ **Automatic Compression**: Images are automatically compressed to save storage space
- 🎨 **Modern UI**: Beautiful Material Design 3 dark mode interface
- 🔄 **Soft Deletes**: Albums and photos are archived rather than permanently deleted
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices

## Project Structure

```
photo-organiser/
├── backend/
│   ├── app.py              # Flask application with API endpoints
│   ├── models.py           # SQLAlchemy database models
│   ├── requirements.txt    # Python dependencies
│   ├── database.db         # SQLite database (created on first run)
│   └── uploads/            # Directory for storing compressed images
│
└── frontend/
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── api/
    │   │   └── index.js       # API calls using Axios
    │   ├── components/        # Reusable React components
    │   │   ├── AlbumCard.js
    │   │   ├── AlbumForm.js
    │   │   ├── Photo.js
    │   │   └── PhotoUpload.js
    │   ├── views/             # Main application views
    │   │   ├── AlbumList.js
    │   │   └── AlbumView.js
    │   ├── App.js
    │   └── index.js
    └── package.json
```

## Prerequisites

- **Python 3.8+**: Required for the backend
- **Node.js 14+**: Required for the frontend
- **npm or yarn**: Package manager for frontend dependencies

## Installation

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

## Running the Application

You'll need to run both the backend and frontend servers simultaneously.

### Start the Backend Server

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Activate your virtual environment (if not already activated):
   ```bash
   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. Start the Flask server:
   ```bash
   python app.py
   ```

   The backend server will start on `http://localhost:5000`

### Start the Frontend Server

1. Open a new terminal/command prompt

2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

3. Start the React development server:
   ```bash
   npm start
   ```

   The frontend will automatically open in your browser at `http://localhost:3000`

## Using the Application

### Creating Albums

1. Click the "Create Album" button on the home page
2. Enter an album name (required) and description (optional)
3. Click "Create" to save the album

### Managing Albums

- **View Album**: Click on any album card to view its photos
- **Edit Album**: Click the edit icon (pencil) on an album card
- **Delete Album**: Click the delete icon (trash) on an album card and confirm

### Uploading Photos

1. Click on an album to open it
2. Use the upload area at the top to add photos:
   - Drag and drop photos directly
   - Or click to open file picker
3. Supported formats: PNG, JPEG, HEIC
4. Multiple photos can be uploaded at once

### Managing Photos

- **View Photo**: Photos are displayed in a grid layout
- **Delete Photo**: Hover over a photo and click the delete icon

## Test Cases

### Album Management Tests

1. **Create Multiple Albums**
   - Create 3-5 albums with different names and descriptions
   - Verify all albums appear on the home page
   - ✅ Expected: All albums should be listed

2. **Edit Album**
   - Edit an existing album's name and description
   - ✅ Expected: Changes should be saved and reflected immediately

3. **Delete Album**
   - Delete an album
   - ✅ Expected: Album should be removed from the list

### Photo Upload Tests

1. **Upload PNG Images**
   - Upload one or more PNG files
   - ✅ Expected: Photos should appear in the album

2. **Upload JPEG Images**
   - Upload one or more JPEG/JPG files
   - ✅ Expected: Photos should appear in the album

3. **Upload HEIC Images** (iOS format)
   - Upload HEIC files from an iPhone
   - ✅ Expected: Photos should be converted and appear in the album

4. **Multiple File Upload**
   - Select and upload 5-10 images at once
   - ✅ Expected: All images should upload successfully

5. **Drag and Drop Upload**
   - Drag images from file explorer to the upload area
   - ✅ Expected: Images should upload successfully

### Compression Verification

1. **Check File Size Reduction**
   - Note the original size of an image before uploading
   - Upload the image
   - Navigate to `backend/uploads/album_X/` directory
   - Compare the compressed file size with the original
   - ✅ Expected: Compressed file should be smaller than the original

2. **Compare Multiple Images**
   - Upload several large images (>2MB each)
   - Check the total size of compressed images
   - ✅ Expected: Significant storage savings should be observed

### User Interface Tests

1. **Responsive Design**
   - Test the application on different screen sizes
   - ✅ Expected: UI should adapt smoothly

2. **Dark Mode Colors**
   - Verify the Material Design 3 color scheme is applied
   - ✅ Expected: Dark background (#0D0D0D) with proper contrast

3. **Hover Effects**
   - Hover over albums and photos
   - ✅ Expected: Visual feedback with color changes and shadows

## Technical Details

### Backend (Flask)

- **Framework**: Flask 3.0.0
- **Database**: SQLite with SQLAlchemy ORM
- **Image Processing**: Pillow (PIL) with HEIC support via pillow-heif
- **CORS**: Enabled for frontend communication
- **Compression**: JPEG quality set to 50% for optimal size/quality balance

### Frontend (React)

- **Framework**: React 18.2.0
- **Routing**: React Router DOM 6.x
- **HTTP Client**: Axios
- **Design System**: Material Design 3 (Dark Mode)
- **Fonts**: Montserrat (Google Fonts)
- **Icons**: Material Symbols (Google Icons)

### Color Scheme

Following Material Design 3 principles:

- **Color 1** (#0D0D0D): Base background
- **Color 2** (#1A1A1A): Panel backgrounds
- **Color 3** (#262626): Default button state
- **Color 4** (#333333): Hover state
- **Color 5** (#404040): Active state
- **Color 7** (#FFFFFF): Text and highlights
- **Accent** (#C82FFF): Magenta accent for UI elements
- **Gradient**: #C82FFF to #00AAFF for primary actions
- **Borders** (#A8A8A8): Panel borders and placeholders

## API Endpoints

### Albums

- `GET /albums` - Get all active albums
- `POST /albums` - Create a new album
- `PUT /albums/<id>` - Update an album
- `DELETE /albums/<id>` - Soft delete an album

### Photos

- `GET /albums/<id>/photos` - Get all photos in an album
- `POST /albums/<id>/photos` - Upload a photo to an album
- `DELETE /albums/<id>/photos/<photo_id>` - Soft delete a photo
- `GET /uploads/<album_id>/<filename>` - Serve photo file

## Database Schema

### Albums Table

| Column      | Type      | Description                    |
|-------------|-----------|--------------------------------|
| id          | Integer   | Primary key                    |
| name        | Text      | Album name                     |
| description | Text      | Album description (optional)   |
| created_at  | Timestamp | Creation timestamp             |
| status      | Integer   | 1 = active, 0 = archived       |

### Photos Table

| Column            | Type      | Description                    |
|-------------------|-----------|--------------------------------|
| id                | Integer   | Primary key                    |
| album_id          | Integer   | Foreign key to albums          |
| original_filename | Text      | Original uploaded filename     |
| stored_filename   | Text      | Unique stored filename         |
| created_at        | Timestamp | Upload timestamp               |
| status            | Integer   | 1 = active, 0 = archived       |

## Troubleshooting

### Backend Issues

**Error: "Module not found"**
- Ensure you've activated your virtual environment
- Run `pip install -r requirements.txt` again

**Error: "Port 5000 already in use"**
- Change the port in `app.py`: `app.run(debug=True, port=5001)`
- Update the API base URL in `frontend/src/api/index.js`

**HEIC images not working**
- Ensure `pillow-heif` is installed correctly
- On Windows, you may need to install additional dependencies

### Frontend Issues

**Error: "npm command not found"**
- Install Node.js from https://nodejs.org/

**Error: "Failed to compile"**
- Delete `node_modules` folder and `package-lock.json`
- Run `npm install` again

**CORS errors**
- Ensure the backend server is running
- Check that Flask-CORS is installed and configured

## Future Enhancements

- 🔐 User authentication and multi-user support
- 🏷️ Photo tagging and search functionality
- 📊 Album statistics (photo count, total size)
- 🎞️ Photo slideshow mode
- 💾 Export album as ZIP file
- 🖼️ Photo editing capabilities
- ☁️ Cloud storage integration
- 📱 Native mobile apps

## License

This project is provided as-is for educational and personal use.

## Support

For issues or questions, please check the troubleshooting section above or review the code comments for detailed implementation notes.
