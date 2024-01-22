# Minimax Implementation

## Table of Contents

- [Minimax Implementation](#minimax-implementation)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Detailed Explanation](#detailed-explanation)
  - [Conclusion](#conclusion)

## Introduction

The `minimax(wall: list, depth: int, alpha: int, beta: int, maximizing_player: bool) -> tuple[int, int]` function is the main function implementing the Minimax algorithm with Alpha-Beta pruning. The function takes the current game state (`wall`), the depth of the search tree (`depth`), the current best values for Alpha and Beta (`alpha` and `beta`), and a boolean indicating whether the current player is maximizing or minimizing (`maximizing_player`). The function returns a tuple containing the best column to play and the score of that move.

To go back to the main documentation, click [here](../README.md).

To explore project call flow, click [here](flow.md).

## Detailed Explanation

If the current game state is a terminal state (i.e., the game is over) or the maximum depth has been reached, the function evaluates the game state and returns the score.
If the current player is the maximizing player, the function iterates over all valid moves, simulates each move, and recursively calls the `minimax` function for the opponent (minimizing player). The function keeps track of the best score and the move associated with it. It also updates the Alpha value and performs Alpha-Beta pruning.
If the current player is the minimizing player, the function does the same but keeps track of the minimum score and updates the Beta value.

1. `is_final_node(wall: list) -> bool`: This function checks if the current game state is a terminal state. A terminal state is reached when one player has won the game, or there are no more valid moves (i.e., the game is a draw). The function uses the `is_winner` and `get_available_slots` functions to check these conditions.

2. `get_available_slots(wall: list) -> list[int]`: This function returns a list of all columns in the game wall where a new token can be dropped. It uses the `is_slot_available` function to check if a token can be dropped in a column.

3. `get_available_slot(wall: list, col: int) -> int`: This function returns the next available row in a given column where a new token can be dropped.

4. `drop_token(wall: list, row: int, col: int, token: int) -> list`: This function drops a token in the specified location of the game wall and returns the updated game wall.

5. `score_position(wall: list, token: int) -> int`: This function scores the game wall for a given token. It checks all possible 4-token combinations (horizontally, vertically, and diagonally) and uses the `evaluate_wall` function to score each combination.

6. `evaluate_wall(wall: list, token: int) -> int`: This function evaluates the score of a token in a 4-token combination. It checks the number of tokens and empty cells in the combination and updates the score accordingly.

In the context of this project, we didn't incorporate heuristics such as those used in the A* algorithm. The reason for this is that the Minimax algorithm, which we've implemented here, doesn't typically require heuristics. Minimax is a decision-making algorithm used in two-player games with perfect information. It operates by exploring all possible paths up to a certain depth to make its decision.

Heuristics, on the other hand, are often used in pathfinding algorithms like A* to estimate the remaining cost to reach the goal and improve search efficiency. They are typically used in problems where the solution involves finding the shortest or most efficient path, such as route finding in navigation systems or path planning in robotics.

In our case, the Minimax algorithm, enhanced with Alpha-Beta pruning, provides an efficient solution for decision making in our game scenario. Alpha-Beta pruning is an optimization technique that eliminates branches in the search tree that don't need to be explored because they can't possibly influence the final decision, thereby speeding up the search process.

## Conclusion

The Minimax algorithm is a depth-first search algorithm. It builds a search tree by exploring all possible moves to a certain depth, then it backtracks to explore other branches. The Alpha-Beta pruning is an optimization technique that eliminates branches in the search tree that don't need to be explored because they can't possibly influence the final decision.
