import torch
from torchvision import models, transforms
from PIL import Image
from io import BytesIO
import streamlit as st

@st.cache_resource
def load_model():
    model = models.resnet18(weights="IMAGENET1K_V1")
    model.fc = torch.nn.Sequential(
        torch.nn.Linear(model.fc.in_features, 1),
        torch.nn.Sigmoid()
    )
    model.load_state_dict(torch.load("models/leftSideMirror_model.pt", map_location="cpu"))
    model.eval()
    return model

model = load_model()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def validate(image_bytes):
    try:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        tensor = transform(image).unsqueeze(0)
        with torch.no_grad():
            output = model(tensor)
            pred = torch.sigmoid(output).item()
        return "✅ Accepted" if pred > 0.5 else "❌ Rejected"
    except Exception as e:
        return f"❌ Error during validation: {str(e)}"
