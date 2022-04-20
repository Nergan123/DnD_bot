import discord
import os
from discord.ext import commands, tasks
from dotenv import load_dotenv


class Dandy_bot(commands.AutoShardedBot):
    def __init__(self, token):
        self.token = token
        super().__init__(command_prefix="!")

    async def on_ready(self):
        print(f'Ready to rock!')

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to my Discord server!'
        )

    async def on_message(self, message):
        if message.author == self.user:
            return

        if 'happy birthday' in message.content.lower():
            await message.channel.send('Happy Birthday! 🎈🎉')

    def awaken(self):
        self.run(self.token)
