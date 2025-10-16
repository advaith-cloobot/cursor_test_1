import React, { useState, useEffect } from 'react';
import './Toast.css';

function Toast({ message, type = 'success', duration = 3000, onClose }) {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(false);
      if (onClose) {
        setTimeout(onClose, 300); // Wait for animation to complete
      }
    }, duration);

    return () => clearTimeout(timer);
  }, [duration, onClose]);

  if (!isVisible) return null;

  return (
    <div className={`toast toast-${type} ${isVisible ? 'toast-visible' : ''}`}>
      <div className="toast-content">
        <span className="material-symbols-outlined toast-icon">
          {type === 'success' ? 'check_circle' : type === 'error' ? 'error' : 'info'}
        </span>
        <span className="toast-message">{message}</span>
        <button className="toast-close" onClick={() => setIsVisible(false)}>
          <span className="material-symbols-outlined">close</span>
        </button>
      </div>
    </div>
  );
}

export default Toast;
