import os
from config import settings
from dotenv import load_dotenv
from discord.ext import commands
from Dandy import Dandy_bot


load_dotenv()
token = os.getenv('Token')
bot = commands.Bot(command_prefix=settings['prefix'])
Dandy = Dandy_bot()


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='dice',
             help='Rolls the dice. Command example "!dice 2 6" where player rolls 2 dices of 6 sides')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    author = ctx.message.author.display_name
    message_back = Dandy.roll(number_of_dice, number_of_sides)
    await ctx.send(f'{author} rolls ' + message_back)


if __name__ == "__main__":
    bot.run(token)
