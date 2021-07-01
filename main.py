from __future__ import unicode_literals
import asyncio
import configparser
import discord
from discord.ext import commands
from discord.ext.commands import bot
import requests
import json

import youtube_dl

config = configparser.ConfigParser()
config.read("config.ini")
youtubekey = config["Token"]["youtubekey"]

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='$', intents=intents)
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
}
ch = None


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_member_update(before, after):
    if before.id == 622157169504288778 and before.activity != after.activity:
        if after.activity == None:
            try:
                await after.edit(nick='Why not?')
            except discord.errors.Forbidden:
                print('Не хватает прав на изменение ника!')
        else:
            try:
                a = 'Why are we not in ' + after.activity.name + '?'
                if (len(a) >= 32):
                    a = a[:30] + '?'
                await after.edit(nick=a)
            except discord.errors.Forbidden:
                print('Не хватает прав на изменение ника!')


@bot.command()
async def vc(ctx):
    global ch
    channel = ctx.author.voice.channel
    ch = await channel.connect()


@bot.command()
async def bruh(ctx):
    global ch
    ch.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source='test.mp3'))


@bot.command()
async def ds(ctx):
    global ch
    await ctx.guild.voice_client.disconnect()
    ch = None


@bot.command()
async def hello(ctx):
    await ctx.send('hello')


@bot.command()
async def say(ctx, *, arg='bruh'):
    print('test')
    await ctx.send(arg)

@bot.command()
async def play(ctx, *, arg='test'):
    url = "https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q=" + arg + "&type=video&key=" + youtubekey
    r = requests.get(url)
    print(r.text)
    a = r.text[r.text.find('"videoId":'):]
    a= a[:a.find("}")]
    a = a[12:-8]
    b = r.text[r.text.find('"title":'):]
    b = b[:b.find('"description"') - 11]
    b = b[10:]
    print(a)
    print(b)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['http://www.youtube.com/watch?v=' + a])
    if ch is not None:
        ch.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=b + "-" + a + '.mp3'))
    else:
        ctx.send('Отсутствует')


bot.run(config['Token']['token'])
