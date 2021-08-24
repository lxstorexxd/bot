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
    check()
    await client.wait_until_ready()
    channel = client.get_channel(id=867467195991064636)
    while not client.is_closed():
        check()
        with open("setting.txt", "r") as f:
            token_dict = json.load(f)
        vk_session = vk_api.VkApi(token_dict['login'], token_dict['password'])
        try:
            vk_session.auth(token_only=True)
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return

        rand = rd.randint(0, 7824)
        data = vk_session.method('photos.get',
                                 {'owner_id': -194425593, 'album_id': 274267819, 'offset': rand, 'count': 1})
        items = data['items']
        for item in items:
            max_height = max(item['sizes'], key=lambda item: int(item['height']))
            url = max_height['url']
            print(url)
            await channel.send(url)
        await asyncio.sleep(7200)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    client.loop.create_task(my_background_task())

client.run(settings['TOKEN'])
