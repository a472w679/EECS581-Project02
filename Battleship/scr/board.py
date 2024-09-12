"""
Authors:
Kemar Wilson
Yadhunath Tharakeswaran
Jawad Ahsan
Dev Patel
Sanketh Reddy

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

    def all_ships_sunk(self):
    # Check if all parts of all ships have been hit
        for ship in self.ships:
            x, y = ship['position']
            orientation = ship['orientation']
            for i in range(ship['size']):
                if orientation == 'H' and self.grid[x][y + i] != 'X':
                    return False
                elif orientation == 'V' and self.grid[x + i][y] != 'X':
                    return False
        return True


