from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from models import db, Album, Photo
import os
from PIL import Image
import uuid
from werkzeug.utils import secure_filename
import pillow_heif

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
    return jsonify([photo.to_dict() for photo in photos])

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
        # Compress and save image
        stored_filename, file_path = compress_and_save_image(file, album_id)
        
        # Create photo record
        photo = Photo(
            album_id=album_id,
            original_filename=file.filename,
            stored_filename=stored_filename
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)

