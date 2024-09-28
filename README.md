# EECS581-Team-5-Project-1
Team 5 Project 1 Repository for EECS581 2024 Fall \
\
Derived from team EECS581 Team 5's repository. This program is an implementation
of the game BattleShip made in Python. In the spirit of the project, design decisions
made by Team 5 such as  programming language, UI type, etc. have been retained.

## Documentation
- Check for documentation in `documentation\Documentation-Project2.pdf`

- The previous team's documentation is in Battleship/docs

## How to run it?
1) Make sure Python is installed.
2) Enter the repository's root directory.
3) Install dependencies with `pip3 install -r requirements.txt`
4) Run `python Battleship/src/main.py` \
   OR `python3 Battleship/src/main.py`


# TODO
### Fixes:
- [x] Make it so that the ship count of both player is always the same.
- [x] Fix ship sinking logic so that ships only sink when all cells are struck.
- [x] Make it so that the board is displayed during placing.
- [x] Make it so that the board is displayed after a turn.

### Features:
- [x] Add easy difficulty AI.
- [x] Add medium difficulty AI.
- [x] Add hard difficulty AI.
- [x] Add ship hit sound effect.
- [x] Add ship miss sound effect.
- [x] Add victory sound effect

### QoL:
- [x] Improve user input sanitation, especially initialization input.
- [ ] Cleanup terminal outputs to make it more aesthetically coherent.
- [ ] Color different cell types in the grid using different colors.
- [ ] Clear the terminal between turns to prevent cheating.
- [ ] Add intermediary "screen" between turns to to confirm player switches.


# Potential Issues and Troubleshooting
- Pathing for sounds in player might cause problems depending on the operating system of the user. 
- If all else fails, make sure the path is absolute to the sound_files directory. 

- Example:

- `
playsound(f"absolute/path/to/Battleship/src/sound_files/miss-2.wav")
`