import cv2
from ultralytics import YOLO
import torch

class Inference:
    def __init__(self, model_path="runs/train/visionary_tracker_train/weights/best.pt"):
        self.model = YOLO(model_path)
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use index 0 with CAP_DSHOW
        if not self.cap.isOpened():
            raise Exception("Error: Could not open camera with index 0. Check connection or permissions.")

        print("Camera opened successfully with index 0")

    def generate_frames(self):
        while self.cap.isOpened():
            success, frame = self.cap.read()
            if not success:
                print("Failed to read frame from camera")
                break

            frame = cv2.resize(frame, (416, 416))
            results = self.model.track(frame, persist=True, conf=0.3, iou=0.5)
            annotated_frame = results[0].plot()

            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            if not ret:
                print("Failed to encode frame")
                continue
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def release(self):
        if self.cap:
            self.cap.release()