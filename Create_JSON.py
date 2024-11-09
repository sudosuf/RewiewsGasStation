import json
from bs4 import BeautifulSoup

def create_JSON(address: str, medial_mark: str, reviews: []) -> str:
    """
    Данная функция нужна для перевода данных полученных при обращении к API в JSON формат, для последующего обращения к этим данным.

    :param address: Адресс заправочной станции.
    :param medial_mark: Средняя оценка заправочной станции
    :param reviews: 2-ерный массив с датой создания отзыва и  отзывом клиента по данной заправочной станции
    :return: str (JSON формат)
    
    Пример: 
    
    create_JSON("Улица свободы, 16", "4.3", ["Отличная заправка", "Супер заправка"])
    
    return:\n
    {
        "adress": "Улица свободы, 16",\n
        "medial-mark": "4.3",\n
        "reviews":[
             "data": 4 ода назад,\n
             "review":"Отличная заправка",\n
             "data": 2 ода назад,\n
             "review":""Супер заправка"",\n]
    }
    
    """
    data = []

    # Создаем цикл для прохода по всем отзывам
    station_data = {
        "content": str(address),
        "medial-mark": str(medial_mark),
        "reviews": [{"data": str(review[0]), "review": str(review[1])} for review in reviews] if reviews else "Нет отзывов"
    }
    data.append(station_data)
    print(data)
    # Преобразуем данные в JSON
    return json.dumps(data, ensure_ascii=False, indent=4)

