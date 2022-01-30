import requests
from bs4 import BeautifulSoup
import re
import sqlite3


class ParserInfo:
    def __init__(self, link_list: list, headers: dict):
        self.headers = headers
        self.link_list = link_list

    def get_html(self, link):
        return requests.get(link, headers=self.headers)

    @staticmethod
    def get_title(html):
        soup = BeautifulSoup(html.text, features="html.parser")
        title = re.sub(r'\(.*\)', '', str(soup.find('h1', class_='product__title').text))
        return title

    @staticmethod
    def get_price(html):
        replace_list = ["\u00a0", "₴", " "]
        soup = BeautifulSoup(html.text, features="html.parser")
        if soup.find('div', class_='product-carriage__price ng-star-inserted'):
            price = str(soup.find('div', class_='product-carriage__price ng-star-inserted').text)
            for item in replace_list:
                if item in price:
                    price = price.replace(item, "")
        else:
            price = str(soup.find('p', class_='product-carriage__price_type_old ng-star-inserted').text)
            for item in replace_list:
                if item in price:
                    price = price.replace(item, "")
        return int(price)

    @staticmethod
    def get_characteristics_info(html):
        keys_list = []
        values_list = []
        soup = BeautifulSoup(html.text, features="html.parser")
        for i in soup.findChildren('dt', class_='characteristics-full__label'):
            keys_list.append(i.text)

        for i in soup.findChildren('dd', class_='characteristics-full__value'):
            values_list.append(i.text)

        characteristics_dict = dict(zip(keys_list, values_list))
        return characteristics_dict

    @staticmethod
    def insert_db(title, price, memory_frequency, graphics_chip, memory_capacity, max_resolution, min_power_capacity):
        connection = sqlite3.connect('videocards_db.sqlite')
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO source (title, price, memory_frequency, graphics_chip, memory_capacity, 
            max_resolution, min_power_capacity)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, price, memory_frequency, graphics_chip, memory_capacity, max_resolution, min_power_capacity))
        connection.commit()

    def parse(self):
        for link in self.link_list:
            html = self.get_html(link + "characteristics/")
            title = self.get_title(html)
            price = self.get_price(html)
            memory_frequency = self.get_characteristics_info(html).get("Частота памяти")
            graphics_chip = self.get_characteristics_info(html).get("Графический чип")
            memory_capacity = self.get_characteristics_info(html).get("Объем памяти")
            max_resolution = self.get_characteristics_info(html).get("Максимально поддерживаемое разрешение")
            min_power_capacity = self.get_characteristics_info(html).get("Минимально необходимая мощность БП")

            self.insert_db(title, price, memory_frequency, graphics_chip, memory_capacity,
                           max_resolution, min_power_capacity)


