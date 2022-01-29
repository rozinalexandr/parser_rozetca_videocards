from Parser import Parser

url = "https://hard.rozetka.com.ua/videocards/c80087/"

headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/87.0.4280.88 Safari/537.36"
}

if __name__ == '__main__':
    parser = Parser(url, headers)
    parser.parse()
