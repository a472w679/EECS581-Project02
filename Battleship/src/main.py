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
from player import Player

def main():
    player1 = Player(input("Enter name for Player 1: "))
    player2 = Player(input("Enter name for Player 2: "))
    
    player1.place_ships()
    player2.place_ships()
    
    while True:
        print(f"\n{player1.name}'s turn to guess:")
        player1.make_guess(player2)

        if player2.board.all_ships_sunk():
            print(f"{player1.name} wins! All ships of {player2.name} are sunk.")
            break

        # Player 2's turn
        print(f"\n{player2.name}'s turn to guess:")
        player2.make_guess(player1)

        if player1.board.all_ships_sunk():
            print(f"{player2.name} wins! All ships of {player1.name} are sunk.")
            break

if __name__ == "__main__":
    main()
