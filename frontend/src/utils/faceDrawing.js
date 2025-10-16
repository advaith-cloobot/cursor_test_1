// Simple utility for drawing face bounding boxes on canvas
// This is a lightweight utility that only handles drawing, not detection

export const drawFaceBoundingBoxes = (canvas, faces, imageElement) => {
  if (!canvas || !faces || faces.length === 0) return;
  
  const ctx = canvas.getContext('2d');
  
  // Use displayed image dimensions, not natural dimensions
  const displayedWidth = imageElement.offsetWidth;
  const displayedHeight = imageElement.offsetHeight;
  
  // Clear canvas first
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  faces.forEach((face, index) => {
    // Convert normalized coordinates to pixel coordinates using displayed dimensions
    const x = face.bbox_x * displayedWidth;
    const y = face.bbox_y * displayedHeight;
    const width = face.bbox_width * displayedWidth;
    const height = face.bbox_height * displayedHeight;
    
    // Debug logging
    console.log(`Face ${index + 1} coordinates:`, {
      normalized: {
        x: face.bbox_x,
        y: face.bbox_y,
        width: face.bbox_width,
        height: face.bbox_height
      },
      pixel: {
        x: x,
        y: y,
        width: width,
        height: height
      },
      naturalImageSize: {
        width: imageElement.naturalWidth,
        height: imageElement.naturalHeight
      },
      displayedImageSize: {
        width: displayedWidth,
        height: displayedHeight
      },
      canvasSize: {
        width: canvas.width,
        height: canvas.height
      }
    });
    
    // Draw bounding box
    ctx.strokeStyle = '#C82FFF';
    ctx.lineWidth = 2;
    ctx.strokeRect(x, y, width, height);
    
    // Draw face number
    ctx.fillStyle = '#C82FFF';
    ctx.font = '14px Montserrat';
    ctx.fillText(`Face ${index + 1}`, x, y - 5);
  });
};

export const createFaceInputBoxes = (faces, imageElement, onFaceNameChange, editingFace, setEditingFace) => {
  if (!faces || faces.length === 0) return null;
  
  const displayedWidth = imageElement.offsetWidth;
  const displayedHeight = imageElement.offsetHeight;
  
  return faces.map((face, index) => {
    const x = face.bbox_x * displayedWidth;
    const y = face.bbox_y * displayedHeight;
    const width = face.bbox_width * displayedWidth;
    const height = face.bbox_height * displayedHeight;
    
    // Position input box below the face box
    const inputX = x;
    const inputY = y + height + 5;
    const inputWidth = Math.max(120, width);
    
    return (
      <div
        key={face.id}
        className="face-input-overlay"
        style={{
          position: 'absolute',
          left: inputX,
          top: inputY,
          width: inputWidth,
          zIndex: 10
        }}
      >
        {editingFace === face.id ? (
          <input
            type="text"
            placeholder="Enter name"
            defaultValue={face.name || ''}
            onBlur={(e) => onFaceNameChange(face.id, e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                onFaceNameChange(face.id, e.target.value);
              }
            }}
            autoFocus
            className="face-name-input-overlay"
          />
        ) : (
          <div 
            className="face-name-display-overlay"
            onClick={() => setEditingFace(face.id)}
          >
            {face.name || 'Click to add name'}
          </div>
        )}
      </div>
    );
  });
};

export const clearCanvas = (canvas) => {
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);
};
