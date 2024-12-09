from Dice import Dice
from Player import Player
from Table import Table


class Game:
    def __init__(self, game_mode):
        self.dice = Dice()
        if game_mode.lower() == 'pvp':
            self.player1 = Player('Player 1', -1)
            self.player2 = Player('Player 2', 1)
        else:
            self.player1 = Player('Human', -1)
            self.player2 = Player('AI', 1)
        self.table = Table()
        self.table.prepare_table()

    def pick_starting_player(self):
        self.dice.roll_dice()
        if self.dice.values[0] >= self.dice.values[1]:
            first_player = 1
        else:
            first_player = 2
        return first_player

    def game_finished(self):
        if self.player1.points == 15 or self.player2.points == 15:
            return True
        return False

    def player_turn(self, player):
        self.table.print_table()
        if player.player_color == 1:
            color = 'White'
        else:
            color = 'Black'
        print(f"{player.name}'s ({color}) turn")
        self.dice.roll_dice()
        print(f"Dice values: {self.dice.values}")
        self.make_move(player, self.dice.values)

    def for_position_display_available_moves(self, player, position, dice_values):
        available_moves = []
        player_color = -1 if player == 1 else 1
        dice1_ok = False
        dice2_ok = False
        dice3_ok = False
        dice4_ok = False
        if player_color == 1:
            if self.table.validate_move(player_color, position, dice_values[0]):
                dice1_ok = True
                available_moves.append(max(position - dice_values[0], -1))
            if len(dice_values) == 1:
                return available_moves
            if self.table.validate_move(player_color, position, dice_values[1]):
                dice2_ok = True
                available_moves.append(max(position - dice_values[1], -1))
            if (dice1_ok or dice2_ok) \
                    and self.table.validate_move(player_color, position, dice_values[0] + dice_values[1]):
                available_moves.append(max(position - dice_values[0] - dice_values[1], -1))
                dice3_ok = True
            if len(dice_values) == 2:
                return available_moves
            if dice3_ok and self.table.validate_move(player_color, position, dice_values[0] * 3):
                available_moves.append(max(position - dice_values[0] * 3, -1))
                dice4_ok = True
            if len(dice_values) == 3:
                return available_moves
            if dice4_ok and self.table.validate_move(player_color, position, dice_values[0] * 4):
                available_moves.append(max(position - dice_values[0] * 4, -1))
        else:
            if self.table.validate_move(player_color, position, dice_values[0]):
                dice1_ok = True
                available_moves.append(min(position + dice_values[0], 24))
            if len(dice_values) == 1:
                return available_moves
            if self.table.validate_move(player_color, position, dice_values[1]):
                dice2_ok = True
                available_moves.append(min(position + dice_values[1], 24))
            if (dice1_ok or dice2_ok) \
                    and self.table.validate_move(player_color, position, dice_values[0] + dice_values[1]):
                available_moves.append(min(position + dice_values[0] + dice_values[1], 24))
                dice3_ok = True
            if len(dice_values) == 2:
                return available_moves
            if dice3_ok and self.table.validate_move(player_color, position, dice_values[0] * 3):
                available_moves.append(min(position + dice_values[0] * 3, 24))
                dice4_ok = True
            if len(dice_values) == 3:
                return available_moves
            if dice4_ok and self.table.validate_move(player_color, position, dice_values[0] * 4):
                available_moves.append(min(position + dice_values[0] * 4, 24))
        print(available_moves)
        return available_moves

    def make_move(self, player, dice_values):
        if not self.player_can_move(player.player_color, dice_values):
            return
        if dice_values[0] == dice_values[1]:
            for _ in range(4):
                if self.game_finished():
                    return
                position = int(input(f"Select a position to move {dice_values[0]} steps: "))
                while not self.table.move_piece(player, position, dice_values[0]):
                    position = int(input('Invalid move. Try again: '))
                self.table.print_table()
                print(self.player1.points)
                print(self.player2.points)
        else:
            first_move = int(input("Select which die to use first (0 or 1): "))
            while first_move not in [0, 1]:
                first_move = int(input('Invalid die. Try again: '))
            moves = [dice_values[first_move], dice_values[1 - first_move]]
            for move in moves:
                if self.game_finished():
                    return
                position = int(input(f"Select a position to move {move} steps: "))
                while not self.table.move_piece(player, position, move):
                    position = int(input('Invalid move. Try again: '))
                self.table.print_table()
                print(self.player1.points)
                print(self.player2.points)

    def player_can_move(self, player_color, dice_values):
        for value in dice_values:
            for i in range(-1, 25):
                if self.table.validate_move(player_color, i, value):
                    return True
            return False
