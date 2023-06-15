import pygame
import basescreen


class Player:
    """
    Class for the Player
    who can play the Game
    """
    
    def __init__(self, name: str, color: tuple):
        """
        creates a new Player
        
        :param name: name of the Player
        """
        self.name: str = name
        self.color: pygame.Color = pygame.Color(color[0], color[1], color[2])

    def __repr__(self):
        return self.name


    def turn(self, _grid) -> pygame.Vector2:
        """
        runs the turn for this Player,
        taking the input
        """
        pos = basescreen.listen()
        while pos is None:
            pos = basescreen.listen()
        
        return pos
    
    
if __name__ == "__main__":
    p = Player("maxi", (255, 212, 123))