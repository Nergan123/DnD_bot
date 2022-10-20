import os
import random


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
