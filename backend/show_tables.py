#!/usr/bin/env python3
"""
Script to show the exact SQL CREATE TABLE statements used
"""

import sqlite3
import os
from app import app

def show_create_statements():
    """Show the CREATE TABLE statements for all tables"""
    print("SQLite CREATE TABLE Statements")
    print("=" * 50)
    
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
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            print(f"\n-- Table: {table_name}")
            print("-" * 30)
            
            # Get CREATE statement
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            create_sql = cursor.fetchone()
            
            if create_sql and create_sql[0]:
                print(create_sql[0])
            else:
                print(f"CREATE statement not found for {table_name}")
        
        # Show indexes
        print(f"\n-- Indexes")
        print("-" * 30)
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND sql IS NOT NULL;")
        indexes = cursor.fetchall()
        
        if indexes:
            for idx_name, idx_sql in indexes:
                print(f"-- {idx_name}")
                print(idx_sql)
        else:
            print("No custom indexes found")
        
        # Show foreign key constraints
        print(f"\n-- Foreign Key Constraints")
        print("-" * 30)
        cursor.execute("PRAGMA foreign_key_list(photos);")
        fks = cursor.fetchall()
        
        if fks:
            for fk in fks:
                print(f"FOREIGN KEY ({fk[3]}) REFERENCES {fk[2]}({fk[4]})")
        else:
            print("No foreign key constraints found")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    show_create_statements()
