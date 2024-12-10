import random


class Dice:
    """
    A class to represent the dice used in the Backgammon game.

    Attributes
    ----------
    values : list
        The list of dice values.

    Methods
    -------
    __init__(self):
        Initializes the dice with default values.
    roll_dice(self):
        Rolls the dice and updates the values.
    """

    def __init__(self):
        """
                Initializes the dice with default values.
        """
        self.values = [0, 0]

    def roll_dice(self):
        """
                Rolls the dice and updates the values.
        """
        self.values[0] = random.randint(1, 6)
        self.values[1] = random.randint(1, 6)
