from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from models import db, Album, Photo, Face
import os
from PIL import Image
import uuid
from werkzeug.utils import secure_filename
import pillow_heif
from face_detection import face_detector

# Register HEIF opener with Pillow
pillow_heif.register_heif_opener()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Initialize database
db.init_app(app)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Create tables
with app.app_context():
    db.create_all()

# Helper function to compress and save image
def compress_and_save_image(file, album_id):
    """
    Compress image and save to album directory
    Returns: (stored_filename, file_path)
    """
    # Create album directory if it doesn't exist
    album_dir = os.path.join(app.config['UPLOAD_FOLDER'], f'album_{album_id}')
    os.makedirs(album_dir, exist_ok=True)
    
    # Generate unique filename
    file_ext = os.path.splitext(file.filename)[1].lower()
    unique_filename = f"{uuid.uuid4()}.jpg"  # Always save as JPEG after compression
    file_path = os.path.join(album_dir, unique_filename)
    
    # Open and compress image
    try:
        image = Image.open(file)
        
        # Convert to RGB if necessary (for HEIC and PNG with transparency)
        if image.mode in ('RGBA', 'LA', 'P'):
            # Create white background
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Compress and save with reduced quality
        image.save(file_path, 'JPEG', quality=50, optimize=True)
        
        return unique_filename, file_path
    except Exception as e:
        raise Exception(f"Error processing image: {str(e)}")

# API Endpoints

@app.route('/albums', methods=['GET'])
def get_albums():
    """Get all active albums"""
    albums = Album.query.filter_by(status=1).order_by(Album.created_at.desc()).all()
    return jsonify([album.to_dict() for album in albums])

@app.route('/albums', methods=['POST'])
def create_album():
    """Create a new album"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Album name is required'}), 400
    
    album = Album(
        name=data['name'],
        description=data.get('description', '')
    )
    
    db.session.add(album)
    db.session.commit()
    
    # Create album directory
    album_dir = os.path.join(app.config['UPLOAD_FOLDER'], f'album_{album.id}')
    os.makedirs(album_dir, exist_ok=True)
    
    return jsonify(album.to_dict()), 201

@app.route('/albums/<int:album_id>', methods=['PUT'])
def update_album(album_id):
    """Update an album"""
    album = Album.query.filter_by(id=album_id, status=1).first()
    
    if not album:
        return jsonify({'error': 'Album not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        album.name = data['name']
    if 'description' in data:
        album.description = data['description']
    
    db.session.commit()
    
    return jsonify(album.to_dict())

@app.route('/albums/<int:album_id>', methods=['DELETE'])
def delete_album(album_id):
    """Soft delete an album (archive it)"""
    album = Album.query.filter_by(id=album_id, status=1).first()
    
    if not album:
        return jsonify({'error': 'Album not found'}), 404
    
    # Soft delete album and all its photos
    album.status = 0
    Photo.query.filter_by(album_id=album_id).update({'status': 0})
    
    db.session.commit()
    
    return jsonify({'message': 'Album archived successfully'})

@app.route('/albums/<int:album_id>/photos', methods=['GET'])
def get_album_photos(album_id):
    """Get all active photos for an album"""
    album = Album.query.filter_by(id=album_id, status=1).first()
    
    if not album:
        return jsonify({'error': 'Album not found'}), 404
    
    photos = Photo.query.filter_by(album_id=album_id, status=1).order_by(Photo.created_at.desc()).all()
    return jsonify({
        'photos': [photo.to_dict() for photo in photos],
        'album_name': album.name
    })

@app.route('/albums/<int:album_id>/photos', methods=['POST'])
def upload_photo(album_id):
    """Upload and compress a photo to an album"""
    album = Album.query.filter_by(id=album_id, status=1).first()
    
    if not album:
        return jsonify({'error': 'Album not found'}), 404
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Validate file extension
    allowed_extensions = {'.png', '.jpg', '.jpeg', '.heic', '.heif'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        return jsonify({'error': 'Invalid file format. Allowed: PNG, JPEG, HEIC'}), 400
    
    try:
        # Get original file size
        original_size = len(file.read())
        file.seek(0)  # Reset file pointer for compression
        
        # Compress and save image
        stored_filename, file_path = compress_and_save_image(file, album_id)
        
        # Get compressed file size
        stored_size = os.path.getsize(file_path)
        
        # Create photo record
        photo = Photo(
            album_id=album_id,
            original_filename=file.filename,
            stored_filename=stored_filename,
            original_size=original_size,
            stored_size=stored_size
        )
        
        db.session.add(photo)
        db.session.commit()
        
        return jsonify(photo.to_dict()), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/uploads/<int:album_id>/<filename>')
def serve_photo(album_id, filename):
    """Serve a photo file"""
    album_dir = os.path.join(app.config['UPLOAD_FOLDER'], f'album_{album_id}')
    return send_from_directory(album_dir, filename)

@app.route('/albums/<int:album_id>/photos/<int:photo_id>', methods=['DELETE'])
def delete_photo(album_id, photo_id):
    """Soft delete a photo"""
    photo = Photo.query.filter_by(id=photo_id, album_id=album_id, status=1).first()
    
    if not photo:
        return jsonify({'error': 'Photo not found'}), 404
    
    photo.status = 0
    db.session.commit()
    
    return jsonify({'message': 'Photo deleted successfully'})

# Face-related endpoints

@app.route('/albums/<int:album_id>/photos/<int:photo_id>/faces', methods=['GET'])
def get_photo_faces(album_id, photo_id):
    """Get all faces for a specific photo"""
    photo = Photo.query.filter_by(id=photo_id, album_id=album_id, status=1).first()
    
    if not photo:
        return jsonify({'error': 'Photo not found'}), 404
    
    faces = Face.query.filter_by(photo_id=photo_id, status=1).order_by(Face.created_at.asc()).all()
    return jsonify([face.to_dict() for face in faces])


@app.route('/albums/<int:album_id>/faces/<int:face_id>', methods=['PUT'])
def update_face_name(album_id, face_id):
    """Update a face's name"""
    face = Face.query.filter_by(id=face_id, album_id=album_id, status=1).first()
    
    if not face:
        return jsonify({'error': 'Face not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        face.name = data['name']
    
    db.session.commit()
    
    return jsonify(face.to_dict())

@app.route('/albums/<int:album_id>/faces/<int:face_id>', methods=['DELETE'])
def delete_face(album_id, face_id):
    """Soft delete a face"""
    face = Face.query.filter_by(id=face_id, album_id=album_id, status=1).first()
    
    if not face:
        return jsonify({'error': 'Face not found'}), 404
    
    face.status = 0
    db.session.commit()
    
    return jsonify({'message': 'Face deleted successfully'})

@app.route('/albums/<int:album_id>/faces', methods=['GET'])
def get_album_faces(album_id):
    """Get all faces for an album (Face Library) with photo information"""
    album = Album.query.filter_by(id=album_id, status=1).first()
    
    if not album:
        return jsonify({'error': 'Album not found'}), 404
    
    # Get faces with their associated photo information
    faces = Face.query.filter_by(album_id=album_id, status=1).order_by(Face.created_at.desc()).all()
    
    faces_with_photos = []
    for face in faces:
        # Get the associated photo
        photo = Photo.query.filter_by(id=face.photo_id, status=1).first()
        if photo:
            face_data = face.to_dict()
            face_data['photo'] = {
                'id': photo.id,
                'original_filename': photo.original_filename,
                'stored_filename': photo.stored_filename,
                'created_at': photo.created_at.isoformat() if photo.created_at else None
            }
            faces_with_photos.append(face_data)
    
    return jsonify(faces_with_photos)

@app.route('/albums/<int:album_id>/photos/<int:photo_id>/detect-faces', methods=['POST'])
def detect_faces_opencv(album_id, photo_id):
    """Detect faces using OpenCV (more accurate)"""
    photo = Photo.query.filter_by(id=photo_id, album_id=album_id, status=1).first()
    
    if not photo:
        return jsonify({'error': 'Photo not found'}), 404
    
    try:
        # Get the photo file path
        album_dir = os.path.join(app.config['UPLOAD_FOLDER'], f'album_{album_id}')
        photo_path = os.path.join(album_dir, photo.stored_filename)
        
        print(f"Attempting face detection for photo: {photo_path}")
        
        if not os.path.exists(photo_path):
            print(f"Photo file not found: {photo_path}")
            return jsonify({'error': 'Photo file not found'}), 404
        
        # Check file permissions and size
        if not os.access(photo_path, os.R_OK):
            print(f"No read permission for: {photo_path}")
            return jsonify({'error': 'No read permission for photo file'}), 403
        
        file_size = os.path.getsize(photo_path)
        if file_size == 0:
            print(f"Photo file is empty: {photo_path}")
            return jsonify({'error': 'Photo file is empty'}), 400
        
        print(f"Photo file found: {photo_path} (size: {file_size} bytes)")
        
        # Detect faces using OpenCV
        detected_faces = face_detector.detect_faces_in_image(photo_path)
        
        if not detected_faces:
            return jsonify({'message': 'No faces detected', 'faces': []}), 200
        
        # Save detected faces to database
        created_faces = []
        for face_data in detected_faces:
            face = Face(
                photo_id=photo_id,
                album_id=album_id,
                confidence=face_data['confidence'],
                bbox_x=face_data['bbox_x'],
                bbox_y=face_data['bbox_y'],
                bbox_width=face_data['bbox_width'],
                bbox_height=face_data['bbox_height']
            )
            db.session.add(face)
            created_faces.append(face)
        
        db.session.commit()
        
        return jsonify({
            'message': f'Detected {len(detected_faces)} faces',
            'faces': [face.to_dict() for face in created_faces]
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Face detection failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

