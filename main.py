import os
import time
import random
from config import settings
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import PCMVolumeTransformer
from discord import File
from youtube_dl import YoutubeDL
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
    role = get(ctx.guild.roles, name="DM")
    if role in ctx.message.author.roles:
        dm = True
    else:
        dm = False
    message = message.split('d')
    author = ctx.message.author.display_name
    message_back = Dandy.roll(int(message[0]), int(message[1]), author, dm)
    await ctx.send(message_back)


@bot.command(name='login', help='Adds a player to the campaign list. Example "!login Name"')
async def add_player(ctx, name: str):
    out = Dandy.add_player(name, ctx.author.id)
    if out:
        await ctx.send(f'Added {name}')
    else:
        await ctx.send(f'Already logged in')


@bot.command(name='logout', help='Removes a player from campaign. Example "!logout Name"')
async def remove_player(ctx, name):
    out = Dandy.remove_player(name)
    if out:
        await ctx.send(f'Removed {name}')
    else:
        await ctx.send(f"Can't find {name} in the list")


@bot.command(name='join_voice',
             help='Commands bot to join a voice channel in which you are now. Requires a Admin role')
async def join(ctx):
    role = get(ctx.guild.roles, name="Admin")
    if role not in ctx.message.author.roles:
        await ctx.send("Only Admin can use this command!")
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

    if not ctx.voice_client:
        await ctx.send("I'm not in a voice client")

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    if Dandy.platform == 'windows':
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn', 'executable': 'ffmpeg_util\\win\\ffmpeg.exe'}
    else:
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'}
    voice = get(bot.voice_clients, guild=ctx.guild)
    url = Dandy.get_url()
    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.source = PCMVolumeTransformer(voice.source, volume=Dandy.volume)
        voice.is_playing()

    else:
        await ctx.send("Bot is already playing")
        return


@bot.command(name='pause', help='Pauses the music.')
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()


@bot.command(name='resume', help='Resumes music.')
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("Music is not paused.")


@bot.command(name='set_campaign', help='Sets campaign. DM role required.')
async def set_campaign(ctx, name=''):
    role = get(ctx.guild.roles, name="DM")
    if role not in ctx.message.author.roles:
        await ctx.send("Only DM can use this command!")
        return

    if not Dandy.interaction_ongoing:
        if name == '':
            await ctx.send("Name can't be blank")
            return
        out = Dandy.set_campaign(name)
        if out:
            await ctx.send(f'Campaign set to {name}')
        else:
            await ctx.send(f'Campaign {name} not found')
    else:
        await ctx.send("Can't set campaign while interaction is going.")


@bot.command(name='set_location', help='Sets current location. DM role required.')
async def location(ctx, name=''):
    role = get(ctx.guild.roles, name="DM")
    if role not in ctx.message.author.roles:
        await ctx.send("Only DM can use this command!")
        return

    if not Dandy.interaction_ongoing:
        out = Dandy.set_location(name)
        if out:
            if ctx.voice_client:
                voice = get(bot.voice_clients, guild=ctx.guild)
                if voice.is_paused():
                    await play(ctx)
                else:
                    await pause(ctx)
                    await play(ctx)
            await ctx.send(f"Current location set to {name}")
            image = Dandy.get_location_image()
            image = os.path.join(Dandy.campaign_path, image)
            with open(image, 'rb') as f:
                picture = File(f)
                await ctx.send(file=picture)
        else:
            await ctx.send(f"I can't find a location named {name}")
    else:
        await ctx.send("Can't change location while interaction is going.")


@bot.command(name='location_photo', help='Sends a photo of a current location.')
async def photo_location(ctx):
    image = Dandy.get_location_image()
    image = os.path.join(Dandy.campaign_path, image)
    with open(image, 'rb') as f:
        picture = File(f)
        await ctx.send(file=picture)


@bot.command(name='interaction', help='Starts an interaction with npc. DM role required.')
async def interaction(ctx, name: str):
    role = get(ctx.guild.roles, name="DM")
    if role not in ctx.message.author.roles:
        await ctx.send("Only DM can use this command!")
        return
    if not Dandy.interaction_ongoing:
        out = Dandy.interaction(name)
        if out:
            await ctx.send(f'You meet {Dandy.name_npc}')
            with open(Dandy.image, 'rb') as f:
                picture = File(f)
                await ctx.send(file=picture)
        else:
            await ctx.send("I can't find this npc")
    else:
        await ctx.send('You are already in the interaction')


@bot.command(name='npc_photo', help='Sends a photo of a current npc.')
async def photo_npc(ctx):
    image = Dandy.image
    image = os.path.join(Dandy.campaign_path, image)
    with open(image, 'rb') as f:
        picture = File(f)
        await ctx.send(file=picture)


@bot.command(name='end_interaction', help='Ends current interaction with npc. DM role required.')
async def end_interaction(ctx):
    role = get(ctx.guild.roles, name="DM")
    if role not in ctx.message.author.roles:
        await ctx.send("Only DM can use this command!")
        return

    if Dandy.mechanics != '':
        mechanics_message.stop()
    Dandy.end_interaction()
    if ctx.voice_client:
        voice = get(bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            await play(ctx)
        else:
            await pause(ctx)
            await play(ctx)


@bot.command(name='bestiary', help='Shows information about last npc you interacted with.')
async def bestiary(ctx):
    if Dandy.bestiary != '':
        await ctx.send(Dandy.bestiary)
    else:
        await ctx.send('There were no interactions yet')


@bot.command(name='battle', help='Starts battle with current npc. DM role required.')
async def battle(ctx):
    role = get(ctx.guild.roles, name="DM")
    if role not in ctx.message.author.roles:
        await ctx.send("Only DM can use this command!")
        return

    channel_id = ctx.channel.id
    Dandy.start_battle(channel_id)
    if ctx.voice_client:
        voice = get(bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            await play(ctx)
        else:
            await pause(ctx)
            await play(ctx)
    if Dandy.mechanics != '':
        mechanics_message.start(ctx)


@bot.command(name='damage_sanity')
async def damage_sanity(ctx, name: str, val: int):
    role = get(ctx.guild.roles, name="DM")
    if role not in ctx.message.author.roles:
        await ctx.send("Only DM can use this command!")
        return
    if Dandy.mechanics == 'Sanity':
        if name in Dandy.players:
            ind = Dandy.players.index(name)
            Dandy.sanity_mec.damage(ind, val)
            await ctx.send(f'{name} loses {val}% sanity.')
        else:
            await ctx.send(f'{name} not found')
    else:
        await ctx.send("Can't do that right now.")
        return


@bot.command(name='heal_sanity')
async def heal_sanity(ctx, name: str, val: int):
    role = get(ctx.guild.roles, name="DM")
    if role not in ctx.message.author.roles:
        await ctx.send("Only DM can use this command!")
        return
    if Dandy.mechanics == 'Sanity':
        if name in Dandy.players:
            ind = Dandy.players.index(name)
            Dandy.sanity_mec.heal(ind, val)
            await ctx.send(f'{name} gains {val}% sanity.')
        else:
            await ctx.send(f'{name} not found')
    else:
        await ctx.send("Can't do that right now.")
        return


@bot.command(name='stop_mechanics', help='Stops current mechanic.')
async def mechanics_stop(ctx):
    role = get(ctx.guild.roles, name="DM")
    if role not in ctx.message.author.roles:
        await ctx.send("Only DM can use this command!")
        return

    mechanics_message.stop()


@bot.command(name='get_sanity')
async def get_sanity_list(ctx):
    role = get(ctx.guild.roles, name="DM")
    if role not in ctx.message.author.roles:
        await ctx.send("Only DM can use this command!")
        return
    if Dandy.mechanics == 'Sanity':
        message = Dandy.sanity_mec.get_sanity()
        await ctx.send(message)
        return
    else:
        await ctx.send("Can't do that right now.")
        return


@tasks.loop(seconds=5)
async def mechanics_message(ctx):
    if Dandy.mechanics == 'Sanity':
        i = 0
        for player_id in Dandy.id:
            if time.time() >= Dandy.sanity_mec.sanity_timers[i]:
                user = await bot.fetch_user(player_id)
                message = Dandy.sanity_mec.message(i)
                output = '**' + Dandy.name_npc + ': ' + '**' + message
                await user.send(output)
                Dandy.sanity_mec.update_timers(i)
            i += 1
    elif Dandy.mechanics == 'Nightmare':
        if ctx.voice_client:
            voice = get(bot.voice_clients, guild=ctx.guild)
            if not voice.is_playing():
                await play(ctx)

        if random.randint(0, 100) < 2:
            if random.randint(1, 2) == 1:
                if ctx.voice_client:
                    voice = get(bot.voice_clients, guild=ctx.guild)
                    if voice.is_paused():
                        await play_nightmare(ctx)
                    else:
                        await pause(ctx)
                        await play_nightmare(ctx)
            else:
                image = Dandy.nightmare_mec.get_image()
                image = os.path.join('comments_data', 'nightmare_pics', image)
                timer = float(random.randint(1, 5))
                with open(image, 'rb') as f:
                    picture = File(f)
                    await ctx.send(file=picture, delete_after=timer)


@bot.command(pass_context=True)
async def play_nightmare(ctx):
    role = get(ctx.guild.roles, name="DM")
    if role not in ctx.message.author.roles:
        await ctx.send("Only DM can use this command!")
        return

    if not ctx.voice_client:
        await ctx.send("I'm not in a voice client")

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    if Dandy.platform == 'windows':
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn', 'executable': 'ffmpeg_util\\win\\ffmpeg.exe'}
    else:
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'}
    voice = get(bot.voice_clients, guild=ctx.guild)
    url = Dandy.nightmare_mec.get_url()
    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.source = PCMVolumeTransformer(voice.source, volume=Dandy.volume)
        voice.is_playing()


@bot.command(name='volume', help='Sets volume of the bot.')
async def volume(ctx, vol: int):
    if ctx.voice_client:
        voice = get(bot.voice_clients, guild=ctx.guild)
        if 0 <= vol <= 100:
            new_volume = vol / 100
            voice.source.volume = new_volume
            Dandy.set_volume(new_volume)
        else:
            await ctx.send('Please enter a volume between 0 and 100')


if __name__ == "__main__":
    bot.run(token)
