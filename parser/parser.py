import json
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozila/1.0',  # Указание имени и версии парсера
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',  # Желаемые языковые предпочтения
    'Accept-Encoding': 'gzip, deflate, br',  # Поддерживаемые методы сжатия данных
    'Connection': 'keep-alive',  # Поддержка постоянного соединения
    'Referer': 'https://www.example.com',  # Ссылка на источник данных или предыдущую страницу
    'Cache-Control': 'max-age=0',  # Управление кешированием
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN',  # Авторизационный токен, если требуется
    # Другие пользовательские заголовки, если необходимо
}

def parser():
    url = 'https://eda.ru/recepty/bulony?page=2'
    req = requests.get(url=url, headers=headers)
    src = req.text

    soup = BeautifulSoup(src, 'html.parser')

    container = soup.find_all(class_ = 'emotion-m0u77r')

    for item in container:
        a_tag = item.find('a')
        print(a_tag.get('href'))

if __name__ == '__main__':
    parser()
