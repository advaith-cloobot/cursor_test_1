import React from 'react';
import { getPhotoUrl } from '../api';
import './Photo.css';

function Photo({ photo, albumId, onDelete }) {
  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this photo?')) {
      onDelete(photo.id);
    }
  };

  return (
    <div className="photo-item">
      <img
        src={getPhotoUrl(albumId, photo.stored_filename)}
        alt={photo.original_filename}
        className="photo-image"
        loading="lazy"
      />
      <div className="photo-overlay">
        <div className="photo-info">
          <p className="photo-filename">{photo.original_filename}</p>
        </div>
        <button className="photo-delete-btn" onClick={handleDelete}>
          <span className="material-symbols-outlined">delete</span>
        </button>
      </div>
    </div>
  );
}

export default Photo;

