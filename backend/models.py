from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Album(db.Model):
    __tablename__ = 'albums'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Integer, nullable=False, default=1)
    
    # Relationship to photos
    photos = db.relationship('Photo', backref='album', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'status': self.status
        }

class Photo(db.Model):
    __tablename__ = 'photos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'), nullable=False)
    original_filename = db.Column(db.Text, nullable=False)
    stored_filename = db.Column(db.Text, nullable=False, unique=True)
    original_size = db.Column(db.Integer, nullable=False)  # Original file size in bytes
    stored_size = db.Column(db.Integer, nullable=False)    # Compressed file size in bytes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Integer, nullable=False, default=1)
    
    # Relationship to faces
    faces = db.relationship('Face', backref='photo', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'album_id': self.album_id,
            'original_filename': self.original_filename,
            'stored_filename': self.stored_filename,
            'original_size': self.original_size,
            'stored_size': self.stored_size,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'status': self.status
        }

class Face(db.Model):
    __tablename__ = 'faces'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id'), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'), nullable=False)
    name = db.Column(db.Text, nullable=True)  # User-assigned name
    confidence = db.Column(db.Float, nullable=False)  # Detection confidence
    bbox_x = db.Column(db.Float, nullable=False)  # Bounding box x coordinate (0-1)
    bbox_y = db.Column(db.Float, nullable=False)  # Bounding box y coordinate (0-1)
    bbox_width = db.Column(db.Float, nullable=False)  # Bounding box width (0-1)
    bbox_height = db.Column(db.Float, nullable=False)  # Bounding box height (0-1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Integer, nullable=False, default=1)
    
    def to_dict(self):
        return {
            'id': self.id,
            'photo_id': self.photo_id,
            'album_id': self.album_id,
            'name': self.name,
            'confidence': self.confidence,
            'bbox_x': self.bbox_x,
            'bbox_y': self.bbox_y,
            'bbox_width': self.bbox_width,
            'bbox_height': self.bbox_height,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'status': self.status
        }

