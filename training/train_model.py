import os
import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from pathlib import Path
from PIL import UnidentifiedImageError

# === Custom dataset to skip unreadable images ===
class SafeImageFolder(datasets.ImageFolder):
    def __getitem__(self, index):
        try:
            return super().__getitem__(index)
        except (UnidentifiedImageError, OSError):
            # Try the next image if current one fails
            new_index = (index + 1) % len(self)
            return self.__getitem__(new_index)

# === Model training function for one car angle ===
def train_model_for_angle(angle_name, data_dir, save_dir="models", epochs=10, batch_size=8, lr=1e-4):
    angle_path = Path(data_dir) / angle_name
    save_path = Path(save_dir) / f"{angle_name}_model.pt"
    os.makedirs(save_dir, exist_ok=True)

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
    ])

    dataset = SafeImageFolder(angle_path, transform=transform)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model = models.resnet18(weights="IMAGENET1K_V1")
    model.fc = nn.Sequential(
        nn.Linear(model.fc.in_features, 1),
        nn.Sigmoid()
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    model.train()
    for epoch in range(epochs):
        total_loss = 0
        for images, labels in dataloader:
            images, labels = images.to(device), labels.to(device).float().unsqueeze(1)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"[{angle_name}] Epoch {epoch+1}/{epochs}, Loss: {total_loss:.4f}")

    torch.save(model, save_path)
    print(f"[{angle_name}] Model saved to: {save_path}")

# === Train models for all angles ===
if __name__ == "__main__":
    angles = ["front", "leftSide", "leftSideMirror", "back", "rightSide", "rightSideMirror"]
    for angle in angles:
        train_model_for_angle(angle_name=angle, data_dir="training/data")
