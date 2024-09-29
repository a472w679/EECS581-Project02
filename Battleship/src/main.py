'''
Filename: main.py 

Description:  This Python program implements a console-based Battleship game for two players

Game Overview:
Players secretly place a specified number of ships on a 10x10 grid.
Players take turns guessing the locations of their opponent's ships.
The game continues until one player successfully sinks all of the opponent's ships.
with an optional AI opponent and different difficulty levels.
Players take turns placing ships on a 10x10 board and guessing the locations 
of their opponent’s ships. The game continues until one player sinks all of the opponent’s ships.

Inputs: 
Number of ships (from 1 to 5)
Player names (for two-player mode) or AI difficulty (for AI mode)
Ship placement positions (row and column, orientation)
Attack positions (row and column)

Output: 
Display of game boards (player’s and enemy’s)
Result of each attack (hit, miss, or sunk)
End game result (win or loss)
Other sources for the code: 
ChatGPT, StackOverflow for some AI logic, and general game-loop structure inspiration

Author: 
Kemar Wilson
Yadhunath Tharakeswaran
Jawad Ahsan
Dev Patel
Sanketh Reddy
Creation Date: 
'''

from player import Player, AIDifficulties, AI_factory
from playsound import playsound

def main():
    """
    Main function for executing the Battleship game logic. It sets up players, allows for
    ship placement, and alternates turns until all ships of one player are sunk.
    """
    while True:
        num_ships = input("How many ships are you playing with? (1-5): ")
        # Check if the input is a digit and within the valid range
        if num_ships.isdigit() and 1 <= int(num_ships) <= 5:
            num_ships = int(num_ships)  # Valid input, convert to int
            break  # Exit the loop
        else:
            print("Please enter a valid number of ships (1-5).")

    # Ask the user if they want to play against an AI
    play_against_AI = input(f"Play against an AI? (y/N): ")
    play_against_AI = False if not len(play_against_AI) else \
                      play_against_AI.upper()[0] == 'Y'
    
    if play_against_AI:
        # Ask the user to choose AI difficulty
        difficulty_input = input("Choose AI difficulty (E/m/h): ")
        difficulty = {
            'E': AIDifficulties.EASY,
            'M': AIDifficulties.MEDIUM,
            'H': AIDifficulties.HARD
        }[difficulty_input.upper()[0]]

        # Initialize Player 1 and the AI player
        player1 = Player("Player", num_ships)
        player2 = AI_factory(difficulty, num_ships)
    else: 
        # Initialize Player 1 and Player 2 (human players)
        player1 = Player(input("Enter name for Player 1: "), num_ships)
        player2 = Player(input("Enter name for Player 2: "), num_ships)
    
    # Ship placement phase
    player1.place_ships()
    player2.place_ships()
    
    # Main game loop: players alternate turns making guesses
    while True:
        player1.print_boards()
        print(f"\n{player1.name}'s turn to guess:")
        player1.make_guess(player2)

        # Check if Player 1 wins by sinking all ships of Player 2
        if player2.board.all_ships_sunk():
            print(f"{player1.name} wins! All ships of {player2.name} are sunk.")
            playsound("Battleship/src/sound_files/win.mp3")
            break

        # Player 2's turn
        player2.print_boards()
        print(f"\n{player2.name}'s turn to guess:")
        player2.make_guess(player1)

        # Check if Player 2 wins by sinking all ships of Player 1
        if player1.board.all_ships_sunk():
            print(f"{player2.name} wins! All ships of {player1.name} are sunk.")
            playsound("Battleship/src/sound_files/win.mp3")
            break

# Run the main function if this script is executed
if __name__ == "__main__":
    main()
