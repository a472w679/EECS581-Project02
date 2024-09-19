# Import necessary classes from other modules
from board import Board
from ship import Ship

class Player:
    """
    The Player class represents a player in a battleship game. Each player has a board for placing ships and 
    another board for tracking their guesses on the opponent's ships.
    """

    def __init__(self, name):
        """
        Initializes a new player with a given name. The player also has two boards: one for their own ships and
        one for recording their guesses on the opponent's board.
        """
        self.name = name  # Name of the player
        self.board = Board()  # Board object representing the player's ship placements
        self.guesses = Board()  # Board object representing the player's guesses on the opponent's board

    def place_ships(self):
        """
        Handles the process of placing ships on the player's board. The player is prompted to input the number of ships 
        (between 1 and 5), and for each ship, the player is asked to provide the starting position and orientation 
        (horizontal or vertical). The function checks if the position is valid and places the ship on the board.
        """
        # Get the number of ships from the player (between 1 and 5)
        num_ships = int(input(f"{self.name}, enter the number of ships (1-5): "))
        
        # Validate the number of ships
        while num_ships < 1 or num_ships > 5:
            print("Please enter a valid number of ships (1-5).")
            num_ships = int(input(f"{self.name}, enter the number of ships (1-5): "))

        # Loop to place ships based on size
        for size in range(1, num_ships + 1):
            valid_position = False  # Flag to indicate if a valid position has been chosen
            
            # Keep asking for a valid position until the ship is successfully placed
            while not valid_position:
                position = input(f"Place your {size}x1 ship (e.g., B3): ").upper()

                # Validate the input format (must be letter followed by a number)
                if len(position) < 2 or not position[0].isalpha() or not position[1:].isdigit():
                    print("Invalid input format. Please use the format 'LetterNumber' (e.g., B3).")
                    continue

                # Convert the input into coordinates for the board
                x = int(position[1:]) - 1  # Convert number part to a 0-based index
                y = ord(position[0]) - 65  # Convert letter part to a 0-based index (A=0, B=1, etc.)
                
                # Check if the position is within the board's bounds
                if x < 0 or x >= self.board.size or y < 0 or y >= self.board.size:
                    print("Position out of bounds. Please choose a valid position on the board.")
                    continue

                # Ask for the ship's orientation (H for horizontal, V for vertical)
                orientation = input("Choose orientation (H for horizontal, V for vertical): ").upper()
                if orientation not in ['H', 'V']:
                    print("Invalid orientation. Please enter 'H' for horizontal or 'V' for vertical.")
                    continue

                # Create a new Ship object and attempt to place it on the board
                ship = Ship(size, (x, y), orientation)
                if self.board.place_ship(ship):  # Place the ship and check if the position is valid
                    valid_position = True  # Ship placed successfully, exit the loop

    def make_guess(self, opponent):
        """
        Allows the player to guess the position of the opponent's ships. The player enters a position, and it is 
        checked for validity. The result of the guess is recorded on the player's guesses board, with 'X' for a hit 
        and 'O' for a miss.
        """
        valid_guess = False  # Flag to indicate if a valid guess has been made
        
        # Keep asking for a valid guess until a valid input is provided
        while not valid_guess:
            guess = input(f"{self.name}, enter your guess (e.g., B3): ").upper()

            # Validate the input format (must be letter followed by a number)
            if len(guess) < 2 or not guess[0].isalpha() or not guess[1:].isdigit():
                print("Invalid input format. Please use the format 'LetterNumber' (e.g., B3).")
                continue

            # Convert the input into coordinates for the guess
            x = int(guess[1:]) - 1  # Convert number part to a 0-based index
            y = ord(guess[0]) - 65  # Convert letter part to a 0-based index (A=0, B=1, etc.)
            
            # Check if the guess is within the board's bounds
            if x < 0 or x >= self.guesses.size or y < 0 or y >= self.guesses.size:
                print("Guess out of bounds. Please choose a valid position on the board.")
                continue

            # Check if the guess hits an opponent's ship
            hit = opponent.board.receive_fire(x, y)
            
            # Update the guesses board with 'X' for hit and 'O' for miss
            self.guesses.grid[x][y] = 'X' if hit else 'O'
            
            # Inform the player about the result of the guess
            if hit:
                print("It's a hit!")
            else:
                print("It's a miss!")
            valid_guess = True  # Valid guess made, exit the loop
