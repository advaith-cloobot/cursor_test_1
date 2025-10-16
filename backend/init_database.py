#!/usr/bin/env python3
"""
Database initialization script for Photo Organiser
Creates SQLite database and all required tables
"""

from app import app, db
from models import Album, Photo
import os

def init_database():
    """Initialize the database and create all tables"""
    print("Initializing Photo Organiser Database...")
    print("=" * 50)
    
    # Create database tables
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("[SUCCESS] Database tables created successfully!")
            
            # Verify tables exist
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"\n[INFO] Database contains {len(tables)} tables:")
            for table in tables:
                print(f"  - {table}")
            
            # Check if tables have the expected columns
            print("\n[VERIFY] Verifying table structure:")
            
            # Check albums table
            if 'albums' in tables:
                album_columns = [col['name'] for col in inspector.get_columns('albums')]
                print(f"  [ALBUMS] albums table columns: {', '.join(album_columns)}")
                
                expected_album_cols = ['id', 'name', 'description', 'created_at', 'status']
                missing_cols = [col for col in expected_album_cols if col not in album_columns]
                if missing_cols:
                    print(f"    [WARNING] Missing columns: {missing_cols}")
                else:
                    print("    [SUCCESS] All expected columns present")
            
            # Check photos table
            if 'photos' in tables:
                photo_columns = [col['name'] for col in inspector.get_columns('photos')]
                print(f"  [PHOTOS] photos table columns: {', '.join(photo_columns)}")
                
                expected_photo_cols = ['id', 'album_id', 'original_filename', 'stored_filename', 'created_at', 'status']
                missing_cols = [col for col in expected_photo_cols if col not in photo_columns]
                if missing_cols:
                    print(f"    [WARNING] Missing columns: {missing_cols}")
                else:
                    print("    [SUCCESS] All expected columns present")
            
            # Create uploads directory
            uploads_dir = app.config['UPLOAD_FOLDER']
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)
                print(f"\n[DIRECTORY] Created uploads directory: {uploads_dir}")
            else:
                print(f"\n[DIRECTORY] Uploads directory already exists: {uploads_dir}")
            
            print("\n[SUCCESS] Database initialization completed successfully!")
            print("\nNext steps:")
            print("1. Start the backend server: python app.py")
            print("2. Start the frontend server: npm start (in frontend directory)")
            print("3. Open http://localhost:3000 in your browser")
            
        except Exception as e:
            print(f"[ERROR] Error creating database: {str(e)}")
            return False
    
    return True

def show_database_info():
    """Show information about the database"""
    print("\n" + "=" * 50)
    print("DATABASE INFORMATION")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Database file location
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            db_path = db_uri.replace('sqlite:///', '')
            print(f"[DATABASE] Database file: {os.path.abspath(db_path)}")
            
            # Check if database file exists
            if os.path.exists(db_path):
                file_size = os.path.getsize(db_path)
                print(f"[SIZE] Database size: {file_size} bytes")
            else:
                print("[WARNING] Database file not found")
            
            # Count records in each table
            print("\n[RECORDS] Record counts:")
            try:
                album_count = Album.query.count()
                print(f"  [ALBUMS] Albums: {album_count}")
            except:
                print("  [ALBUMS] Albums: Table not accessible")
            
            try:
                photo_count = Photo.query.count()
                print(f"  [PHOTOS] Photos: {photo_count}")
            except:
                print("  [PHOTOS] Photos: Table not accessible")
                
        except Exception as e:
            print(f"[ERROR] Error reading database info: {str(e)}")

if __name__ == "__main__":
    success = init_database()
    if success:
        show_database_info()
    else:
        print("\n[ERROR] Database initialization failed!")
        exit(1)
