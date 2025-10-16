import React, { useEffect, useState, useRef } from 'react';
import { getPhotoUrl, getPhotoFaces, updateFaceName, detectFacesOpenCV } from '../api';
import { formatFileSize, getCompressionRatio } from '../utils/fileSize';
import { drawFaceBoundingBoxes, clearCanvas, createFaceInputBoxes } from '../utils/faceDrawing';
import './PhotoModal.css';

function PhotoModal({ photo, albumId, isOpen, onClose, onDelete }) {
  const [faces, setFaces] = useState([]);
  const [detecting, setDetecting] = useState(false);
  const [editingFace, setEditingFace] = useState(null);
  const canvasRef = useRef(null);
  const imageRef = useRef(null);

  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    const handleResize = () => {
      // Redraw faces when window is resized (affects displayed image size)
      if (faces.length > 0 && canvasRef.current && imageRef.current) {
        // Update canvas size to match new displayed image size
        const displayedWidth = imageRef.current.offsetWidth;
        const displayedHeight = imageRef.current.offsetHeight;
        canvasRef.current.width = displayedWidth;
        canvasRef.current.height = displayedHeight;
        canvasRef.current.style.width = displayedWidth + 'px';
        canvasRef.current.style.height = displayedHeight + 'px';
        
        // Redraw faces with new dimensions
        setTimeout(() => redrawFaces(), 100);
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      window.addEventListener('resize', handleResize);
      document.body.style.overflow = 'hidden';
      // Reset faces state when opening modal
      setFaces([]);
      setEditingFace(null);
      // Load existing faces first, then detect new ones
      loadFaces();
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      window.removeEventListener('resize', handleResize);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose, photo]);

  // Redraw faces when faces state changes
  useEffect(() => {
    if (isOpen && faces.length > 0) {
      // Small delay to ensure canvas and image are ready
      setTimeout(() => {
        redrawFaces();
      }, 100);
    }
  }, [faces, isOpen]);

  const loadFaces = async () => {
    if (!photo) return;
    
    try {
      const response = await getPhotoFaces(albumId, photo.id);
      setFaces(response.data);
      
      // Redraw face boxes if faces exist
      if (response.data.length > 0 && canvasRef.current && imageRef.current) {
        drawFaceBoundingBoxes(canvasRef.current, response.data, imageRef.current);
      }
      
      // Always trigger face detection when opening image
      // This will either detect new faces or refresh existing ones
      setTimeout(() => autoDetectFaces(), 200);
    } catch (error) {
      console.error('Error loading faces:', error);
      // Even if loading fails, still try to detect faces
      setTimeout(() => autoDetectFaces(), 200);
    }
  };

  const redrawFaces = () => {
    if (faces.length > 0 && canvasRef.current && imageRef.current) {
      clearCanvas(canvasRef.current);
      drawFaceBoundingBoxes(canvasRef.current, faces, imageRef.current);
    }
  };

  const autoDetectFaces = async () => {
    if (!imageRef.current || detecting) return; // Only prevent if currently detecting
    
    setDetecting(true);
    try {
      // Use OpenCV face detection on the backend
      const response = await detectFacesOpenCV(albumId, photo.id);
      
      if (response.data.faces && response.data.faces.length > 0) {
        setFaces(response.data.faces);
        
        // Draw face boxes on canvas
        if (canvasRef.current) {
          clearCanvas(canvasRef.current);
          drawFaceBoundingBoxes(canvasRef.current, response.data.faces, imageRef.current);
        }
      } else {
        console.log('No faces detected by OpenCV');
        // Clear any existing faces if no new ones detected
        setFaces([]);
      }
    } catch (error) {
      console.error('Error in OpenCV face detection:', error);
    } finally {
      setDetecting(false);
    }
  };


  const handleFaceNameChange = async (faceId, name) => {
    try {
      await updateFaceName(albumId, faceId, name);
      setFaces(faces.map(face => 
        face.id === faceId ? { ...face, name } : face
      ));
      setEditingFace(null);
    } catch (error) {
      console.error('Error updating face name:', error);
      alert('Error updating face name. Please try again.');
    }
  };

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
          <div className="photo-container">
            <img
              ref={imageRef}
              src={getPhotoUrl(albumId, photo.stored_filename)}
              alt={photo.original_filename}
              className="photo-modal-image"
              onLoad={() => {
                if (canvasRef.current && imageRef.current) {
                  // Set canvas size to match the displayed image size, not natural size
                  const displayedWidth = imageRef.current.offsetWidth;
                  const displayedHeight = imageRef.current.offsetHeight;
                  canvasRef.current.width = displayedWidth;
                  canvasRef.current.height = displayedHeight;
                  canvasRef.current.style.width = displayedWidth + 'px';
                  canvasRef.current.style.height = displayedHeight + 'px';
                }
                // Redraw existing faces if any (detection is handled in loadFaces)
                setTimeout(() => redrawFaces(), 100);
              }}
            />
            <canvas
              ref={canvasRef}
              className="face-detection-canvas"
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                pointerEvents: 'none'
              }}
            />
            {/* Face input boxes positioned below face boxes */}
            {faces.length > 0 && imageRef.current && createFaceInputBoxes(
              faces, 
              imageRef.current, 
              handleFaceNameChange, 
              editingFace, 
              setEditingFace
            )}
          </div>
          
          <div className="faces-section">
            <h4>Detected Faces</h4>
            {faces.length > 0 ? (
              <div className="faces-list">
                {faces.map((face, index) => (
                  <div key={face.id} className="face-item">
                    <div className="face-info">
                      <span className="face-number">Face {index + 1}</span>
                      <span className="face-confidence">
                        {Math.round(face.confidence * 100)}% confidence
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-faces-message">
                <span className="material-symbols-outlined">face</span>
                <p>No faces detected yet. Face detection will run automatically when you view this photo.</p>
              </div>
            )}
          </div>
          
          {detecting && (
            <div className="face-detection-section">
              <div className="detecting-faces-message">
                <div className="detecting-spinner"></div>
                <span>Detecting faces...</span>
              </div>
            </div>
          )}
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
