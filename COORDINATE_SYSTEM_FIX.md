# Face Detection Coordinate System Fix

## 🎯 **Problem Identified:**
The face bounding boxes were misaligned because of a **coordinate system mismatch** between:
- **Backend**: Calculates coordinates based on natural image dimensions
- **Frontend**: Displays image at different size due to CSS scaling (`max-width: 100%`, `object-fit: contain`)

## 🔧 **Root Cause:**
```css
.photo-modal-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;  /* This scales the image! */
}
```

The image was being **scaled down** by CSS, but the canvas was sized to the **natural image dimensions**, creating a mismatch.

## ✅ **Solution Implemented:**

### **1. Canvas Sizing Fix:**
```javascript
// OLD: Used natural image dimensions
canvasRef.current.width = imageRef.current.width;
canvasRef.current.height = imageRef.current.height;

// NEW: Use displayed image dimensions
const displayedWidth = imageRef.current.offsetWidth;
const displayedHeight = imageRef.current.offsetHeight;
canvasRef.current.width = displayedWidth;
canvasRef.current.height = displayedHeight;
```

### **2. Coordinate Calculation Fix:**
```javascript
// OLD: Used natural dimensions with scaling
const scaleX = canvas.width / imageElement.width;
const scaleY = canvas.height / imageElement.height;
const x = face.bbox_x * imageElement.width * scaleX;

// NEW: Use displayed dimensions directly
const displayedWidth = imageElement.offsetWidth;
const displayedHeight = imageElement.offsetHeight;
const x = face.bbox_x * displayedWidth;
```

### **3. Window Resize Handling:**
- Added resize listener to redraw faces when window size changes
- Updates canvas size to match new displayed image size
- Automatically redraws face boxes with correct coordinates

## 🎨 **Expected Results:**

### **Before Fix:**
- Face boxes shifted upwards and too wide
- Mismatch between natural and displayed image sizes
- Boxes not aligned with actual faces

### **After Fix:**
- Face boxes should be precisely aligned with faces
- Canvas matches displayed image size exactly
- Coordinates calculated using correct dimensions
- Responsive to window resizing

## 🔍 **Debug Information:**
Added comprehensive logging to track:
- Normalized coordinates from backend
- Natural vs displayed image dimensions
- Canvas dimensions
- Final pixel coordinates for drawing

## 📱 **Testing:**
1. Open photo modal with face detection
2. Check browser console for coordinate debug info
3. Verify face boxes align with actual faces
4. Test window resizing to ensure boxes stay aligned

The coordinate system should now be perfectly aligned! 🎯
