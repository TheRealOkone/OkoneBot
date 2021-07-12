from __future__ import unicode_literals
import asyncio
import configparser
import queue
import time
import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse
import discord
import eyed3
from discord import FFmpegPCMAudio
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
q = queue.Queue()


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
    global q
    global ch
    if arg.find("list") != -1:

        u = arg[arg.rfind("list") + 5:]

        print(u)
        url = 'https://www.youtube.com/playlist?list=' + u
        query = parse_qs(urlparse(url).query, keep_blank_values=True)
        playlist_id = query["list"][0]

        print(f'get all playlist items links from {playlist_id}')
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=youtubekey)

        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50
        )
        response = request.execute()

        playlist_items = []
        while request is not None:
            response = request.execute()
            playlist_items += response["items"]
            request = youtube.playlistItems().list_next(request, response)

        print(f"total: {len(playlist_items)}")
        print([
            f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&t=0s'
            for t in playlist_items
        ])
        for t in playlist_items:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download(['http://www.youtube.com/watch?v=' + t["snippet"]["resourceId"]["videoId"]])
                str = t["snippet"]["title"] + "-" + t["snippet"]["resourceId"]["videoId"] + '.mp3'
                q.put(str)
    else:
        url = "https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q=" + arg + "&type=video&key=" + youtubekey
        r = requests.get(url)
        print(r.text)
        a = r.text[r.text.find('"videoId":'):]
        a = a[:a.find("}")]
        a = a[12:-8]
        b = r.text[r.text.find('"title":'):]
        b = b[:b.find('"description"') - 11]
        b = b[10:]
        print(a)
        print(b)
        str = b + "-" + a + '.mp3'
        q.put(str)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['http://www.youtube.com/watch?v=' + a])
    if ch is None:
        channel = ctx.author.voice.channel
        ch = await channel.connect()
    print("Starting///")
    while not q.empty():
        n = q.get(0)
        voice_file = eyed3.load(n)
        secs = int(voice_file.info.time_secs)
        ch.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=n))
        print(secs)
        while ch.is_playing() or ch.is_paused():
            await asyncio.sleep(1)


@bot.command()
async def skip(ctx):
    global ch
    global q
    if ch is None:
        ctx.send("Play smh")
    else:
        ch.stop()
        n = q.get(0)
        voice_file = eyed3.load(n)
        secs = int(voice_file.info.time_secs)
        ch.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=n))

@bot.command()
async def pause(ctx):
    global ch
    if ch is None:
        ctx.send("Play smh")
    else:
        ch.stop()


@bot.command()
async def resume(ctx):
    global ch
    if ch is None:
        ctx.send("Play smh")
    else:
        ch.resume()


# @bot.command()
# async def playlist(ctx, *, arg='test'):
#     global ch
#     if ch is None:
#         ctx.send("Play smh")
#     else:
#         URL = arg
#         player = FFmpegPCMAudio(URL, executable="C:/ffmpeg/bin/ffmpeg.exe")
#         queue.append(player)
#         source = queue.pop(0)
#         voice.play(player, after=lambda e: play_next(ctx, source))
#         await ctx.send('playing song')


bot.run(config['Token']['token'])
