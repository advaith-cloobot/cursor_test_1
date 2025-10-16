import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AlbumList from './views/AlbumList';
import AlbumView from './views/AlbumView';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="app-header">
          <h1>Photo Organiser</h1>
        </header>
        <main className="app-main">
          <Routes>
            <Route path="/" element={<AlbumList />} />
            <Route path="/album/:albumId" element={<AlbumView />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

