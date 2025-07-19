from flask import Flask
from process import process_blueprint
from report import report_blueprint
import os

app = Flask(__name__)

# Настройка папки с результатами
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, '..', 'public', 'media', 'results')
app.config['UPLOAD_FOLDER'] = MEDIA_DIR

# Регистрируем модули (blueprints)
app.register_blueprint(process_blueprint)
app.register_blueprint(report_blueprint)

# Главная страница API
@app.route('/flask', methods=['GET'])
@app.route('/')
def index():
    return {'status': 'ok', 'message': 'SheepCounter Flask API работает'}

if __name__ == '__main__':
    app.run(debug=True)
