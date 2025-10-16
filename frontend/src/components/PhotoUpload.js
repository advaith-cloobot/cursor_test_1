import React, { useState, useRef } from 'react';
import './PhotoUpload.css';

function PhotoUpload({ albumId, onUploadComplete }) {
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef(null);

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFiles(files);
    }
  };

  const handleFileSelect = (e) => {
    const files = e.target.files;
    if (files.length > 0) {
      handleFiles(files);
    }
  };

  const handleFiles = async (files) => {
    const validFiles = Array.from(files).filter((file) => {
      const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/heic', 'image/heif'];
      return validTypes.includes(file.type) || file.name.toLowerCase().endsWith('.heic');
    });

    if (validFiles.length === 0) {
      alert('Please select valid image files (PNG, JPEG, or HEIC)');
      return;
    }

    setUploading(true);

    try {
      for (const file of validFiles) {
        await onUploadComplete(file);
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert('Error uploading files. Please try again.');
    } finally {
      setUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div
      className={`photo-upload ${isDragging ? 'dragging' : ''} ${uploading ? 'uploading' : ''}`}
      onDragEnter={handleDragEnter}
      onDragLeave={handleDragLeave}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
      onClick={handleClick}
    >
      <input
        ref={fileInputRef}
        type="file"
        accept="image/png,image/jpeg,image/jpg,.heic,.heif"
        multiple
        onChange={handleFileSelect}
        className="file-input"
      />
      <div className="upload-content">
        {uploading ? (
          <>
            <div className="upload-spinner"></div>
            <p className="upload-text">Uploading...</p>
          </>
        ) : (
          <>
            <span className="material-symbols-outlined upload-icon">cloud_upload</span>
            <p className="upload-text">
              Drag & drop photos here or click to select
            </p>
            <p className="upload-subtext">
              Supports PNG, JPEG, and HEIC formats
            </p>
          </>
        )}
      </div>
    </div>
  );
}

export default PhotoUpload;

