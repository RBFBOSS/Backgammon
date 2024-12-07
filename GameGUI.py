import tkinter as tk

from Game import Game


class GameGUI:
    def __init__(self, root_input, game):
        self.roll_button = None
        self.canvas = None
        self.root = root_input
        self.root.title("Backgammon Game")
        self.game = game
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()

        self.roll_button = tk.Button(self.root, text="Roll Dice", command=self.roll_dice)
        self.roll_button.pack()

        self.update_table()

    def roll_dice(self):
        self.game.dice.roll_dice()
        self.update_table()

    def update_table(self):
        self.canvas.delete("all")
        self.draw_delimiter_rectangle()
        self.draw_triangles()
        self.draw_delimiter_line()
        self.draw_pieces()

    def draw_delimiter_rectangle(self):
        self.canvas.create_rectangle(11, 10, 650, 505, outline="IndianRed4", width=20, fill="AntiqueWhite2")

    def draw_delimiter_rectangle_border(self):
        self.canvas.create_rectangle(21, 20, 640, 495, outline="black", width=2)

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

