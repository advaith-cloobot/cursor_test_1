import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getAlbumFaces, updateFaceName, deleteFace } from '../api';
import './FaceLibrary.css';

function FaceLibrary() {
  const { albumId } = useParams();
  const navigate = useNavigate();
  const [faces, setFaces] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingFace, setEditingFace] = useState(null);
  const [albumName, setAlbumName] = useState('Face Library');

  useEffect(() => {
    fetchFaces();
  }, [albumId]);

  const fetchFaces = async () => {
    try {
      setLoading(true);
      const response = await getAlbumFaces(albumId);
      setFaces(response.data);
    } catch (error) {
      console.error('Error fetching faces:', error);
    } finally {
      setLoading(false);
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

  const handleDeleteFace = async (faceId) => {
    try {
      await deleteFace(albumId, faceId);
      setFaces(faces.filter(face => face.id !== faceId));
    } catch (error) {
      console.error('Error deleting face:', error);
      alert('Error deleting face. Please try again.');
    }
  };

  const handleBack = () => {
    navigate(`/albums/${albumId}`);
  };

  if (loading) {
    return (
      <div className="face-library-container">
        <div className="face-library-header">
          <button className="back-btn" onClick={handleBack}>
            <span className="material-symbols-outlined">arrow_back</span>
            Back to Album
          </button>
          <h1>Face Library</h1>
        </div>
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading faces...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="face-library-container">
      <div className="face-library-header">
        <button className="back-btn" onClick={handleBack}>
          <span className="material-symbols-outlined">arrow_back</span>
          Back to Album
        </button>
        <h1>Face Library</h1>
        <div className="face-stats">
          <span className="face-count">{faces.length} faces detected</span>
        </div>
      </div>

      {faces.length === 0 ? (
        <div className="empty-faces-state">
          <span className="material-symbols-outlined empty-icon">face</span>
          <h3>No faces detected yet</h3>
          <p>Open photos in the album and use the "Detect Faces" feature to find faces</p>
        </div>
      ) : (
        <div className="faces-grid">
          {faces.map((face, index) => (
            <div key={face.id} className="face-card">
              <div className="face-card-header">
                <span className="face-number">Face {index + 1}</span>
                <button 
                  className="delete-face-btn"
                  onClick={() => handleDeleteFace(face.id)}
                  title="Delete face"
                >
                  <span className="material-symbols-outlined">delete</span>
                </button>
              </div>
              
              <div className="face-card-body">
                {/* Photo thumbnail with face box overlay */}
                {face.photo && (
                  <div className="face-photo-container">
                    <img 
                      src={`http://127.0.0.1:5000/uploads/album_${albumId}/${face.photo.stored_filename}`}
                      alt={face.photo.original_filename}
                      className="face-photo-thumbnail"
                    />
                    <div 
                      className="face-box-overlay"
                      style={{
                        left: `${face.bbox_x * 100}%`,
                        top: `${face.bbox_y * 100}%`,
                        width: `${face.bbox_width * 100}%`,
                        height: `${face.bbox_height * 100}%`
                      }}
                      title={`Face ${index + 1} - ${face.name || 'Unnamed'} (${Math.round(face.confidence * 100)}% confidence)`}
                    />
                    {/* Face number label */}
                    <div 
                      className="face-number-overlay"
                      style={{
                        left: `${face.bbox_x * 100}%`,
                        top: `${(face.bbox_y - 0.02) * 100}%`, // Slightly above the box
                        fontSize: '12px',
                        color: '#C82FFF',
                        fontWeight: 'bold',
                        textShadow: '1px 1px 2px rgba(0,0,0,0.8)',
                        pointerEvents: 'none'
                      }}
                    >
                      Face {index + 1}
                    </div>
                  </div>
                )}
                
                {/* Face name input/display */}
                <div className="face-name-section">
                  {editingFace === face.id ? (
                    <input
                      type="text"
                      placeholder="Enter name"
                      defaultValue={face.name || ''}
                      onBlur={(e) => handleFaceNameChange(face.id, e.target.value)}
                      onKeyPress={(e) => {
                        if (e.key === 'Enter') {
                          handleFaceNameChange(face.id, e.target.value);
                        }
                      }}
                      autoFocus
                      className="face-name-input"
                    />
                  ) : (
                    <div 
                      className="face-name-display"
                      onClick={() => setEditingFace(face.id)}
                    >
                      {face.name || 'Click to add name'}
                    </div>
                  )}
                </div>
                
                <div className="face-metadata">
                  <div className="metadata-item">
                    <span className="metadata-label">Confidence:</span>
                    <span className="metadata-value">
                      {Math.round(face.confidence * 100)}%
                    </span>
                  </div>
                  {face.photo && (
                    <div className="metadata-item">
                      <span className="metadata-label">From:</span>
                      <span className="metadata-value">
                        {face.photo.original_filename}
                      </span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default FaceLibrary;
