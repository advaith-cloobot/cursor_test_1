#!/usr/bin/env python3
"""
Test script to verify file size tracking functionality
"""

from app import app, db
from models import Photo
import os

def test_file_size_tracking():
    """Test file size tracking functionality"""
    print("Photo Organiser File Size Tracking Test")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Check if file size columns exist
            inspector = db.inspect(db.engine)
            photo_columns = [col['name'] for col in inspector.get_columns('photos')]
            
            if 'original_size' not in photo_columns or 'stored_size' not in photo_columns:
                print("[ERROR] File size columns not found in photos table")
                print("Run: python migrate_database.py")
                return False
            
            print("[SUCCESS] File size columns found in photos table")
            
            # Check existing photos
            photos = Photo.query.all()
            print(f"\n[PHOTOS] Found {len(photos)} photos in database")
            
            if photos:
                print("\n[FILE SIZES] Photo file size information:")
                for photo in photos:
                    print(f"  Photo {photo.id}: {photo.original_filename}")
                    print(f"    Original: {photo.original_size} bytes")
                    print(f"    Stored:   {photo.stored_size} bytes")
                    
                    if photo.original_size > 0 and photo.stored_size > 0:
                        ratio = ((photo.original_size - photo.stored_size) / photo.original_size * 100)
                        print(f"    Compression: {ratio:.1f}% smaller")
                    else:
                        print(f"    Compression: No data (uploaded before file size tracking)")
                    print()
            else:
                print("[INFO] No photos found. Upload some photos to test file size tracking.")
            
            # Test file size formatting
            print("\n[FORMATTING] File size formatting examples:")
            test_sizes = [0, 1024, 1048576, 1073741824]  # 0B, 1KB, 1MB, 1GB
            
            for size in test_sizes:
                formatted = format_file_size(size)
                print(f"  {size:>10} bytes = {formatted}")
            
            print("\n[SUCCESS] File size tracking test completed!")
            print("\nNext steps:")
            print("1. Upload new photos to see file size tracking in action")
            print("2. Check the frontend to see file sizes displayed on photos")
            print("3. Hover over photos to see compression information")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Test failed: {str(e)}")
            return False

def format_file_size(bytes):
    """Format file size in human readable format"""
    if bytes == 0:
        return "0 B"
    k = 1024
    sizes = ['B', 'KB', 'MB', 'GB', 'TB']
    i = int(math.floor(math.log(bytes) / math.log(k)))
    return f"{bytes / (k ** i):.1f} {sizes[i]}"

if __name__ == "__main__":
    import math
    test_file_size_tracking()
