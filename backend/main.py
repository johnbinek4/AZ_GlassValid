from fastapi import FastAPI, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import torch
from torchvision import models, transforms
from PIL import Image
from io import BytesIO
import os
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Car Angle Validator API",
    description="API for validating car images from different angles using PyTorch models",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model cache
model_cache: Dict[str, Any] = {}

# Image transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def load_model(angle: str) -> torch.nn.Module:
    """Load and cache PyTorch model for the specified angle."""
    if angle in model_cache:
        return model_cache[angle]
    
    try:
        # Model path - adjust based on your deployment structure
        model_path = f"models/{angle}_model.pt"
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        # Load ResNet18 model
        model = models.resnet18(weights="IMAGENET1K_V1")
        model.fc = torch.nn.Sequential(
            torch.nn.Linear(model.fc.in_features, 1),
            torch.nn.Sigmoid()
        )
        
        # Load trained weights
        model.load_state_dict(torch.load(model_path, map_location="cpu"))
        model.eval()
        
        # Cache the model
        model_cache[angle] = model
        logger.info(f"Model loaded successfully for angle: {angle}")
        
        return model
    except Exception as e:
        logger.error(f"Error loading model for angle {angle}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to load model for angle: {angle}")

def validate_image(image_bytes: bytes, angle: str) -> str:
    """Validate image using the appropriate model."""
    try:
        # Load image
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        
        # Transform image
        tensor = transform(image).unsqueeze(0)
        
        # Load model
        model = load_model(angle)
        
        # Make prediction
        with torch.no_grad():
            output = model(tensor)
            prediction = torch.sigmoid(output).item()
        
        # Return result
        return "accepted" if prediction > 0.5 else "rejected"
        
    except Exception as e:
        logger.error(f"Error during validation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Car Angle Validator API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "models_loaded": list(model_cache.keys())}

@app.post("/validate")
async def validate(
    image: bytes = File(...),
    angle: str = Form(...)
):
    """
    Validate a car image for a specific angle.
    
    Args:
        image: The image file bytes
        angle: The car angle (front, leftSide, leftSideMirror, back, rightSide, rightSideMirror)
    
    Returns:
        JSON response with validation status
    """
    # Validate angle parameter
    valid_angles = ["front", "leftSide", "leftSideMirror", "back", "rightSide", "rightSideMirror"]
    if angle not in valid_angles:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid angle. Must be one of: {valid_angles}"
        )
    
    # Validate image
    if not image:
        raise HTTPException(status_code=400, detail="No image provided")
    
    try:
        # Validate the image
        result = validate_image(image, angle)
        
        logger.info(f"Validation completed for angle {angle}: {result}")
        
        return JSONResponse(content={"status": result})
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during validation: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 