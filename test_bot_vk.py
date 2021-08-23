import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from random import randint as rd
import json
import requests
import time
import fake_useragent
from bs4 import BeautifulSoup

try:
    with open("core/auth.json", "r") as f:
        token = json.load(f)
        id_group = token[1]
        token = token[0]
except:
    done = "Failed"
    time.sleep(0.2)
    print("Не удалось открыть файл с токеном!")
    raise
    exit()

try:
    vk = vk_api.VkApi(token=token)
    vk._auth_token()
    longpoll = VkBotLongPoll(vk, id_group)

except:
    done = "Failed"
    time.sleep(0.2)
    print("Не удалось авторизироваться! Проверьте токен и id сообщества!")
    raise
    exit()

def get_film(min_years, max_years):

    url = f'https://www.kinopoisk.ru/chance/?item=true&count=1&max_years={max_years}&min_years={min_years}'
    link = 'https://www.kinopoisk.ru'

    user = fake_useragent.UserAgent().random
    header = {
        'user-agent': user
    }

    session = requests.Session()
    response = session.post(url, headers=header).json()
    for req in response:
        soup = BeautifulSoup(req, 'lxml')

        image = soup.find_all('div', class_='poster')
        for img in image:
            url_img = img.find_all('img')
            for url in url_img:
                photo_url = link + url['src']

        film_name = soup.find('div', class_='filmName')
        film_name_rus = film_name.find_all('a')
        film_name_en = film_name.find_all('span')
        for name_rus in film_name_rus:
            for name_en in film_name_en:
                common_name = name_rus.text + ' / ' + name_en.text

        estimation = soup.find_all('div', class_='imdb')
        for score in estimation:
            common_score = score.text + '-оценок'

        description = soup.find_all('div', class_='syn')
        for syn in description:
            descriptions = 'Описание: ' + syn.text
    return (photo_url + '\n\n' + common_name + '\n\n' + common_score + '\n\n' + descriptions)

keyboard = {
    "one_time": False,
    "buttons": [
        [{"action": {"type": "text","payload": "{\"button\": \"1\"}","label": "Случайный фильм"},"color": "positive"}],
        [{"action": {"type": "text","payload": "{\"button\": \"1\"}","label": "Фильтры"},"color": "primary"}],
        [{"action": {"type": "text","payload": "{\"button\": \"1\"}","label": "↓ Скрыть ↓"},"color": "negative"}]
               ]
            }

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

keyboard_clear = {
    "one_time": True,
    "buttons": []
            }

keyboard_clear = json.dumps(keyboard_clear, ensure_ascii=False).encode('utf-8')
keyboard_clear = str(keyboard_clear.decode('utf-8'))

keyboard_filter = {
    "one_time": False,
    "buttons": [
        [{"action": {"type": "text","payload": "{\"button\": \"1\"}","label": "Жанр"},"color": "positive"}, {"action": {"type": "text","payload": "{\"button\": \"1\"}","label": "Год выхода"},"color": "positive"}],
        [{"action": {"type": "text","payload": "{\"button\": \"1\"}","label": "← Назад ←"},"color": "negative"}]
               ]
            }

keyboard_filter = json.dumps(keyboard_filter, ensure_ascii=False).encode('utf-8')
keyboard_filter = str(keyboard_filter.decode('utf-8'))

keyboard_years = {
    "one_time": False,
    "buttons": [
        [{"action": {"type": "text","payload": "{\"button\": \"1\"}","label": "Новинки"},"color": "positive"}],
        [{"action": {"type": "text","payload": "{\"button\": \"1\"}","label": "2011 - 2021"},"color": "primary"}],
        [{"action": {"type": "text","payload": "{\"button\": \"1\"}","label": "2001 - 2010"},"color": "primary"}],
        [{"action": {"type": "text","payload": "{\"button\": \"1\"}","label": "1920 - 2000"},"color": "primary"}],
        [{"action": {"type": "text","payload": "{\"button\": \"1\"}","label": "← Назад ←"},"color": "negative"}]
               ]
            }

keyboard_years = json.dumps(keyboard_years, ensure_ascii=False).encode('utf-8')
keyboard_years = str(keyboard_years.decode('utf-8'))


while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                message = event.object['text'].lower()
                id = event.obj['peer_id']

                if message == '↓ скрыть ↓':
                    vk.method('messages.send', {'user_id': id, 'message': '&#11015; Клавиатура скрыта &#11015;',
                                                'random_id': rd(1, 1000000), 'keyboard': keyboard_clear})
                elif message == '← назад ←':
                    vk.method('messages.send', {'user_id': id, 'message': '&#13;', 'random_id': rd(1, 1000000), 'keyboard': keyboard})

                elif message == 'начать':
                    vk.method('messages.send',
                              {'user_id': id, 'message': 'Приветствую! Я помогу подобрать тебе фильм на вечер :3',
                               'random_id': rd(1, 1000000), 'keyboard': keyboard})

                elif message == 'случайный фильм':
                        vk.method('messages.send', {'user_id': id, 'message': get_film(min_years=1920, max_years=2021), 'random_id': rd(1, 1000000)})

                elif message == 'фильтры':
                    vk.method('messages.send',
                              {'user_id': id, 'message': 'Выберите фильтр',
                               'random_id': rd(1, 1000000), 'keyboard': keyboard_filter})
                elif message == 'год выхода':
                    vk.method('messages.send',
                              {'user_id': id, 'message': 'Выберите дату выхода фильма',
                               'random_id': rd(1, 1000000), 'keyboard': keyboard_years})

                elif message == 'жанр':
                    vk.method('messages.send',
                              {'user_id': id, 'message': 'Данная функция пока не доступна(',
                               'random_id': rd(1, 1000000)})

                elif message == '1920 - 2000':
                    vk.method('messages.send', {'user_id': id, 'message': get_film(min_years=1920, max_years=2000),
                                                'random_id': rd(1, 1000000)})
                elif message == '2001 - 2010':
                    vk.method('messages.send', {'user_id': id, 'message': get_film(min_years=2001, max_years=2010),
                                                'random_id': rd(1, 1000000)})
                elif message == '2011 - 2021':
                    vk.method('messages.send', {'user_id': id, 'message': get_film(min_years=2011, max_years=2021),
                                                'random_id': rd(1, 1000000)})
                elif message == 'новинки':
                    vk.method('messages.send', {'user_id': id, 'message': get_film(min_years=2021, max_years=2021),
                                                'random_id': rd(1, 1000000)})

    except:
        pass

