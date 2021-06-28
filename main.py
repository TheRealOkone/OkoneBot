import discord
import os

from discord.ext import *
from discord.ext import commands

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    elif message.content.startswith('$meme'):
        await message.channel.send('It is meme!')
    elif message.content.startswith('$vc'):
        channel = message.author.voice.channel
        await channel.connect()
    elif message.content.startswith('$ds'):
        await message.guild.voice_client.disconnect()


@client.event
async def entrar(ctx):
    canal = ctx.author.voice.channel
    #I suggest make it global so other commands can acess it
    global voice_client
    voice_client = await canal.connect()





client.run("TOKEN")