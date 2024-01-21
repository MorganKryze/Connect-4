# Project Call Flow

## Table of Contents

- [Project Call Flow](#project-call-flow)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Detailed Explanation](#detailed-explanation)
    - [Constants.py](#constantspy)
    - [Functions.py](#functionspy)
    - [Visuals.py](#visualspy)
    - [Main.py](#mainpy)
    - [Game Flow](#game-flow)

## Introduction

This document provides a high-level overview of the interaction between the four main files in the project: `constants.py`, `functions.py`, `main.py`, and `visuals.py`.

To go back to the main documentation, click [here](../README.md).

To explore the minimax implementation, click [here](minimax_implementation.md).

## Detailed Explanation

### Constants.py

This file defines all the constants used throughout the project. These constants include the number of columns and rows in the game, the maximum number of tokens, the tokens for player 1 and player 2, and the game modes. These constants are imported and used in the other files.

### Functions.py

This file contains the logic of the game. It includes functions for creating the game wall (a 2D array), switching turns, dropping a token in the wall, and checking if a player has won. These functions are imported and used in the `main.py` file.

### Visuals.py

This file handles the visual aspect of the game. It uses the blessed library to create a terminal-based user interface. It includes functions for printing the game menu, displaying the game screen, and printing the game wall. These functions are used in the `main.py` file to interact with the user.

### Main.py

This is the main entry point of the game. It imports the constants and functions from the other files. It initializes the game wall and player turns, and then enters a loop where it alternates between players, takes their inputs, updates the game wall, and checks if there's a winner or if it's a draw. If a player wins or the game is a draw, it breaks the loop and ends the game.

### Game Flow

The game starts in `main.py`, which initializes the game wall and player turns. The game enters a loop where it alternates between players. For each player, it uses the functions from `functions.py` to take the player's input, update the game wall, and check if there's a winner. It uses the functions from `visuals.py` to display the game state to the user. If a player wins or the game is a draw, it breaks the loop and ends the game. This flow is repeated until the game ends.
