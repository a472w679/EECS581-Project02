from board import Board
from ship import Ship

class Player:
    def __init__(self, name):
        self.name = name
        self.board = Board()
        self.guesses = Board()

    def place_ships(self):
        num_ships = int(input(f"{self.name}, enter the number of ships (1-5): "))
        
        while num_ships < 1 or num_ships > 5:
            print("Please enter a valid number of ships (1-5).")
            num_ships = int(input(f"{self.name}, enter the number of ships (1-5): "))

        for size in range(1, num_ships + 1):
            valid_position = False
            
            while not valid_position:
                position = input(f"Place your {size}x1 ship (e.g., B3): ").upper()
                if len(position) < 2 or not position[0].isalpha() or not position[1:].isdigit():
                    print("Invalid input format. Please use the format 'LetterNumber' (e.g., B3).")
                    continue

                x = int(position[1:]) - 1
                y = ord(position[0]) - 65
                
                if x < 0 or x >= self.board.size or y < 0 or y >= self.board.size:
                    print("Position out of bounds. Please choose a valid position on the board.")
                    continue

                orientation = input("Choose orientation (H for horizontal, V for vertical): ").upper()
                if orientation not in ['H', 'V']:
                    print("Invalid orientation. Please enter 'H' for horizontal or 'V' for vertical.")
                    continue

                ship = Ship(size, (x, y), orientation)
                if self.board.place_ship(ship):
                    valid_position = True

    def make_guess(self, opponent):
        valid_guess = False
        
        while not valid_guess:
            guess = input(f"{self.name}, enter your guess (e.g., B3): ").upper()
            
            if len(guess) < 2 or not guess[0].isalpha() or not guess[1:].isdigit():
                print("Invalid input format. Please use the format 'LetterNumber' (e.g., B3).")
                continue

            x = int(guess[1:]) - 1
            y = ord(guess[0]) - 65
            
            if x < 0 or x >= self.guesses.size or y < 0 or y >= self.guesses.size:
                print("Guess out of bounds. Please choose a valid position on the board.")
                continue

            hit = opponent.board.receive_fire(x, y)
            self.guesses.grid[x][y] = 'X' if hit else 'O'
            if hit:
                print("It's a hit!")
            else:
                print("It's a miss!")
            valid_guess = True
