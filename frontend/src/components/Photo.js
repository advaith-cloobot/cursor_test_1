import React from 'react';
import { getPhotoUrl } from '../api';
import { formatFileSize, getCompressionRatio } from '../utils/fileSize';
import './Photo.css';

function Photo({ photo, albumId, onDelete, onPreview }) {
  const handleDelete = () => {
    onDelete(photo.id);
  };

  const compressionRatio = getCompressionRatio(photo.original_size, photo.stored_size);

  const handlePhotoClick = () => {
    if (onPreview) {
      onPreview(photo);
    }
  };

  return (
    <div className="photo-item" onClick={handlePhotoClick}>
      <img
        src={getPhotoUrl(albumId, photo.stored_filename)}
        alt={photo.original_filename}
        className="photo-image"
        loading="lazy"
      />
      <div className="photo-overlay">
        <div className="photo-info">
          <p className="photo-filename">{photo.original_filename}</p>
          {photo.original_size && photo.stored_size && (
            <div className="photo-file-sizes">
              <div className="file-size-row">
                <span className="file-size-label">Original:</span>
                <span className="file-size-value">{formatFileSize(photo.original_size)}</span>
              </div>
              <div className="file-size-row">
                <span className="file-size-label">Stored:</span>
                <span className="file-size-value">{formatFileSize(photo.stored_size)}</span>
              </div>
              {compressionRatio && (
                <div className="compression-info">
                  <span className="compression-ratio">{compressionRatio}% smaller</span>
                </div>
              )}
            </div>
          )}
        </div>
        <button 
          className="photo-delete-btn" 
          onClick={(e) => {
            e.stopPropagation();
            handleDelete();
          }}
        >
          <span className="material-symbols-outlined">delete</span>
        </button>
      </div>
    </div>
  );
}

export default Photo;

