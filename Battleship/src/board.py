from ship import Ship

class Board:
    def __init__(self):
        """
        Initializes a board with a default size of 10x10 and an empty grid. 
        Ships are stored in a list.
        """
        self.size = 10  # Board size is 10x10
        self.grid = [['~' for _ in range(self.size)] for _ in range(self.size)]  # '~' represents water (empty cell)
        self.ships = []  # List to store placed ships

    def print_board(self):
        """
        Prints the current state of the board, displaying row numbers and column letters (A-J).
        """
        print("  " + " ".join(chr(65 + i) for i in range(self.size)))  # Print column headers (A-J)
        for i in range(self.size):
            print(f"{i + 1} " + " ".join(self.grid[i]))  # Print row numbers and grid content

    def place_ship(self, ship):
        """
        Places a ship on the board if it fits within bounds and does not overlap with other ships.
        """
        
        # Check if the ship is within the board's bounds
        if not ship.is_within_bounds(self.size):
            print("Ship cannot be placed. It exceeds the board limits.")
            return False

        # Check if the ship overlaps with any existing ships
        for existing_ship in self.ships:
            if ship.overlaps_with(existing_ship):
                print("Ship overlaps with another ship. Choose a different location.")
                return False

        # Place the ship on the grid and mark it with 'S'
        for x, y in ship.coordinates:
            self.grid[x][y] = 'S'  # 'S' indicates a ship's location
        
        self.ships.append(ship)  # Add the ship to the ships list
        return True

    def receive_fire(self, x, y):
        """
        Handles a shot fired at the board by checking if it hits or misses a ship.
        """
        # Check if the shot hits a ship
        for ship in self.ships:
            if (x, y) in ship.coordinates and not ship.destroyed:
                self.grid[x][y] = 'X'  # Mark a hit with 'X'
                print(f"Ship at {x+1},{chr(y+65)} has been hit!")  # Inform the player

                if all(self.grid[i][j] == 'X' for i, j in ship.coordinates):
                    ship.destroyed = True  # Mark the ship as destroyed
                    print("Ship was sunk!")

                return True
        
        # If no ship is hit, mark it as a miss with 'O'
        if self.grid[x][y] == '~':
            self.grid[x][y] = 'O'  # 'O' indicates a miss
        return False

    def all_ships_sunk(self):
        """
        Checks if all ships on the board have been sunk.
        """
        return all(ship.destroyed for ship in self.ships)  # Returns True if all ships are destroyed

