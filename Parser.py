import requests
from bs4 import BeautifulSoup


class Parser:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def get_html(self, page):
        return requests.get(self.url + f'/page={page}/', headers=self.headers)

    def get_clicks_amount(self):
        soup = BeautifulSoup(self.get_html(1).text, features="html.parser")
        return int(soup.find_all('a', class_='pagination__link ng-star-inserted')[-1].text)

    def get_links(self):
        link_list = []
        for page in range(1, self.get_clicks_amount() + 1):
            soup = BeautifulSoup(self.get_html(page).text, features="html.parser")
            for link in soup.find_all('a', class_='goods-tile__heading ng-star-inserted', href=True):
                link_list.append(link.get('href'))
        return link_list

    def parse(self):

        print(len(self.get_links()))
        print(self.get_links())
