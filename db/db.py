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

    def add_subscription(self, user_telegram_id, is_fulltime = 0): 
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions` (`telegram_id`, `is_fulltime`) VALUES (?, ?)", (user_telegram_id, is_fulltime, ))
