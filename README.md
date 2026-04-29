
# Mini Game Hub

## 1. Project Overview

We will build a secure, multi-user game hub consisting of at least 3 two player games consisting of a menu, gameplay via a graphical interface and a persistent leaderboard using Bash scripting for authentication and Pygame and NumPy for gameplay.

## 2. Features

### Authentication System (Bash)

- User registration and login via terminal
- Secure password handling using SHA-256 hashing
- Persistent storage of user credentials (users.tsv)

### Game Engine (Python + Pygame)

- Manages the game menu, gameplay, post-game recordings and analytics
- Gameboard created using NumPy arrays
- Interactive gameplay in a Python GUI window

### Analytics, Leaderboard and Data Visualisation

- Record of results history (including total wins, losses etc.)
- Leaderboard display (which can be sorted based on any of the above metrics)
- Visualisation using Matplotlib via different graphs and charts

## 3. Project Structure

The repository is organised as follows:

```
hub/
├── main.sh              # Entry point (authentication)
├── game.py              # Game engine
├── leaderboard.sh       # Leaderboard
├── games/
|   ├── tictactoe.py      # Tic-Tac-Toe implementation
|   ├── othello.py        # Othello implementation
|   └── connect4.py       # Connect Four implementation
├── users.tsv            # Stored user credentials
├── history.csv          # Game history
└── README.md
```

### Components

- hub: directory that contains all the files required for the game hub
- main.sh: handles user authentication before launching the game engine
- game.py: manages the full Python side-flow: the game menu, gameplay, post-game recording and analytics
- leaderboard.sh: displays leaderboard of the players
- games: subdirectory containing the codes for the different games
- users.tsv: stores usernames and hash passwords with SHA-256 of all players
- history.csv: contains data about winners, losers, dates and game names of all games played

## 4. Design Plan

- Set up github repository and folder structure
- Create main.sh to implement login system in Bash with password hashing
- Build a central game controller in Python (game.py)
- Implement multiple games using NumPy
- Add GUI using Pygame for interaction
- Store match results
- Develop leaderboard system using Bash

## 5. Things Specific to Us

- Add timers to the games
- Display rules before the game starts
- Make new games (including multi-player ones, not just 2 player)

