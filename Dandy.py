import os
import random
import time
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
        self.sanity_comments = pd.read_csv('comments_data/sanity_comments.csv', delimiter=';')
        self.name_npc = ''
        self.bestiary = ''
        self.image = ''
        self.mechanics = ''
        self.boss = False
        self.battle = False
        self.players = []
        self.id = []
        self.sanity_level = []
        self.sanity_timers = []

    def add_player(self, name='', id=''):
        if id in self.id:
            return False
        if name != '':
            if name not in self.players:
                self.players.append(name)
                self.id.append(id)
                return True
            else:
                return False

    def remove_player(self, name=''):
        if name != '':
            if name in self.players:
                ind = self.players.index(name)
                self.players.remove(name)
                self.id.pop(ind)
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
        if self.mechanics == 'Sanity':
            self.sanity_level = [100 for player in self.players]
            self.sanity_timers = [time.time() + 180 for player in self.players]

    def damage_sanity(self, name, dmg):
        if name in self.players:
            ind = self.players.index(name)
            self.sanity_level[ind] = self.sanity_level[ind] - dmg
            self.update_sanity_timers(ind)
            return True
        else:
            return False

    def sanity_message(self, index):
        result = round(self.sanity_level[index]/10)
        sanity_comments_list = self.sanity_comments[self.sanity_comments.sanity == result]
        line = sanity_comments_list.sample()
        output = '**' + self.name_npc + ': ' + '**' + line.iloc[0]['comment']
        return output

    def update_sanity_timers(self, i):
        self.sanity_timers[i] = time.time() + 175*(self.sanity_level[i]/100) + 5 + random.randint(1, 5)


# TODO add Iriy location to xml
# TODO ffmpeg for linux
# TODO add this https://www.youtube.com/watch?v=1rgDPmnAUtE to forest music, this https://www.youtube.com/watch?v=bsvzP8EO65w to Koshey
