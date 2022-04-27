import os
from config import settings
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from Dandy import Dandy_bot


load_dotenv()
token = os.getenv('Token')
bot = commands.Bot(command_prefix=settings['prefix'])
Dandy = Dandy_bot()


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='dice',
             help='Rolls the dice. Command example "!dice 2d6"')
async def roll(ctx, message):
    message = message.split('d')
    author = ctx.message.author.display_name
    message_back = Dandy.roll(int(message[0]), int(message[1]), author)
    await ctx.send(message_back)


@bot.command(name='join_voice',
             help='Commands bot to join a voice channel in which you are now. Requires a DM role')
async def join(ctx):
    role = get(ctx.guild.roles, name="DM")
    if role not in ctx.message.author.roles:
        await ctx.send("Only DM can use this command!")
        return

    if not ctx.message.author.voice:
        await ctx.send(f'{ctx.message.author.name} is not connected to a voice channel')
        return

    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()


@bot.command(name='leave_voice',
             help='Commands bot to leave a voice channel. Requires a DM role')
async def leave(ctx):
    role = get(ctx.guild.roles, name="DM")
    if role not in ctx.message.author.roles:
        await ctx.send("Only DM can use this command!")
        return

    if not ctx.message.author.voice:
        await ctx.send(f'{ctx.message.author.name} is not connected to a voice channel')
        return

    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("I'm not in a voice channel")


@bot.command(name='play', help='Plays music of current location. DM role required.')
async def play(ctx):
    role = get(ctx.guild.roles, name="DM")
    if role not in ctx.message.author.roles:
        await ctx.send("Only DM can use this command!")
        return

    voice = get(bot.voice_clients, guild=ctx.guild)
    name = Dandy.music()
    song = os.path.join(Dandy.campaign_path, 'music', name)
    voice.play(FFmpegPCMAudio(song, executable="ffmpeg_util\\win\\ffmpeg.exe"))


@bot.command(name='pause', help='Pauses the music.')
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("No audio is playing.")


if __name__ == "__main__":
    bot.run(token)
