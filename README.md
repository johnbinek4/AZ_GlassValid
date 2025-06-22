# Car Angle Validator

A mobile-first web application for validating car images from different angles using PyTorch models.

## 🚀 Features

- **6 Car Angles**: front, leftSide, leftSideMirror, back, rightSide, rightSideMirror
- **Mobile Camera**: Direct camera access with back camera preference
- **File Upload**: Fallback option for devices without camera access
- **Real-time Validation**: Instant feedback with ✅/❌ results
- **Responsive Design**: Optimized for mobile devices
- **Modern UI**: Beautiful gradient design with smooth animations

## 📁 Project Structure

```
AZ_GlassValidator/
├── frontend/                 # React frontend
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── vercel.json
├── backend/                  # FastAPI backend
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── models/                   # PyTorch models (existing)
│   ├── front_model.pt
│   ├── leftSide_model.pt
│   └── ...
└── modelHandlers/           # Existing model handlers
```

## 🛠️ Local Development

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Copy your models:**
   ```bash
   cp ../models/*.pt models/
   ```

5. **Start the server:**
   ```bash
   python start.py
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## 🚀 Deployment

### Backend Deployment (Render)

1. **Create a Render account** at [render.com](https://render.com)

2. **Create a new Web Service:**
   - Connect your GitHub repository
   - Select the `backend` directory
   - Choose "Docker" as the environment
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Add environment variables:**
   - `PORT`: 8000

4. **Upload your models:**
   - In the Render dashboard, go to your service
   - Use the shell to upload your `.pt` files to the `models/` directory

### Frontend Deployment (Vercel)

1. **Create a Vercel account** at [vercel.com](https://vercel.com)

2. **Deploy from GitHub:**
   - Connect your GitHub repository
   - Select the `frontend` directory
   - Vercel will automatically detect it's a React app

3. **Set environment variables:**
   - `REACT_APP_BACKEND_URL`: Your Render backend URL (e.g., `https://your-app.onrender.com`)

4. **Deploy:**
   - Click "Deploy" and wait for the build to complete

## 🔧 Configuration

### Environment Variables

**Frontend (.env):**
```
REACT_APP_BACKEND_URL=https://your-backend-app.onrender.com
```

**Backend:**
- No environment variables required for basic setup

### Model Files

Ensure your PyTorch models are named correctly:
- `front_model.pt`
- `leftSide_model.pt`
- `leftSideMirror_model.pt`
- `back_model.pt`
- `rightSide_model.pt`
- `rightSideMirror_model.pt`

## 📱 Mobile Usage

1. **Open the app** on your mobile device
2. **Select an angle** from the grid
3. **Choose camera or file upload:**
   - Camera: Opens back camera for direct capture
   - File: Select from gallery
4. **Capture/select image**
5. **Validate** and see results
6. **Status icons** show validation results for each angle

## 🔍 API Endpoints

### GET `/`
Health check endpoint

### GET `/health`
Returns API status and loaded models

### POST `/validate`
Validates an image for a specific angle

**Parameters:**
- `image`: Image file (multipart/form-data)
- `angle`: String (front, leftSide, leftSideMirror, back, rightSide, rightSideMirror)

**Response:**
```json
{
  "status": "accepted" | "rejected"
}
```

## 🐛 Troubleshooting

### Common Issues

1. **Camera not working:**
   - Ensure HTTPS is enabled (required for camera access)
   - Check browser permissions
   - Use file upload as fallback

2. **Models not loading:**
   - Verify model files are in the correct location
   - Check file permissions
   - Ensure model files are compatible with PyTorch version

3. **CORS errors:**
   - Backend CORS is configured to allow all origins
   - Check if backend URL is correct in frontend

4. **Deployment issues:**
   - Verify environment variables are set correctly
   - Check build logs for errors
   - Ensure all dependencies are in requirements.txt

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Open an issue on GitHub 