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
        self.interaction_ongoing = False
        self.dice_comments = pd.read_csv('comments_data/dice_comments.csv', delimiter=';')
        self.name_npc = ''
        self.bestiary = ''
        self.image = ''
        self.mechanics = ''
        self.boss = False
        self.battle = False
        self.players = []

    def add_player(self, name=''):
        if name != '':
            if name not in self.players:
                self.players.append(name)
                return True
            else:
                return False

    def remove_player(self, name=''):
        if name != '':
            if name in self.players:
                self.players.remove(name)
                return True
            else:
                return False

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
            output = line.iloc[0]['comment'] + '**' + f' {user} rolls ' + str(roll) + '**'
        else:
            for throw in range(number_of_dice):
                roll = random.choice(range(1, number_of_sides+1))
                output = output + ' ' + str(roll)
            output = '**' + f'{user} rolls ' + output + '**'

        return output

    def get_url(self):
        url = self.parser.get_music(self.location, self.battle)

        return url

    def set_location(self, name):
        if name not in self.locations_list:
            return False
        else:
            self.location = name
            return True

    def get_location_image(self):
        return self.parser.get_location_image(self.location)

    def get_bestiary(self):
        return self.bestiary

    def interaction(self, name):
        npc_xml = self.parser.get_npc(self.location, name)
        if npc_xml:
            self.name_npc, self.boss, self.image, self.mechanics, self.bestiary = self.parser.get_npc_info(npc_xml)
            self.image = os.path.join(self.campaign_path, self.image)
            return True
        else:
            return False

    def end_interaction(self):
        self.name_npc = ''
        self.boss = False
        self.image = ''
        self.mechanics = ''
        self.bestiary = ''
        self.battle = False

    def start_battle(self):
        self.battle = True


# TODO add Iriy location to xml
# TODO ffmpeg for linux
# TODO add this https://www.youtube.com/watch?v=1rgDPmnAUtE to forest music, this https://www.youtube.com/watch?v=bsvzP8EO65w to Koshey
