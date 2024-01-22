import math
import time

from constants import (
    GAME_MODE_1,
    GAME_MODE_2,
    MAXIMUM_TOKEN,
    PLAYER_1_TOKEN,
    PLAYER_2_TOKEN,
)
from functions import (
    create_wall,
    drop_token,
    get_available_slot,
    is_slot_available,
    is_winner,
    minimax,
    switch_turn,
)
from visuals import print_menu, print_statistics, print_wall, term

if __name__ == "__main__":
    wall = create_wall()
    total_time_player_1 = 0
    total_time_player_2 = 0
    remaining_tokens = MAXIMUM_TOKEN
    turn_count = 0
    turn = 0

    player_1_name = "player 1"
    player_2_name = "player 2"
    result_of_game = "None"

    choice = print_menu("Please choose your game mode", [GAME_MODE_1, GAME_MODE_2])
    game_mode = GAME_MODE_1 if choice == 0 else GAME_MODE_2

    if game_mode == GAME_MODE_1:
        player_1_name = "Human"
        player_2_name = "AI"
    else:
        player_1_name = "AI"
        player_2_name = "HUMAN"

    turn = PLAYER_1_TOKEN
    while True:
        start_time = time.time()
        print_wall(wall, turn_count)

        if remaining_tokens == 0:
            result_of_game = "It's a draw!"
            break
        elif is_winner(wall, PLAYER_1_TOKEN):
            result_of_game = f"{player_1_name} wins!"
            break
        elif is_winner(wall, PLAYER_2_TOKEN):
            result_of_game = f"{player_2_name} wins!"
            break

        if game_mode == GAME_MODE_1:
            if turn == PLAYER_1_TOKEN:
                col = int(input(f"{player_1_name}, Enter a column (0..11): "))

                if is_slot_available(wall, col):
                    row = get_available_slot(wall, col)
                    drop_token(wall, row, col, PLAYER_1_TOKEN)

                    print(
                        term.red(f"{player_1_name} played the column:"),
                        col,
                    )

            elif turn == PLAYER_2_TOKEN:
                col, _ = minimax(wall, 5, -math.inf, math.inf, True)

                if is_slot_available(wall, col):
                    row = get_available_slot(wall, col)
                    drop_token(wall, row, col, PLAYER_2_TOKEN)

                    print(
                        term.yellow(f"{player_2_name} played the column:"),
                        col,
                    )

        elif game_mode == GAME_MODE_2:
            if turn == PLAYER_1_TOKEN:
                col, _ = minimax(wall, 5, -math.inf, math.inf, True)

                if is_slot_available(wall, col):
                    row = get_available_slot(wall, col)
                    drop_token(wall, row, col, PLAYER_2_TOKEN)

                    print(
                        term.yellow(f"{player_2_name} played the column:"),
                        col,
                    )

            elif turn == PLAYER_2_TOKEN:
                col = int(input(f"{player_1_name}, Enter a column (0..11): "))

                if is_slot_available(wall, col):
                    row = get_available_slot(wall, col)
                    drop_token(wall, row, col, PLAYER_1_TOKEN)

                    print(
                        term.red(f"{player_1_name} played the column:"),
                        col,
                    )

        elapsed_time = time.time() - start_time

        if turn == PLAYER_1_TOKEN:
            total_time_player_1 += elapsed_time
        else:
            total_time_player_2 += elapsed_time
        turn = switch_turn(turn)
        remaining_tokens -= 1
        turn_count += 1

        print(
            term.green("Elapsed time for this turn: "),
            elapsed_time,
            "seconds",
        )

    print_statistics(
        turn_count,
        remaining_tokens,
        total_time_player_1,
        total_time_player_2,
        player_1_name,
        player_2_name,
        result_of_game,
    )
