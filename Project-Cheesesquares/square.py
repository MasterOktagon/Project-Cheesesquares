import player

class Square:
    """
    a Class for a Square
    with the Owner of the
    Square and each edge 
    """
    
    def __init__(self):
        """
        creates a new Square
        """
        self.north = None
        self.east = None
        self.south = None
        self.west = None
        self.owner = None
    
    def count_edges(self) -> int:
        """
        counts the amount of marked edges
        """
        return int(self.north!=None) +\
               int(self.east !=None) +\
               int(self.west !=None) +\
               int(self.south!=None)
    
    def get_owner(self) -> player.Player|None:
        """
        returns the owner of the Square
        """
        return self.owner
        
    def weight(self, player: player.Player) -> int:
        """
        returns the Computers weight of this field
        """
        w: int = 0
        if self.get_owner() == player:
            return 5
        elif self.get_owner() != None:
            return -5
        w = self.count_edges()
        if w == 3:
            return -3
        return w
    
    def copy(self):
        """
        returns a copy of this objekt
        """
        obj = type(self)()
        obj.north = self.north
        obj.east = self.east
        obj.south = self.south
        obj.west = self.west
        obj.owner = self.owner
        
        return obj
    
    
    
    
    