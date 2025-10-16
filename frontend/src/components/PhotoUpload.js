import React, { useState, useRef } from 'react';
import './PhotoUpload.css';

function PhotoUpload({ albumId, onUploadComplete }) {
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState({ current: 0, total: 0 });
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
    const fileArray = Array.from(files);
    const validFiles = fileArray.filter((file) => {
      const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/heic', 'image/heif'];
      return validTypes.includes(file.type) || file.name.toLowerCase().endsWith('.heic');
    });

    if (validFiles.length === 0) {
      alert('Please select valid image files (PNG, JPEG, or HEIC)');
      return;
    }

    if (validFiles.length !== fileArray.length) {
      const invalidCount = fileArray.length - validFiles.length;
      alert(`${invalidCount} file(s) were skipped (invalid format). ${validFiles.length} valid file(s) will be uploaded.`);
    }

    setUploading(true);
    setUploadProgress({ current: 0, total: validFiles.length });

    try {
      // Pass all valid files to the upload handler
      await onUploadComplete(validFiles);
    } catch (error) {
      console.error('Upload error:', error);
      alert('Error uploading files. Please try again.');
    } finally {
      setUploading(false);
      setUploadProgress({ current: 0, total: 0 });
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
            <p className="upload-text">
              Uploading {uploadProgress.current} of {uploadProgress.total} photos...
            </p>
            {uploadProgress.total > 1 && (
              <div className="upload-progress-bar">
                <div 
                  className="upload-progress-fill" 
                  style={{ width: `${(uploadProgress.current / uploadProgress.total) * 100}%` }}
                ></div>
              </div>
            )}
          </>
        ) : (
          <>
            <span className="material-symbols-outlined upload-icon">cloud_upload</span>
            <p className="upload-text">
              Drag & drop photos here or click to select
            </p>
            <p className="upload-subtext">
              Select multiple photos at once • PNG, JPEG, HEIC formats
            </p>
          </>
        )}
      </div>
    </div>
  );
}

export default PhotoUpload;

