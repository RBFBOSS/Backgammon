from Dice import Dice
from Player import Player


class Game:
    def __init__(self):
        dice = Dice()
        player1 = Player('Human')
        player2 = Player('AI')
