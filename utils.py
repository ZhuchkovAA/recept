from db.db import SQLighter;
db = SQLighter("db/recept.db")

def insert_dish_database():
    data = {}
    with open('main_data.json', 'r', encoding='utf8') as file:
        data = json.load(file)

    for category in data.keys():
        for item in data[category]:
            print(category + ': ' + item)
            db.insert_dish(category, data[category][item]['name'], data[category][item]['yield_'], data[category][item]['time'], data[category][item]['img'], data[category][item]['url'])

def insert_ingredients_database():
    data = {}
    with open('main_data.json', 'r', encoding='utf8') as file:
        data = json.load(file)

    for category in data.keys():
        for item in data[category]:
            for name in data[category][item]['ingredients'].keys(): 
                print(name, data[category][item]['ingredients'][name])
                db.insert_ingredients(data[category][item]['url'], name, data[category][item]['ingredients'][name])
