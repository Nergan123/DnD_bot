import os
import random
from config import settings
from dotenv import load_dotenv
from discord.ext import commands
from Dandy import Dandy_bot


load_dotenv()
token = os.getenv('Token')
bot = commands.Bot(command_prefix = settings['prefix'])
Dandy = Dandy_bot()


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='dice', help='Rolls the dice. Command example "!dice 2 6"')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    Dandy.roll(number_of_dice, number_of_sides)
    await ctx.send()


if __name__ == "__main__":
    bot.run(token)
