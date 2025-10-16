#!/usr/bin/env python3
"""
Database migration script to add faces table
"""

from app import app, db
from models import Face
import sqlite3
import os

def migrate_faces_table():
    """Add faces table to database"""
    print("Photo Organiser Faces Migration")
    print("=" * 40)
    
    with app.app_context():
        try:
            # Check if faces table already exists
            inspector = db.inspect(db.engine)
            tables = [table[0] for table in inspector.get_table_names()]
            
            if 'faces' in tables:
                print("[INFO] Faces table already exists. Migration not needed.")
                return True
            
            print("[MIGRATION] Creating faces table...")
            
            # Get database path
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            db_path = db_uri.replace('sqlite:///', '')
            
            if not os.path.exists(db_path):
                instance_path = os.path.join('instance', 'database.db')
                if os.path.exists(instance_path):
                    db_path = instance_path
                else:
                    print("[ERROR] Database file not found!")
                    return False
            
            # Connect to SQLite database directly
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create faces table
            cursor.execute("""
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
                )
            """)
            
            # Create indexes for better performance
            cursor.execute("CREATE INDEX idx_faces_photo_id ON faces(photo_id);")
            cursor.execute("CREATE INDEX idx_faces_album_id ON faces(album_id);")
            cursor.execute("CREATE INDEX idx_faces_status ON faces(status);")
            
            # Commit changes
            conn.commit()
            conn.close()
            
            print("[SUCCESS] Faces table created successfully!")
            
            # Verify the migration
            inspector = db.inspect(db.engine)
            tables = [table[0] for table in inspector.get_table_names()]
            
            if 'faces' in tables:
                print("[SUCCESS] Migration verified - faces table exists")
                
                # Show table structure
                print("\n[SCHEMA] Faces table columns:")
                for col in inspector.get_columns('faces'):
                    nullable_text = 'NOT NULL' if not col['nullable'] else 'NULL'
                    print(f"  {col['name']:20} {col['type']:15} {nullable_text:8}")
                
                return True
            else:
                print("[ERROR] Migration failed - faces table not found")
                return False
                
        except Exception as e:
            print(f"[ERROR] Migration failed: {str(e)}")
            return False

def show_migration_info():
    """Show information about the faces migration"""
    print("\n" + "=" * 40)
    print("FACES MIGRATION INFORMATION")
    print("=" * 40)
    
    with app.app_context():
        try:
            # Database file location
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            db_path = db_uri.replace('sqlite:///', '')
            
            if not os.path.exists(db_path):
                instance_path = os.path.join('instance', 'database.db')
                if os.path.exists(instance_path):
                    db_path = instance_path
            
            print(f"[DATABASE] Database file: {os.path.abspath(db_path)}")
            
            # Check if database file exists
            if os.path.exists(db_path):
                file_size = os.path.getsize(db_path)
                print(f"[SIZE] Database size: {file_size} bytes")
            
            # Count faces
            try:
                face_count = Face.query.count()
                print(f"[RECORDS] Faces in database: {face_count}")
            except:
                print("[RECORDS] Faces table not accessible")
            
        except Exception as e:
            print(f"[ERROR] Error reading database info: {str(e)}")

if __name__ == "__main__":
    print("Adding face detection support to Photo Organiser database...")
    print("This will create the 'faces' table for storing face detection data.")
    print()
    
    success = migrate_faces_table()
    if success:
        show_migration_info()
        print("\n[SUCCESS] Faces migration completed!")
        print("\nNext steps:")
        print("1. Restart the backend server")
        print("2. Install face detection dependencies in frontend")
        print("3. Test face detection functionality")
    else:
        print("\n[ERROR] Faces migration failed!")
        exit(1)
