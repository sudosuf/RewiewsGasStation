# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from flask import Flask, jsonify, request, render_template, send_file
from fastapi.staticfiles import StaticFiles
from flask_cors import CORS
import os
import json
from config import FOLDER_PATH_JSON

app = Flask(__name__)
CORS(app)  # Настройка CORS для всех маршрутов и источников

# Пример маршрута для отправки JSON данных
@app.route("/api/tiles", methods=["GET"])
def send_json():
    result = []
    # Чтение JSON данных из файла
    for file_name in os.listdir(FOLDER_PATH_JSON):
        file_path = os.path.join(FOLDER_PATH_JSON, file_name)

        # Проверяем, что это файл (игнорируем подпапки)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                print(f"Чтение файла: {file_path}")
                data = json.load(file)
                result.append(data)
    return jsonify(result), 200


@app.route('/send-summury-review', methods=['POST'])
def receive_summary_review():
    # Извлекаем геоадрес из тела запроса
    incoming_data = request.get_json()  # Предполагается, что данные приходят в формате JSON
    if not incoming_data:
        return jsonify({"error": "No data provided"}), 400

    geo_address = incoming_data.get("geolocation")
    summary_text = ""

    # Ищем соответствие геолокации в JSON файлах
    for file_name in os.listdir(FOLDER_PATH_JSON):
        file_path = os.path.join(FOLDER_PATH_JSON, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # Сравниваем геолокацию в данных
                if data[0].get('geolocation') == geo_address:
                    summary_text = data[0].get('sammary-review', "")
                    break

    return jsonify({"sammary-review": summary_text}), 200


@app.route('/write-to-llm', methods=['POST'])
def receive_strings():
    # Извлекаем сообщение и геолокацию из тела запроса
    incoming_data = request.get_json()
    if not incoming_data:
        return jsonify({"error": "No data provided"}), 400

    geo_address = incoming_data.get("geolocation")
    message = incoming_data.get("message")

    # Ищем отзывы по геолокации
    reviews = []
    for file_name in os.listdir(FOLDER_PATH_JSON):
        file_path = os.path.join(FOLDER_PATH_JSON, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if data[0].get('geolocation') == geo_address:
                    reviews = data[0].get('reviews', [])
                    break

    # Здесь добавьте логику для отправки данных в LLM и получения ответа.
    # Пока что возвращаем просто данные, чтобы показать пример.
    response_from_llm = "Ответ от LLM на сообщение: " + message

    return jsonify({"received_data": response_from_llm, "reviews": reviews}), 200

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/templates/detail.html")
def details():
    return render_template("details.html")

@app.route('/templates/chat.html')
def chat():
    return render_template('chat.html')

@app.route("/api/news", methods=["GET"])
def send_news():
    results = []
    # Чтение JSON данных из файла
    file_path = "./JSON/news/news.json"

        # Проверяем, что это файл (игнорируем подпапки)

    with open(file_path, 'r', encoding='utf-8') as file:
        print(f"Чтение файла: {file_path}")
        data = json.load(file)
    return jsonify(data), 200

@app.route('/api/get_photo', methods=['GET'])
def get_photo():
    # Путь к изображению на сервере
    photo_path = './img/map.jpeg'  # Замените на реальный путь к файлу

    # Отправляем файл клиенту
    return send_file(photo_path, mimetype='image/jpeg')
# Запуск сервера
if __name__ == "__main__":
    app.run(host="192.168.1.9", port=5000)


