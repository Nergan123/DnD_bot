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
             help='Rolls the dice. Command example "!dice 2 6" where player rolls 2d6')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    author = ctx.message.author.display_name
    message_back = Dandy.roll(number_of_dice, number_of_sides, author)
    await ctx.send(message_back)


@bot.command(name='join_voice',
             help='Commands bot to join a voice channel in which you are now. Requires a DM role')
async def join(ctx):
    if 'DM' not in ctx.message.author.roles:
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


if __name__ == "__main__":
    bot.run(token)
