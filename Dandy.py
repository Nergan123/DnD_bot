import os

import pandas as pd
from parser import *


class Dandy_bot:
    def __init__(self, campaign=''):
        if campaign == '':
            self.campaign = 'nergan_campaign'
        else:
            self.campaign = campaign

        self.parser = Parser(self.campaign)
        self.campaign_path = os.path.join(os.getcwd(), 'campaign', self.campaign)
        self.location = ''
        self.locations_list = self.parser.get_all_locations()
        self.rolls = []
        self.dice_comments = pd.read_csv('comments_data/dice_comments.csv', delimiter=';')

    def set_campaign(self, campaign=''):
        if campaign in os.listdir('campaign'):
            self.campaign = campaign
            self.parser = Parser(self.campaign)
            self.campaign_path = os.path.join(os.getcwd(), 'campaign', self.campaign)
            self.location = ''
            self.locations_list = self.parser.get_all_locations()
            return True
        else:
            return False

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

    def set_location(self, name):
        if name not in self.locations_list:
            return False
        else:
            self.location = name
            return True


# TODO add Iriy location to xml
# TODO ffmpeg for linux
