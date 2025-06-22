# Deployment Guide

This guide will walk you through deploying both the frontend and backend of the Car Angle Validator application.

## Prerequisites

- GitHub account
- Vercel account (free)
- Render account (free)
- Your PyTorch model files (`.pt` files)

## Step 1: Prepare Your Repository

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit with React frontend and FastAPI backend"
   git push origin main
   ```

2. **Ensure your models are in the correct location:**
   ```
   models/
   ├── front_model.pt
   ├── leftSide_model.pt
   ├── leftSideMirror_model.pt
   ├── back_model.pt
   ├── rightSide_model.pt
   └── rightSideMirror_model.pt
   ```

## Step 2: Deploy Backend to Render

### 2.1 Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Verify your email

### 2.2 Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure the service:
   - **Name**: `car-angle-validator-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Docker`
   - **Branch**: `main`
   - **Build Command**: Leave empty (Docker will handle this)
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 2.3 Configure Environment Variables
1. Go to "Environment" tab
2. Add variable:
   - **Key**: `PORT`
   - **Value**: `8000`

### 2.4 Upload Model Files
1. Wait for the first deployment to complete
2. Go to your service dashboard
3. Click "Shell" tab
4. Run these commands:
   ```bash
   mkdir -p models
   cd models
   ```
5. Upload your `.pt` files using the file upload feature or drag-and-drop
6. Verify files are uploaded:
   ```bash
   ls -la
   ```

### 2.5 Test Backend
1. Go to your service URL (e.g., `https://your-app.onrender.com`)
2. You should see: `{"message": "Car Angle Validator API is running", "status": "healthy"}`
3. Test health endpoint: `https://your-app.onrender.com/health`

## Step 3: Deploy Frontend to Vercel

### 3.1 Create Vercel Account
1. Go to [vercel.com](https://vercel.com)
2. Sign up with your GitHub account

### 3.2 Import Project
1. Click "New Project"
2. Import your GitHub repository
3. Configure the project:
   - **Framework Preset**: `Create React App`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

### 3.3 Set Environment Variables
1. Go to "Settings" → "Environment Variables"
2. Add variable:
   - **Name**: `REACT_APP_BACKEND_URL`
   - **Value**: Your Render backend URL (e.g., `https://your-app.onrender.com`)
   - **Environment**: Production, Preview, Development

### 3.4 Deploy
1. Click "Deploy"
2. Wait for build to complete
3. Your app will be available at the provided URL

## Step 4: Test the Complete Application

### 4.1 Test on Desktop
1. Open your Vercel frontend URL
2. Test file upload functionality
3. Verify API communication

### 4.2 Test on Mobile
1. Open the app on your phone
2. Test camera functionality
3. Test file upload from gallery
4. Verify all angles work correctly

## Step 5: Troubleshooting

### Backend Issues

**Models not loading:**
```bash
# Check if models are in the correct location
ls -la models/

# Check file permissions
chmod 644 models/*.pt
```

**Build failures:**
- Check Render logs for specific errors
- Ensure all dependencies are in `requirements.txt`
- Verify Dockerfile is correct

**CORS errors:**
- Backend CORS is configured to allow all origins
- Check if frontend URL is correct

### Frontend Issues

**API connection errors:**
- Verify `REACT_APP_BACKEND_URL` is set correctly
- Check if backend is running
- Test API endpoints directly

**Camera not working:**
- Ensure you're using HTTPS
- Check browser permissions
- Use file upload as fallback

**Build failures:**
- Check Vercel build logs
- Ensure all dependencies are in `package.json`
- Verify React scripts are correct

## Step 6: Monitoring and Maintenance

### Backend Monitoring
1. **Render Dashboard:**
   - Monitor service health
   - Check logs for errors
   - Monitor resource usage

2. **API Health Checks:**
   - `/health` endpoint shows loaded models
   - Monitor response times
   - Check for model loading issues

### Frontend Monitoring
1. **Vercel Analytics:**
   - Monitor page views
   - Check performance metrics
   - Monitor error rates

2. **User Experience:**
   - Test on different devices
   - Monitor camera functionality
   - Check validation accuracy

## Step 7: Updates and Maintenance

### Updating Models
1. Upload new `.pt` files to Render
2. Restart the service to reload models
3. Test validation accuracy

### Code Updates
1. Push changes to GitHub
2. Render and Vercel will auto-deploy
3. Test functionality after deployment

### Environment Variables
1. Update in respective dashboards
2. Redeploy if necessary
3. Test configuration changes

## Security Considerations

1. **HTTPS Only:**
   - Both Vercel and Render provide HTTPS
   - Camera access requires HTTPS

2. **CORS Configuration:**
   - Backend allows all origins for development
   - Consider restricting to specific domains in production

3. **File Upload:**
   - Validate file types on frontend and backend
   - Consider file size limits
   - Sanitize uploaded files

4. **API Security:**
   - Consider adding authentication if needed
   - Rate limiting for API endpoints
   - Input validation and sanitization

## Cost Optimization

### Render (Backend)
- Free tier: 750 hours/month
- Auto-sleep after 15 minutes of inactivity
- Consider paid plan for always-on service

### Vercel (Frontend)
- Free tier: Unlimited deployments
- 100GB bandwidth/month
- Sufficient for most use cases

## Support Resources

- **Render Documentation**: [docs.render.com](https://docs.render.com)
- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **FastAPI Documentation**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **React Documentation**: [reactjs.org/docs](https://reactjs.org/docs) 