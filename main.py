import asyncio
import configparser
import discord
from discord.ext import commands
from discord.ext.commands import bot

config = configparser.ConfigParser()
config.read("config.ini")

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='$', intents=intents)

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
    if ch is not None:
        ch.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=arg + '.mp3'))
    else:
        ctx.send('Отсутствует')


bot.run(config['Token']['token'])
