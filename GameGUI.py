from PIL import Image, ImageTk
import tkinter as tk


class GameGUI:
    def __init__(self, root_input, game):
        self.available_moves = None
        self.dice_images = []
        self.dice_labels = []
        self.player2_label = None
        self.player1_label = None
        self.roll_button = None
        self.canvas = None
        self.root = root_input
        self.root.title("Backgammon Game")
        self.game = game
        first_player = game.pick_starting_player()
        self.create_widgets()
        self.current_player = first_player
        print(f"Player {first_player} starts the game")

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
        print(f"Clicked at x={event.x}, y={event.y}")
        if 300 < event.x < 350 and 550 < event.y < 570:
            self.roll_dice()
            return
        triangle_clicked = -1
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
        if triangle_clicked == -1:
            return
        self.available_moves = self.game.for_position_display_available_moves(self.current_player,
                                                                         triangle_clicked,
                                                                         self.game.dice.values)
        if self.available_moves:
            self.update_table()

    def roll_dice(self):
        print("Rolling dice")
        self.game.dice.roll_dice()
        self.update_table()

    def update_table(self):
        self.canvas.delete("all")
        self.draw_delimiter_rectangle()
        self.draw_triangles()
        self.draw_delimiter_line()
        self.draw_pieces()
        if self.available_moves:
            self.draw_available_moves(self.available_moves)
        self.draw_dice()

    def draw_dice(self):
        dice_values = self.game.dice.values
        x = 460
        y = 260
        self.dice_images = []  # Clear previous images
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
            color1 = "saddle brown" if i % 2 == 0 else "burlywood2"
            color2 = "burlywood2" if i % 2 == 0 else "saddle brown"
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

    def draw_available_moves(self, available_moves):
        positions = self.game.table.positions
        for move in available_moves:
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

