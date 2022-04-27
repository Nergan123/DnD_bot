import random
import os
import pandas as pd
import youtube_dl
from parser import *


class Dandy_bot:
    def __init__(self, campaign=''):
        if campaign == '':
            self.campaign = 'nergan_campaign'
        else:
            self.campaign = campaign

        self.parser = Parser()
        self.campaign_path = os.path.join(os.getcwd(), 'campaign', self.campaign)
        self.location = ''
        self.rolls = []
        self.dice_comments = pd.read_csv('comments_data/dice_comments.csv', delimiter=';')

    def roll(self, number_of_dice, number_of_sides, user=''):
        output = ''
        if number_of_dice == 1 and number_of_sides == 20:
            roll = random.choice(range(1, number_of_sides+1))
            output = output + ' ' + str(roll)
            throw_list = self.dice_comments[self.dice_comments.dice == roll]
            line = throw_list.sample()
            self.rolls.append(roll)
            output = line.iloc[0]['comment'] + '**' + f' {user} rolls ' + str(roll) + '**'
        else:
            for throw in range(number_of_dice):
                roll = random.choice(range(1, number_of_sides+1))
                output = output + ' ' + str(roll)
                self.rolls.append(roll)
            output = '**' + f'{user} rolls ' + output + '**'

        return output

    def music(self):
        path = os.path.join(self.campaign_path, 'music')
        if not os.path.isdir(path):
            os.makedirs(path)
        url, name = self.parser.get_music()
        file_name = os.path.join(path, name)
        files = os.listdir(path)
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': file_name,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        if name not in files:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        return name

# TODO add Iriy location to xml
# TODO init to download songs
# TODO ffmpeg for linux
