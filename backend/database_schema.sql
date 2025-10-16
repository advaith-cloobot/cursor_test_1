-- Photo Organiser Database Schema
-- SQLite database with SQLAlchemy ORM

-- Albums table
CREATE TABLE albums (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status INTEGER NOT NULL DEFAULT 1
);

-- Photos table
CREATE TABLE photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    album_id INTEGER NOT NULL,
    original_filename TEXT NOT NULL,
    stored_filename TEXT NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (album_id) REFERENCES albums (id)
);

-- Indexes for better performance
CREATE INDEX idx_albums_status ON albums(status);
CREATE INDEX idx_photos_album_id ON photos(album_id);
CREATE INDEX idx_photos_status ON photos(status);
CREATE INDEX idx_photos_stored_filename ON photos(stored_filename);

-- Sample data (optional)
INSERT INTO albums (name, description) VALUES 
    ('Vacation Photos', 'Summer vacation 2024'),
    ('Family Events', 'Birthdays, holidays, and celebrations'),
    ('Nature Photography', 'Landscapes and wildlife');

-- Views for common queries
CREATE VIEW active_albums AS
SELECT id, name, description, created_at
FROM albums 
WHERE status = 1;

CREATE VIEW active_photos AS
SELECT p.id, p.album_id, p.original_filename, p.stored_filename, p.created_at, a.name as album_name
FROM photos p
JOIN albums a ON p.album_id = a.id
WHERE p.status = 1 AND a.status = 1;

-- Album with photo count view
CREATE VIEW album_photo_counts AS
SELECT 
    a.id,
    a.name,
    a.description,
    a.created_at,
    COUNT(p.id) as photo_count
FROM albums a
LEFT JOIN photos p ON a.id = p.album_id AND p.status = 1
WHERE a.status = 1
GROUP BY a.id, a.name, a.description, a.created_at;
