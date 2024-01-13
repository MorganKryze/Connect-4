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
    WINDOW_LENGTH,
)


def create_board() -> list:
    """Create a 2D array of zeros.

    Returns
    -------
        list: 2D array of zeros
    """
    return [[0 for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]


def drop_piece(board: list, row: int, col: int, piece: int) -> None:
    """Drop a piece in the board at the specified location.

    Args:
    ----
    board (list): 2D array of zeros
    row (int): row index
    col (int): column index
    piece (int): piece to drop

    Returns:
    -------
    None
    """
    board[row][col] = piece


def is_valid_location(board: list, col: int) -> bool:
    """Check if a piece can be dropped in the specified column.

    Args:
    ----
    board (list): 2D array of zeros
    col (int): column index

    Returns:
    -------
    bool: True if the piece can be dropped, False otherwise
    """
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board: list, col: int) -> int:
    """Get the next open row in the specified column.

    Args:
    ----
    board (list): 2D array of zeros
    col (int): column index

    Returns:
    -------
    int: index of the next open row
    """
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
    return 0


def winning_move(board: list, piece: int) -> bool:
    """Check if the specified piece has won.

    Args:
    ----
    board (list): 2D array of zeros
    piece (int): piece to check

    Returns:
    -------
    bool: True if the piece has won, False otherwise
    """
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                return True

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == piece
            ):
                return True
    return False


def evaluate_window(window: list, piece: int) -> int:
    """Evaluate the score of a piece in the window.

    Args:
    ----
    window (list): list of 4 cells
    piece (int): piece to evaluate

    Returns:
    -------
    int: score of the piece
    """
    score = 0
    opp_piece = HUMAN_TOKEN if piece == AI_TOKEN else AI_TOKEN

    if window.count(piece) == SCORE_4:
        score += 100
    elif window.count(piece) == SCORE_3 and window.count(0) == SCORE_1:
        score += 5
    elif window.count(piece) == SCORE_2 and window.count(0) == SCORE_2:
        score += 2

    if window.count(opp_piece) == SCORE_3 and window.count(0) == SCORE_1:
        score -= 4

    return score


def score_position(board: list, piece: int) -> int:
    """Score the board for the specified piece.

    Args:
    ----
    board (list): 2D array of zeros
    piece (int): piece to score

    Returns:
    -------
    int: score of the piece
    """
    score = 0

    # Score center column
    center_array = [int(row[COLUMN_COUNT // 2]) for row in board]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in board[r]]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c : c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(row[c]) for row in board]
        for r in range(ROW_COUNT - 3):
            window = col_array[r : r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positive diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score negative diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(3, COLUMN_COUNT):
            window = [board[r + i][c - i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board: list) -> bool:
    """Check if the game is over.

    Args:
    ----
    board (list): 2D array of zeros

    Returns:
    -------
    bool: True if the game is over, False otherwise
    """
    return (
        winning_move(board, HUMAN_TOKEN)
        or winning_move(board, AI_TOKEN)
        or len(get_valid_locations(board)) == 0
    )


def get_valid_locations(board: list) -> list[int]:
    """Get the valid locations to drop a piece.

    Args:
    ----
    board (list): 2D array of zeros

    Returns:
    -------
    list: list of valid locations
    """
    return [col for col in range(COLUMN_COUNT) if is_valid_location(board, col)]


def minimax(
    board: list,
    depth: int,
    alpha: int,
    beta: int,
    maximizing_player: bool,
) -> tuple[int, int]:
    """Minimax algorithm.

    Args:
    ----
    board (list): 2D array of zeros
    depth (int): depth of the search
    alpha (int): alpha value
    beta (int): beta value
    maximizing_player (bool): True if the player is maximizing, False otherwise

    Returns:
    -------
    tuple: best column to play and the score
    """
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_TOKEN):
                return (None, 100000000000000)
            elif winning_move(board, HUMAN_TOKEN):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_TOKEN))
    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_TOKEN)
            new_score = minimax(board, depth - 1, alpha, beta, False)[1]
            # Undo the move
            board[row][col] = 0
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, HUMAN_TOKEN)
            new_score = minimax(board, depth - 1, alpha, beta, True)[1]
            # Undo the move
            board[row][col] = 0
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def pick_best_move(board: list, piece: int) -> int:
    """Pick the best move for the specified piece.

    Args:
    ----
    board (list): 2D array of zeros
    piece (int): piece to play

    Returns:
    -------
    int: best column to play
    """
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def total_points(board: list) -> int:
    """Get the total points of the board.

    Args:
    ----
    board (list): 2D array of zeros

    Returns:
    -------
    int: total points of the board
    """
    total = 0
    for row in board:
        for cell in row:
            if cell in (HUMAN_TOKEN, AI_TOKEN):
                total += 1
    return total


def print_board(board: list) -> None:
    """Print the board on the console.

    Args:
    ----
    board (list): 2D array of zeros

    Returns:
    -------
    None
    """
    flipped_board = list(reversed(board))
    col_nums = [str(i + 1) for i in range(COLUMN_COUNT)]
    formatted_col_nums = [" " + num.rjust(2) for num in col_nums]
    for row in flipped_board:
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
