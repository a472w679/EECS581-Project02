"""This class contains the parameters for the ship that is to be placed by the user.
    It determines the size of each ship depending on the number of ships the user places on the grid.
    If the user would like to place 5 ships then it would ask the user to place each ships of the following demension, according to the mentioned orentation.
    1st boat = 1x1, 2nd boat = 1x2, 3rd boat = 1x3, 4th boat = 1x4, 5 th boat = 1x5.
    
    The class also makes sure the following:
    - It doesn't allow any of the factors such as dimension or orientation that would cause it go beyond the bound.
    - It also makes sure that the ships of the same player doesn't overlap each other.
    
    """
class Ship:
    def __init__(self, size, position, orientation):
        self.size = size  #tracks size
        self.position = position #tracks the position on the grid
        self.orientation = orientation #tracks the orientation such as horizontal or vertical.
        self.coordinates = self.get_coordinates() #this will ensure cordinates the a ship is allowed to be placed on.
        self.destroyed = False  # Flag to track if the ship is destroyed

    def get_coordinates(self):
        """Generate all coordinates that this ship will cover."""
        x, y = self.position
        coordinates = []
        #Detemines the valid positions for the horizontal co-ordinates.
        if self.orientation == 'H':
            coordinates = [(x, y + i) for i in range(self.size)]
        #Detemines the valid positions for the vertical co-ordinates.
        else:  
            coordinates = [(x + i, y) for i in range(self.size)]
        return coordinates

    def is_within_bounds(self, board_size):
        """Check if the ship is within board boundaries."""
        #Takes the column name "A-J" and row number "1-10" and makes sure that they are within the bound.
        for x, y in self.coordinates:
            if x < 0 or x >= board_size or y < 0 or y >= board_size:
                return False
        return True

    def overlaps_with(self, other_ship):
        """Check if this ship overlaps with another ship."""
        #Boolean function, that returns true if it overlaps, else returns False.
        for coord in self.coordinates:
            if coord in other_ship.coordinates:
                return True
        return False

"""Imperfections with this code.

    1. if a 1X2 ship is to be placed vertically on C3, there are 2 posibilities:
        a. B3 and C3
        b. C3 and D3
        But this function only covers C3 and D3 as it takes C3 to be the starting point and only moves forward and not backwards.
        This it the same case with horizontal placements of the ships as well.
        
        This cause placing ships with longer dimensions on the corner co-ordinates for the grid."""