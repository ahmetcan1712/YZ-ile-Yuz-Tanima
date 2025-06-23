from ultralytics import YOLO
import os
import sys

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

model_path = os.path.join(base_path, 'face-bigdata-n.pt')
yolo_model = YOLO(model_path)

def detect_faces(frame_rgb):
    results = yolo_model(frame_rgb)
    boxes = results[0].boxes.xyxy.cpu().numpy()
    return boxes