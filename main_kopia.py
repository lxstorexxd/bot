import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from random import randint as rd
import json
import time
import requests
import xmltodict
import wikipedia

def write_msg(chat_id, message):
    vk.method('messages.send', {'chat_id': chat_id, 'message': message, 'random_id': rd(1, 1000000)})


try:
    with open("core/auth.json", "r") as f:
        token = json.load(f)
        id = token[1]
        token = token[0]
except:
    done = "Failed"
    time.sleep(0.2)
    print("Не удалось открыть файл с токеном!")
    raise
    exit()

try:
    vk = vk_api.VkApi(token=token)
    longpoll = VkBotLongPoll(vk, id)

except:
    done = "Failed"
    time.sleep(0.2)
    print("Не удалось авторизироваться! Проверьте токен и id сообщества!")
    raise
    exit()


def get_weather():
    weather = requests.get("https://api.openweathermap.org/data/2.5/weather",
                           params={'id': 472459, 'units': 'metric', 'lang': 'ru',
                                   'APPID': '12d031d12a45baf529d87fa5136a115f'})
    weather = weather.json()
    description = weather["weather"]
    description = description[0]

    description = description["description"]
    main = weather["main"]

    temp = main["temp"]
    bar = float(main["pressure"]) * 0.750064

    wind = weather["wind"]
    wind = wind["speed"]

    result = '''&#127760;''' + 'Погода в Вологде' + '''&#127760;
Состояние: ''' + description + '''
Температура: ''' + str(temp) + ''' °C
Давление: ''' + str(round(bar, 2)) + ''' м.р.с.
Ветер: ''' + str(wind) + ''' м/с'''
    return result



def get_anecdot():
    anecdote = requests.get('http://rzhunemogu.ru/Rand.aspx', params={'CType': 1})
    xml = xmltodict.parse(anecdote.text)

    items = xml['root']
    item = items['content']
    return item


def wiki(response):
    try:
        wikipedia.set_lang("ru")
        search = wikipedia.summary(response)
        write_msg(event.chat_id, search)
    except:
        write_msg(event.chat_id, "Запрос не найден")


dictionary = {'опд': '[331853910|Ковшикова Юлия Сергеевна]',
              'математика': '[id501463244|Авдуевская Наталья Сергеевна]',
              'физика': '[id103708643|Валентина Алексеевна Богатикова]',
              'история': '[id139792191|Удальцова Елена Олеговна]',
              'физра': '[id49028795|Новикова Людмила Петровна]',
              'информатика': '[id96441649|Пролыгина Елена Андреевна]',
              'куратор': '[id522552847|Сидорова Юлия Васильевна]',
              'английский': '[id86172528|Анисимова Людмила Вадимовна]',
              'русский': '[id34508049|Ревелева Елена Сергеевна]',
              'литра': '[id34508049|Ревелева Елена Сергеевна]',
              'химия': '[id58495715|Юдичева Наталья Анатольевна]',
              'биология': '[id58495715|Юдичева Наталья Анатольевна]'
              }
request = []

Приветствия = {0: "Здравствуйте",
               1: "Привет",
               2: "Хай",
               3: "Приветствую",
               4: "Здарова бандит",
               5: "А теперь спросите меня: «Как дела?»",
               6: "Сам Привет",
               7: "Hi",
               8: "А теперь раскодируйте пожалуйста ваше сообщение.", }

столы = {'переверни стол': '(╯°□°）╯︵ ┻━┻',
         'поставь стол': '(ヘ･_･)ヘ┳━┳', }
request = []

Настроение = {
    0: "Хорошо",
    1: "Отлично",
    2: "Так себе",
    3: "Плохо",
    4: "Жесть",
    5: "Замечательно",
    6: "Бывало и лучше",
    7: "Лучше не спрашивай",
    8: "Нормально",
    9: "«Хреношо» (догадайся, где тут ошибка).",
    10: "Дела мои амбивалентно…",
    11: "В душе осталась горстка пепла и плоть изношена дотла. Но обстоят великолепно мои душевные дела!",
    12: "В порядке, только вот в случайном.",
    13: "Вот как вы спросили, так сразу прекрасно стало, так мне этого не хватало!",
    14: "Все дела переданы прокурору.",
    15: "Вы несравненно оригинальны в своих вопросах!",
    16: "Да вот как раз думаю, как отвязаться от назойливого собеседника.",
    17: "Дела бывают у того, кто что-то делает, а я – отдыхаю!",
    18: "Думаю, знаешь ответ? Оба же в России живем, ничего хорошего не происходит.",
    19: "Есть два способа поставить человека в тупик: спросить у него «Как дела?» и попросить рассказать что-нибудь…"
}

Занятия = {0: "Играю в виртуальный футбол",
           1: "Отдыхаю от рутины",
           2: "Развиваюсь",
           3: "Общаюсь с тобой",
           4: "Да ничего собственно",
           5: "Именно сейчас? Отвечаю Вам на поставленный вопрос!",
           6: "Помогаю президенту урегулировать положение в нашей стране",
           7: "Мечтаю о счастливом будущем",
           8: "Мою мыло",
           9: "Сплю и вижу страшный сон, в котором ты у меня спрашиваешь, что я делаю.",
           10: "Что я могу делать? Конечно же, кошу сено в комнате и перед монитором его раскладываю.",
           11: "Стреляю из самого мощного автомата в мире, скорее нагнись, чтобы тебя не зацепило.",
           12: "Отмечаю день города в Кейптауне",
           13: "Думаю о том, куда обычно прячут труп сантехника",
           14: "Это повод написать или на самом деле интересно?",
           15: "Страдаю не опознанным и никому не понятным – ерундой",
           16: "Считаю, какой по счету ты спросил, чем я занимаюсь.",
           17: "Думаю, как отвязаться от надоедливого собеседника."
}

от1до100 = list(range(1, 101))
монетка = {0: "ОРЕЛ", 1: "РЕШКА"}
while 1:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                request = event.message.text.lower()
                if request in dictionary:
                    write_msg(event.chat_id, dictionary[request])
                elif request == 'привет' or request == 'приветствую' or request == 'хай' or request == 'здарова' or request == 'ку':
                    write_msg(event.chat_id, str(Приветствия[rd(0, len(Приветствия) - 1)]))
                elif request == 'эдик, как дела' or request == 'как дела':
                    write_msg(event.chat_id, str(Настроение[rd(0, len(Настроение) - 1)]))
                elif 'эдик, что делаешь' or 'что делаешь' in request:
                    write_msg(event.chat_id, str(Занятия[rd(0, len(Занятия) - 1)]))
                elif request == 'roll':
                    write_msg(event.chat_id, str(от1до100[rd(0, len(от1до100) - 1)]))
                elif request == '((' or request == '(' or request == '(((' or request == '((((' or request == '(((((' or request == '((((((':
                    write_msg(event.chat_id, 'Не грусти, лучше попроси меня скинуть анекдот!')
                elif request == ')' or request == ')))' or request == '))' or request == '))))' or request == ')))))' or request == '))))))':
                    write_msg(event.chat_id, 'Я рад за тебя')
                elif request == 'эдик, погода' or request == 'погода':
                    write_msg(event.chat_id, get_weather())
                elif request == 'эдик, анекдот' or request == 'навали кринжа' or request == 'анекдот':
                    write_msg(event.chat_id, get_anecdot())
                elif request == 'монетка' or request == "flip":
                    write_msg(event.chat_id, str(монетка[rd(0, len(монетка) - 1)]))
                elif request == "журнал":
                    write_msg(event.chat_id, "https://ssuz.vip.edu35.ru/")
                elif request == "дистант":
                    write_msg(event.chat_id, "http://moodle.kolledgsvyazi.ru:808")
                elif request in столы:
                    write_msg(event.chat_id, столы[request])
                elif '/' in request:
                    responce = request[0:]
                    wiki(responce)
    except:
        pass