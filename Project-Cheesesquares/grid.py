import pygame
import player
from square import *

class Grid:
    """
    Class for the Grid
    (Board of play) contains
    a lot of the game logic
    """
    def __init__(self, w: int, h: int, players: list[player.Player]) -> None:
        """
        creates a new Grid
        :param w: width of the Grid (int, max 20)
        :param h: height of the Grid (int, max 20)
        """
        self.width = w
        self.height = h
        
        self.grid = []
        for x in range(w):
            self.grid.append([])
            for y in range(h):
                self.grid[x].append(Square())

        self.active_player = 0
        self.players = players
        self.neutral = player.Player("neutralman", (128, 128, 128))

        self.set_neutral()


        
    def winner(self) -> None|player.Player:
        """
        returns the winning Player or None(no winner yet)
        """
    
        playersquares: list[int] = []
        for i in range(len(self.players)):
            playersquares.append(0)

        for Row in self.grid:
            for Square in Row:
                if Square.get_owner() is None:
                    return None
                else:
                    playersquares[self.players.index(Square.get_owner())] += 1
        return self.players[playersquares.index(max(playersquares))]


    def next_turn(self, _rek_level=0) -> None:
        """
        runs the turn of the next Player
        """
        print(self.players[self.active_player])
        try: self.place(self.players[self.active_player], self.players[self.active_player].turn(self))
        except IndexError:
            print("Invalid Move")
            self.next_turn(_rek_level+1)
        except EOFError:
            print("Already Placed")
            self.next_turn(_rek_level+1)


        if _rek_level == 0:
            self.active_player += 1
            if self.active_player > len(self.players)-1:
                self.active_player = 0


    def get_square_count(self, owner: player.Player) -> int:
        """
        returns the amount of owned squares

        :param owner: Player to count the squares of
        """
        square_amount = 0
        for row in self.grid:
            for Square in row:
                if Square.get_owner() == owner:
                    square_amount += 1

        return square_amount
                
    def in_bounds(self, pos: pygame.Vector2) -> bool:
        """
        checks if a chosen position is inside the Grid
        
        :param pos: position to use
        """
        if pos.y % 2 == 0:
            return 0 <= pos.x <= self.width and 0 < pos.y <= self.height * 2 + 1
        else:
            return 0 <= pos.x <= self.width-1 and 0 < pos.y <= self.height * 2 + 1

    def tryget(self, x: int, y: int, direction: str, do):
        """
        tries to get a grid square
        :param x: x coord
        :param y: y coord
        :param direction: which direction, leave empty str for object
        :param do: function, what to do with it
        :return:
        """
        if direction != "":
            direction = "." + direction
        try:
            do(eval(f"self.grid[x][x]{direction}"))  # very evil way of doing this
        except IndexError:
            pass

    def check_valid(self, pos: pygame.Vector2, edge_player: player.Player) -> bool:
        """
        checks if a chosen position is valid and connected to an owned or neutral edge
        :param pos: position to check
        """
        edge_neighbors = []
        if pos.y % 2 == 0:
            try: edge_neighbors.append(self.grid[int(pos.x)][int((pos.y - 2) / 2)].north)
            except IndexError: pass
            try: edge_neighbors.append(self.grid[int(pos.x)][int((pos.y - 2) / 2)].south)
            except IndexError: pass
            try: edge_neighbors.append(self.grid[int(pos.x - 1)][int((pos.y - 2) / 2)].north)
            except IndexError: pass
            try: edge_neighbors.append(self.grid[int(pos.x - 1)][int((pos.y - 2) / 2)].south)
            except IndexError: pass
            try: edge_neighbors.append(self.grid[int(pos.x)][int((pos.y - 2) / 2 + 1)].west)
            except IndexError: pass
            try: edge_neighbors.append(self.grid[int(pos.x)][int((pos.y - 2) / 2 - 1)].west)
            except IndexError: pass

        else:
            try: edge_neighbors.append(self.grid[int(pos.x + 1)][int((pos.y-2) / 2)].south)
            except IndexError: pass
            try: edge_neighbors.append(self.grid[int(pos.x - 1)][int((pos.y-2) / 2)].south)
            except IndexError: pass
            try: edge_neighbors.append(self.grid[int(pos.x)][int((pos.y-2) / 2)].east)
            except IndexError: pass
            try: edge_neighbors.append(self.grid[int(pos.x)][int((pos.y-2) / 2)].west)
            except IndexError: pass
            try: edge_neighbors.append(self.grid[int(pos.x)][int(((pos.y-1) / 2))].west)
            except IndexError: pass
            try: edge_neighbors.append(self.grid[int(pos.x)][int(((pos.y-1) / 2))].east)
            except IndexError: pass
        return (edge_player in edge_neighbors) or (self.neutral in edge_neighbors)

    def place(self, player: player.Player, pos: pygame.Vector2, admin: bool=False) -> None:
        """
        marks a Grid edge, errors if impossible
        
        :param player: active player
        :param position: valid position inside the Grid
        """
        pos.y += 2
        print(pos)
        if admin or (self.in_bounds(pos) and self.check_valid(pos, player)):
            if pos.y % 2 == 0:
                try: a = bool(self.grid[int(pos.x)][int((pos.y-2)/2)].west is None)
                except IndexError: a = bool(self.grid[int(pos.x)-1][int((pos.y-2)/2)].east is None)
                if a or admin:
                    try:
                        self.grid[int(pos.x)][int((pos.y-2)/2)].west = player
                        if self.grid[int(pos.x)][int((pos.y-2)/2)].count_edges() == 4 and not admin and self.grid[int(pos.x)][int((pos.y - 2) / 2)].owner is None:
                            self.grid[int(pos.x)][int((pos.y-2)/2)].owner = player
                    except IndexError: pass
                    if pos.x != 0:
                        try:
                            self.grid[int(pos.x)-1][int((pos.y-2)/2)].east = player
                            if self.grid[int(pos.x)-1][int((pos.y - 2) / 2)].count_edges() == 4 and not admin and self.grid[int(pos.x)-1][int((pos.y - 2) / 2)].owner is None:
                                self.grid[int(pos.x)-1][int((pos.y - 2) / 2)].owner = player
                        except IndexError: pass
                    return
                else:
                    raise EOFError
            else:
                try: a = bool(self.grid[int(pos.x)][int((pos.y) / 2)].north is None)
                except IndexError: a = bool(self.grid[int(pos.x - 1)][int((pos.y) / 2)-1].south is None)
                if a or admin:
                    try:
                        self.grid[int(pos.x)][int((pos.y)/2)-1].south = player
                        if not admin and self.grid[int(pos.x)][int((pos.y-2)/2)].count_edges() == 4:
                            self.grid[int(pos.x)][int((pos.y-2)/2)].owner = player
                    except IndexError: pass
                    try:
                        if pos.y != self.height * 2 + 1:
                            self.grid[int(pos.x)][int((pos.y)/2)].north = player

                        if not admin and self.grid[int(pos.x)][int((pos.y - 2) / 2)+1].count_edges() == 4:
                            self.grid[int(pos.x)][int((pos.y - 2) / 2)+1].owner = player
                    except IndexError: pass
                    return
                else:
                    raise EOFError

        else: raise IndexError
            
    def copy(self):
        """
        copies this Grid object
        """
        g = type(self)(1, 1, self.players)
        g.players = self.players
        g.neutral = self.neutral
        g.active_player = self.active_player
        g.width = self.width
        g.height = self.height
        g.grid = []
        for x in range(self.width):
            g.grid.append([])
            for y in range(self.height):
                g.grid[x].append(self.grid[x][y].copy())
        return g

    def set_neutral(self):
        """
        sets the outest edges to neutral
        """
        for x in range(self.width + 1):
            for y in range(self.height * 2 + 1):
                pass
                if (x == 0 and y % 2 == 1) or y == 0 or y == self.height * 2 + 1 or (x == self.width and y % 2 == 1):
                    self.place(self.neutral, pygame.Vector2(x, y - 3), True)



