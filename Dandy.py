import json
import os
import random
import time
import sys
import pandas as pd
import boto3
from parser import *
from mechanics.sanity import *
from mechanics.nightmare import *
from mechanics.illusions import *


class Dandy_bot:
    SERIALIZABLE_FIELDS = [
        'location',
        'interaction_ongoing',
        'name_npc',
        'bestiary',
        'image',
        'mechanics',
        'boss',
        'battle',
        'players',
        'id',
        'volume',
        'guild',
        'channel',
        'voice_channel'
    ]
    STATE_BUCKET = "nergan-bot"
    STATE_REMOTE_FILE_NAME = "state.json"

    def __init__(self, campaign=''):
        if campaign == '':
            self.campaign = 'nergan_campaign'
        else:
            self.campaign = campaign
        if sys.platform == 'linux':
            self.platform = 'linux'
        else:
            self.platform = 'windows'
        self.parser = Parser(self.campaign)
        self.guild = ''
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
        self.id = []
        self.volume = 1.0
        self.playing = False
        self.channel = ''
        self.voice_channel = ''
        self.load_state()
        if self.battle:
            if self.mechanics == 'Sanity':
                self.sanity_mec = sanity(self.players)
                self.sanity_mec.load_state()
            elif self.mechanics == 'Nightmare':
                self.nightmare_mec = nightmare()
            elif self.mechanics == 'Illusions':
                self.illusion_mec = illusions(self.players, self.id)

        # AWS_ACCESS_KEY_ID
        # AWS_SECRET_ACCESS_KEY

# TODO Fix sanity load and save system

    def save_state(self):
        state = {}
        for property_name in self.SERIALIZABLE_FIELDS:
            state[property_name] = self.__getattribute__(property_name)

        # s3 = boto3.resource('s3')
        # remote_object = s3.Object(self.STATE_BUCKET, self.STATE_REMOTE_FILE_NAME)
        # remote_object.put(Body=(bytes(json.dumps(state).encode('UTF-8'))))
        with open('dandy_data.json', 'w') as f:
            json.dump(state, f)

    def load_state(self):
        # s3 = boto3.client('s3')
        # s3_response = s3.get_object(Bucket=self.STATE_BUCKET, Key=self.STATE_REMOTE_FILE_NAME)
        # state_json = s3_response['Body'].read()
        with open('dandy_data.json', 'r') as f:
            state = json.loads(f.read())
        print(state)
        for property_name in self.SERIALIZABLE_FIELDS:
            self.__setattr__(property_name, state[property_name])

    def set_volume(self, vol: float):
        self.volume = vol
        self.save_state()

    def add_player(self, name='', id=''):
        if id in self.id:
            return False
        if name != '':
            if name not in self.players:
                self.players.append(name)
                self.id.append(id)
                self.save_state()
                return True
            else:
                return False

    def remove_player(self, name=''):
        if name != '':
            if name in self.players:
                ind = self.players.index(name)
                self.players.remove(name)
                self.id.pop(ind)
                self.save_state()
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
            self.save_state()
            return True
        else:
            return False

    def roll(self, number_of_dice, number_of_sides, user='', dm=False):
        output = ''
        summ = 0
        if number_of_dice == 1 and number_of_sides == 20:
            roll = random.choice(range(1, number_of_sides+1))
            throw_list = self.dice_comments[self.dice_comments.dice == roll]
            line = throw_list.sample()
            if dm and self.battle:
                output = line.iloc[0]['comment'] + '**' + f' {self.name_npc} rolls ' + str(roll) + '**'
            else:
                output = line.iloc[0]['comment'] + '**' + f' {user} rolls ' + str(roll) + '**'
        else:
            for throw in range(number_of_dice):
                roll = random.choice(range(1, number_of_sides+1))
                output = output + ' + ' + str(roll)
                summ = summ + roll
            if dm and self.battle:
                output = '**' + f'{self.name_npc} rolls ' + '**' + output[2:] + f' = {summ}'
            else:
                output = '**' + f'{user} rolls ' + '**' + output[2:] + f' = {summ}'

        return output

    def get_url(self):
        url = self.parser.get_music(self.location, self.battle)

        return url

    def set_location(self, name):
        self.locations_list = self.parser.get_all_locations()
        if name not in self.locations_list:
            return False
        else:
            self.location = name
            self.save_state()
            return True

    def get_location_image(self):
        return self.parser.get_location_image(self.location)

    def get_bestiary(self):
        return self.bestiary

    def interaction(self, name):
        npc_xml = self.parser.get_npc(self.location, name)
        if npc_xml:
            self.interaction_ongoing = True
            self.name_npc, self.boss, self.image, self.mechanics, self.bestiary = self.parser.get_npc_info(npc_xml)
            self.image = os.path.join(self.campaign_path, self.image)
            self.save_state()
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
        self.interaction_ongoing = False
        self.save_state()

    def start_battle(self):
        self.battle = True
        self.save_state()
        if self.mechanics == 'Sanity':
            self.sanity_mec = sanity(self.players)
        elif self.mechanics == 'Nightmare':
            self.nightmare_mec = nightmare()
        elif self.mechanics == 'Illusions':
            self.illusion_mec = illusions(self.players, self.id)


# TODO add Iriy location to xml
# TODO add this https://www.youtube.com/watch?v=1rgDPmnAUtE to forest music, this https://www.youtube.com/watch?v=bsvzP8EO65w to Koshey
# TODO add this for ending song https://www.youtube.com/watch?v=6FJXjJeOU6Q
# TODO add this to elven lands <url>https://www.youtube.com/watch?v=HJLaTSjnd9Q</url>
