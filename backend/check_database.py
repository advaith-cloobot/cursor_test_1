#!/usr/bin/env python3
"""
Database verification script for Photo Organiser
Shows database structure and can run SQL queries
"""

from app import app, db
from models import Album, Photo
import sqlite3
import os

def show_database_structure():
    """Show the complete database structure"""
    print("Photo Organiser Database Structure")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Database file location
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            db_path = db_uri.replace('sqlite:///', '')
            
            # Handle Flask instance folder
            if not os.path.exists(db_path):
                # Try in instance folder
                instance_path = os.path.join('instance', 'database.db')
                if os.path.exists(instance_path):
                    db_path = instance_path
            
            if not os.path.exists(db_path):
                print(f"[ERROR] Database file not found: {db_path}")
                return False
            
            print(f"[DATABASE] Database file: {os.path.abspath(db_path)}")
            
            # Connect to SQLite database directly
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            print(f"\n[TABLES] Found {len(tables)} tables:")
            for table in tables:
                print(f"  - {table[0]}")
            
            # Show schema for each table
            for table in tables:
                table_name = table[0]
                print(f"\n[SCHEMA] Table: {table_name}")
                print("-" * 30)
                
                # Get table info
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()
                
                for col in columns:
                    col_id, name, data_type, not_null, default_val, pk = col
                    nullable = "NOT NULL" if not_null else "NULL"
                    primary = "PRIMARY KEY" if pk else ""
                    default = f"DEFAULT {default_val}" if default_val else ""
                    
                    print(f"  {name:20} {data_type:15} {nullable:8} {primary:12} {default}")
            
            # Show foreign key relationships
            print(f"\n[RELATIONSHIPS] Foreign Key Constraints:")
            cursor.execute("PRAGMA foreign_key_list(photos);")
            fks = cursor.fetchall()
            
            if fks:
                for fk in fks:
                    print(f"  photos.{fk[3]} -> {fk[2]}.{fk[4]}")
            else:
                print("  No foreign key constraints found")
            
            # Show indexes
            print(f"\n[INDEXES] Database Indexes:")
            cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND sql IS NOT NULL;")
            indexes = cursor.fetchall()
            
            if indexes:
                for idx in indexes:
                    print(f"  {idx[0]}: {idx[1]}")
            else:
                print("  No custom indexes found")
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"[ERROR] Error reading database: {str(e)}")
            return False

def show_sample_queries():
    """Show sample SQL queries for the database"""
    print("\n" + "=" * 50)
    print("SAMPLE SQL QUERIES")
    print("=" * 50)
    
    queries = [
        ("Get all albums", "SELECT * FROM albums WHERE status = 1;"),
        ("Get all photos", "SELECT * FROM photos WHERE status = 1;"),
        ("Get photos for album 1", "SELECT * FROM photos WHERE album_id = 1 AND status = 1;"),
        ("Count albums", "SELECT COUNT(*) as album_count FROM albums WHERE status = 1;"),
        ("Count photos", "SELECT COUNT(*) as photo_count FROM photos WHERE status = 1;"),
        ("Get album with photo count", """
            SELECT a.id, a.name, a.description, COUNT(p.id) as photo_count 
            FROM albums a 
            LEFT JOIN photos p ON a.id = p.album_id AND p.status = 1 
            WHERE a.status = 1 
            GROUP BY a.id, a.name, a.description;
        """),
    ]
    
    for description, query in queries:
        print(f"\n[QUERY] {description}:")
        print(f"  {query.strip()}")

def run_sample_data():
    """Insert some sample data for testing"""
    print("\n" + "=" * 50)
    print("SAMPLE DATA INSERTION")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Check if we already have data
            album_count = Album.query.count()
            if album_count > 0:
                print(f"[INFO] Database already contains {album_count} albums")
                return
            
            # Create sample albums
            sample_albums = [
                {"name": "Vacation Photos", "description": "Summer vacation 2024"},
                {"name": "Family Events", "description": "Birthdays, holidays, and celebrations"},
                {"name": "Nature Photography", "description": "Landscapes and wildlife"},
            ]
            
            for album_data in sample_albums:
                album = Album(**album_data)
                db.session.add(album)
            
            db.session.commit()
            print("[SUCCESS] Sample albums created successfully!")
            
            # Show created albums
            albums = Album.query.all()
            for album in albums:
                print(f"  - {album.name}: {album.description}")
            
        except Exception as e:
            print(f"[ERROR] Error creating sample data: {str(e)}")

if __name__ == "__main__":
    print("Photo Organiser Database Checker")
    print("=" * 50)
    
    success = show_database_structure()
    if success:
        show_sample_queries()
        
        # Ask if user wants sample data
        print("\n[OPTION] Would you like to create sample albums? (y/n): ", end="")
        try:
            response = input().lower().strip()
            if response in ['y', 'yes']:
                run_sample_data()
        except:
            print("\n[INFO] Skipping sample data creation")
    
    print("\n[COMPLETE] Database check completed!")
