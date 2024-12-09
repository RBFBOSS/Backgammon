class Table:
    def __init__(self):
        self.positions = []
        for i in range(24):
            self.positions.append(0)
        self.captured_pieces = {1: 0, -1: 0}

    def prepare_table(self):
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
        print('-----------------')
        first_row = self.positions[:12]
        second_row = self.positions[12:][::-1]  # Reverse the second row

        print(first_row[:6], "|", first_row[6:])
        print(second_row[:6], "|", second_row[6:])

    def move_piece(self, player, position, steps):
        if not self.validate_move(player.player_color, position, steps):
            print("Invalid move.")
            return False
        if player.player_color == 1:
            if self.captured_pieces[1] > 0:
                self.captured_pieces[1] -= 1
                if self.positions[position - steps] == -1:
                    self.captured_pieces[-1] += 1
                    self.positions[position - steps] = 1
                    print('captured piece')
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
                    print('captured piece')
                else:
                    self.positions[position] -= 1
                    self.positions[position - steps] += 1
        else:
            if self.captured_pieces[-1] > 0:
                self.captured_pieces[-1] -= 1
                if self.positions[position + steps] == 1:
                    self.captured_pieces[1] += 1
                    self.positions[position + steps] = -1
                    print('captured piece')
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
                    print('captured piece')
                else:
                    self.positions[position] += 1
                    self.positions[position + steps] -= 1
        return True

    def max_piece_for_player(self, player_color):
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
        print(f'Max piece for player {player_color}: {max_piece}')
        return max_piece

    def validate_move(self, player, position, steps):
        if player == 1:
            if self.captured_pieces[1] > 0:
                print(f'captured pieces for {player}')
                if position != 24:
                    return False
                if self.positions[position - steps] < -1:
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
        if player == 1:
            return all([self.positions[i] <= 0 for i in range(6, 24)])
        else:
            return all([self.positions[i] >= 0 for i in range(0, 18)])
