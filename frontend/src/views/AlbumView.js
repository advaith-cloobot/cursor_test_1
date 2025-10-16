import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Photo from '../components/Photo';
import PhotoUpload from '../components/PhotoUpload';
import { getAlbumPhotos, uploadPhoto, deletePhoto } from '../api';
import './AlbumView.css';

function AlbumView() {
  const { albumId } = useParams();
  const navigate = useNavigate();
  const [photos, setPhotos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [albumName, setAlbumName] = useState('Album');

  useEffect(() => {
    fetchPhotos();
  }, [albumId]);

  const fetchPhotos = async () => {
    try {
      setLoading(true);
      const response = await getAlbumPhotos(albumId);
      setPhotos(response.data);
    } catch (error) {
      console.error('Error fetching photos:', error);
      if (error.response?.status === 404) {
        alert('Album not found');
        navigate('/');
      } else {
        alert('Error loading photos. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handlePhotoUpload = async (file) => {
    try {
      const response = await uploadPhoto(albumId, file);
      setPhotos([response.data, ...photos]);
      return response.data;
    } catch (error) {
      console.error('Error uploading photo:', error);
      throw error;
    }
  };

  const handlePhotoDelete = async (photoId) => {
    try {
      await deletePhoto(albumId, photoId);
      setPhotos(photos.filter((photo) => photo.id !== photoId));
    } catch (error) {
      console.error('Error deleting photo:', error);
      alert('Error deleting photo. Please try again.');
    }
  };

  const handleBack = () => {
    navigate('/');
  };

  if (loading) {
    return (
      <div className="album-view-container">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading photos...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="album-view-container">
      <div className="album-view-header">
        <button className="back-btn" onClick={handleBack}>
          <span className="material-symbols-outlined">arrow_back</span>
          <span>Back to Albums</span>
        </button>
        <h2>{albumName}</h2>
      </div>

      <PhotoUpload albumId={albumId} onUploadComplete={handlePhotoUpload} />

      {photos.length === 0 ? (
        <div className="empty-photos-state">
          <span className="material-symbols-outlined empty-icon">photo</span>
          <h3>No photos yet</h3>
          <p>Upload your first photo using the area above</p>
        </div>
      ) : (
        <div className="photo-grid">
          {photos.map((photo) => (
            <Photo
              key={photo.id}
              photo={photo}
              albumId={albumId}
              onDelete={handlePhotoDelete}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default AlbumView;

