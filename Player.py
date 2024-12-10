
class Player:
    """
        A class to represent a player in the Backgammon game.

        Attributes
        ----------
        player_color : int
            The color of the player (1 for white, -1 for black).
        name : str
            The name of the player.
        points : int
            The points scored by the player.

        Methods
        -------
        __init__(self, player_name, player_color):
            Initializes the player with the given name and color.
    """
    def __init__(self, player_name, player_color):
        """
                Initializes the player with the given name and color.

                Parameters
                ----------
                player_name : str
                    The name of the player.
                player_color : int
                    The color of the player (1 for white, -1 for black).
        """
        self.player_color = player_color
        self.name = player_name
        self.points = 0
