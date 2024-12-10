from Player import Player


class Table:
    """
        A class to represent the Backgammon game table.

        Attributes
        ----------
        positions : list
            The list of positions on the board, each representing the number of pieces at that position.
        captured_pieces : dict
            The dictionary of captured pieces for each player.

        Methods
        -------
        __init__(self):
            Initializes the table with the starting positions.
        prepare_table(self):
            Prepares the table with the initial setup.
        print_table(self):
            Prints the current state of the table.
        move_piece(self, player, position, steps):
            Moves a piece for the given player from the start position by the given number of steps.
        max_piece_for_player(self, player_color):
            Returns the position of the furthest piece for the given player.
        validate_move(self, player, position, steps):
            Checks if the move is valid for the given player.
        all_pieces_in_house(self, player):
            Checks if all pieces of the given player are in the home area.
    """
    def __init__(self):
        """
                Initializes the table with the starting positions.
        """
        self.positions = []
        for i in range(24):
            self.positions.append(0)
        self.captured_pieces = {1: 0, -1: 0}

    def prepare_table(self):
        """
                Prepares the table with the initial setup.
        """
        self.positions[0] = -2
        self.positions[5] = 5
        self.positions[7] = 3
        self.positions[11] = -5
        self.positions[12] = 5
        self.positions[16] = -3
        self.positions[18] = -5
        self.positions[23] = 2
        # self.positions[0] = 1
        # self.positions[1] = 1
        # self.positions[23] = -1

    def print_table(self):
        """
                Prints the current state of the table.
        """
        print('-----------------')
        first_row = self.positions[:12]
        second_row = self.positions[12:][::-1]  # Reverse the second row

        print(first_row[:6], "|", first_row[6:])
        print(second_row[:6], "|", second_row[6:])

    def move_piece(self, player, position, steps):
        """
                Moves a piece for the given player from the start position by the given number of steps.

                Parameters
                ----------
                player : Player
                    The player making the move.
                position : int
                    The starting position of the piece.
                steps : int
                    The number of steps to move the piece.

                Returns
                -------
                bool
                    True if the move is valid and performed, False otherwise.
                """
        if not self.validate_move(player.player_color, position, steps):
            print("Invalid move.")
            return False
        if player.player_color == 1:
            if self.captured_pieces[1] > 0:
                self.captured_pieces[1] -= 1
                if self.positions[position - steps] == -1:
                    self.captured_pieces[-1] += 1
                    self.positions[position - steps] = 1
                else:
                    self.positions[position - steps] += 1
            else:
                if self.all_pieces_in_house(player.player_color) and position - steps < 0:
                    player.points += 1
                    self.positions[position] -= 1
                elif self.positions[position - steps] == -1:
                    self.positions[position] -= 1
                    self.captured_pieces[-1] += 1
                    self.positions[position - steps] = 1
                else:
                    self.positions[position] -= 1
                    self.positions[position - steps] += 1
        else:
            if self.captured_pieces[-1] > 0:
                self.captured_pieces[-1] -= 1
                if self.positions[position + steps] == 1:
                    self.captured_pieces[1] += 1
                    self.positions[position + steps] = -1
                else:
                    self.positions[position + steps] -= 1
            else:
                if self.all_pieces_in_house(player.player_color) and position + steps > 23:
                    player.points += 1
                    self.positions[position] += 1
                elif self.positions[position + steps] == 1:
                    self.positions[position] += 1
                    self.captured_pieces[1] += 1
                    self.positions[position + steps] = -1
                else:
                    self.positions[position] += 1
                    self.positions[position + steps] -= 1
        return True

    def max_piece_for_player(self, player_color):
        """
                Returns the position of the furthest piece for the given player.

                Parameters
                ----------
                player_color : int
                    The color of the player (1 for white, -1 for black).

                Returns
                -------
                int
                    The position of the furthest piece.
        """
        max_piece = 0
        if player_color == 1:
            for i in range(5):
                if self.positions[i] * player_color > 0:
                    max_piece = i
        else:
            for i in range(18, 24):
                if self.positions[i] * player_color > 0:
                    max_piece = i
                    break
        return max_piece

    def validate_move(self, player, position, steps):
        """
                Checks if the move is valid for the given player.

                Parameters
                ----------
                player : int
                    The color of the player (1 for white, -1 for black).
                position : int
                    The starting position of the piece.
                steps : int
                    The number of steps to move the piece.

                Returns
                -------
                bool
                    True if the move is valid, False otherwise.
        """
        if player == 1:
            if self.captured_pieces[1] > 0:
                if position != 24:
                    return False
                if self.positions[position - steps] < -1:
                    print('too many pieces')
                    return False
            elif self.positions[position] <= 0:
                return False
            elif self.all_pieces_in_house(player):
                if position - steps == -1:
                    return True
                if position - steps < -1:
                    if self.max_piece_for_player(player) == position:
                        return True
                    return False
                if self.positions[position - steps] < -1:
                    return False
            else:
                if position - steps <= -1:
                    return False
                if self.positions[position] <= 0:
                    return False
                if self.positions[position - steps] < -1:
                    return False
        else:
            if self.captured_pieces[-1] > 0:
                if position != -1:
                    return False
                if self.positions[position + steps] > 1:
                    print('too many pieces')
                    return False
            elif self.positions[position] >= 0:
                return False
            elif self.all_pieces_in_house(player):
                if position + steps == 24:
                    return True
                if position + steps > 24:
                    if self.max_piece_for_player(player) == position:
                        return True
                    return False
                if self.positions[position + steps] > 1:
                    return False
            else:
                if position + steps >= 24:
                    return False
                if position == -1:
                    return False
                if self.positions[position + steps] > 1:
                    return False
        return True

    def all_pieces_in_house(self, player):
        """
                Checks if all pieces of the given player are in the home area.

                Parameters
                ----------
                player : int
                    The color of the player (1 for white, -1 for black).

                Returns
                -------
                bool
                    True if all pieces are in the home area, False otherwise.
        """
        if player == 1:
            return all([self.positions[i] <= 0 for i in range(6, 24)])
        else:
            return all([self.positions[i] >= 0 for i in range(0, 18)])
