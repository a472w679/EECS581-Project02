from ship import Ship

class Board:
    def __init__(self):
        self.size = 10
        self.grid = [['~' for _ in range(self.size)] for _ in range(self.size)]
        self.ships = []

    def print_board(self):
        """Prints the board grid for the player to view."""
        print("  " + " ".join(chr(65 + i) for i in range(self.size)))  # A-J
        for i in range(self.size):
            print(f"{i + 1} " + " ".join(self.grid[i]))

    def place_ship(self, ship):
        """Places the ship on the board if it passes bounds and overlap checks."""
        if not ship.is_within_bounds(self.size):
            print("Ship cannot be placed. It exceeds the board limits.")
            return False

        for existing_ship in self.ships:
            if ship.overlaps_with(existing_ship):
                print("Ship overlaps with another ship. Choose a different location.")
                return False

        # Place the ship if all checks pass
        for x, y in ship.coordinates:
            self.grid[x][y] = 'S'
        
        self.ships.append(ship)
        return True

    def receive_fire(self, x, y):
        """Handles the result of a guess (hit or miss)."""
        for ship in self.ships:
            if (x, y) in ship.coordinates and not ship.destroyed:
                self.grid[x][y] = 'X'  # Hit
                ship.destroyed = True  # Mark the ship as destroyed
                print(f"Ship at {x+1},{chr(y+65)} has been destroyed!")
                return True
        if self.grid[x][y] == '~':
            self.grid[x][y] = 'O'  # Miss
        return False

    def all_ships_sunk(self):
        """Checks if all ships on the board have been sunk."""
        return all(ship.destroyed for ship in self.ships)
