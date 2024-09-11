"""
This Python program implements a console-based version of the classic Battleship game for two players.

Game Overview:
- Players secretly place a specified number of ships on a 10x10 grid.
- Players take turns guessing the locations of their opponent's ships.
- The game continues until one player successfully sinks all of the opponent's ships.

Key Components:
1. Board Class:
   - Represents the game board for each player, managing ship placement, firing at positions, and checking for sunk ships.
   - Contains methods to print the board, place ships, receive fire from guesses, and check if any ships have been sunk.

2. Player Class:
   - Represents a player in the game, including their name, game board, and tracking of guesses.
   - Includes methods for placing ships on their board and making guesses against the opponent's board, with input validation to enhance user experience.

3. Main Function:
   - Initializes two players and prompts them to enter their names.
   - Facilitates the ship placement phase for both players, ensuring valid input.
   - Implements the main game loop where players alternate turns making guesses until one player's ships are completely sunk.

Error Checking Enhancements:
- The program includes input validation to ensure that users enter positions and orientations correctly, reducing the likelihood of errors during gameplay.
- Clear feedback is provided to users for incorrect inputs, enhancing overall user experience and game flow.

Usage:
- The game is played in the console, where players are prompted to input ship placements and guesses.
- The program keeps track of hits and misses, providing real-time feedback to players.

Note:
- Future improvements could include graphical interfaces and advanced error handling to further enhance the gameplay experience.
"""

import random

class Board:
    def __init__(self):
        self.size = 10
        self.grid = [['~' for _ in range(self.size)] for _ in range(self.size)]
        self.ships = []

    def print_board(self):
        print("  " + " ".join(chr(65 + i) for i in range(self.size)))  # A-J
        for i in range(self.size):
            print(f"{i + 1} " + " ".join(self.grid[i]))

    def place_ship(self, ship):
        # Simple ship placement logic (can be improved)
        x, y = ship['position']
        orientation = ship['orientation']
        
        if orientation == 'H':
            for i in range(ship['size']):
                self.grid[x][y + i] = 'S'
        else:  # Vertical
            for i in range(ship['size']):
                self.grid[x + i][y] = 'S'
        
        self.ships.append(ship)

    def receive_fire(self, x, y):
        if self.grid[x][y] == 'S':
            self.grid[x][y] = 'X'  # Hit
            return True
        else:
            self.grid[x][y] = 'O'  # Miss
            return False

    def check_sunk_ships(self):
        sunk_ships = []
        for ship in self.ships:
            x, y = ship['position']
            orientation = ship['orientation']
            sunk = True
            for i in range(ship['size']):
                if orientation == 'H' and self.grid[x][y + i] != 'X':
                    sunk = False
                elif orientation == 'V' and self.grid[x + i][y] != 'X':
                    sunk = False
            if sunk:
                sunk_ships.append(ship)
        return sunk_ships

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

                # Check if the ship can be placed
                if orientation == 'H' and (y + size > self.board.size):
                    print("Ship cannot be placed horizontally. It exceeds the board limits.")
                    continue
                if orientation == 'V' and (x + size > self.board.size):
                    print("Ship cannot be placed vertically. It exceeds the board limits.")
                    continue

                # Place the ship if all checks are passed
                ship = {'size': size, 'position': (x, y), 'orientation': orientation}
                self.board.place_ship(ship)
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

def main():
    player1 = Player(input("Enter name for Player 1: "))
    player2 = Player(input("Enter name for Player 2: "))
    
    player1.place_ships()
    player2.place_ships()
    
    while True:
        player1.make_guess(player2)
        player2.make_guess(player1)

        # Check for sunk ships
        sunk_ships_player2 = player1.guesses.check_sunk_ships()
        sunk_ships_player1 = player2.guesses.check_sunk_ships()

        if sunk_ships_player2:
            print(f"{player1.name} wins! All ships of {player2.name} are sunk.")
            break
        if sunk_ships_player1:
            print(f"{player2.name} wins! All ships of {player1.name} are sunk.")
            break

if __name__ == "__main__":
    main()
