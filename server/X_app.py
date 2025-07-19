from flask import Flask, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np
import os
from datetime import datetime
import json

# Разрешённые расширения
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
MODEL_NAME = 'yolov8n.pt'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, '..', 'public', 'media', 'results')
MODEL_PATH = os.path.join(BASE_DIR, '..', 'model', MODEL_NAME)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = MEDIA_DIR

os.makedirs(MEDIA_DIR, exist_ok=True)
model = YOLO(MODEL_PATH)

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/process', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': 'Файл не найден'}), 400

    file = request.files['image']

    if not allowed_file(file.filename):
        return jsonify({'status': 'error', 'message': 'Недопустимый формат файла'}), 400

    # Определяем расширение
    ext = file.filename.rsplit('.', 1)[1].lower()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}.{ext}"
    jsonname = f"{timestamp}.json"
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    json_path = os.path.join(app.config['UPLOAD_FOLDER'], jsonname)

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

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(sheep_data, f, ensure_ascii=False, indent=2)

    return jsonify({
        'status': 'success',
        'message': 'Обработка завершена',
        'image_filename': filename,
        'result_filename': jsonname,
        'sheep_count': len(sheep_data)
    })

if __name__ == '__main__':
    app.run(debug=True)
