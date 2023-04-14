import os
import discord
from discord.ext import commands, tasks
import requests
from io import BytesIO
from imgurpython import ImgurClient
from random import choice

# get TOKEN from .env file
TOKEN = os.environ['IMG_TOKEN']

PREFIX = '!'
IMGUR_CLIENT_ID = '0e89f2a718854ca'
IMGUR_ALBUM_ID = 'RtSjSYc'


intents = discord.Intents.default()
intents.typing = False
intents.presences = False
imgur_client = ImgurClient(IMGUR_CLIENT_ID, '')

bot = commands.Bot(command_prefix=PREFIX, intents=intents)


def get_image_bytes(url: str):
    response = requests.get(url)
    return BytesIO(response.content)


def get_random_image_url_from_album(album_id: str):
    images = imgur_client.get_album_images(album_id)
    return choice(images).link


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    send_image.start()


@bot.command(name='sexta', help='Certamente é sexta-feira')
async def send_image_command(ctx):
    await send_image_to_channel(ctx.channel)


@tasks.loop(hours=24)
async def send_image():
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await send_image_to_channel(channel)
                break


async def send_image_to_channel(channel):
    image_url = get_random_image_url_from_album(IMGUR_ALBUM_ID)
    image_bytes = get_image_bytes(image_url)
    await channel.send(file=discord.File(fp=image_bytes, filename='diogo.png'))

bot.run(TOKEN)
