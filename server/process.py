import os
import cv2
import numpy as np
from datetime import datetime
import json
from ultralytics import YOLO
from flask import Blueprint, request, jsonify


process_blueprint = Blueprint('process', __name__)

# Разрешённые расширения
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
MODEL_NAME = 'yolov8n.pt'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, '..', 'public', 'media', 'results')
MODEL_PATH = os.path.join(BASE_DIR, '..', 'model', MODEL_NAME)

os.makedirs(MEDIA_DIR, exist_ok=True)

model = YOLO(MODEL_PATH)

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@process_blueprint.route('/process', methods=['POST'])
def process_image_logic():
    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': 'Файл не найден'}), 400

    file = request.files['image']

    if not allowed_file(file.filename):
        return jsonify({'status': 'error', 'message': 'Недопустимый формат файла'}), 400

    ext = file.filename.rsplit('.', 1)[1].lower()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}.{ext}"
    jsonname = f"{timestamp}.json"
    save_path = os.path.join(MEDIA_DIR, filename)
    json_path = os.path.join(MEDIA_DIR, jsonname)

    img_array = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    results = model(img)
    result = results[0]

    output_img = result.plot()
    cv2.imwrite(save_path, output_img)

    sheep_data = []
    for box, cls, conf in zip(result.boxes.xyxy, result.boxes.cls, result.boxes.conf):
        if int(cls) == 18:  # Класс "овца"
            sheep_data.append({
                'bbox': box.tolist(),
                'class': 18,
                'confidence': float(conf)
            })
    result_json = {
        'status': 'success',
        'timestamp': timestamp,
        'image_filename': filename,
        'sheep_count': len(sheep_data),
        'detections': sheep_data
    }

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result_json, f, ensure_ascii=False, indent=2)
		

    return jsonify({
        'status': 'success',
        'message': 'Обработка завершена',
        'image_filename': filename,
        'result_filename': jsonname,
        'sheep_count': len(sheep_data)
    })
