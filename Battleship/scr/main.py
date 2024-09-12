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
