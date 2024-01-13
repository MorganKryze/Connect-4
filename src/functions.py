import copy
import math
import random

from colorama import Fore, Style
from constants import (
    AI_TOKEN,
    COLUMN_COUNT,
    HUMAN_TOKEN,
    ROW_COUNT,
    SCORE_1,
    SCORE_2,
    SCORE_3,
    SCORE_4,
    WALL_LENGTH,
)


def total_points(wall: list) -> int:
    """Get the total points of the wall.

    Args:
    ----
    wall (list): 2D array of zeros

    Returns:
    -------
    int: total points of the wall
    """
    return sum(cell in (HUMAN_TOKEN, AI_TOKEN) for row in wall for cell in row)


def drop_token(wall: list, row: int, col: int, token: int) -> list:
    """Drop a token in the wall at the specified location.

    Args:
    ----
    wall (list): 2D array of zeros
    row (int): row index
    col (int): column index
    token (int): token to drop

    Returns:
    -------
    list: updated wall
    """
    wall[row][col] = token
    return wall


def get_next_open_row(wall: list, col: int) -> int:
    """Get the next open row in the specified column.

    Args:
    ----
    wall (list): 2D array of zeros
    col (int): column index

    Returns:
    -------
    int: index of the next open row
    """
    for r in range(ROW_COUNT):
        if wall[r][col] == 0:
            return r
    return 0


def evaluate_window(window: list, token: int) -> int:
    """Evaluate the score of a token in the window.

    Args:
    ----
    window (list): list of 4 cells
    token (int): token to evaluate

    Returns:
    -------
    int: score of the token
    """
    score = 0
    opp_token = HUMAN_TOKEN if token == AI_TOKEN else AI_TOKEN

    if window.count(token) == SCORE_4:
        score += 100
    elif window.count(token) == SCORE_3 and window.count(0) == SCORE_1:
        score += 5
    elif window.count(token) == SCORE_2 and window.count(0) == SCORE_2:
        score += 2

    if window.count(opp_token) == SCORE_3 and window.count(0) == SCORE_1:
        score -= 4

    return score


def score_position(wall: list, token: int) -> int:
    """Score the wall for the given token.

    Args:
    ----
    wall (list): 2D array of zeros
    token (int): token to score

    Returns:
    -------
    int: score of the token
    """
    score = 0

    # Center column
    center_array = [int(row[COLUMN_COUNT // 2]) for row in wall]
    center_count = center_array.count(token)
    score += center_count * 3

    # Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in wall[r]]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c : c + WALL_LENGTH]
            score += evaluate_window(window, token)

    # Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(row[c]) for row in wall]
        for r in range(ROW_COUNT - 3):
            window = col_array[r : r + WALL_LENGTH]
            score += evaluate_window(window, token)

    # Positive diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [wall[r + i][c + i] for i in range(WALL_LENGTH)]
            score += evaluate_window(window, token)

    # Negative diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(3, COLUMN_COUNT):
            window = [wall[r + i][c - i] for i in range(WALL_LENGTH)]
            score += evaluate_window(window, token)

    return score


def is_winner(wall: list, token: int) -> bool:
    """Check if the specified token has won.

    Args:
    ----
    wall (list): 2D array of zeros
    token (int): token to check

    Returns:
    -------
    bool: True if the token has won, False otherwise
    """
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (
                wall[r][c] == token
                and wall[r][c + 1] == token
                and wall[r][c + 2] == token
                and wall[r][c + 3] == token
            ):
                return True

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (
                wall[r][c] == token
                and wall[r + 1][c] == token
                and wall[r + 2][c] == token
                and wall[r + 3][c] == token
            ):
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                wall[r][c] == token
                and wall[r + 1][c + 1] == token
                and wall[r + 2][c + 2] == token
                and wall[r + 3][c + 3] == token
            ):
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                wall[r][c] == token
                and wall[r - 1][c + 1] == token
                and wall[r - 2][c + 2] == token
                and wall[r - 3][c + 3] == token
            ):
                return True
    return False


def is_slot_availabe(wall: list, col: int) -> bool:
    """Check if a token can be dropped in the specified column.

    Args:
    ----
    wall (list): 2D array of zeros
    col (int): column index

    Returns:
    -------
    bool: True if the token can be dropped, False otherwise
    """
    return wall[ROW_COUNT - 1][col] == 0


def get_available_slots(wall: list) -> list[int]:
    """Get the valid slots to drop a token.

    Args:
    ----
    wall (list): 2D array of zeros

    Returns:
    -------
    list: list of valid locations
    """
    return [col for col in range(COLUMN_COUNT) if is_slot_availabe(wall, col)]


def is_final_node(wall: list) -> bool:
    """Check if the game is over.

    Args:
    ----
    wall (list): 2D array of zeros

    Returns:
    -------
    bool: True if the game is over, False otherwise
    """
    return (
        is_winner(wall, HUMAN_TOKEN)
        or is_winner(wall, AI_TOKEN)
        or len(get_available_slots(wall)) == 0
    )


def minimax(
    wall: list,
    depth: int,
    alpha: int,
    beta: int,
    maximizing_player: bool,
) -> tuple[int, int]:
    """Minimax algorithm.

    Args:
    ----
    wall (list): 2D array of zeros
    depth (int): depth of the search
    alpha (int): alpha value
    beta (int): beta value
    maximizing_player (bool): True if the player is maximizing, False otherwise

    Returns:
    -------
    tuple: best column to play and the score
    """
    valid_locations = get_available_slots(wall)
    is_terminal = is_final_node(wall)
    if depth == 0 or is_terminal:
        if is_terminal:
            if is_winner(wall, AI_TOKEN):
                return (None, 100000000000000)
            elif is_winner(wall, HUMAN_TOKEN):
                return (None, -10000000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(wall, AI_TOKEN))
    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(wall, col)
            drop_token(wall, row, col, AI_TOKEN)
            new_score = minimax(wall, depth - 1, alpha, beta, False)[1]
            wall[row][col] = 0
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(wall, col)
            drop_token(wall, row, col, HUMAN_TOKEN)
            new_score = minimax(wall, depth - 1, alpha, beta, True)[1]
            wall[row][col] = 0
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value




def print_wall(wall: list) -> None:
    """Print the wall on the console.

    Args:
    ----
    wall (list): 2D array of zeros

    Returns:
    -------
    None
    """
    flipped_wall = list(reversed(wall))
    col_nums = [str(i + 1) for i in range(COLUMN_COUNT)]
    formatted_col_nums = [" " + num.rjust(2) for num in col_nums]
    for row in flipped_wall:
        row_repr = []
        for cell in row:
            if cell == HUMAN_TOKEN:
                row_repr.append(Fore.CYAN + "X" + Style.RESET_ALL)
            elif cell == AI_TOKEN:
                row_repr.append(Fore.MAGENTA + "O" + Style.RESET_ALL)
            else:
                row_repr.append(" ")
        print("".join(" | " + cell.center(2 - 1) for cell in row_repr) + " |  ")
    print(" " + " ".join(formatted_col_nums))
