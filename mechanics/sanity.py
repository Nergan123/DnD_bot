import time
import random
import pandas as pd


class sanity:
    def __init__(self, players):
        self.players = players
        self.sanity_level = [100 for player in self.players]
        self.sanity_timers = [time.time() + 180 for player in self.players]
        self.sanity_comments = pd.read_csv('comments_data/sanity_comments.csv', delimiter=';')

    def damage(self, ind, dmg):
        self.sanity_level[ind] = self.sanity_level[ind] - dmg
        self.update_timers(ind)

    def update_timers(self, i):
        self.sanity_timers[i] = time.time() + 175*(self.sanity_level[i]/100) + 5 + random.randint(1, 5)

    def message(self, index):
        result = round(self.sanity_level[index]/10)
        sanity_comments_list = self.sanity_comments[self.sanity_comments.sanity == result]
        line = sanity_comments_list.sample()
        output = line.iloc[0]['comment']
        return output

