# -*- coding: utf-8 -*-
import sqlite3
from unittest import result
from datetime import datetime

class MyCustomError(Exception):
    pass

class SQLighter:
    def __init__(self , database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_profile(self, telegram_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `users` WHERE `telegram_id` = ?", (telegram_id, )).fetchone()

    def is_user(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `telegram_id` = ?", (user_id, )).fetchall()
            return bool(len(result))

    def add_user(self, user_telegram_id, user_firstname, user_lastname):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`telegram_id`, `first_name`, `last_name`, `registration_date`) VALUES (?, ?, ?, ?)", (user_telegram_id, user_firstname, user_lastname, datetime.now(), ))

    def add_start_subscription(self, user_telegram_id, is_fulltime = 0, datetime_finaly = '2020-01-01 00:00:00.111111'): 
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions` (`telegram_id`, `is_fulltime`, `datetime_finaly`) VALUES (?, ?, ?)", (user_telegram_id, is_fulltime, datetime_finaly, ))

    def set_subscription_time(self, user_id, datetime):
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `datetime_finaly` = ? WHERE `telegram_id` = ?", (datetime, user_id, ))
    
    def get_subscription(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `is_fulltime`, `datetime_finaly`, `counter` FROM `subscriptions` WHERE `telegram_id` = ?", (user_id, )).fetchone()
            try:
                is_time_sub = datetime.now() < datetime.strptime(result[1], '%Y-%m-%d %H:%M:%S.%f')
                if (result[0] or is_time_sub or result[2]): 
                    return {'data': {
                        'status': True,
                        'description': {
                            'is_fulltime': result[0],
                            'datetime_finaly': {
                                'is_current': is_time_sub,
                                'datetime': result[1][:-7]
                            },
                            'counter': result[2],
                        }
                    }}
                raise MyCustomError('To except')
            except:
                return {'data': {
                        'status': False
                    }}

    def decrement_counter_subscription(self, user_id):
        with self.connection:
            counter = self.cursor.execute('SELECT `counter` FROM `subscriptions` WHERE `telegram_id` = ?', (user_id, )).fetchone()[0] - 1
            if counter < 0: counter = 0 
            return self.cursor.execute("UPDATE `subscriptions` SET `counter` = ? WHERE `telegram_id` = ?", (counter, user_id, ))
    
    def set_state_dish(self, user_id, type_dish):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `state_dish` = ? WHERE `telegram_id` = ?", (type_dish, user_id, ))
    
    def set_state_time(self, user_id, time):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `state_time` = ? WHERE `telegram_id` = ?", (time, user_id, ))
   
    def set_state_counter(self, user_id, count_page):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `state_counter` = ? WHERE `telegram_id` = ?", (count_page, user_id, ))

    def get_state_dish(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT `state_dish` FROM `users` WHERE `telegram_id` = ?", (user_id, )).fetchone()[0]
   
    def get_state_time(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT `state_time` FROM `users` WHERE `telegram_id` = ?", (user_id, )).fetchone()[0]
    
    def get_state_counter(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT `state_counter` FROM `users` WHERE `telegram_id` = ?", (user_id, )).fetchone()[0]

    def get_ingredients(self, url):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `ingredients` WHERE `url` = ?", (url, )).fetchall()

    def get_recepts_page(self, user_id):
        with self.connection:
            self.cursor.execute('SELECT `state_dish`, `state_time`, `state_counter` FROM `users` WHERE `telegram_id` = ?', (user_id, ))
            name_db, time, counter = self.cursor.fetchone()
            time = time.split('-')
            return self.cursor.execute(f"SELECT * FROM `{name_db}` WHERE `current_time` >= {time[0]} AND `current_time` <= {time[1]} LIMIT 10 OFFSET {counter * 10}").fetchall()

    def set_increment_page(self, user_id):
         with self.connection:
            counter = self.cursor.execute('SELECT `state_counter` FROM `users` WHERE `telegram_id` = ?', (user_id, )).fetchone()[0] + 1
            return self.cursor.execute("UPDATE `users` SET `state_counter` = ? WHERE `telegram_id` = ?", (counter, user_id, ))

    def set_decrement_page(self, user_id):
         with self.connection:
            counter = self.cursor.execute('SELECT `state_counter` FROM `users` WHERE `telegram_id` = ?', (user_id, )).fetchone()[0] - 1
            if counter < 0: counter = 0 
            return self.cursor.execute("UPDATE `users` SET `state_counter` = ? WHERE `telegram_id` = ?", (counter, user_id, ))

    def get_photo_dish(self, name_db, url):
        with self.connection:
            data = self.cursor.execute(f"SELECT `name`, `img` FROM `{name_db}` WHERE `url` = '{url}'").fetchone()
            return {
                'name': data[0],
                'img': data[1]
            }

    def konstructor(self, data):
        with self.connection:
            result = []

            for ref in data:
                urls = self.cursor.execute(f"SELECT `url` FROM `ingredients` WHERE `name` LIKE '%{ref.lower()}%' OR '%{ref.title()}%'").fetchall()
                urls = [item[0] for item in urls]
                for item in urls:
                    ingredients = self.cursor.execute(f"SELECT `name` FROM ingredients WHERE `url` = ?", (item, )).fetchall()
                    ingredients = [item[0] for item in ingredients]
                    current_dish = True
                    for ingredient in ingredients:
                        if len(ingredient.split(' ')) == 1:
                            if ingredient.title() not in data and ingredient.lower() not in data and ingredient not in ['Молоко', 'Петрушка', 'Морковь', 'Масло', 'Помидоры', 'Вода', 'Лук', 'Сахар', 'Чеснок', 'Перец', 'Соль']:
                                current_dish = False
                                break

                        else:
                            flag = False
                            for ingredient_val in ingredient.split(' '):
                                if ingredient_val.lower() in data or ingredient_val.title() in data or ingredient_val.title() in ['Молоко', 'Петрушка', 'Морковь', 'Масло', 'Помидоры', 'Вода', 'Лук', 'Сахар', 'Чеснок', 'Перец', 'Соль'] or ingredient_val.lower() in ['Молоко', 'Петрушка', 'Морковь', 'Масло', 'Помидоры', 'Вода', 'Лук', 'Сахар', 'Чеснок', 'Перец', 'Соль']:
                                    flag = True
                                    break
                            if not flag: current_dish = False
                    if current_dish: result.append(item)

            return list(set(result)) 

    def set_konstructor(self, user_id, ingredients):
        with self.connection:
            for ingredient in ingredients:
                self.cursor.execute("INSERT INTO `konstructor` (`telegram_id`, `ingredient`) VALUES (?, ?)", (user_id, ingredient, ))

    def get_konstructor(self, user_id):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM `konstructor` WHERE `telegram_id` = {user_id}").fetchall()

    def delete_ingredient(self, user_id, ingredient):
        with self.connection:
            self.cursor.execute(f"DELETE FROM 'konstructor' WHERE `telegram_id` = ? AND `ingredient` = ?", (user_id, ingredient, )) 
    
    def create_page_konstructor(self, urls):
        with self.connection:
            result = []
            for url in urls:
                result.append(self.cursor.execute(f"SELECT * FROM `{url.split('/')[2]}` WHERE `url` = '{url}'").fetchone())

            return result

    # def insert_dish(self, name_category, name, yield_, time, img, url):
    #      with self.connection:
    #         return self.cursor.execute(f"INSERT INTO `{name_category}` (`name`, `yield`, `time`, `img`, `url`) VALUES (?, ?, ?, ?, ?)", (name, yield_, time, img, url, ))

    # def insert_ingredients(self, url, name, count):
    #      with self.connection:
    #         return self.cursor.execute("INSERT INTO `ingredients` (`url`, `name`, `count`) VALUES (?, ?, ?)", (url, name, count, ))

    # def  create_current_time(self, name_db):
    #     with self.connection:
    #         self.cursor.execute(f"SELECT id, time FROM '{name_db}'")
    #         for row in self.cursor.fetchall():
    #             try:
    #                 pre_time = row[1].split(' ')
    #                 time = 0
    #                 for i in range(len(pre_time)):
    #                     if pre_time[i] in ['час', 'часа']:
    #                         time += int(pre_time[i - 1]) * 60
    #                     if pre_time[i] == 'минут':
    #                         time += int(pre_time[i - 1])
    #                 self.cursor.execute(f"UPDATE `{name_db}` SET `current_time` = ? WHERE `id` = ?", (time, row[0]))
    #             except:
    #                 print(f'Error. name_db: {name_db}, id: {row[0]}')

    # def delete_over_url(self, name_db):
    #     with self.connection:
    #         self.cursor.execute(f"SELECT * FROM '{name_db}'")
    #         for row in self.cursor.fetchall():
    #             print(len(row[-2]))
    #             if len(row[-2]) > 63:
    #                 self.cursor.execute(f"DELETE FROM '{name_db}' WHERE `url` = ?", (row[-2],)) 

    # def refresh_url(self, name_db):
    #     with self.connection:
    #         self.cursor.execute(f"SELECT * FROM '{name_db}'")
    #         for row in self.cursor.fetchall():
    #             new_url = row[-3].replace('c88x88', '-x900')
    #             self.cursor.execute(f"UPDATE `{name_db}` SET `img` = ? WHERE `id` = ?", (new_url, row[0]))
    #             print(new_url)

    def most_popular_ingredients(self):
        with self.connection:
            main_list = {}
            result = self.cursor.execute(f"SELECT `name` from `ingredients`").fetchall()

            for ingredient in result:
                main_list[ingredient[0]] = 0

            for ingredient in result:
                main_list[ingredient[0]] += 1

            most_popular = sorted(main_list.items(), key=lambda item: item[1])[-15:]

            for i in range(len(most_popular)):
                most_popular[i] = most_popular[i][0]

            print(most_popular)