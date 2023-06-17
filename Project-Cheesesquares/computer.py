import time

import pygame
import basescreen
import grid
import player

class Computer(player.Player):
    """
    is a type of Player
    that automatically makes
    the best move possible
    """
    
    def __init__(self):
        """
        creates a Player(Computer) which
        makes always the best possible move
        """
        super().__init__(name = "SmartQuang", color = (123, 234, 134))
            
        
    def turn(self, grid: grid.Grid)-> pygame.Vector2:
        """
        runs the turn for this Computer Player
        :return: position of the move (of the best edge)
        """
        
        pos = basescreen.listen()
        time.sleep(0.5)
        return self.evaluate_grid(grid.copy())
    

    def evaluate_grid(self, grid: grid.Grid)-> pygame.Vector2:
        """
        evaluates the playsituation of a Grid
        :param grid: Grid to be evaluated
        :return: position to place
        """
        options: list[int] = []
        options_position: list[pygame.Vector2] = [] 
        for x in range(grid.width + 1):
            for y in range(grid.height*2 + 1):
                g = grid.copy()
                try:
                    g.place(self, pygame.Vector2(x, y))
                    options.append(self.grid_sum(g))
                    options_position.append(pygame.Vector2(x, y))
                except IndexError: pass
                except EOFError: pass

        print(options_position, options)
        if len(options_position) == 1: return options_position[0]
        return options_position[options.index(max(options))]
                        




    def grid_sum(self, grid: grid.Grid):
        gridWeightSum = 0
        for row in range(grid.height):
            for square in grid.grid[row]:
                gridWeightSum += square.weight(self)
        return gridWeightSum
                    


    
                        

        