import os
from ultralytics import YOLO

def train_model():
    # Load a pretrained YOLOv5 model (medium version for balance)
    model = YOLO("yolov5m.pt")
    
    # Train the model on the VisDrone dataset
    results = model.train(
        data="data/VisDrone.yaml",
        epochs=1,
        imgsz=50,
        batch=16,
        name="visionary_tracker_train",
        freeze=14,  # Freeze first 14 layers for faster training
        project="runs/train",
        exist_ok=True
    )

if __name__ == "__main__":
    train_model()