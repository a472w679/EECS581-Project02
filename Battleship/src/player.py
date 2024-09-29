# Name:player.py
# Description: This module defines the Player and AI classes for a console-based Battleship game. 
# Players can place ships, make guesses, and play against AI of varying difficulties (easy, medium, hard).
# Inputs: Player names, ship placements, and guesses. AI behavior based on difficulty.
# Outputs: Results of guesses (hits/misses), board states.
# Authors: Kemar Wilson, Yadhunath Tharakeswaran, Jawad Ahsan, Dev Patel, Sanketh Reddy
# Sources: Self-authored with potential adaptations from previous projetcs or online references.
# Creation Date: 

# Import necessary classes from other modules
from board import Board  # Handles the grid and ship placements for each player
from ship import Ship    # Defines the properties and behavior of ships in the game
from enum import Enum    # Used for AI difficulty settings
from playsound import playsound  # To play sound effects for hits and misses
import os                # To interact with the file system for sound file paths
import random            # For AI to randomly choose ship placements and guesses

# python3 -m venv battleship
# source battleship/bin/activate
# pip3 install PyObjC
# pip3 install playsound

class Player:
    """
    The Player class represents a player in a battleship game. Each player has a board for placing ships and 
    another board for tracking their guesses on the opponent's ships.
    """

    def __init__(self, name, num_ships):
        """
        Initializes a new player with a given name. The player also has two boards: one for their own ships and
        one for recording their guesses on the opponent's board.

        Args:
            name (str): The player's name.
            num_ships (int): Number of ships the player can place.
        """
        self.name = name  # Name of the player
        self.board = Board()  # Board object representing the player's ship placements
        self.guesses = Board()  # Board object representing the player's guesses on the opponent's board
        self.num_ships = num_ships  # Number of ships the player is allowed to place

    def place_ships(self):
        """
        Handles the process of placing ships on the player's board. The player is prompted to input the number of ships 
        (between 1 and 5), and for each ship, the player is asked to provide the starting position and orientation 
        (horizontal or vertical). The function checks if the position is valid and places the ship on the board.
        """
        # Loop to place ships based on size
        for size in range(1, self.num_ships + 1):
            print()
            self.board.print_board()
            print()

            valid_position = False  # Flag to indicate if a valid position has been chosen
            
            # Keep asking for a valid position until the ship is successfully placed
            while not valid_position:
                position = input(self.name + f" place your {size}x1 ship (e.g., B3): ").upper()

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
                if size != 1:
                    orientation = input("Choose orientation (H for horizontal, V for vertical): ").upper()
                    if orientation not in ['H', 'V']:
                        print("Invalid orientation. Please enter 'H' for horizontal or 'V' for vertical.")
                        continue
                else: 
                    orientation = 'H'  # Single-tile ships are placed horizontally by default

                # Create a new Ship object and attempt to place it on the board
                ship = Ship(size, (x, y), orientation)
                if self.board.place_ship(ship):  # Place the ship and check if the position is valid
                    valid_position = True  # Ship placed successfully, exit the loop

    def print_boards(self):
        """
        Displays both the player's ship board and guess board.
        """
        print()
        self.guesses.print_two_boards(self.board, self.name)

    @staticmethod
    def submit_guess(self, opponent, position):
        """
        Handles the logic for submitting a guess. Determines if the guess is valid and whether it hits or misses.
        Updates the guesses board accordingly.

        Args:
            opponent (Player): The opponent's player object.
            position (tuple): The coordinates of the guessed position.

        Returns:
            bool: True if it's a hit, False if it's a miss.
        """
        x, y = position

        # Check if the guess is within the board's bounds
        if x < 0 or x >= self.board.size or \
           y < 0 or y >= self.board.size:
            return None
        
        # Ensure the guess hasn't already been made at this position
        if self.guesses.grid[x][y] != '~':
            return None
    
        # Check if the guess hits an opponent's ship
        hit = opponent.board.receive_fire(x, y)
        
        # Update the guesses board with 'X' for hit and 'O' for miss
        self.guesses.grid[x][y] = 'X' if hit else 'O'

        # Play sound effects based on the result of the guess
        cwd = str(os.getcwd())
        if hit:
            print("It's a hit!")
            playsound(f"{cwd}/Battleship/src/sound_files/hit-2.wav")
        else:
            print("It's a miss!")
            playsound(f"{cwd}/Battleship/src/sound_files/miss-2.wav")

        return hit

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

            hit = Player.submit_guess(self, opponent, (x, y))

            valid_guess = True  # Valid guess made, exit the loop


### AI Player Logic ############################################################

def get_random_position():
    """
    Generates a random (x, y) position within the 10x10 board.
    
    Returns:
        tuple: A tuple representing a random position on the board.
    """
    return tuple(int(random.random() * 10) for _ in range(2))

def add_tuples(tuple1, tuple2):
    """
    Adds two (x, y) tuples together.
    
    Args:
        tuple1 (tuple): The first tuple representing an (x, y) position.
        tuple2 (tuple): The second tuple representing an (x, y) offset.
    
    Returns:
        tuple: A new tuple representing the sum of the two positions.
    """
    return (
        tuple1[0] + tuple2[0],
        tuple1[1] + tuple2[1]
    )

class AIDifficulties(Enum):
    
    EASY   = 0  # Randomly firing AI with no strategy
    MEDIUM = 1  # AI that mimics human strategy by targeting nearby cells after a hit
    HARD   = 2  # AI that always knows where the ships are, effectively 'cheating'

def AI_factory(difficulty, num_ships):
    """
    Factory function to create an AI player of the specified difficulty.
    
    Args:
        difficulty (AIDifficulties): The difficulty level of the AI (EASY, MEDIUM, HARD).
        num_ships (int): The number of ships each AI player will control.
    
    Returns:
        AIPlayer: An instance of an AI player with the appropriate difficulty.
    """
    return [
        AIPlayerEasy(num_ships),
        AIPlayerMedium(num_ships),
        AIPlayerHard(num_ships)
    ][difficulty.value]

class AIPlayer(Player):
    """
    Base class for AI players. Defines the shared behaviors and attributes of AI players.
    
    Args:
        num_ships (int): Number of ships the AI player will place on the board.
    
    Attributes:
        board (Board): The board where the AI places its ships.
        guesses (Board): The board where the AI records its guesses on the opponent.
    """
    
    def __init__(self, num_ships):
        """
        Initializes the AI player with a board and guess board.
        """
        self.num_ships = num_ships
        self.board     = Board()
        self.guesses   = Board()

    def place_ships(self):
        """
        Places ships randomly on the board for the AI player.
        """
        for size in range(1, self.num_ships + 1):
            valid_place = False

            # Keep attempting to place the ship until a valid position is found
            while not valid_place:
                orientation = ['H', 'V'][random.getrandbits(1)]  # Randomly choose orientation
                position    = get_random_position()  # Get a random starting position

                ship = Ship(size, position, orientation)  # Create a ship object
                valid_place = self.board.place_ship(ship)  # Place the ship on the board

    def print_boards(self):
        """
        Placeholder method for printing boards, intentionally left blank for AI players.
        """
        pass

    def make_guess(self, opponent):
        """
        Abstract method for making a guess, intended to be implemented by subclasses.
        """
        raise NotImplementedError()


class AIPlayerEasy(AIPlayer):
    """
    AI player for the easy difficulty level. This AI randomly selects positions without any strategy.
    
    Attributes:
        name (str): Name of the AI player.
    """
    
    def __init__(self, num_ships):
        """
        Initializes an easy AI player with a name and a number of ships.
        """
        super().__init__(num_ships)
        self.name = "AI (EASY)"

    def make_guess(self, opponent):
        """
        Makes a random guess for the easy AI, which fires randomly on the board.
        
        Args:
            opponent (Player): The opponent player whose ships are being targeted.
        """
        valid_guess = False

        while not valid_guess:
            position = get_random_position()  # Select a random position on the board
            valid_guess = Player.submit_guess(self, opponent, position) is not None  # Ensure guess is valid


class AIPlayerMedium(AIPlayer):
    """
    AI player for the medium difficulty level. This AI uses a more sophisticated strategy by 
    targeting adjacent cells when it hits a ship, attempting to find and sink the entire ship.
    
    Attributes:
        name (str): Name of the AI player.
        initial_hit (tuple): Coordinates of the first hit on a ship.
        previous_hit (tuple): Coordinates of the last hit, used to find the direction of the ship.
        hit_direction (int): Index representing the direction (up, down, left, right) of the ship.
    """
    
    def __init__(self, num_ships):
        """
        Initializes a medium AI player with a name and strategies for targeting ships.
        """
        super().__init__(num_ships)
        self.name = "AI (MEDIUM)"
        self.initial_hit = None
        self.previous_hit = None
        self.hit_direction = None

    def clear_strategy_if_sunk(self, opponent):
        """
        Resets the targeting strategy if the ship being tracked is sunk.
        
        Args:
            opponent (Player): The opponent player whose ships are being targeted.
        """
        for ship in opponent.board.ships:
            if self.initial_hit in ship.coordinates and ship.destroyed:
                self.initial_hit = None
                self.previous_hit = None
                self.hit_direction = None
                return

    def make_guess(self, opponent):
        """
        Makes a guess for the medium AI. This AI will continue targeting adjacent cells after a hit
        to attempt to find the full ship, switching directions as necessary.
        
        Args:
            opponent (Player): The opponent player whose ships are being targeted.
        """
        STEPS = [
            (-1, 0), (0, 1),
            (1, 0), (0, -1)  # Directional steps (up, right, down, left)
        ]

        # CASE ONE: No ship is currently being targeted
        if self.initial_hit is None:
            position = None
            guess_status = None

            while guess_status is None:
                position = get_random_position()  # Select a random position
                guess_status = Player.submit_guess(self, opponent, position)  # Fire at the position

            if guess_status:
                self.initial_hit = position  # Record the first hit
                self.clear_strategy_if_sunk(opponent)  # Check if the ship is sunk
            return

        # CASE TWO: A ship has been hit, but no direction is confirmed yet
        if self.previous_hit is None:
            for direction in range(4):  # Try all four directions (up, right, down, left)
                step = STEPS[direction]
                position = self.initial_hit

                for _ in opponent.board.ships:
                    position = add_tuples(position, step)  # Probe further in the chosen direction

                    x, y = position

                    # Check another direction if probe goes off board
                    if x < 0 or x >= opponent.board.size or \
                       y < 0 or y >= opponent.board.size:
                        break

                    if self.guesses.grid[x][y] == 'X':  # Check if cell has been hit already
                        continue

                    guess_status = Player.submit_guess(self, opponent, position)

                    if guess_status is not None:
                        if guess_status:
                            self.previous_hit = position  # Record the hit
                            self.hit_direction = direction  # Record the direction
                            self.clear_strategy_if_sunk(opponent)
                        return
                    
                    break # Probe hit invalid cell

            # If no valid direction found, reset and retry
            self.initial_hit = None
            self.make_guess(opponent)
            return

        # CASE THREE: A direction has been found, continue probing in that direction
        step = STEPS[self.hit_direction]
        position = self.previous_hit

        for _ in opponent.board.ships:
            position = add_tuples(position, step)  # Move in the confirmed direction            
            x, y = position

            # Check another direction if probe goes off board
            if x < 0 or x >= opponent.board.size or \
               y < 0 or y >= opponent.board.size:
                break

            # Check if probe is a known miss
            if self.guesses.grid[x][y] == 'O':
                break

            guess_status = Player.submit_guess(self, opponent, position)
            if guess_status is not None:
                if guess_status:
                    self.previous_hit = position  # Continue in the same direction
                    self.clear_strategy_if_sunk(opponent)
                else:
                    # If a miss occurs, reset and stop targeting in this direction
                    self.previous_hit = None
                    self.hit_direction = None
                return
        
        # If the direction goes off the board, reset and retry
        self.previous_hit  = None
        self.hit_direction = None
        self.make_guess(opponent)


class AIPlayerHard(AIPlayer):
    """
    AI player for the hard difficulty level. This AI 'cheats' by directly targeting the
    opponent's ships based on their known locations on the board.
    
    Attributes:
        name (str): Name of the AI player.
    """
    
    def __init__(self, num_ships):
        """
        Initializes a hard AI player that knows the opponent's ship positions.
        """
        super().__init__(num_ships)
        self.name = "AI (HARD)"

    def make_guess(self, opponent):
        """
        Makes a guess for the hard AI. This AI always targets unhit cells that contain an opponent's ship.
        
        Args:
            opponent (Player): The opponent player whose ships are being targeted.
        """
        for x in range(self.board.size):
            for y in range(self.board.size):

                is_ship = opponent.board.grid[x][y] == 'S'  # Check if there is a ship at this location
                is_hit  = self.guesses.grid[x][y] == 'X'  # Check if this position has already been hit

                if is_ship and not is_hit:
                    Player.submit_guess(self, opponent, (x, y))  # Directly hit the ship's position
                    return
