"""
Name: ship.py

Description: This class contains the parameters for the ship that is to be placed by the user.
It determines the size of each ship depending on the number of ships the user places on the grid.
If the user would like to place 5 ships, then it would ask the user to place each ship of the following dimensions, according to the mentioned orientation:
1st boat = 1x1, 2nd boat = 1x2, 3rd boat = 1x3, 4th boat = 1x4, 5th boat = 1x5.

The class also ensures:
- It doesn't allow any dimensions or orientations that would cause it to go beyond the bounds.
- It makes sure that ships of the same player don't overlap each other.

Inputs: Size, position, and orientation of the ship.

Output: Coordinates for ship placement and overlap checking.

Other sources: None

Authors: Kemar Wilson, Yadhunath Tharakeswaran, Jawad Ahsan, Dev Patel, Sanketh Reddy

Creation date: 
"""

class Ship:
    def __init__(self, size, position, orientation):
        """
        Initializes a new ship with a specified size, position, and orientation.

        Parameters:
        size: The size of the ship (length).
        position: The starting coordinates (row, column) for the ship.
        orientation: The orientation of the ship ('H' for horizontal, 'V' for vertical).
        """
        self.size = size  # Tracks size of the ship
        self.position = position  # Tracks the position on the grid (starting point)
        self.orientation = orientation  # Tracks the orientation ('H' or 'V')
        self.coordinates = self.get_coordinates()  # Gets the coordinates for the ship's placement
        self.destroyed = False  # Flag to track if the ship is destroyed

    def get_coordinates(self):
        """
        Generate all coordinates that this ship will cover based on its orientation.

        Returns:
        list: A list of tuples representing the coordinates covered by the ship.
        """
        x, y = self.position  # Unpack starting position
        coordinates = []  # Initialize an empty list to store coordinates

        # Determines the valid positions for horizontal placement.
        if self.orientation == 'H':
            coordinates = [(x, y + i) for i in range(self.size)]  # Horizontal coordinates
        # Determines the valid positions for vertical placement.
        else:
            coordinates = [(x + i, y) for i in range(self.size)]  # Vertical coordinates
            
        return coordinates  # Return the calculated coordinates

    def is_within_bounds(self, board_size):
        """
        Check if the ship is within the boundaries of the board.

        Parameters:
        board_size (int): The size of the board (usually 10 for a 10x10 grid).

        Returns:
        bool: True if all coordinates are within bounds, False otherwise.
        """
        # Check each coordinate to ensure it's within the board limits
        for x, y in self.coordinates:
            if x < 0 or x >= board_size or y < 0 or y >= board_size:
                return False  # Out of bounds
        return True  # All coordinates are valid

    def overlaps_with(self, other_ship):
        """
        Check if this ship overlaps with another ship.

        Parameters:
        other_ship (Ship): Another Ship object to check overlap against.

        Returns:
        bool: True if there is an overlap, False otherwise.
        """
        # Check for any common coordinates between this ship and the other ship
        for coord in self.coordinates:
            if coord in other_ship.coordinates:
                return True  # Overlap detected
        return False  # No overlap

"""
Imperfections with this code.

1. If a 1x2 ship is to be placed vertically on C3, there are 2 possibilities:
    a. B3 and C3
    b. C3 and D3
But this function only covers C3 and D3 as it takes C3 to be the starting point and only moves forward and not backward.
This is the same case with horizontal placements of the ships as well.

This causes placing ships with longer dimensions on the corner coordinates for the grid.
"""
