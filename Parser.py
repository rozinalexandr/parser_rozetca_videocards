import requests
from bs4 import BeautifulSoup
from ParserInfo import ParserInfo
from tqdm import tqdm


class Parser:
    def __init__(self, url: str, headers: dict):
        """
        :param url: Base URL with all video cards
        :param headers: Headers
        """
        self.url = url
        self.headers = headers

    def get_html(self, page: int):
        return requests.get(self.url + f'/page={page}/', headers=self.headers)

    def get_pages_amount(self):
        """
        Method collects a number of all pages, which are needed to be parsed. Method is used to substitute a specific
        page number in the URL address
        :return: Amount of pages
        """
        soup = BeautifulSoup(self.get_html(1).text, features="html.parser")
        return int(soup.find_all('a', class_='pagination__link ng-star-inserted')[-1].text)

    def get_links(self):
        """
        Method collects links to each video card and saves them to a list
        :return: List with video cards links
        """
        link_list = []
        for page in tqdm(range(1, self.get_pages_amount() + 1), desc="Parsing links...", unit=" links",
                         dynamic_ncols=True):
            soup = BeautifulSoup(self.get_html(page).text, features="html.parser")
            for link in soup.find_all('a', class_='goods-tile__heading ng-star-inserted', href=True):
                link_list.append(link.get('href'))
        return link_list

    def parse(self):
        """
        In this method creates a class object that collects all the necessary information for each link to
        a video card
        """
        parser_info = ParserInfo(self.get_links(), self.headers)
        parser_info.parse()
