import os
import random


class nightmare:
    def __init__(self, players, channel_id):
        self.players = players
        self.channel_id = channel_id
        pics = os.listdir('comments_data/nightmare_pics')
        self.files = pics
        self.urls = []
        with open('comments_data/nightmare_music_links') as f:
            for line in f:
                line = line.replace("\n", "")
                self.urls.append(line)

    def get_image(self):
        return random.choice(self.files)

    def get_url(self):
        return random.choice(self.urls)
