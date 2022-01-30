import requests
from bs4 import BeautifulSoup
import re
import sqlite3
from tqdm import tqdm


class ParserInfo:
    def __init__(self, link_list: list, headers: dict):
        """
        :param link_list: List with all links to video cards
        :param headers: Headers
        """
        self.headers = headers
        self.link_list = link_list

    def get_html(self, link):
        return requests.get(link, headers=self.headers)

    @staticmethod
    def get_title(html):
        """
        Method parses the name of a video card
        :param html: HTML page
        :return: Name of a video card
        """
        soup = BeautifulSoup(html.text, features="html.parser")
        title = re.sub(r'\(.*\)', '', str(soup.find('h1', class_='product__title').text))
        return title

    @staticmethod
    def get_price(html):
        """
        Method parses price of a video card
        :param html: HTML page
        :return: Price of a video card
        """
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
        return price

    @staticmethod
    def get_characteristics_info(html):
        """
        Method collects all information from the video card specifications
        :param html: HTML page
        :return: Dictionary with (characteristic_name: characteristic_value)
        """
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
        """
        Method that inserts information of a video card into DataBase
        :param title: Video card name
        :param price: Video card price
        :param memory_frequency: Video card technical information
        :param graphics_chip: Video card technical information
        :param memory_capacity: Video card technical information
        :param max_resolution: Video card technical information
        :param min_power_capacity: Video card technical information
        """
        connection = sqlite3.connect('videocards_db.sqlite')
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO source (title, price, memory_frequency, graphics_chip, memory_capacity, 
            max_resolution, min_power_capacity)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, price, memory_frequency, graphics_chip, memory_capacity, max_resolution, min_power_capacity))
        connection.commit()

    def parse(self):
        """
        Method in which all information about video cards is parsed and the information is further added to the DataBase
        """
        for link in tqdm(self.link_list, desc="Parsing all info...", unit=" video cards", dynamic_ncols=True):
            html = self.get_html(link + "characteristics/")
            title = self.get_title(html)
            price = self.get_price(html)
            dict_with_all_characteristics_info = self.get_characteristics_info(html)
            memory_frequency = dict_with_all_characteristics_info.get("Частота памяти")
            graphics_chip = dict_with_all_characteristics_info.get("Графический чип")
            memory_capacity = dict_with_all_characteristics_info.get("Объем памяти")
            max_resolution = dict_with_all_characteristics_info.get("Максимально поддерживаемое разрешение")
            min_power_capacity = dict_with_all_characteristics_info.get("Минимально необходимая мощность БП")

            self.insert_db(title, price, memory_frequency, graphics_chip, memory_capacity,
                           max_resolution, min_power_capacity)
