import math
import random
import time

from colorama import Fore, Style
from constants import AI_TOKEN, GAME_MODE_1, GAME_MODE_2, HUMAN_TOKEN, MAXIMUM_TOKEN
from functions import (
    create_wall,
    drop_token,
    get_next_open_row,
    is_slot_availabe,
    is_winner,
    minimax,
    total_points,
)
from visuals import print_menu, print_statistics, print_wall

if __name__ == "__main__":
    wall = create_wall()
    turn = 0

    choice = print_menu("Choisissez le mode de jeu :", [GAME_MODE_1, GAME_MODE_2])
    game_mode = GAME_MODE_1 if choice == 0 else GAME_MODE_2

    if game_mode == GAME_MODE_1:
        choice = print_menu("Qui commence ?", ["Joueur", "IA"])
        turn = HUMAN_TOKEN if choice == 0 else AI_TOKEN
    else:
        turn = random.choice([HUMAN_TOKEN, AI_TOKEN])

    total_time_player_1 = 0
    total_time_player_2 = 0
    remaining_tokens = 42
    turn_count = 0

    game_over = False
    while not game_over:
        start_time = time.time()

        # Vérifier si le total des points est de 42
        if total_points(wall) == MAXIMUM_TOKEN:
            print("La partie est terminée, le total de points est de 42.")
            break

        print_wall(wall, turn_count + 1)
        # Player 1 (Human) input
        if turn == HUMAN_TOKEN and game_mode == GAME_MODE_1:
            col = int(input("Joueur 1, fait ton choix entre (1-12): ")) - 1

            if is_slot_availabe(wall, col):
                row = get_next_open_row(wall, col)
                drop_token(wall, row, col, HUMAN_TOKEN)

                if is_winner(wall, HUMAN_TOKEN):
                    print(Fore.CYAN + "Joueur 1 wins!" + Style.RESET_ALL)
                    game_over = True

                turn = AI_TOKEN

        # AI Player input
        elif turn == AI_TOKEN and not game_over and game_mode == GAME_MODE_1:
            col, _ = minimax(wall, 4, -math.inf, math.inf, True)

            if is_slot_availabe(wall, col):
                row = get_next_open_row(wall, col)
                drop_token(wall, row, col, AI_TOKEN)

                if is_winner(wall, AI_TOKEN):
                    print(Fore.MAGENTA + "AI wins!" + Style.RESET_ALL)
                    game_over = True

                turn = HUMAN_TOKEN if game_mode == GAME_MODE_1 else AI_TOKEN

        elif game_mode == GAME_MODE_2:
            if turn == HUMAN_TOKEN:  # IA2 input
                col, _ = minimax(wall, 4, -math.inf, math.inf, True)

                if is_slot_availabe(wall, col):
                    row = get_next_open_row(wall, col)
                    drop_token(wall, row, col, HUMAN_TOKEN)

                    if is_winner(wall, HUMAN_TOKEN):
                        print(Fore.CYAN + "AI 2 wins!" + Style.RESET_ALL)
                        game_over = True

                    turn = AI_TOKEN
                    print(
                        Fore.CYAN + "IA2 a joué la colonne :" + Style.RESET_ALL,
                        col + 1,
                    )

            elif turn == AI_TOKEN and not game_over:  # AI1 Player input
                col, _ = minimax(wall, 4, -math.inf, math.inf, True)

                if is_slot_availabe(wall, col):
                    row = get_next_open_row(wall, col)
                    drop_token(wall, row, col, AI_TOKEN)

                    if is_winner(wall, AI_TOKEN):
                        print(Fore.MAGENTA + "AI 1 wins!" + Style.RESET_ALL)
                        game_over = True

                    turn = HUMAN_TOKEN
                    print(
                        Fore.MAGENTA + "IA1 a joué la colonne :" + Style.RESET_ALL,
                        col + 1,
                    )

        elapsed_time = time.time() - start_time

        if turn == AI_TOKEN:
            total_time_player_1 += elapsed_time
        else:
            total_time_player_2 += elapsed_time

        remaining_tokens -= 1
        turn_count += 1

        print(
            Fore.GREEN + "Temps écoulé pour ce tour :" + Style.RESET_ALL,
            elapsed_time,
            "secondes",
        )

    print_statistics(
        turn_count,
        remaining_tokens,
        total_time_player_1,
        total_time_player_2,
        "Joueur 1",
        "Joueur 2",
    )
