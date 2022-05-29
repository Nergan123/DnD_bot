import os
import random
import boto3
import json


class nightmare:
    def __init__(self):
        pics = os.listdir('comments_data/nightmare_pics')
        self.files = pics
        self.played = []
        self.shown = []
        self.urls = []
        with open('comments_data/nightmare_music_links') as f:
            for line in f:
                line = line.replace("\n", "")
                self.urls.append(line)

    def get_image(self):
        x = random.choice(self.files)
        while x in self.shown:
            x = random.choice(self.files)
        self.shown.append(x)
        if len(self.shown) == len(self.files):
            self.shown = []
        return x

    def get_url(self):
        x = random.choice(self.urls)
        while x in self.played:
            x = random.choice(self.urls)
        self.played.append(x)
        if len(self.played) == len(self.urls):
            self.played = []
        return x

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
