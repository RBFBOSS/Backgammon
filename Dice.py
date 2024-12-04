import random


class Dice:
    def __init__(self):
        self.values = [0, 0]

    def roll_dice(self):
        self.values[0] = random.randint(1, 6)
        self.values[1] = random.randint(1, 6)
