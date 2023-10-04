# -*- coding: utf-8 -*-
import sqlite3
from unittest import result
from datetime import datetime

class SQLighter:
    def __init__(self , database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def is_user(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `telegram_id` = ?", (user_id, )).fetchall()
            return bool(len(result))

    def add_user(self, user_telegram_id, user_firstname, user_lastname):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`telegram_id`, `first_name`, `last_name`, `registration_date`) VALUES (?, ?, ?, ?)", (user_telegram_id, user_firstname, user_lastname, datetime.now(), ))

    def add_subscription(self, user_telegram_id, is_fulltime = 0, datetime_finaly = '2020-01-01 00:00:00.111111'): 
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions` (`telegram_id`, `is_fulltime`, `datetime_finaly`) VALUES (?, ?, ?)", (user_telegram_id, is_fulltime, datetime_finaly, ))

    def set_subscription_time(self, user_id, datetime):
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `datetime_finaly` = ? WHERE `telegram_id` = ?", (datetime, user_id))

    def get_subscription_time(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT `datetime_finaly` FROM `subscriptions` WHERE `telegram_id` = ?", (user_id, )).fetchone()[0]
    
    def is_subscription(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `is_fulltime` FROM `subscriptions` WHERE `telegram_id` = ?", (user_id, )).fetchone()[0]
            if (result == 1): return (result)
            result = self.cursor.execute("SELECT `datetime_finaly` FROM `subscriptions` WHERE `telegram_id` = ?", (user_id, )).fetchone()[0]
            if (datetime.now() < datetime.strptime(result, '%Y-%m-%d %H:%M:%S.%f' )): return(True) 
            return False

    def get_ingredients(self, url):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `ingredients` WHERE `url` = ?", (url, )).fetchall()

    def insert_dish(self, name_category, name, yield_, time, img, url):
         with self.connection:
            return self.cursor.execute(f"INSERT INTO `{name_category}` (`name`, `yield`, `time`, `img`, `url`) VALUES (?, ?, ?, ?, ?)", (name, yield_, time, img, url, ))

    def insert_ingredients(self, url, name, count):
         with self.connection:
            return self.cursor.execute("INSERT INTO `ingredients` (`url`, `name`, `count`) VALUES (?, ?, ?)", (url, name, count, ))

