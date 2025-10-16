# Photo Organiser Database Guide

This guide explains the SQLite database structure, management, and operations for the Photo Organiser application.

## Database Overview

The Photo Organiser uses SQLite as its database, managed through SQLAlchemy ORM. The database is automatically created when the Flask application starts.

### Database Location
- **Windows**: `backend\instance\database.db`
- **macOS/Linux**: `backend/instance/database.db`

## Database Schema

### Albums Table

| Column      | Type      | Constraints           | Description                    |
|-------------|-----------|----------------------|--------------------------------|
| id          | INTEGER   | PRIMARY KEY, AUTO    | Unique album identifier        |
| name        | TEXT      | NOT NULL             | Album name                     |
| description | TEXT      | NULL                 | Album description (optional)   |
| created_at  | DATETIME  | DEFAULT CURRENT_TIME | Creation timestamp             |
| status      | INTEGER   | NOT NULL, DEFAULT 1 | 1=active, 0=archived           |

### Photos Table

| Column            | Type      | Constraints           | Description                    |
|-------------------|-----------|----------------------|--------------------------------|
| id                | INTEGER   | PRIMARY KEY, AUTO    | Unique photo identifier        |
| album_id          | INTEGER   | NOT NULL, FOREIGN KEY| References albums.id           |
| original_filename | TEXT      | NOT NULL             | Original uploaded filename     |
| stored_filename   | TEXT      | NOT NULL, UNIQUE     | Compressed stored filename     |
| created_at        | DATETIME  | DEFAULT CURRENT_TIME | Upload timestamp               |
| status            | INTEGER   | NOT NULL, DEFAULT 1 | 1=active, 0=archived           |

### Relationships

- **One-to-Many**: Albums → Photos
- **Foreign Key**: `photos.album_id` → `albums.id`
- **Soft Delete**: Both tables use `status` column for soft deletes

## Database Management

### Initialization

The database is automatically created when you start the Flask application. However, you can manually initialize it:

```bash
# Navigate to backend directory
cd backend

# Initialize database
python init_database.py

# Or use the management script
python manage_database.py init
```

### Management Commands

Use the `manage_database.py` script for database operations:

```bash
# Show database status
python manage_database.py status

# Create sample data
python manage_database.py sample

# Create backup
python manage_database.py backup

# Restore from backup
python manage_database.py restore

# Clear all data (WARNING: destructive)
python manage_database.py clear

# Show help
python manage_database.py help
```

### Database Verification

Check database structure and integrity:

```bash
# Run database checker
python check_database.py

# This will show:
# - Database file location
# - Table structure
# - Column definitions
# - Foreign key relationships
# - Sample SQL queries
```

## SQL Queries

### Basic Queries

```sql
-- Get all active albums
SELECT * FROM albums WHERE status = 1;

-- Get all active photos
SELECT * FROM photos WHERE status = 1;

-- Get photos for a specific album
SELECT * FROM photos WHERE album_id = 1 AND status = 1;

-- Count albums and photos
SELECT 
    (SELECT COUNT(*) FROM albums WHERE status = 1) as album_count,
    (SELECT COUNT(*) FROM photos WHERE status = 1) as photo_count;
```

### Advanced Queries

```sql
-- Albums with photo counts
SELECT 
    a.id,
    a.name,
    a.description,
    a.created_at,
    COUNT(p.id) as photo_count
FROM albums a
LEFT JOIN photos p ON a.id = p.album_id AND p.status = 1
WHERE a.status = 1
GROUP BY a.id, a.name, a.description, a.created_at
ORDER BY a.created_at DESC;

-- Recent photos across all albums
SELECT 
    p.id,
    p.original_filename,
    p.created_at,
    a.name as album_name
FROM photos p
JOIN albums a ON p.album_id = a.id
WHERE p.status = 1 AND a.status = 1
ORDER BY p.created_at DESC
LIMIT 10;

-- Storage usage by album
SELECT 
    a.name,
    COUNT(p.id) as photo_count,
    SUM(LENGTH(p.stored_filename)) as filename_length
FROM albums a
LEFT JOIN photos p ON a.id = p.album_id AND p.status = 1
WHERE a.status = 1
GROUP BY a.id, a.name
ORDER BY photo_count DESC;
```

### Maintenance Queries

```sql
-- Find orphaned photos (album deleted but photos remain)
SELECT p.* FROM photos p
LEFT JOIN albums a ON p.album_id = a.id
WHERE a.id IS NULL;

-- Find albums with no photos
SELECT a.* FROM albums a
LEFT JOIN photos p ON a.id = p.album_id AND p.status = 1
WHERE a.status = 1 AND p.id IS NULL;

-- Clean up archived records (permanent delete)
DELETE FROM photos WHERE status = 0;
DELETE FROM albums WHERE status = 0;
```

## File Storage

### Upload Directory Structure

```
backend/uploads/
├── album_1/
│   ├── uuid1.jpg
│   ├── uuid2.jpg
│   └── ...
├── album_2/
│   ├── uuid3.jpg
│   └── ...
└── ...
```

### File Naming Convention

- **Original filename**: Stored in `photos.original_filename`
- **Stored filename**: UUID-based (e.g., `a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg`)
- **Format**: All images stored as JPEG after compression
- **Quality**: 50% compression for optimal size/quality balance

## Backup and Recovery

### Creating Backups

```bash
# Manual backup
python manage_database.py backup

# This creates: database_backup_YYYYMMDD_HHMMSS.db
```

### Restoring Backups

```bash
# List available backups
python manage_database.py restore

# Select backup to restore
```

### Manual Backup (Alternative)

```bash
# Copy database file manually
copy instance\database.db database_backup_manual.db

# Restore manually
copy database_backup_manual.db instance\database.db
```

## Performance Optimization

### Indexes

The database includes these indexes for performance:

```sql
-- Status indexes for soft delete queries
CREATE INDEX idx_albums_status ON albums(status);
CREATE INDEX idx_photos_status ON photos(status);

-- Foreign key index
CREATE INDEX idx_photos_album_id ON photos(album_id);

-- Unique filename index
CREATE INDEX idx_photos_stored_filename ON photos(stored_filename);
```

### Query Optimization Tips

1. **Always filter by status**: Use `WHERE status = 1` for active records
2. **Use LIMIT**: For large datasets, use `LIMIT` clauses
3. **Index usage**: Queries on `album_id`, `status`, and `stored_filename` are optimized
4. **JOIN efficiency**: Use `LEFT JOIN` for optional relationships

## Troubleshooting

### Common Issues

**Database locked error:**
```bash
# Stop all Flask processes
# Check for running processes
tasklist | findstr python

# Kill if necessary
taskkill /PID <process_id> /F
```

**Database corruption:**
```bash
# Check database integrity
python -c "import sqlite3; conn = sqlite3.connect('instance/database.db'); print(conn.execute('PRAGMA integrity_check;').fetchone())"
```

**Missing tables:**
```bash
# Recreate tables
python manage_database.py init
```

### Database Inspection

```bash
# Check database file size
dir instance\database.db

# View database schema
python check_database.py

# Test database connection
python -c "from app import app, db; app.app_context().push(); print('Database connected:', db.engine.url)"
```

## Security Considerations

### Data Protection

1. **Soft Deletes**: Data is archived, not permanently deleted
2. **File Validation**: Only image files are accepted
3. **Size Limits**: 50MB maximum file size
4. **Path Security**: UUID-based filenames prevent directory traversal

### Backup Security

1. **Regular Backups**: Create backups before major changes
2. **Secure Storage**: Store backups in secure locations
3. **Access Control**: Limit database file access permissions

## Migration and Updates

### Schema Changes

If you need to modify the database schema:

1. **Backup first**: `python manage_database.py backup`
2. **Modify models**: Update `models.py`
3. **Recreate tables**: `python manage_database.py clear` then `python manage_database.py init`
4. **Restore data**: If needed, restore from backup

### Data Migration

For complex data migrations, use SQLAlchemy migrations:

```bash
# Install Flask-Migrate
pip install Flask-Migrate

# Initialize migrations
flask db init

# Create migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade
```

## Monitoring and Maintenance

### Regular Tasks

1. **Backup Database**: Weekly or before major changes
2. **Check File Storage**: Monitor `uploads/` directory size
3. **Review Logs**: Check for database errors in application logs
4. **Performance**: Monitor query performance for large datasets

### Health Checks

```bash
# Database health check
python manage_database.py status

# File system check
dir uploads /s

# Application connectivity test
python -c "from app import app; print('App config loaded successfully')"
```

## API Integration

The database is accessed through the Flask API endpoints:

- **GET /albums** - Query albums table
- **POST /albums** - Insert into albums table
- **PUT /albums/<id>** - Update albums table
- **DELETE /albums/<id>** - Soft delete (status = 0)
- **GET /albums/<id>/photos** - Query photos table
- **POST /albums/<id>/photos** - Insert into photos table
- **DELETE /albums/<id>/photos/<photo_id>** - Soft delete photo

All operations use SQLAlchemy ORM for type safety and SQL injection prevention.

---

This database guide provides comprehensive information for managing the Photo Organiser database. For application-specific questions, refer to the main README.md file.
