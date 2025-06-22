import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const ANGLES = ['front', 'leftSide', 'leftSideMirror', 'back', 'rightSide', 'rightSideMirror'];

function App() {
  const [selectedAngle, setSelectedAngle] = useState(null);
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [stream, setStream] = useState(null);
  const [capturedImage, setCapturedImage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState({});
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

  const startCamera = async () => {
    console.log('Starting camera...');
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
    }

    try {
      console.log('Requesting camera permissions...');
      let mediaStream;
      try {
        mediaStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
        console.log('Back camera accessed');
      } catch (err) {
        console.warn('Back camera failed, trying any camera:', err);
        mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
        console.log('Fallback camera accessed');
      }

      setStream(mediaStream);
      setIsCameraActive(true);
      setError(null);

    } catch (err) {
      console.error('Failed to get camera permissions:', err);
      setError('Camera access denied. Please check browser permissions.');
      setIsCameraActive(false);
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
    setIsCameraActive(false);
    setCapturedImage(null);
  };

  const capturePhoto = () => {
    console.log('Attempting to capture photo...');
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      const context = canvas.getContext('2d');

      canvas.width = video.videoWidth || 640;
      canvas.height = video.videoHeight || 480;
      
      try {
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        console.log('Image drawn to canvas');
        
        canvas.toBlob((blob) => {
          if (blob) {
            console.log('Blob created, size:', blob.size);
            setCapturedImage(blob);
          } else {
            console.error('Failed to create blob from canvas');
            setError('Could not capture image.');
          }
          stopCamera();
        }, 'image/jpeg', 0.8);

      } catch (err) {
        console.error('Error capturing photo:', err);
        setError('Failed to capture photo.');
      }
    } else {
      console.error('Video or canvas ref not available');
      setError('Camera not ready.');
    }
  };

  const validateImage = async () => {
    if (!capturedImage || !selectedAngle) return;

    setIsLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const formData = new FormData();
      formData.append('image', capturedImage);
      formData.append('angle', selectedAngle);

      const response = await axios.post(`${BACKEND_URL}/validate`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 30000,
      });

      const result = response.data.status;
      setResults(prev => ({ ...prev, [selectedAngle]: result }));
      
      if (result === 'accepted') {
        setSuccess(`✅ ${selectedAngle} validation successful!`);
      } else {
        setError(`❌ ${selectedAngle} validation failed. Please try again.`);
      }
    } catch (err) {
      console.error('Validation error:', err);
      setError('Failed to validate image. Please check your connection.');
    } finally {
      setIsLoading(false);
      setCapturedImage(null);
    }
  };

  const handleAngleSelect = (angle) => {
    setSelectedAngle(angle);
    setCapturedImage(null);
    setError(null);
    setSuccess(null);
    if (isCameraActive) {
      stopCamera();
    }
  };

  const getStatusIcon = (angle) => {
    const result = results[angle];
    if (result === 'accepted') return '✅';
    if (result === 'rejected') return '❌';
    return null;
  };

  useEffect(() => {
    if (isCameraActive && stream && videoRef.current) {
      console.log('useEffect: Attaching stream to video element.');
      videoRef.current.srcObject = stream;
      videoRef.current.onloadedmetadata = () => {
        videoRef.current.play().catch(e => console.error("Error playing video:", e));
      };
    }
  }, [isCameraActive, stream]);

  return (
    <div className="container">
      <div className="header">
        <h1>📷 Car Angle Validator</h1>
        <p>Select an angle and capture a photo to validate</p>
      </div>

      <div className="content">
        <div className="angle-grid">
          {ANGLES.map((angle) => (
            <button
              key={angle}
              className={`angle-button ${selectedAngle === angle ? 'active' : ''}`}
              onClick={() => handleAngleSelect(angle)}
            >
              {angle}
              {getStatusIcon(angle) && (
                <span className="status">{getStatusIcon(angle)}</span>
              )}
            </button>
          ))}
        </div>

        {selectedAngle && (
          <div className="camera-section">
            <h3>📸 Capture {selectedAngle} Image</h3>
            
            {!isCameraActive && !capturedImage && (
              <div className="camera-controls">
                <button className="camera-button" onClick={startCamera}>
                  📷 Open Camera
                </button>
              </div>
            )}

            {isCameraActive && (
              <div className="camera-container">
                <video
                  ref={videoRef}
                  autoPlay
                  playsInline
                  muted
                  style={{ width: '100%', height: 'auto', display: 'block' }}
                />
                <canvas ref={canvasRef} style={{ display: 'none' }} />
                <div className="camera-controls">
                  <button className="camera-button" onClick={capturePhoto}>
                    📸 Capture
                  </button>
                  <button className="camera-button secondary" onClick={stopCamera}>
                    ❌ Cancel
                  </button>
                </div>
              </div>
            )}

            {capturedImage && (
              <div>
                <img
                  src={URL.createObjectURL(capturedImage)}
                  alt="Captured"
                  className="preview-image"
                />
                <div className="camera-controls">
                  <button 
                    className="camera-button" 
                    onClick={validateImage}
                    disabled={isLoading}
                  >
                    {isLoading ? '🔄 Validating...' : '✅ Validate Image'}
                  </button>
                  <button 
                    className="camera-button secondary" 
                    onClick={() => setCapturedImage(null)}
                  >
                    ❌ Cancel
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}
        {isLoading && <div className="loading">🔄 Processing image...</div>}
      </div>
    </div>
  );
}

export default App; 