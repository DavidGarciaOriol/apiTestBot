import discord
import logging
import json
import requests
from pybooru import Danbooru

### JSON KEYS ACCESS MODULE ###

def access_json(key:str):
    response = ""
    token = ""
    try:
        file = open('tokens.json')
        jsondata = json.load(file)
    except:
        response = "No se puede acceder al JSON."
        print(response)
        return

    try:
        token = jsondata[key]
    except:
        response = "El término introducido no coincide con ninguna clave o no es válido."
        print(response)
    finally:
        file.close()

    return token


### RANDOM TEXT GENERATOR MODULE ###

def text_api_call():
    url = "https://baconator-bacon-ipsum.p.rapidapi.com/"

    querystring = {"type":"all-meat", "paras":"1"}

    headers = {
	"X-RapidAPI-Key": f"{access_json('text-api-token')}",
	"X-RapidAPI-Host": "baconator-bacon-ipsum.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.text

### PYBOORU MODULE - WIP ###

def pybooru_api_call():
    client = Danbooru('danbooru')
    artists = client.artist_list('ma')

    for artist in artists:
        print("Name: {0}".format(artist['name']))


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

### - - - ###


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$help'):
        response = '''```
        COMMAND LIST
        ------------
         $hola => El bot saluda con su descripción por defecto.
         $cerdada => El bot accede a la API de un Lorem Ipsum generator peculiar y porcino.
        ```'''
        await message.channel.send(response)

    if message.content.startswith('$hola'):
        await message.channel.send('Soy un BOT dedicado a las conexiones externas con distintas APIs y usos varios.')

    if message.content.startswith('$cerdada'):
        random_response = text_api_call()
        print(random_response)
        await message.channel.send(f'Diario de Latam: {random_response[2:-2]}')

client.run(access_json('bot-token'), log_handler=handler)