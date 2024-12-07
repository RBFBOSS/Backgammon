import tkinter as tk

from Game import Game
from GameGUI import GameGUI

root = tk.Tk()
game = Game('pvp')
app = GameGUI(root, game)
root.mainloop()
