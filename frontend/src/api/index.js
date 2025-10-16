import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Album APIs
export const getAllAlbums = () => api.get('/albums');

export const createAlbum = (data) => api.post('/albums', data);

export const updateAlbum = (albumId, data) => api.put(`/albums/${albumId}`, data);

export const deleteAlbum = (albumId) => api.delete(`/albums/${albumId}`);

// Photo APIs
export const getAlbumPhotos = (albumId) => api.get(`/albums/${albumId}/photos`);

export const uploadPhoto = (albumId, file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post(`/albums/${albumId}/photos`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const deletePhoto = (albumId, photoId) => api.delete(`/albums/${albumId}/photos/${photoId}`);

export const getPhotoUrl = (albumId, filename) => `${API_BASE_URL}/uploads/${albumId}/${filename}`;

export default api;

