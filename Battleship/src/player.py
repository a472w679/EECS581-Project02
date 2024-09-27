# Import necessary classes from other modules
from board import Board
from ship import Ship
from enum import Enum
from playsound import playsound
import random

#python3 -m venv battleship
#source battleship/bin/activate
#pip3 install PyObjC
#pip3 install playsound

class Player:
    """
    The Player class represents a player in a battleship game. Each player has a board for placing ships and 
    another board for tracking their guesses on the opponent's ships.
    """
    def __init__(self, name, num_ships):
        """
        Initializes a new player with a given name. The player also has two boards: one for their own ships and
        one for recording their guesses on the opponent's board.
        """
        self.name = name  # Name of the player
        self.board = Board()  # Board object representing the player's ship placements
        self.guesses = Board()  # Board object representing the player's guesses on the opponent's board
        self.num_ships = num_ships

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
                    orientation = 'H'

                # Create a new Ship object and attempt to place it on the board
                ship = Ship(size, (x, y), orientation)
                if self.board.place_ship(ship):  # Place the ship and check if the position is valid
                    valid_position = True  # Ship placed successfully, exit the loop

    def print_boards(self):
        print()
        self.guesses.print_two_boards(self.board, self.name)

    @staticmethod
    def submit_guess(self, opponent, position):
            x, y = position

            if x < 0 or x >= self.board.size or \
               y < 0 or y >= self.board.size:
                return None
            
            if self.guesses.grid[x][y] != '~':
                return None
    
            # Check if the guess hits an opponent's ship
            hit = opponent.board.receive_fire(x, y)
            
            # Update the guesses board with 'X' for hit and 'O' for miss
            self.guesses.grid[x][y] = 'X' if hit else 'O'

            # Inform the player about the result of the guess
            if hit:
                print("It's a hit!")
                playsound("Battleship/src/sound_files/hit.wav")
            else:
                print("It's a miss!")
                playsound("Battleship/src/sound_files/miss.mp3")

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
    return tuple(int(random.random() * 10) for _ in range(2))

def add_tuples(tuple1, tuple2):
    return (
        tuple1[0] + tuple2[0],
        tuple1[1] + tuple2[1]
    )

class AIDifficulties(Enum):
    EASY   = 0 # Randomly firing dummy AI
    MEDIUM = 1 # Classic human strategy
    HARD   = 2 # Cheating strategy

def AI_factory(difficulty, num_ships):
    """
    GoF Factory function for getting AI adversaries 
    of varying difficulties.
    """
    return [
        AIPlayerEasy(num_ships),
        AIPlayerMedium(num_ships),
        AIPlayerHard(num_ships)
    ][difficulty.value]

class AIPlayer(Player):
    """
    AI bandwagon stuff
    """

    def __init__(self, num_ships):
        self.num_ships = num_ships
        self.board     = Board()
        self.guesses   = Board()

    def place_ships(self):
        for size in range(1, self.num_ships + 1):
            valid_place = False

            while not valid_place:
                orientation = ['H', 'V'][random.getrandbits(1)]
                position    = get_random_position()

                ship = Ship(size, position, orientation)
                valid_place = self.board.place_ship(ship)

    def print_boards(self):
        pass

    def make_guess(self, opponent):
        raise NotImplementedError()

class AIPlayerEasy(AIPlayer):
    def __init__(self, num_ships):
        super().__init__(num_ships)
        self.name    = "AI (EASY)"

    def make_guess(self, opponent):
        valid_guess = False

        while not valid_guess:
            # This AI isn't very smart and just picks randomly.
            position    = get_random_position()
            valid_guess = Player.submit_guess(self, opponent, position) is not None

class AIPlayerMedium(AIPlayer):
    def __init__(self, num_ships):
        super().__init__(num_ships)
        self.name          = "AI (MEDIUM)"
        self.initial_hit   = None
        self.previous_hit  = None
        self.hit_direction = None

    def clear_strategy_if_sunk(self, opponent):
        for ship in opponent.board.ships:
            if self.initial_hit in ship.coordinates and ship.destroyed:
                self.initial_hit   = None
                self.previous_hit  = None
                self.hit_direction = None
                return

    def make_guess(self, opponent):
        STEPS = [
            (-1,  0), (0,  1),
            ( 1,  0), (0, -1)
        ]

        # CASE ONE
        # If there currently isn't a ship to be targeted
        if self.initial_hit is None:
            position     = None
            guess_status = None
    
            while guess_status is None:
                position     = get_random_position()
                guess_status = Player.submit_guess(self, opponent, position)
            
            if guess_status:
                self.initial_hit = position
                self.clear_strategy_if_sunk(opponent)

            return

        # CASE TWO
        # If we have a hit but not an orthogonal hit yet
        if self.previous_hit is None:
            for direction in range(4):
                step     = STEPS[direction]
                position = self.initial_hit

                # Loop for a maximum of the longest ships length
                # This way, we can probe ship cells even if they
                # are separated by successful hits from old probes.
                for _ in opponent.board.ships:
                    position = add_tuples(position, step)

                    # If probe lands on an already hit cell, then 
                    # proceed to probe deeper along the direction.
                    x, y   = position
                    is_hit = self.guesses.grid[x][y] == 'X'
                    if is_hit: continue

                    guess_status = Player.submit_guess(self, opponent, position)

                    # Hit was valid, this probe is complete.
                    if guess_status is not None:
                        if guess_status:
                            self.previous_hit  = position
                            self.hit_direction = direction
                            self.clear_strategy_if_sunk(opponent)

                        return

                    # Direction is invalid, try another one.
                    break
                
            # Failed to find a valid direction. This should
            # never happen, but if it does, fail gracefully.
            self.initial_hit = None
            self.make_guess(opponent)
            return

        # CASE THREE
        # Otherwise, we have both an initial position and
        # an previous hit, along with a strategy direction.

        step = STEPS[self.hit_direction]
        position = self.previous_hit

        for _ in opponent.board.ships:
            position = add_tuples(position, step)

            guess_status = Player.submit_guess(self, opponent, position)
            if guess_status is not None:
                if guess_status:
                    self.previous_hit = position
                    self.clear_strategy_if_sunk(opponent)
                else:
                    self.previous_hit  = None
                    self.hit_direction = None

                return

class AIPlayerHard(AIPlayer):
    def __init__(self, num_ships):
        super().__init__(num_ships)
        self.name = "AI (HARD)"
    
    def make_guess(self, opponent):
        for x in range(self.board.size):
            for y in range(self.board.size):
    
                is_ship = opponent.board.grid[x][y] == 'S'
                is_hit  = self.guesses.grid[x][y] == 'X'
        
                if is_ship and not is_hit:
                    Player.submit_guess(self, opponent, (x, y))
                    return
    