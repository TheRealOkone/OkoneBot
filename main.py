import asyncio

import discord



class MyClient(discord.Client):
    ch = None
    async def entrar(self,ctx):
        canal = ctx.author.voice.channel
        # I suggest make it global so other commands can acess it
        global voice_client
        voice_client = await canal.connect()
    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')
        elif message.content.startswith('$meme'):
            await message.channel.send('It is meme!')
        elif message.content.startswith('$vc'):
            channel = message.author.voice.channel
            self.ch = await channel.connect()
        elif message.content.startswith('$ds'):
            await message.guild.voice_client.disconnect()
            self.ch = None
        elif message.content.startswith('$bruh'):
            self.ch.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source ='test.mp3'))


    async def on_ready(self):
        print('We have logged in as {0.user}'.format(client))
    async def on_member_update(self, before, after):
        if before.id == 622157169504288778 and before.activity != after.activity:
            if after.activity == None:
                try:
                    await after.edit(nick='Why not?')
                except discord.errors.Forbidden:
                    print('Не хватает прав на изменение ника!')
            else:
                try:
                    a = 'Why are we not in ' + after.activity.name + '?'
                    if(len(a) >=32):
                        a = a[:30] + '?'
                    await after.edit(nick=a)
                except discord.errors.Forbidden:
                    print('Не хватает прав на изменение ника!')


intents = discord.Intents().all()
client = MyClient(intents=intents)
client.run("")