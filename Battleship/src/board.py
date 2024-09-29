# Filename: board.py
# Description: This module defines the Board class for a Battleship game. It manages the game board, placing ships, handling attacks, and checking if all ships are sunk.
# Inputs: A ship object to place on the board, and coordinates for firing at the board.
# Output: The visual representation of the board, hit/miss feedback, and whether all ships are sunk.
# Other sources for the code: 
# Authors: 
# Creation Date: 

from ship import Ship  # Importing the Ship class, which represents each ship placed on the board.

class Board:
    def __init__(self):
        """
        Initializes a Board instance with a default size of 10x10, representing the Battleship game grid.
        Ships are stored in a list for placement and hit detection.
        """
        self.size = 10  # Board size is 10x10 (standard Battleship board dimensions)
        self.grid = [['~' for _ in range(self.size)] for _ in range(self.size)]  # Grid initialized with water cells ('~')
        self.ships = []  # List to store ships placed on the board

    def print_board(self):
        """
        Prints the current state of the board for one player.
        Displays row numbers (1-10) and column letters (A-J) along with the current state of each cell.
        """
        print("   " + " ".join(chr(65 + i) for i in range(self.size)))  # Print column headers (A-J)
        for i in range(self.size):
            print(f"{str(i + 1).rjust(2, ' ')} " + " ".join(self.grid[i]))  # Print row numbers (1-10) and grid contents

    def print_two_boards(self, other, name="Your"):
        """
        Prints both the current player's guess board and their own placement board side-by-side.
        Displays column headers and row numbers for both boards.
        Args:
            other: The other board to compare against (e.g., the enemy board).
            name: The name of the current player.
        """
        column_labels = " ".join(chr(65 + i) for i in range(self.size))  # Prepare column labels (A-J)
        print(f"   {name}'s Guesses".ljust(28) + f"{name}'s Placements")  # Print the title of each board
        print("   " + column_labels + "      " + column_labels)  # Print column labels for both boards

        # Print row numbers and the corresponding grid for both boards side by side
        for i in range(self.size):
            print(
                f"{str(i + 1).rjust(2, ' ')} " + " ".join(self.grid[i]),  # Current player's guess grid
                f"{str(i + 1).rjust(4, ' ')} " + " ".join(other.grid[i])   # Current player's own placement grid
            )

    def place_ship(self, ship):
        """
        Places a ship on the board if it fits within the board's bounds and does not overlap with other ships.
        Args:
            ship: An instance of the Ship class containing the ship's coordinates and size.
        Returns:
            True if the ship is placed successfully, False if placement fails due to out-of-bounds or overlap.
        """
        
        # Check if the ship fits within the board's boundaries
        if not ship.is_within_bounds(self.size):
            print("Ship cannot be placed. It exceeds the board limits.")
            return False

        # Check if the ship overlaps with any previously placed ships
        for existing_ship in self.ships:
            if ship.overlaps_with(existing_ship):
                print("Ship overlaps with another ship. Choose a different location.")
                return False

        # If valid, place the ship on the board by marking its coordinates with 'S'
        for x, y in ship.coordinates:
            self.grid[x][y] = 'S'  # 'S' represents a ship on the board
        
        self.ships.append(ship)  # Add the placed ship to the list of ships on the board
        return True  # Return True if ship placement is successful

    def receive_fire(self, x, y):
        """
        Handles an attack at the specified (x, y) coordinates on the board.
        Args:
            x: The row number where the attack is targeted.
            y: The column number where the attack is targeted.
        Returns:
            True if the attack hits a ship, False if it misses.
        """
        # Check each ship to see if the coordinates match any ship's location
        for ship in self.ships:
            if (x, y) in ship.coordinates and not ship.destroyed:
                self.grid[x][y] = 'X'  # Mark a hit with 'X'
                print(f"Ship at {x+1},{chr(y+65)} has been hit!")  # Notify player of the hit

                # If all parts of the ship have been hit, mark the ship as destroyed
                if all(self.grid[i][j] == 'X' for i, j in ship.coordinates):
                    ship.destroyed = True
                    print("Ship was sunk!")  # Notify player that the ship was sunk

                return True  # Return True to indicate a successful hit
        
        # If no ship was hit, mark the cell as a miss with 'O'
        if self.grid[x][y] == '~':
            self.grid[x][y] = 'O'  # 'O' represents a missed shot
        return False  # Return False if the attack missed

    def all_ships_sunk(self):
        """
        Checks if all the ships on the board have been sunk.
        Returns:
            True if all ships are destroyed, otherwise False.
        """
        return all(ship.destroyed for ship in self.ships)  # Check if every ship in the ships list is destroyed
