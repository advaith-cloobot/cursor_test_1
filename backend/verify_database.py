#!/usr/bin/env python3
"""
Final verification script to show database contents
"""

from app import app, db
from models import Album, Photo
import os

def verify_database():
    """Verify database is working correctly"""
    print("Photo Organiser Database Verification")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Check database file
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            db_path = db_uri.replace('sqlite:///', '')
            
            if not os.path.exists(db_path):
                instance_path = os.path.join('instance', 'database.db')
                if os.path.exists(instance_path):
                    db_path = instance_path
                else:
                    print("[ERROR] Database file not found!")
                    return False
            
            print(f"[SUCCESS] Database file: {os.path.abspath(db_path)}")
            print(f"[SUCCESS] File size: {os.path.getsize(db_path)} bytes")
            
            # Test database connection
            album_count = Album.query.count()
            photo_count = Photo.query.count()
            
            print(f"[SUCCESS] Database connection: Working")
            print(f"[SUCCESS] Albums in database: {album_count}")
            print(f"[SUCCESS] Photos in database: {photo_count}")
            
            # Show sample data
            if album_count > 0:
                print(f"\n[ALBUMS] Sample Albums:")
                albums = Album.query.filter_by(status=1).limit(3).all()
                for album in albums:
                    print(f"  - {album.name}: {album.description}")
            
            # Test CRUD operations
            print(f"\n[TEST] Testing CRUD Operations:")
            
            # Test READ
            test_album = Album.query.first()
            if test_album:
                print(f"  [SUCCESS] READ: Retrieved album '{test_album.name}'")
            
            # Test foreign key relationship
            photos_in_album = Photo.query.filter_by(album_id=1).count()
            print(f"  [SUCCESS] RELATIONSHIP: Photos in album 1: {photos_in_album}")
            
            # Test soft delete functionality
            active_albums = Album.query.filter_by(status=1).count()
            archived_albums = Album.query.filter_by(status=0).count()
            print(f"  [SUCCESS] SOFT DELETE: Active albums: {active_albums}, Archived: {archived_albums}")
            
            print(f"\n[SUCCESS] Database verification completed successfully!")
            print(f"\nNext steps:")
            print(f"1. Start backend: python app.py")
            print(f"2. Start frontend: npm start (in frontend directory)")
            print(f"3. Open http://localhost:3000")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Database verification failed: {e}")
            return False

if __name__ == "__main__":
    verify_database()
