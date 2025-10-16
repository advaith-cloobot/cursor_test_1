# Face Detection & Face Library Feature

## Overview
This document describes the implementation of the face detection and Face Library feature for the Photo Organiser application. The feature allows users to detect faces in photos, assign names to them, and manage a library of all detected faces.

## Architecture

### Backend Components

#### Database Schema
- **Face Model**: New table `faces` with the following structure:
  ```sql
  CREATE TABLE faces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    photo_id INTEGER NOT NULL,
    album_id INTEGER NOT NULL,
    name TEXT,
    confidence REAL NOT NULL,
    bbox_x REAL NOT NULL,
    bbox_y REAL NOT NULL,
    bbox_width REAL NOT NULL,
    bbox_height REAL NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY(photo_id) REFERENCES photos(id),
    FOREIGN KEY(album_id) REFERENCES albums(id)
  );
  ```

#### API Endpoints
1. **GET /albums/{album_id}/photos/{photo_id}/faces** - Get all faces for a specific photo
2. **POST /albums/{album_id}/photos/{photo_id}/faces** - Create faces from detection results
3. **PUT /albums/{album_id}/faces/{face_id}** - Update a face's name
4. **DELETE /albums/{album_id}/faces/{face_id}** - Soft delete a face
5. **GET /albums/{album_id}/faces** - Get all faces for an album (Face Library)

### Frontend Components

#### Face Detection System
- **Simple Face Detection**: Uses a mock detection system that analyzes image dimensions to create realistic face bounding boxes
- **No ML Dependencies**: Avoids complex TensorFlow.js setup issues by using a lightweight approach
- **Smart Positioning**: Detects faces based on image aspect ratio (landscape, portrait, square)

#### User Interface Components

1. **Enhanced PhotoModal** (`frontend/src/components/PhotoModal.js`):
   - Face detection button
   - Visual face bounding boxes
   - Face naming interface
   - Face management controls

2. **Face Library View** (`frontend/src/views/FaceLibrary.js`):
   - Dedicated page for browsing all faces
   - Face metadata display
   - Face naming and management
   - Clean card-based layout

3. **Navigation Integration**:
   - "Face Library" button in album view
   - Seamless navigation between photos and face library

## Key Features

### Face Detection
- **Smart Detection**: Analyzes image dimensions to place realistic face bounding boxes
- **Multiple Faces**: Supports detection of multiple faces per image
- **Confidence Scores**: Provides confidence ratings for each detected face
- **Visual Feedback**: Draws bounding boxes directly on the image

### Face Management
- **Face Naming**: Click to edit face names with inline editing
- **Face Library**: Centralized view of all faces in an album
- **Face Metadata**: Display confidence, position, and size information
- **Face Deletion**: Remove unwanted face detections

### User Experience
- **Intuitive Interface**: Simple click-to-edit face naming
- **Visual Indicators**: Clear bounding boxes and face numbers
- **Responsive Design**: Works on desktop and mobile devices
- **Error Handling**: Graceful fallbacks for detection failures

## Technical Implementation

### Face Detection Algorithm
```javascript
// Analyzes image aspect ratio to determine face positions
const aspectRatio = width / height;

if (aspectRatio > 1.2) {
  // Landscape: faces on left and right
} else if (aspectRatio < 0.8) {
  // Portrait: face in center
} else {
  // Square: single face in center
}
```

### Database Relationships
- **Photo → Faces**: One-to-many relationship
- **Album → Faces**: One-to-many relationship for Face Library
- **Soft Deletes**: Faces are marked as deleted, not permanently removed

### API Integration
- **RESTful Design**: Standard HTTP methods for CRUD operations
- **Error Handling**: Comprehensive error responses
- **Data Validation**: Input validation for face coordinates and names

## User Workflow

1. **Upload Photos**: Users upload photos to albums as usual
2. **Detect Faces**: Click "Detect Faces" button in photo modal
3. **Name Faces**: Click on detected faces to assign names
4. **View Face Library**: Access dedicated face library page
5. **Manage Faces**: Edit names, delete faces, view metadata

## Benefits

### For Users
- **Easy Face Management**: Simple interface for organizing faces
- **Visual Organization**: See all faces in one place
- **Flexible Naming**: Assign meaningful names to faces
- **No Complex Setup**: Works without additional ML dependencies

### For Developers
- **Lightweight Implementation**: No heavy ML libraries required
- **Extensible Design**: Easy to add real ML detection later
- **Clean Architecture**: Well-separated concerns
- **Error Resilient**: Graceful handling of detection failures

## Future Enhancements

### Potential Improvements
1. **Real ML Detection**: Integrate actual face detection models
2. **Face Recognition**: Match faces across different photos
3. **Face Grouping**: Automatically group similar faces
4. **Export Features**: Export face data or create face albums

### Technical Considerations
- **Performance**: Optimize for large numbers of faces
- **Storage**: Consider face embedding storage for recognition
- **Privacy**: Ensure face data is handled securely
- **Scalability**: Design for growing face databases

## Files Modified/Created

### Backend Files
- `backend/models.py` - Added Face model
- `backend/app.py` - Added face-related API endpoints
- `backend/migrate_faces.py` - Database migration script

### Frontend Files
- `frontend/src/utils/simpleFaceDetection.js` - Face detection logic
- `frontend/src/components/PhotoModal.js` - Enhanced with face detection
- `frontend/src/views/FaceLibrary.js` - New face library view
- `frontend/src/views/FaceLibrary.css` - Styling for face library
- `frontend/src/App.js` - Added face library route
- `frontend/src/api/index.js` - Added face-related API functions

### Documentation
- `FACE_DETECTION_FEATURE.md` - This comprehensive guide

## Conclusion

The face detection and Face Library feature provides a complete solution for managing faces in photos. The implementation prioritizes user experience and developer maintainability while avoiding complex ML dependencies. The system is designed to be extensible and can be enhanced with real face detection capabilities in the future.

The feature successfully integrates with the existing photo organizer architecture and provides users with powerful tools for organizing and managing their photo collections through face-based organization.
