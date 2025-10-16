#!/usr/bin/env python3
"""
Database management script for Photo Organiser
Provides commands to manage the database
"""

import sys
import os
from app import app, db
from models import Album, Photo

def show_help():
    """Show available commands"""
    print("Photo Organiser Database Manager")
    print("=" * 40)
    print("Available commands:")
    print("  init     - Initialize database and tables")
    print("  status   - Show database status")
    print("  sample   - Create sample data")
    print("  clear    - Clear all data (WARNING: destructive)")
    print("  backup   - Create database backup")
    print("  restore  - Restore from backup")
    print("  help     - Show this help")
    print("\nUsage: python manage_database.py <command>")

def init_database():
    """Initialize the database"""
    print("Initializing database...")
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")

def show_status():
    """Show database status"""
    print("Database Status")
    print("=" * 20)
    
    with app.app_context():
        try:
            # Count records
            album_count = Album.query.count()
            photo_count = Photo.query.count()
            active_albums = Album.query.filter_by(status=1).count()
            active_photos = Photo.query.filter_by(status=1).count()
            
            print(f"Total Albums: {album_count} (Active: {active_albums})")
            print(f"Total Photos: {photo_count} (Active: {active_photos})")
            
            # Show recent albums
            recent_albums = Album.query.filter_by(status=1).order_by(Album.created_at.desc()).limit(5).all()
            if recent_albums:
                print("\nRecent Albums:")
                for album in recent_albums:
                    photo_count = Photo.query.filter_by(album_id=album.id, status=1).count()
                    print(f"  - {album.name} ({photo_count} photos)")
            
        except Exception as e:
            print(f"Error: {e}")

def create_sample_data():
    """Create sample data"""
    print("Creating sample data...")
    
    with app.app_context():
        try:
            # Check if data already exists
            if Album.query.count() > 0:
                print("Database already contains data. Skipping sample creation.")
                return
            
            # Create sample albums
            sample_albums = [
                {"name": "Vacation Photos", "description": "Summer vacation 2024"},
                {"name": "Family Events", "description": "Birthdays, holidays, and celebrations"},
                {"name": "Nature Photography", "description": "Landscapes and wildlife"},
                {"name": "Food & Cooking", "description": "Delicious meals and recipes"},
                {"name": "Pets", "description": "Our furry friends"},
            ]
            
            for album_data in sample_albums:
                album = Album(**album_data)
                db.session.add(album)
            
            db.session.commit()
            print(f"Created {len(sample_albums)} sample albums!")
            
        except Exception as e:
            print(f"Error creating sample data: {e}")

def clear_database():
    """Clear all data (destructive)"""
    print("WARNING: This will delete ALL data!")
    response = input("Are you sure? Type 'yes' to confirm: ")
    
    if response.lower() == 'yes':
        with app.app_context():
            try:
                # Delete all records
                Photo.query.delete()
                Album.query.delete()
                db.session.commit()
                print("Database cleared successfully!")
            except Exception as e:
                print(f"Error clearing database: {e}")
    else:
        print("Operation cancelled.")

def backup_database():
    """Create database backup"""
    print("Creating database backup...")
    
    try:
        import shutil
        from datetime import datetime
        
        # Get database path
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        db_path = db_uri.replace('sqlite:///', '')
        
        if not os.path.exists(db_path):
            instance_path = os.path.join('instance', 'database.db')
            if os.path.exists(instance_path):
                db_path = instance_path
            else:
                print("Database file not found!")
                return
        
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"database_backup_{timestamp}.db"
        
        # Copy database file
        shutil.copy2(db_path, backup_path)
        print(f"Backup created: {backup_path}")
        
    except Exception as e:
        print(f"Error creating backup: {e}")

def restore_database():
    """Restore from backup"""
    print("Available backups:")
    
    # Find backup files
    backup_files = [f for f in os.listdir('.') if f.startswith('database_backup_') and f.endswith('.db')]
    
    if not backup_files:
        print("No backup files found!")
        return
    
    for i, backup in enumerate(backup_files):
        print(f"  {i+1}. {backup}")
    
    try:
        choice = int(input("Select backup to restore (number): ")) - 1
        if 0 <= choice < len(backup_files):
            backup_file = backup_files[choice]
            
            # Get current database path
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            db_path = db_uri.replace('sqlite:///', '')
            
            if not os.path.exists(db_path):
                instance_path = os.path.join('instance', 'database.db')
                if os.path.exists(instance_path):
                    db_path = instance_path
                else:
                    # Create instance directory if needed
                    os.makedirs('instance', exist_ok=True)
                    db_path = instance_path
            
            # Restore backup
            import shutil
            shutil.copy2(backup_file, db_path)
            print(f"Database restored from {backup_file}")
        else:
            print("Invalid selection!")
            
    except (ValueError, IndexError):
        print("Invalid input!")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'init':
        init_database()
    elif command == 'status':
        show_status()
    elif command == 'sample':
        create_sample_data()
    elif command == 'clear':
        clear_database()
    elif command == 'backup':
        backup_database()
    elif command == 'restore':
        restore_database()
    elif command == 'help':
        show_help()
    else:
        print(f"Unknown command: {command}")
        show_help()

if __name__ == "__main__":
    main()
