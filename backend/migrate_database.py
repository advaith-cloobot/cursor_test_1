#!/usr/bin/env python3
"""
Database migration script to add file size columns to photos table
"""

from app import app, db
from models import Photo
import sqlite3
import os

def migrate_database():
    """Add file size columns to photos table"""
    print("Photo Organiser Database Migration")
    print("=" * 40)
    
    with app.app_context():
        try:
            # Check if columns already exist
            inspector = db.inspect(db.engine)
            photo_columns = [col['name'] for col in inspector.get_columns('photos')]
            
            if 'original_size' in photo_columns and 'stored_size' in photo_columns:
                print("[INFO] File size columns already exist. Migration not needed.")
                return True
            
            print("[MIGRATION] Adding file size columns to photos table...")
            
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
            
            # Add new columns
            cursor.execute("ALTER TABLE photos ADD COLUMN original_size INTEGER NOT NULL DEFAULT 0;")
            cursor.execute("ALTER TABLE photos ADD COLUMN stored_size INTEGER NOT NULL DEFAULT 0;")
            
            # Commit changes
            conn.commit()
            conn.close()
            
            print("[SUCCESS] File size columns added successfully!")
            
            # Verify the migration
            inspector = db.inspect(db.engine)
            photo_columns = [col['name'] for col in inspector.get_columns('photos')]
            
            if 'original_size' in photo_columns and 'stored_size' in photo_columns:
                print("[SUCCESS] Migration verified - columns exist")
                
                # Show updated table structure
                print("\n[SCHEMA] Updated photos table columns:")
                for col in inspector.get_columns('photos'):
                    nullable_text = 'NOT NULL' if not col['nullable'] else 'NULL'
                    print(f"  {col['name']:20} {col['type']:15} {nullable_text:8}")
                
                return True
            else:
                print("[ERROR] Migration failed - columns not found")
                return False
                
        except Exception as e:
            print(f"[ERROR] Migration failed: {str(e)}")
            return False

def show_migration_info():
    """Show information about the migration"""
    print("\n" + "=" * 40)
    print("MIGRATION INFORMATION")
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
            
            # Count records
            photo_count = Photo.query.count()
            print(f"[RECORDS] Photos in database: {photo_count}")
            
            if photo_count > 0:
                print("\n[NOTE] Existing photos will have file sizes set to 0")
                print("       New uploads will automatically capture file sizes")
            
        except Exception as e:
            print(f"[ERROR] Error reading database info: {str(e)}")

if __name__ == "__main__":
    print("Adding file size tracking to Photo Organiser database...")
    print("This will add 'original_size' and 'stored_size' columns to the photos table.")
    print()
    
    success = migrate_database()
    if success:
        show_migration_info()
        print("\n[SUCCESS] Database migration completed!")
        print("\nNext steps:")
        print("1. Restart the backend server")
        print("2. New photo uploads will include file size information")
        print("3. Existing photos will show 0 bytes (can be updated manually if needed)")
    else:
        print("\n[ERROR] Database migration failed!")
        exit(1)
