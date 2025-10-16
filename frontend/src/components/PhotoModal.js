import React, { useEffect } from 'react';
import { getPhotoUrl } from '../api';
import { formatFileSize, getCompressionRatio } from '../utils/fileSize';
import './PhotoModal.css';

function PhotoModal({ photo, albumId, isOpen, onClose, onDelete }) {
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  if (!isOpen || !photo) return null;

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this photo?')) {
      onDelete(photo.id);
      onClose();
    }
  };

  const compressionRatio = getCompressionRatio(photo.original_size, photo.stored_size);

  return (
    <div className="photo-modal-overlay" onClick={onClose}>
      <div className="photo-modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="photo-modal-header">
          <div className="photo-modal-title">
            <h3>{photo.original_filename}</h3>
            {photo.original_size && photo.stored_size && (
              <div className="photo-modal-file-info">
                <span className="file-size-info">
                  {formatFileSize(photo.original_size)} → {formatFileSize(photo.stored_size)}
                </span>
                {compressionRatio && (
                  <span className="compression-badge">
                    {compressionRatio}% smaller
                  </span>
                )}
              </div>
            )}
          </div>
          <div className="photo-modal-actions">
            <button 
              className="photo-modal-btn download-btn" 
              onClick={() => {
                const link = document.createElement('a');
                link.href = getPhotoUrl(albumId, photo.stored_filename);
                link.download = photo.original_filename;
                link.click();
              }}
              title="Download photo"
            >
              <span className="material-symbols-outlined">download</span>
            </button>
            <button 
              className="photo-modal-btn delete-btn" 
              onClick={handleDelete}
              title="Delete photo"
            >
              <span className="material-symbols-outlined">delete</span>
            </button>
            <button 
              className="photo-modal-btn close-btn" 
              onClick={onClose}
              title="Close"
            >
              <span className="material-symbols-outlined">close</span>
            </button>
          </div>
        </div>
        
        <div className="photo-modal-body">
          <img
            src={getPhotoUrl(albumId, photo.stored_filename)}
            alt={photo.original_filename}
            className="photo-modal-image"
          />
        </div>
        
        <div className="photo-modal-footer">
          <div className="photo-modal-metadata">
            <div className="metadata-item">
              <span className="metadata-label">Filename:</span>
              <span className="metadata-value">{photo.original_filename}</span>
            </div>
            <div className="metadata-item">
              <span className="metadata-label">Uploaded:</span>
              <span className="metadata-value">
                {new Date(photo.created_at).toLocaleString()}
              </span>
            </div>
            {photo.original_size && photo.stored_size && (
              <>
                <div className="metadata-item">
                  <span className="metadata-label">Original Size:</span>
                  <span className="metadata-value">{formatFileSize(photo.original_size)}</span>
                </div>
                <div className="metadata-item">
                  <span className="metadata-label">Stored Size:</span>
                  <span className="metadata-value">{formatFileSize(photo.stored_size)}</span>
                </div>
                {compressionRatio && (
                  <div className="metadata-item">
                    <span className="metadata-label">Compression:</span>
                    <span className="metadata-value compression-value">
                      {compressionRatio}% smaller
                    </span>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default PhotoModal;
