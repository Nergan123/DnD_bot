import random
import pandas as pd


class Dandy_bot:
    def __init__(self):
        self.location = ''
        self.rolls = []

    def roll(self, number_of_dice, number_of_sides):
        output = ''

        for throw in range(number_of_dice):
            output = output + ' ' + str(random.choice(range(1, number_of_sides+1)))

        return output
