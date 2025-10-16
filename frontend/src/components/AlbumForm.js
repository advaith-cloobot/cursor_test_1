import React, { useState, useEffect } from 'react';
import './AlbumForm.css';

function AlbumForm({ isOpen, onClose, onSubmit, album }) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');

  useEffect(() => {
    if (album) {
      setName(album.name);
      setDescription(album.description || '');
    } else {
      setName('');
      setDescription('');
    }
  }, [album]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name.trim()) {
      alert('Album name is required');
      return;
    }
    onSubmit({ name: name.trim(), description: description.trim() });
    setName('');
    setDescription('');
  };

  const handleClose = () => {
    setName('');
    setDescription('');
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={handleClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{album ? 'Edit Album' : 'Create New Album'}</h2>
          <button className="modal-close-btn" onClick={handleClose}>
            <span className="material-symbols-outlined">close</span>
          </button>
        </div>
        <form onSubmit={handleSubmit} className="album-form">
          <div className="form-group">
            <label htmlFor="album-name">Album Name *</label>
            <input
              id="album-name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter album name"
              className="form-input"
              autoFocus
            />
          </div>
          <div className="form-group">
            <label htmlFor="album-description">Description</label>
            <textarea
              id="album-description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Enter album description (optional)"
              className="form-textarea"
              rows="4"
            />
          </div>
          <div className="form-actions">
            <button type="button" onClick={handleClose} className="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              {album ? 'Update' : 'Create'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default AlbumForm;

