import React from 'react';
import { Link } from 'react-router-dom';
import './AlbumCard.css';

function AlbumCard({ album, onEdit, onDelete }) {
  const handleEdit = (e) => {
    e.preventDefault();
    e.stopPropagation();
    onEdit(album);
  };

  const handleDelete = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (window.confirm(`Are you sure you want to delete "${album.name}"?`)) {
      onDelete(album.id);
    }
  };

  return (
    <Link to={`/album/${album.id}`} className="album-card-link">
      <div className="album-card">
        <div className="album-card-content">
          <h3 className="album-card-title">{album.name}</h3>
          <p className="album-card-description">
            {album.description || 'No description'}
          </p>
        </div>
        <div className="album-card-actions">
          <button 
            className="album-card-action-btn" 
            onClick={handleEdit}
            title="Edit album"
          >
            <span className="material-symbols-outlined">edit</span>
          </button>
          <button 
            className="album-card-action-btn delete-btn" 
            onClick={handleDelete}
            title="Delete album"
          >
            <span className="material-symbols-outlined">delete</span>
          </button>
        </div>
      </div>
    </Link>
  );
}

export default AlbumCard;

