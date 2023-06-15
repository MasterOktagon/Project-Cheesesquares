import pygame

import ui

font = pygame.font.SysFont("Arial", 20)

class PlayerActive(ui.UI):
    """
    A UI part showing the active Player
    """
    def __init__(self, player):
        super().__init__(ui.TOPRIGHT)

        self.player = player
        self.surface = pygame.Surface((400, 30))
        self.surface.fill(player.color)
        self.surface.blit(ui.nfont.render(player.name, False, pygame.Color(255, 255, 255)), (10, 10))

    def update(self, player):
        if player == self.player:
            self.position.x += 30

        else:
            self.position.x = 100


class Power(ui.UI):
    def __init__(self, grids):
        super().__init__(ui.TOPLEFT)
        self.grid = grids
        self.surface = pygame.Surface((500, 30))
        self.position = pygame.Vector2(500, 0)
        self.show()

    def update(self):
        self.surface.fill((0, 0, 0))
        psum = 0
        sqsum = 0
        for p in self.grid.players:
            sq = 500/(self.grid.width*self.grid.height) * self.grid.get_square_count(p)
            sqsum += self.grid.get_square_count(p)
            pygame.draw.rect(self.surface, p.color, pygame.Rect(psum, 0, sq, 30))
            squares = self.grid.get_square_count(p)
            if squares != 0: self.surface.blit(font.render(str(squares), False, (255,255,255)),(psum + sq//2\
                            - font.size(str(squares))[0] // 2,5))
            psum += sq

        self.surface.blit(font.render(str(self.grid.width*self.grid.height-sqsum), False, (255, 255, 255)), (psum+(500-psum)//2\
                                                                                                             -font.size(str(self.grid.width*self.grid.height-sqsum))[0]//2, 5))




tut: str = """ 

Tutorial:
1. Goal of the games is it, to own more Squares than the
 other Player. The game ends if all squares have an owner.
 
2. The Player gets the owner of a square, if he gets owner
 of an edge which is the last not owned edge of a square.
 
3. In every turn the Player needs to marks a edge he
 wants to own. The edge is only available if it's
  connected to a neutral or an already self owned edge
  
4. All outer edges all neutral an are counted as already 
owned. 
"""  # Tutorial

class Tutorial(ui.NPatch):
    def __init__(self):
        super().__init__(pygame.rect.Rect(30, 30, 400, 600), "assets/ui/npatch.png")
        self.show()
        self.setlines(tut,pygame.Color(255, 255, 255))
