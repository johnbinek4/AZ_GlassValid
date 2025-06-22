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

  // Backend URL - change this to your Render deployment URL
  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

  const startCamera = async () => {
    console.log('Starting camera...');
    try {
      console.log('Requesting camera permissions...');
      
      // Try back camera first
      let mediaStream;
      try {
        mediaStream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'environment' }
        });
        console.log('Back camera accessed successfully');
      } catch (backCameraError) {
        console.log('Back camera failed, trying any camera...');
        // Fallback to any available camera
        mediaStream = await navigator.mediaDevices.getUserMedia({
          video: true
        });
        console.log('Any camera accessed successfully');
      }
      
      console.log('Camera permission granted, setting up video...');
      setStream(mediaStream);
      
      // Set the stream on the video element immediately
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
        console.log('Video element updated with stream');
        
        // Force the video to play
        videoRef.current.play().then(() => {
          console.log('Video started playing successfully');
        }).catch(err => {
          console.error('Video play failed:', err);
        });
      }
      
      setIsCameraActive(true);
      setError(null);
      console.log('Camera started successfully');
    } catch (err) {
      console.error('Camera access denied:', err);
      console.error('Error details:', err.name, err.message);
      setError('Camera access denied. Please try again.');
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

      console.log('Video dimensions:', video.videoWidth, 'x', video.videoHeight);
      
      // Use video's actual dimensions
      canvas.width = video.videoWidth || 640;
      canvas.height = video.videoHeight || 480;
      
      console.log('Canvas dimensions set to:', canvas.width, 'x', canvas.height);
      
      try {
        context.drawImage(video, 0, 0);
        console.log('Image drawn to canvas successfully');
        
        canvas.toBlob((blob) => {
          console.log('Blob created, size:', blob.size);
          setCapturedImage(blob);
          stopCamera();
        }, 'image/jpeg', 0.8);
      } catch (err) {
        console.error('Error capturing photo:', err);
        setError('Failed to capture photo. Please try again.');
      }
    } else {
      console.error('Video or canvas ref not available');
      setError('Camera not ready. Please try again.');
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

  // Add new useEffect to handle video element
  useEffect(() => {
    if (videoRef.current && stream) {
      const video = videoRef.current;
      
      // Ensure video starts playing when stream is ready
      const handleLoadedMetadata = () => {
        console.log('Video metadata loaded, attempting to play...');
        video.play().catch(err => {
          console.error('Video play failed:', err);
        });
      };

      video.addEventListener('loadedmetadata', handleLoadedMetadata);
      
      // Try to play immediately as well
      video.play().catch(err => {
        console.log('Initial play failed, waiting for metadata...');
      });

      return () => {
        video.removeEventListener('loadedmetadata', handleLoadedMetadata);
      };
    }
  }, [stream, isCameraActive]);

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
                  style={{ width: '100%', height: 'auto', display: 'block' }}
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