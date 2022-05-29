import time
import random
import pandas as pd
import boto3
import json


class sanity:
    SERIALIZABLE_FIELDS = [
        'sanity_level',
        'sanity_timers'
    ]
    STATE_BUCKET = "nergan-bot"
    STATE_REMOTE_FILE_NAME = "state_sanity.json"

    def __init__(self, players):
        self.players = players
        self.sanity_level = [100 for player in self.players]
        self.sanity_timers = [time.time() + 180 for player in self.players]
        self.sanity_comments = pd.read_csv('comments_data/sanity_comments.csv', delimiter=';')

    def damage(self, ind, dmg):
        self.sanity_level[ind] = self.sanity_level[ind] - dmg
        self.update_timers(ind)

    def heal(self, ind, val):
        self.sanity_level[ind] = self.sanity_level[ind] + val
        self.update_timers(ind)

    def update_timers(self, i):
        self.sanity_timers[i] = time.time() + 175*(self.sanity_level[i]/100) + 5 + random.randint(1, 5)
        self.save_state()

    def message(self, index):
        result = round(self.sanity_level[index]/10)
        sanity_comments_list = self.sanity_comments[self.sanity_comments.sanity == result]
        line = sanity_comments_list.sample()
        output = line.iloc[0]['comment']
        return output

    def get_sanity(self):
        output = ''
        for i, player in enumerate(self.players):
            output = output + player + "'s sanity level" + ': ' + str(self.sanity_level[i]) + '%\n'

        return output

    def save_state(self):
        state = {}
        for property_name in self.SERIALIZABLE_FIELDS:
            state[property_name] = self.__getattribute__(property_name)

        s3 = boto3.resource('s3')
        remote_object = s3.Object(self.STATE_BUCKET, self.STATE_REMOTE_FILE_NAME)
        remote_object.put(Body=(bytes(json.dumps(state).encode('UTF-8'))))

    def load_state(self):
        s3 = boto3.client('s3')
        s3_response = s3.get_object(Bucket=self.STATE_BUCKET, Key=self.STATE_REMOTE_FILE_NAME)
        state_json = s3_response['Body'].read()
        state = json.loads(state_json)
        print(state)
        for property_name in self.SERIALIZABLE_FIELDS:
            self.__setattr__(property_name, state[property_name])
