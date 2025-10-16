import React, { useState, useEffect } from 'react';
import AlbumCard from '../components/AlbumCard';
import AlbumForm from '../components/AlbumForm';
import { getAllAlbums, createAlbum, updateAlbum, deleteAlbum } from '../api';
import './AlbumList.css';

function AlbumList() {
  const [albums, setAlbums] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingAlbum, setEditingAlbum] = useState(null);

  useEffect(() => {
    fetchAlbums();
  }, []);

  const fetchAlbums = async () => {
    try {
      setLoading(true);
      const response = await getAllAlbums();
      setAlbums(response.data);
    } catch (error) {
      console.error('Error fetching albums:', error);
      alert('Error loading albums. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateAlbum = () => {
    setEditingAlbum(null);
    setIsFormOpen(true);
  };

  const handleEditAlbum = (album) => {
    setEditingAlbum(album);
    setIsFormOpen(true);
  };

  const handleDeleteAlbum = async (albumId) => {
    try {
      await deleteAlbum(albumId);
      setAlbums(albums.filter((album) => album.id !== albumId));
    } catch (error) {
      console.error('Error deleting album:', error);
      alert('Error deleting album. Please try again.');
    }
  };

  const handleFormSubmit = async (data) => {
    try {
      if (editingAlbum) {
        const response = await updateAlbum(editingAlbum.id, data);
        setAlbums(albums.map((album) =>
          album.id === editingAlbum.id ? response.data : album
        ));
      } else {
        const response = await createAlbum(data);
        setAlbums([response.data, ...albums]);
      }
      setIsFormOpen(false);
      setEditingAlbum(null);
    } catch (error) {
      console.error('Error saving album:', error);
      alert('Error saving album. Please try again.');
    }
  };

  const handleFormClose = () => {
    setIsFormOpen(false);
    setEditingAlbum(null);
  };

  if (loading) {
    return (
      <div className="album-list-container">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading albums...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="album-list-container">
      <div className="album-list-header">
        <h2>My Albums</h2>
        <button className="create-album-btn" onClick={handleCreateAlbum}>
          <span className="material-symbols-outlined">add</span>
          <span>Create Album</span>
        </button>
      </div>

      {albums.length === 0 ? (
        <div className="empty-state">
          <span className="material-symbols-outlined empty-icon">photo_library</span>
          <h3>No albums yet</h3>
          <p>Create your first album to start organizing your photos</p>
          <button className="create-album-btn-large" onClick={handleCreateAlbum}>
            <span className="material-symbols-outlined">add</span>
            <span>Create Your First Album</span>
          </button>
        </div>
      ) : (
        <div className="album-grid">
          {albums.map((album) => (
            <AlbumCard
              key={album.id}
              album={album}
              onEdit={handleEditAlbum}
              onDelete={handleDeleteAlbum}
            />
          ))}
        </div>
      )}

      <AlbumForm
        isOpen={isFormOpen}
        onClose={handleFormClose}
        onSubmit={handleFormSubmit}
        album={editingAlbum}
      />
    </div>
  );
}

export default AlbumList;

