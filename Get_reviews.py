import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from Create_JSON import create_JSON
from config import FOLDER_PATH
# Укажите путь к вашему локальному HTML-файлу


def Find_rewiews_in_HTML_page(file_path: str, file_name: str)->None:
    """
    Данная функция принимает имя файла в котором необходиммо найти данные о заправке, преобразует эти данные в JSON формат и сохраняет в исходном каталоге в папке "JSON_file".
    :param file_path: Путь до файла в котором необходиммо найти данные о заправке. Должен быть в формате HTML.
    :param file_name: Имя файла которое передаться в функцию сохранение, что бы html файл и JSON файл имели одинаковое название.
    :return: None
    """
    # Шаг 1: Открываем файл и читаем его содержимое
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Шаг 2: Создаем объект BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Шаг 3: Извлекаем объект в теге meta
    address = soup.find("meta", {"itemprop": "name"})
    # Извлекаем значение атрибута content, если тег найден
    if address:
        address = address.get("content")
        print("Значение content:", address)
    else:
        address="Нет адреса"
        print("Тег <meta> с itemprop='name' не найден")
    # Шаг 4: Извлекаем среднюю оценку
    medial_mark = soup.find("div", class_="fontDisplayLarge")
    # Извлекаем значение атрибута content, если тег найден
    if medial_mark:
        medial_mark = medial_mark.get_text(strip=True)
        print("Значение medial-mark:", address)
    else:
        medial_mark = "Нет средней оценки"
        print("Тег medial-mark не найден")

    # Шаг 5: Ищем блоки отзывов с классом 'jJc9Ad'
    data_rewiews=[]
    review_blocks = soup.find_all("div", class_="jJc9Ad")
    if review_blocks:
        for i, review_block in enumerate(review_blocks, 1):
            # Внутри каждого блока ищем <span> с классом 'wiI7pd'
            review_text = review_block.find("span", class_="wiI7pd")
            review_date = review_block.find("span", class_="rsqaWe")
            if review_text:
                print(f"Отзыв {i}: {review_date.get_text(strip=True)}", review_text.get_text(strip=True))
                rew = [review_date.get_text(strip=True), review_text.get_text(strip=True)]
                data_rewiews.append(rew)
    else:
        print("Отзывы не найдены")
    #print("data:", data_rewiews[0][1])
    json_data = create_JSON(address, medial_mark, data_rewiews)
    Save_JSON_to_file(json_data, FOLDER_PATH, file_name)


def Save_JSON_to_file(JSON_data: str, folder_path: str, folder_name: str) -> None:
    # Сохранение JSON-данных в файл
    filename = f"{folder_path}\\JSON\\{folder_name}.json"  # имя файла
    with open(filename, "w", encoding="utf-8") as file:
        file.write(JSON_data)

import os

# Путь к папке, содержащей файлы для обработки


# Обход всех файлов в папке
for file_name in os.listdir(FOLDER_PATH):
    file_path = os.path.join(FOLDER_PATH, file_name)

    # Проверяем, что это файл (можно пропустить подпапки)
    if os.path.isfile(file_path):
        # Теперь `file_name` содержит имя текущего файла
        print(f"Обработка файла: {file_name[:-5]}")
        Find_rewiews_in_HTML_page(file_path, file_name[:-5])
        # Здесь выполняются действия с файлом
        # Например, можно его открыть, прочитать данные и т.д.
