from flask import Flask, request, jsonify
from PIL import Image
import numpy as np

import numpy as np
import onnxruntime as ort

app = Flask(__name__)

# Load model
session = ort.InferenceSession("yolov8_waste_final.onnx", providers=['CPUExecutionProvider'])

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']
    img_bytes = file.read()
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Preprocess
    input_img = cv2.resize(img, (640, 640))
    input_img = input_img.transpose(2, 0, 1)[np.newaxis, :, :, :] / 255.0
    input_img = input_img.astype(np.float32)

    # Inference
    outputs = session.run(None, {session.get_inputs()[0].name: input_img})[0]

    # Post-process (dummy for now)
    return jsonify({"message": "Prediction made", "shape": outputs.shape})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
