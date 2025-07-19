import os
import json
from datetime import datetime
from flask import Blueprint, request, jsonify
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

report_blueprint = Blueprint('report', __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, '..', 'public', 'media', 'results')

# Путь к ttf-шрифту
FONT_PATH = os.path.join(BASE_DIR, '..', 'public', 'media', 'fonts', 'DejaVuLGCSans.ttf')
pdfmetrics.registerFont(TTFont('DejaVuLGCSans', FONT_PATH))

# Создаем стиль с нужным шрифтом
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleRus', parent=styles['Title'], fontName='DejaVuLGCSans', fontSize=18, spaceAfter=12))
styles.add(ParagraphStyle(name='NormalRus', parent=styles['Normal'], fontName='DejaVuLGCSans', fontSize=12))
styles.add(ParagraphStyle(name='Heading2Rus', parent=styles['Heading2'], fontName='DejaVuLGCSans', fontSize=14, spaceAfter=6))


@report_blueprint.route('/report', methods=['POST'])
def generate_pdf_report() -> str:
    # Получаем имя JSON-файла из запроса
    json_filename = request.json.get('filename')
    if not json_filename:
        raise ValueError("В запросе отсутствует 'json_filename'.")

    json_path = os.path.join(RESULTS_DIR, json_filename)
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Файл {json_filename} не найден!")

    # Загружаем данные из JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    image_filename = data.get('image_filename')
    detections = data.get('detections', [])
    sheep_count = data.get('sheep_count', len(detections))

    if not image_filename:
        raise ValueError("В JSON отсутствует поле 'image_filename'.")

    image_path = os.path.join(RESULTS_DIR, image_filename)
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Изображение {image_filename} не найдено!")

    # Формируем имя для PDF
    report_filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    report_path = os.path.join(RESULTS_DIR, report_filename)

    # Создание PDF-отчета
    doc = SimpleDocTemplate(report_path, pagesize=A4)
#    styles = getSampleStyleSheet()
    elements = []

    # Заголовок
    elements.append(Paragraph(f"Отчет по изображению: {image_filename}", styles['TitleRus']))
    elements.append(Spacer(1, 12))

    # Добавление изображения
    try:
        img = Image(image_path)
        img.drawHeight = 200
        img.drawWidth = 200 * img.imageWidth / img.imageHeight
        elements.append(img)
        elements.append(Spacer(1, 12))
    except Exception:
        elements.append(Paragraph("Не удалось отобразить изображение.", styles['NormalRus']))

    # Кол-во овец
    elements.append(Paragraph(f"Обнаружено овец: {sheep_count}", styles['Heading2Rus']))
    elements.append(Spacer(1, 12))

    # Таблица по детекциям
    table_data = [['№', 'Координаты (bbox)', 'Точность']]
    for i, obj in enumerate(detections, 1):
        bbox = ', '.join(f"{x:.1f}" for x in obj.get('bbox', []))
        confidence = f"{obj.get('confidence', 0):.2f}"
        table_data.append([str(i), bbox, confidence])

    table = Table(table_data, colWidths=[30, 300, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
		('FONTNAME', (0, 0), (-1, -1), 'DejaVuLGCSans'),
    ]))

    elements.append(table)
    doc.build(elements)
	
	
    result_report_json = {
        'status': 'success',
        'report_filename': report_filename
    }

    return result_report_json