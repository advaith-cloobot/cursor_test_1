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

// Face detection APIs
export const getPhotoFaces = (albumId, photoId) => api.get(`/albums/${albumId}/photos/${photoId}/faces`);


export const updateFaceName = (albumId, faceId, name) => api.put(`/albums/${albumId}/faces/${faceId}`, { name });

export const deleteFace = (albumId, faceId) => api.delete(`/albums/${albumId}/faces/${faceId}`);

export const getAlbumFaces = (albumId) => api.get(`/albums/${albumId}/faces`);

export const detectFacesOpenCV = (albumId, photoId) => api.post(`/albums/${albumId}/photos/${photoId}/detect-faces`);

export default api;

