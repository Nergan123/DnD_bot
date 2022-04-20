import random
import pandas as pd


class Dandy_bot:
    def __init__(self):
        self.location = ''
        self.rolls = []
        self.dice_comments = pd.read_csv('comments_data/dice_comments.csv', delimiter=';')

    def roll(self, number_of_dice, number_of_sides, user=''):
        output = ''
        if number_of_dice == 1 and number_of_sides == 20:
            roll = random.choice(range(1, number_of_sides+1))
            output = output + ' ' + str(roll)
            throw_list = self.dice_comments[self.dice_comments.dice == roll]
            line = throw_list.sample()
            self.rolls.append(roll)
            output = line.iloc[0]['comment'] + '**' + f' {user} rolls ' + str(roll) + '**'
        else:
            for throw in range(number_of_dice):
                roll = random.choice(range(1, number_of_sides+1))
                output = output + ' ' + str(roll)
                self.rolls.append(roll)
            output = '**' + f'{user} rolls ' + output + '**'

        return output
