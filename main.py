import discord
import os
from discord.ext import commands,tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('Token')

client = discord.Client()

@client.event
async def on_ready():
    print('Ready to rock!!!')

client.run(TOKEN)
