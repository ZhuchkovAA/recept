import json
import requests
from bs4 import BeautifulSoup
import time

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

def create_url():
    categories = ['zavtraki', 'bulony', 'zakuski', 'napitki', 'osnovnye-blyuda', 'pasta-picca', 'rizotto', 'salaty', 'sousy-marinady', 'supy', 'sendvichi', 'vypechka-deserty', 'zagotovki']
    main_dict = {}

    for categori in categories:
        href_list = []
        print('Prosessing...   ' + categori)

        for i in range(1, 18):
            url = f'https://eda.ru/recepty/{categori}?page={i}'
            print('Prosessing...   ' + url)
            req = requests.get(url=url, headers=headers)
            src = req.text

            soup = BeautifulSoup(src, 'html.parser')

            container = soup.find_all(class_ = 'emotion-m0u77r')

            for item in container:
                a_tag = item.find('a')
                if (a_tag.get('href') in href_list): 
                    break
                href_list.append(a_tag.get('href'))

            time.sleep(0.3)

        main_dict[categori] = href_list

    with open('data_url.json', 'w', encoding='utf8') as file:
        json.dump(main_dict, file, indent = 6)

def create_fulldata():
    urls = {}

    with open('data_url.json', 'r', encoding='utf8') as file:
        urls = json.load(file)

    dishes_main = {}

    for key in urls.keys():
        dish_sector = {}
        for url in urls[key]:
            try:
                print('Prosessing...   ' + url)
                req = requests.get(url='https://eda.ru' + url, headers=headers)
                src = req.text

                soup = BeautifulSoup(src, 'html.parser')

                ingredients_table = soup.find_all(class_='emotion-7yevpr')
                ingredients = {}
                
                stages = {}
                all_instructions = [item.text for item in soup.findAll(class_='emotion-1dvddtv')]

                dish_ingredients = {}

                for ingredients in ingredients_table:
                    try:
                        ingredient_name = ingredients.find(class_='emotion-mdupit').text
                        ingredient_count = ingredients.find(class_='emotion-bsdd3p').text
                        dish_ingredients[ingredient_name] = ingredient_count
                    except:
                        pass

                try:
                    img = soup.find(class_='emotion-1voj7e4').find('img').get('src')
                except:
                    img = ''

                dish = {
                    'name': soup.find(class_='emotion-gl52ge').text,
                    'yield': soup.find(itemprop='recipeYield').text,
                    'time': soup.find(class_='emotion-my9yfq').text,
                    'ingredients': dish_ingredients,
                    'instructions': all_instructions,
                    'img': img,
                    'url': url
                }

                dish_sector[url] = dish

                time.sleep(0.3)
            except:
                print('SOME ERORR!!!')
                time.sleep(5)
        
        dishes_main[key] = dish_sector

    with open('main_data.json', 'w', encoding='utf8') as file:
        json.dump(dishes_main, file, indent=6)

if __name__ == '__main__':
    # create_url()
    create_fulldata()