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
  const fileInputRef = useRef(null);

  // Backend URL - change this to your Render deployment URL
  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment' } // Use back camera
      });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
      setIsCameraActive(true);
      setError(null);
    } catch (err) {
      console.error('Camera access denied:', err);
      setError('Camera access denied. Please use file upload instead.');
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
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      const context = canvas.getContext('2d');

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      context.drawImage(video, 0, 0);

      canvas.toBlob((blob) => {
        setCapturedImage(blob);
        stopCamera();
      }, 'image/jpeg', 0.8);
    }
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setCapturedImage(file);
      setError(null);
    } else {
      setError('Please select a valid image file.');
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
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 30000, // 30 second timeout
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
      setError('Failed to validate image. Please check your connection and try again.');
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
    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, [stream]);

  return (
    <div className="container">
      <div className="header">
        <h1>📷 Car Angle Validator</h1>
        <p>Select an angle and capture a photo to validate</p>
      </div>

      <div className="content">
        {/* Angle Selection Grid */}
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

        {/* Camera/Upload Section */}
        {selectedAngle && (
          <div className="camera-section">
            <h3>📸 Capture {selectedAngle} Image</h3>
            
            {!isCameraActive && !capturedImage && (
              <div className="camera-controls">
                <button className="camera-button" onClick={startCamera}>
                  📷 Open Camera
                </button>
                <label className="file-label">
                  📁 Upload File
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    onChange={handleFileUpload}
                    className="file-input"
                  />
                </label>
              </div>
            )}

            {/* Camera View */}
            {isCameraActive && (
              <div className="camera-container">
                <video
                  ref={videoRef}
                  autoPlay
                  playsInline
                  muted
                />
                <canvas ref={canvasRef} />
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

            {/* Preview Image */}
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

        {/* Messages */}
        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}
        {isLoading && <div className="loading">🔄 Processing image...</div>}
      </div>
    </div>
  );
}

export default App; 