from fastapi import FastAPI, File, UploadFile
from ultralytics import YOLO
import cv2
import numpy as np
from io import BytesIO

app = FastAPI()

# Load your custom-trained model
model = YOLO("yolov8n.pt")

@app.post("/detect")
async def detect_image(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    results = model(image)
    boxes = results[0].boxes.xyxy.cpu().numpy()
    confidences = results[0].boxes.conf.cpu().numpy()
    classes = results[0].boxes.cls.cpu().numpy()

    return {
        "boxes": boxes.tolist(),
        "confidences": confidences.tolist(),
        "classes": classes.tolist()
    }
