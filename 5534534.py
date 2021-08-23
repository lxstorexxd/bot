import fake_useragent
import requests
from bs4 import BeautifulSoup
import json



url = f'https://www.kinopoisk.ru/chance/?item=true&count=1&max_years=2021&min_years=2012'


user = fake_useragent.UserAgent().random
header = {
    'user-agent': user
}

session = requests.Session()
response = session.post(url, headers=header).json()

print(response)