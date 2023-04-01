import os
import sys
import json
import pandas as pd
import random
from helpers.parser import Parser
from mechanics.sanity import sanity
from mechanics.nightmare import nightmare
from mechanics.illusions import illusions
from helpers.base_class import Base_class
from helpers.player_object import Player


class Dandy_bot(Base_class):
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
        'voice_channel',
        'initiative',
        'npc_initiative',
        'queue',
        'current_turn'
    ]
    STATE_BUCKET = "nergan-bot"
    STATE_REMOTE_FILE_NAME = "state.json"

    def __init__(self, campaign=''):
        super().__init__('dandy')
        if campaign == '':
            self.campaign = 'nergan_campaign'
        else:
            self.campaign = campaign
        if sys.platform == 'linux':
            self.platform = 'linux'
        else:
            self.platform = 'windows'
        self.parser = Parser(self.campaign, os.getcwd())
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
        self.queue = []
        self.id = []
        self.volume = 1.0
        self.playing = False
        self.channel = ''
        self.voice_channel = ''
        self.initiative = False
        self.player_object = []
        self.npc_initiative = 0
        self.current_turn = 0
        self.load_state()

        if os.path.isdir('players'):
            player_files = os.listdir('players')
            for file in player_files:
                file = file.replace('_data.json', '')
                self.player_object.append(Player(f'players/{file}'))
                self.player_object[-1].load_state()
        else:
            os.mkdir('players')
            for val, player_name in enumerate(self.players):
                state = {
                    'name': player_name,
                    'id_player': self.id[val],
                    'initiative': 0,
                    'rolled_initiative': 0
                }
                self.player_object.append(Player(f'players/{player_name}_data.json'))
                with open(f'players/{player_name}_data.json', 'w') as f:
                    json.dump(state, f)

        if self.battle:
            if self.mechanics == 'Sanity':
                self.sanity_mec = sanity(self.players)
                self.sanity_mec.load_state()
            elif self.mechanics == 'Nightmare':
                self.nightmare_mec = nightmare()
            elif self.mechanics == 'Illusions':
                self.illusion_mec = illusions(self.players, self.id)

    def set_volume(self, vol: float):
        self.volume = vol
        self.save_state()

    def add_player(self, name='', id='', ini=0):
        if id in self.id:
            return False
        if name != '':
            if name not in self.players:
                self.players.append(name)
                self.id.append(id)
                self.save_state()
                self.player_object.append(Player(f'players/{name}'))
                self.player_object[-1].name = name
                self.player_object[-1].id_player = id
                self.player_object[-1].initiative = ini
                self.player_object[-1].rolled_initiative = 0
                self.player_object[-1].save_state()
                return True
            else:
                return False

    def remove_player(self, name=''):
        if name != '':
            if name in self.players:
                ind = self.players.index(name)
                for val, obj_name in enumerate(self.player_object):
                    if name == obj_name.name:
                        os.remove(f'{obj_name.file_name}_data.json')
                        self.player_object.pop(val)
                self.players.remove(name)
                self.id.pop(ind)
                self.save_state()
                return True
            else:
                return False

    def initiative_set(self, name, val):
        for obj in self.player_object:
            if obj.name == name:
                obj.initiative = val
                obj.save_state()

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
        self.initiative = False
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

    def create_queue(self):
        self.current_turn = 0
        initiatives = []
        names = []
        for obj in self.player_object:
            if obj.name in self.players:
                initiatives.append(obj.rolled_initiative)
                names.append(obj.name)

        initiatives.append(self.npc_initiative)
        names.append(self.name_npc)

        initiatives_new, names_new = zip(*sorted(zip(initiatives, names)))
        self.queue = names_new[::-1]
        self.save_state()

        message = '**---Turns calculated---**\n'
        counter = 1
        for name in self.queue:
            message = message + f'**{counter}:** {name}\n'
            counter += 1

        message = message + '**------------------------**\n\n'
        message = message + f'You start **{self.queue[self.current_turn]}**'

        return self.queue, message

    def next_turn(self):
        self.current_turn += 1
        if self.current_turn >= len(self.queue):
            self.current_turn = 0

        self.save_state()
        with open('comments_data/turns', 'r') as fp:
            data = fp.readlines()

        message = random.choice(data).replace('\n', '') + f' **{self.queue[self.current_turn]}**'
        return message


# TODO add this for ending song https://www.youtube.com/watch?v=6FJXjJeOU6Q
# TODO add this to elven lands <url>https://www.youtube.com/watch?v=HJLaTSjnd9Q</url>
# TODO https://www.youtube.com/watch?v=PuRFNzizkXs
