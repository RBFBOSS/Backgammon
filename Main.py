import sys
import tkinter as tk

from Game import Game
from GameGUIAI import GameGUIAI
from GameGUIPVP import GameGUIPVP

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1].lower() not in ['pvp', 'pvai']:
        print("Usage: python Main.py [pvp|ai]")
        sys.exit(1)

    game_mode = sys.argv[1]
    root = tk.Tk()
    game = Game(game_mode)
    if game_mode == 'pvp':
        app = GameGUIPVP(root, game)
    else:
        app = GameGUIAI(root, game)
    root.mainloop()
