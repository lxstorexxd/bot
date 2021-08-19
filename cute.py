import requests
import json
import time
import vk_api
import random as rd
import discord
from discord.ext import commands
from config import settings
import asyncio

R = '\033[31m'
G = '\033[32m'
Y = '\033[33;1m'
B = '\033[34;1m'
W = '\033[37m'
LG = '\033[32;1m'


def check():
    try:
        requests.get("https://google.com/", timeout = 3)
    except requests.ConnectionError:
        print(R + "\n[ 〤 ] Проблема с интернет соединением!" + W)
        print(Y + "\n[ * ] Restart..." + W)
        time.sleep(30)
        check()


client = discord.Client()

async def my_background_task():
    await client.wait_until_ready()
    channel = client.get_channel(id=867467195991064636)
    while not client.is_closed():
        check()
        session = requests.Session()
        with open("setting.txt", "r") as f:
            token_dict = json.load(f)
        vk_session = vk_api.VkApi(token_dict['login'], token_dict['password'])
        try:
            vk_session.auth(token_only=True)
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return

        rand = rd.randint(0, 530)
        data = vk_session.method('wall.get', {'owner_id': -183039148, 'offset': rand, 'count': 1})
        item = data['items']
        for i in item:
            attachments = i['attachments']
            for photos in attachments:
                photo = photos['photo']
                sizes = photo['sizes']
                url = sizes[6]['url']
                check()
                resp = requests.post(
                    "https://api.deepai.org/api/nsfw-detector",
                    data={
                        'image': url,
                    },
                    headers={'api-key': '50a4e7bf-6ea2-4ff1-ae12-a9072c058557'}
                )
                req = json.loads(resp.content)['output']
                nsfw = req['nsfw_score']
                if float(nsfw) >= 0.50:
                    print(str('URL: ') + url + ' ' + str('nude %: ') + str(nsfw))
                    await channel.send(url)
                else:
                    print(url)
                    print('No boobs')
                    pass
        await asyncio.sleep(7200)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    client.loop.create_task(my_background_task())

client.run(settings['TOKEN'])
