import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import Photo from '../components/Photo';
import PhotoUpload from '../components/PhotoUpload';
import PhotoModal from '../components/PhotoModal';
import Toast from '../components/Toast';
import { getAlbumPhotos, uploadPhoto, deletePhoto } from '../api';
import './AlbumView.css';

function AlbumView() {
  const { albumId } = useParams();
  const navigate = useNavigate();
  const [photos, setPhotos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [albumName, setAlbumName] = useState('Album');
  const [toast, setToast] = useState(null);
  const [selectedPhoto, setSelectedPhoto] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    fetchPhotos();
  }, [albumId]);

  const fetchPhotos = async () => {
    try {
      setLoading(true);
      const response = await getAlbumPhotos(albumId);
      setPhotos(response.data.photos);
      setAlbumName(response.data.album_name);
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

  const handleMultiplePhotoUpload = async (files) => {
    const fileArray = Array.from(files);
    const successfulUploads = [];
    const failedUploads = [];

    // Upload files sequentially to provide better progress feedback
    for (let i = 0; i < fileArray.length; i++) {
      const file = fileArray[i];
      try {
        const response = await uploadPhoto(albumId, file);
        successfulUploads.push({ success: true, data: response.data, file: file.name });
        
        // Update photos state immediately for each successful upload
        setPhotos(prevPhotos => [response.data, ...prevPhotos]);
        
        // Note: Face detection will happen automatically when user clicks on the photo
        console.log(`Photo ${file.name} uploaded successfully. Face detection will occur when viewing the photo.`);
        
      } catch (error) {
        console.error(`Error uploading ${file.name}:`, error);
        failedUploads.push({ success: false, error: error.message, file: file.name });
      }
    }

    // Show user feedback
    if (successfulUploads.length > 0 && failedUploads.length === 0) {
      setToast({
        message: `Successfully uploaded ${successfulUploads.length} photo(s)! Face detection will occur when viewing photos.`,
        type: 'success'
      });
    } else if (successfulUploads.length > 0 && failedUploads.length > 0) {
      setToast({
        message: `Uploaded ${successfulUploads.length} photo(s) successfully. ${failedUploads.length} failed.`,
        type: 'info'
      });
    } else if (failedUploads.length > 0) {
      setToast({
        message: `Failed to upload ${failedUploads.length} photo(s). Please try again.`,
        type: 'error'
      });
    }

    return [...successfulUploads, ...failedUploads];
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

  const handlePhotoPreview = (photo) => {
    setSelectedPhoto(photo);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedPhoto(null);
  };

  const handleModalDelete = (photoId) => {
    handlePhotoDelete(photoId);
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
        <Link to={`/album/${albumId}/faces`} className="face-library-btn">
          <span className="material-symbols-outlined">face</span>
          Face Library
        </Link>
      </div>

      <PhotoUpload albumId={albumId} onUploadComplete={handleMultiplePhotoUpload} />

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
              onPreview={handlePhotoPreview}
            />
          ))}
        </div>
      )}

      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}

      <PhotoModal
        photo={selectedPhoto}
        albumId={albumId}
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        onDelete={handleModalDelete}
      />
    </div>
  );
}

export default AlbumView;

