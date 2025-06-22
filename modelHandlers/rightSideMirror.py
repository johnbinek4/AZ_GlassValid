# model_handlers/front.py

def validate(image_bytes):
    # TODO: Replace with actual model logic
    return "✅ Front angle image is valid (placeholder)"
import torch
from torchvision import transforms
from PIL import Image
from io import BytesIO
import streamlit as st

@st.cache_resource
def load_model():
    model = torch.load("models/rightSideMirror_model.pt", map_location="cpu")
    model.eval()
    return model

model = load_model()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def validate(image_bytes):
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = model(tensor)
        pred = torch.sigmoid(output).item()
    return "✅ Accepted" if pred > 0.5 else "❌ Rejected"
