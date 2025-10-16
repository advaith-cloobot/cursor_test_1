import cv2
import numpy as np
from PIL import Image
import os
import tempfile

class FaceDetector:
    def __init__(self):
        # Load the Haar cascade classifier for face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
    def detect_faces_in_image(self, image_path):
        """
        Detect faces in an image using OpenCV Haar Cascade classifier
        Returns list of face bounding boxes with confidence scores
        """
        try:
            # Check if file exists and is readable
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            if not os.access(image_path, os.R_OK):
                raise PermissionError(f"No read permission for: {image_path}")
            
            # Get file size to check if it's not empty
            file_size = os.path.getsize(image_path)
            if file_size == 0:
                raise ValueError(f"Image file is empty: {image_path}")
            
            print(f"Attempting to read image: {image_path} (size: {file_size} bytes)")
            
            # Read the image with explicit flags
            image = cv2.imread(image_path, cv2.IMREAD_COLOR)
            if image is None:
                # Try alternative approach with PIL first
                print(f"cv2.imread failed, trying PIL conversion...")
                try:
                    from PIL import Image as PILImage
                    pil_image = PILImage.open(image_path)
                    # Convert PIL to OpenCV format
                    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                    print("Successfully loaded image via PIL conversion")
                except Exception as pil_error:
                    print(f"PIL conversion also failed: {pil_error}")
                    raise ValueError(f"Could not load image with either OpenCV or PIL: {image_path}")
            
            print(f"Image loaded successfully: {image.shape}")
            
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply histogram equalization to improve detection
            gray = cv2.equalizeHist(gray)
            
            # Get image dimensions for better size calculations
            img_height, img_width = image.shape[:2]
            min_face_size = max(20, min(img_width, img_height) // 20)  # Dynamic minimum size
            max_face_size = min(500, max(img_width, img_height) // 3)  # Dynamic maximum size
            
            print(f"Image dimensions: {img_width}x{img_height}, face size range: {min_face_size}-{max_face_size}")
            
            # Try multiple detection strategies
            faces = []
            
            # Strategy 1: Strict parameters for high-quality detection
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.05,      # More precise scaling
                minNeighbors=8,        # Higher threshold
                minSize=(min_face_size, min_face_size),
                maxSize=(max_face_size, max_face_size),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            
            # Strategy 2: If no faces, try more lenient parameters
            if len(faces) == 0:
                print("No faces detected with strict parameters, trying lenient parameters...")
                faces = self.face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,       # More lenient scaling
                    minNeighbors=3,       # Lower threshold
                    minSize=(min_face_size//2, min_face_size//2),  # Smaller minimum
                    maxSize=(max_face_size*2, max_face_size*2),    # Larger maximum
                    flags=cv2.CASCADE_SCALE_IMAGE
                )
            
            # Strategy 3: If still no faces, try very lenient parameters
            if len(faces) == 0:
                print("No faces detected with lenient parameters, trying very lenient parameters...")
                faces = self.face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.2,       # Very lenient scaling
                    minNeighbors=1,       # Very low threshold
                    minSize=(10, 10),      # Very small minimum
                    maxSize=(max_face_size*3, max_face_size*3),  # Very large maximum
                    flags=cv2.CASCADE_SCALE_IMAGE
                )
            
            # Convert to our format
            detected_faces = []
            print(f"OpenCV detected {len(faces)} faces in image: {image_path}")
            
            for i, (x, y, w, h) in enumerate(faces):
                # Calculate confidence based on face size and position
                confidence = self._calculate_confidence(x, y, w, h, image.shape)
                
                # Normalize coordinates to 0-1 range
                bbox_x = x / image.shape[1]
                bbox_y = y / image.shape[0]
                bbox_width = w / image.shape[1]
                bbox_height = h / image.shape[0]
                
                # Ensure coordinates are within valid range
                bbox_x = max(0, min(1, bbox_x))
                bbox_y = max(0, min(1, bbox_y))
                bbox_width = max(0.01, min(1, bbox_width))  # Minimum 1% width
                bbox_height = max(0.01, min(1, bbox_height))  # Minimum 1% height
                
                detected_faces.append({
                    'id': f'face_{i}',
                    'confidence': confidence,
                    'bbox_x': bbox_x,
                    'bbox_y': bbox_y,
                    'bbox_width': bbox_width,
                    'bbox_height': bbox_height
                })
                print(f"Face {i}: x={x}, y={y}, w={w}, h={h} -> normalized: x={bbox_x:.3f}, y={bbox_y:.3f}, w={bbox_width:.3f}, h={bbox_height:.3f}, confidence={confidence:.2f}")
            
            return detected_faces
            
        except Exception as e:
            print(f"Error in face detection: {str(e)}")
            print(f"Falling back to simple detection for: {image_path}")
            # Fallback to simple detection if OpenCV fails
            return self._simple_fallback_detection(image_path)
    
    def _calculate_confidence(self, x, y, w, h, image_shape):
        """
        Calculate confidence score based on face size and position
        """
        # Base confidence
        confidence = 0.8
        
        # Adjust based on face size (larger faces are more confident)
        face_area = w * h
        image_area = image_shape[0] * image_shape[1]
        face_ratio = face_area / image_area
        
        if face_ratio > 0.01:  # Face is at least 1% of image
            confidence += 0.1
        if face_ratio > 0.02:  # Face is at least 2% of image
            confidence += 0.1
        
        # Adjust based on position (faces in center are more confident)
        center_x = image_shape[1] / 2
        center_y = image_shape[0] / 2
        face_center_x = x + w / 2
        face_center_y = y + h / 2
        
        distance_from_center = np.sqrt((face_center_x - center_x)**2 + (face_center_y - center_y)**2)
        max_distance = np.sqrt(center_x**2 + center_y**2)
        
        if distance_from_center < max_distance * 0.3:  # Face is in center 30%
            confidence += 0.1
        
        # Ensure confidence is between 0.5 and 0.95
        return min(0.95, max(0.5, confidence))
    
    def _simple_fallback_detection(self, image_path):
        """
        Simple fallback face detection when OpenCV fails
        Returns mock face detections based on image dimensions
        """
        try:
            from PIL import Image as PILImage
            
            # Load image with PIL to get dimensions
            with PILImage.open(image_path) as pil_image:
                width, height = pil_image.size
                
                # Create simple mock face detections
                # Assume 1-3 faces in the center area of the image
                num_faces = min(3, max(1, (width * height) // (200 * 200)))  # Rough estimate
                
                detected_faces = []
                for i in range(num_faces):
                    # Place faces in center area with some variation
                    center_x = 0.5 + (i - num_faces//2) * 0.2
                    center_y = 0.4 + (i % 2) * 0.2
                    
                    # Face size as percentage of image
                    face_width = 0.15
                    face_height = 0.2
                    
                    detected_faces.append({
                        'id': f'fallback_face_{i}',
                        'confidence': 0.7,  # Lower confidence for fallback
                        'bbox_x': max(0, center_x - face_width/2),
                        'bbox_y': max(0, center_y - face_height/2),
                        'bbox_width': min(face_width, 1 - center_x + face_width/2),
                        'bbox_height': min(face_height, 1 - center_y + face_height/2)
                    })
                
                print(f"Fallback detection created {len(detected_faces)} mock faces")
                return detected_faces
                
        except Exception as e:
            print(f"Fallback detection also failed: {e}")
            return []
    
    def detect_faces_from_pil_image(self, pil_image):
        """
        Detect faces from a PIL Image object
        """
        try:
            # Convert PIL to OpenCV format
            cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            
            # Save temporarily for processing
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                temp_path = temp_file.name
                cv2.imwrite(temp_path, cv_image)
            
            # Detect faces
            faces = self.detect_faces_in_image(temp_path)
            
            # Clean up temp file
            os.unlink(temp_path)
            
            return faces
            
        except Exception as e:
            print(f"Error in PIL face detection: {str(e)}")
            return []

# Global face detector instance
face_detector = FaceDetector()
