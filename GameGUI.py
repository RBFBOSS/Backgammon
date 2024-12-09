from PIL import Image, ImageTk
import tkinter as tk


class GameGUI:
    def __init__(self, root_input, game):
        self.dice_to_do = []
        self.captured_black = None
        self.captured_white = None
        self.selected_position = None
        self.available_moves = None
        self.available_moves_shown = False
        self.dice_images = []
        self.dice_labels = []
        self.player2_label = None
        self.player1_label = None
        self.roll_button = None
        self.canvas = None
        first_player = game.pick_starting_player()
        self.current_player = first_player
        print(f"Player {first_player} starts the game")
        self.root = root_input
        self.root.title("Backgammon Game")
        self.game = game
        self.create_widgets()
        self.roll_dice()
        self.update_table()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=658, height=600)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.clicked_screen)

        self.roll_button = tk.Button(self.root, text="Roll Dice", command=self.roll_dice)
        self.roll_button.place(x=300, y=550)

        self.player1_label = tk.Label(self.root, text=f"{self.game.player1.name} (Black)", font=("Arial", 14, "bold"))
        self.player1_label.place(x=99, y=520)

        self.player2_label = tk.Label(self.root, text=f"{self.game.player2.name} (White)", font=("Arial", 14, "bold"))
        self.player2_label.place(x=422, y=520)

        self.update_table()

    def clicked_screen(self, event):
        if 300 < event.x < 350 and 550 < event.y < 570:
            self.roll_dice()
            return

        triangle_clicked = -10

        self.captured_black = self.game.table.captured_pieces[-1]
        self.captured_white = self.game.table.captured_pieces[1]

        if self.captured_black > 0 and 310 < event.x < 350 and 215 < event.y < 255:
            print("Clicked on captured black piece")
            triangle_clicked = -1
        elif self.captured_white > 0 and 310 < event.x < 350 and 255 < event.y < 295:
            print("Clicked on captured white piece")
            triangle_clicked = 24
        elif self.available_moves_shown and self.game.table.all_pieces_in_house(1) \
                and self.current_player == 2 and 310 < event.x < 350 and 215 < event.y < 255:
            print("Clicked on to check in white piece")
            triangle_clicked = -1
        elif self.available_moves_shown and self.game.table.all_pieces_in_house(-1) \
                and self.current_player == 1 and 310 < event.x < 350 and 255 < event.y < 295:
            print("Clicked on to check in black piece")
            triangle_clicked = 24
        else:
            for i in range(6):
                x1 = i * 50 + 20
                x2 = (i + 1) * 50 + 20
                if 20 < event.y < 257:
                    if x1 < event.x < x2:
                        triangle_clicked = i
                        break
                    x1 = (i + 6) * 50 + 40
                    x2 = (i + 7) * 50 + 40
                    if x1 < event.x < x2:
                        triangle_clicked = i + 6
                        break
                elif 257 < event.y < 495:
                    if x1 < event.x < x2:
                        triangle_clicked = 23 - i
                        break
                    x1 = (i + 6) * 50 + 40
                    x2 = (i + 7) * 50 + 40
                    if x1 < event.x < x2:
                        triangle_clicked = 17 - i
                        break
        print(f"Clicked on triangle {triangle_clicked}")
        if self.available_moves_shown:
            if triangle_clicked in self.available_moves:
                player = self.game.player1 if self.current_player == 1 else self.game.player2
                moves_made = self.eliminate_dice_from_dice_to_be_played(abs(triangle_clicked - self.selected_position))
                for move in moves_made:
                    print(f"Moving piece {player.player_color} from {self.selected_position} to "
                          f"{self.selected_position + move}")
                    self.game.table.move_piece(player, self.selected_position,
                                               move)
                    if player.player_color == 1:
                        self.selected_position -= move
                    else:
                        self.selected_position += move
                self.available_moves_shown = False
                self.available_moves = None
                self.update_table()
                if not self.dice_to_do:
                    self.current_player = 3 - self.current_player
                    self.roll_dice()
                return
        self.selected_position = triangle_clicked
        self.available_moves = self.game.for_position_display_available_moves(self.current_player,
                                                                              triangle_clicked,
                                                                              self.dice_to_do)
        if self.available_moves:
            self.available_moves_shown = True
            self.update_table()
        else:
            self.available_moves_shown = False
            self.update_table()

    def roll_dice(self):
        print("Rolling dice")
        self.game.dice.roll_dice()
        self.dice_to_do = self.game.dice.values.copy()
        if self.game.dice.values[0] == self.game.dice.values[1]:
            self.dice_to_do.extend(self.game.dice.values)
        self.update_table()

    def draw_current_player(self):
        if self.current_player == 1:
            self.player1_label.config(font=("Arial", 14, "bold", "underline"))
            self.player2_label.config(font=("Arial", 14))
        else:
            self.player1_label.config(font=("Arial", 14))
            self.player2_label.config(font=("Arial", 14, "bold", "underline"))

    def update_table(self):
        self.canvas.delete("all")
        self.draw_delimiter_rectangle()
        self.draw_triangles()
        self.draw_delimiter_line()
        self.draw_pieces()
        if self.available_moves:
            self.draw_available_moves(self.available_moves)
        self.draw_dice()
        self.draw_current_player()

    def draw_dice(self):
        dice_values = self.dice_to_do
        x = 460
        y = 260
        self.dice_images = []  # Clear previous images
        if len(dice_values) == 3:
            for i, value in enumerate(dice_values):
                self.load_dice_image(value)
                self.canvas.create_image(x + i * 60 - 30, y, image=self.dice_images[-1])
        elif len(dice_values) == 4:
            for i, value in enumerate(dice_values):
                self.load_dice_image(value)
                self.canvas.create_image(x + i * 60 - 60, y, image=self.dice_images[-1])
        else:
            for i, value in enumerate(dice_values):
                self.load_dice_image(value)
                self.canvas.create_image(x + i * 60, y, image=self.dice_images[-1])

    def load_dice_image(self, value):
        image_path = f'images/dice{value}.png'
        image = Image.open(image_path)
        dice_image = ImageTk.PhotoImage(image)
        self.dice_images.append(dice_image)

    def draw_delimiter_rectangle(self):
        self.canvas.create_rectangle(11, 10, 650, 505, outline="IndianRed4", width=20, fill="AntiqueWhite2")

    def draw_delimiter_line(self):
        self.canvas.create_polygon(321, 0, 340, 0, 340, 505, 321, 505, fill="IndianRed4")

    def draw_triangles(self):
        for i in range(6):
            x1 = i * 50 + 20
            y1 = 20
            x2 = (i + 1) * 50 + 20
            y2 = 195
            color1 = "saddle brown" if i % 2 == 0 else "burlywood2"
            color2 = "burlywood2" if i % 2 == 0 else "saddle brown"
            self.canvas.create_polygon(x1, y1, x2, y1, (x1 + x2) / 2, y2, fill=color1)
            self.canvas.create_line(x1, y1, x2, y1, fill="black")
            self.canvas.create_line(x1, y1, (x1 + x2) / 2, y2, fill="black")
            self.canvas.create_line(x2, y1, (x1 + x2) / 2, y2, fill="black")

            y1 = 495
            y2 = 320
            self.canvas.create_polygon(x1, y1, x2, y1, (x1 + x2) / 2, y2, fill=color2)
            self.canvas.create_line(x1, y1, x2, y1, fill="black")
            self.canvas.create_line(x1, y1, (x1 + x2) / 2, y2, fill="black")
            self.canvas.create_line(x2, y1, (x1 + x2) / 2, y2, fill="black")

        for i in range(6, 12):
            x1 = i * 50 + 40
            y1 = 20
            x2 = (i + 1) * 50 + 40
            y2 = 195
            color2 = "saddle brown" if i % 2 == 0 else "burlywood2"
            color1 = "burlywood2" if i % 2 == 0 else "saddle brown"
            self.canvas.create_polygon(x1, y1, x2, y1, (x1 + x2) / 2, y2, fill=color2)
            self.canvas.create_line(x1, y1, x2, y1, fill="black")
            self.canvas.create_line(x1, y1, (x1 + x2) / 2, y2, fill="black")
            self.canvas.create_line(x2, y1, (x1 + x2) / 2, y2, fill="black")

            y1 = 495
            y2 = 320
            self.canvas.create_polygon(x1, y1, x2, y1, (x1 + x2) / 2, y2, fill=color1)
            self.canvas.create_line(x1, y1, x2, y1, fill="black")
            self.canvas.create_line(x1, y1, (x1 + x2) / 2, y2, fill="black")
            self.canvas.create_line(x2, y1, (x1 + x2) / 2, y2, fill="black")

    def draw_pieces(self):
        positions = self.game.table.positions
        for i, pos in enumerate(positions):
            if 5 < i < 12:
                x = (i % 12) * 50 + 65
            else:
                x = (i % 12) * 50 + 45
            y = 42 if i < 12 else 473
            if i >= 12:
                if i < 18:
                    x = (11 - (i % 12)) * 50 + 65
                else:
                    x = (11 - (i % 12)) * 50 + 45
            if pos == 0:
                continue
            color = "white" if pos > 0 else "black"
            count = abs(pos)
            actual_count = 0
            if count > 5:
                actual_count = count
                count = 5
            while count > 0:
                self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color)
                if i < 12:
                    y += 40
                else:
                    y -= 40
                count -= 1
            if actual_count != 0:
                self.canvas.create_text(x, y, text=str(actual_count), fill="red", font=("Arial", 12, "bold"))

        # Draw captured pieces
        self.captured_black = self.game.table.captured_pieces[-1]
        self.captured_white = self.game.table.captured_pieces[1]
        if self.captured_black > 0:
            self.canvas.create_oval(310, 215, 350, 255, fill="black")
            self.canvas.create_text(330, 235, text=str(self.captured_black), fill="red", font=("Arial", 12, "bold"))
        if self.captured_white > 0:
            self.canvas.create_oval(310, 255, 350, 295, fill="white")
            self.canvas.create_text(330, 275, text=str(self.captured_white), fill="red", font=("Arial", 12, "bold"))

    def draw_available_moves(self, available_moves):
        positions = self.game.table.positions
        for move in available_moves:
            if move <= -1:
                x = 330
                y = 235
            elif move >= 24:
                x = 330
                y = 275
            else:
                if move < 12:
                    if move > 5:
                        x = (move % 12) * 50 + 65
                    else:
                        x = (move % 12) * 50 + 45
                    y = 42 + 40 * min(abs(positions[move]), 5)
                else:
                    if move < 18:
                        x = (11 - (move % 12)) * 50 + 65
                    else:
                        x = (11 - (move % 12)) * 50 + 45
                    y = 473 - 40 * min(abs(positions[move]), 5)
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="gray")

    def max_piece_for_player(self, player):
        player_color = 1 if player == 2 else -1
        if not self.game.table.all_pieces_in_house(player_color):
            raise Exception("All pieces are not in house")
        max_piece = 0
        if player_color == 1:
            for i in range(5):
                if self.game.table.positions[i] * player_color > 0:
                    max_piece = i
        else:
            for i in range(18, 23):
                if self.game.table.positions[i] * player_color > 0:
                    max_piece = i
                    break
        return max_piece

    def eliminate_dice_from_dice_to_be_played(self, value):
        moves_made = []
        print(f'Dice to do: {self.dice_to_do}, value: {value}, '
              f'selected position: {self.selected_position}, '
              f'max piece: {self.max_piece_for_player(self.current_player)}')
        max_piece = self.max_piece_for_player(self.current_player)
        if self.game.table.all_pieces_in_house(1):
            if self.selected_position == max_piece:
                if value <= self.dice_to_do[0]:
                    self.dice_to_do.remove(self.dice_to_do[0])
                    moves_made.append(value)
                elif value <= self.dice_to_do[1]:
                    self.dice_to_do.remove(self.dice_to_do[1])
                    moves_made.append(value)
                elif value <= self.dice_to_do[0] + self.dice_to_do[1]: # to continue from here
                    if self.current_player == 1:
                        if self.selected_position + self.dice_to_do[0] in self.available_moves:
                            moves_made.append(self.dice_to_do[0])
                            moves_made.append(self.dice_to_do[1])
                        else:
                            moves_made.append(self.dice_to_do[1])
                            moves_made.append(self.dice_to_do[0])
        if value in self.dice_to_do:
            self.dice_to_do.remove(value)
            moves_made.append(value)
            return moves_made
        if value == self.dice_to_do[0] + self.dice_to_do[1]:
            if self.current_player == 1:
                if self.selected_position + self.dice_to_do[0] in self.available_moves:
                    moves_made.append(self.dice_to_do[0])
                    moves_made.append(self.dice_to_do[1])
                else:
                    moves_made.append(self.dice_to_do[1])
                    moves_made.append(self.dice_to_do[0])
            else:
                if self.selected_position - self.dice_to_do[0] in self.available_moves:
                    moves_made.append(self.dice_to_do[0])
                    moves_made.append(self.dice_to_do[1])
                else:
                    moves_made.append(self.dice_to_do[1])
                    moves_made.append(self.dice_to_do[0])
            self.dice_to_do.remove(self.dice_to_do[1])
            self.dice_to_do.remove(self.dice_to_do[0])
            return moves_made
        if value == self.dice_to_do[0] * 3:
            moves_made.append(self.dice_to_do[0])
            moves_made.append(self.dice_to_do[0])
            moves_made.append(self.dice_to_do[0])
            self.dice_to_do = [self.dice_to_do[0]]
            return moves_made
        if value == self.dice_to_do[0] * 4:
            moves_made.append(self.dice_to_do[0])
            moves_made.append(self.dice_to_do[0])
            moves_made.append(self.dice_to_do[0])
            moves_made.append(self.dice_to_do[0])
            self.dice_to_do = []
            return moves_made
