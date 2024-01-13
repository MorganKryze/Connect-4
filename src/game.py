import math
import random
import time

from blessed import Terminal
from colorama import Fore, Style
from constants import AI_TOKEN, COLUMN_COUNT, HUMAN_TOKEN, MAXIMUM_TOKEN, ROW_COUNT
from functions import (
    drop_token,
    get_next_open_row,
    is_slot_availabe,
    is_winner,
    minimax,
    print_wall,
    total_points,
)

if __name__ == "__main__":
    # Main game loop
    board = [[0 for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]
    print_wall(board)
    game_over = False
    turn = random.choice([HUMAN_TOKEN, AI_TOKEN])

    # Demandez Ã  l'utilisateur qui sont les 2 joueurs : 2 IAs ou 1 joueur et une IA
    while True:
        game_mode = input(
            "Choisissez le mode de jeu : (1) "
            + Fore.CYAN
            + "Joueur"
            + Style.RESET_ALL
            + " VS "
            + Fore.MAGENTA
            + "IA"
            + Style.RESET_ALL
            + ", (2) "
            + Fore.MAGENTA
            + "IA"
            + Style.RESET_ALL
            + " VS "
            + Fore.MAGENTA
            + "IA"
            + Style.RESET_ALL
            + ": ",
        )
        if game_mode in ["1", "2"]:
            break
        else:
            print("Mode de jeu invalide. Veuillez choisir entre (1) et (2).")

    # On peut dÃ©cider qui commence l'IA ou le joueur
    if game_mode == "1":
        while True:
            first_turn = input(
                "Qui commence ? (1)"
                + Fore.CYAN
                + "Joueur"
                + Style.RESET_ALL
                + ", (2) "
                + Fore.MAGENTA
                + "IA"
                + Style.RESET_ALL
                + ": ",
            )
            if first_turn in ["1", "2"]:
                turn = HUMAN_TOKEN if first_turn == "1" else AI_TOKEN
                break
            else:
                print("Choix invalide. Veuillez choisir entre (1) et (2).")
    else:
        turn = random.choice([HUMAN_TOKEN, AI_TOKEN])

    # Initialisation des variables pour suivre le temps et les tours
    total_time_ia1 = 0
    total_time_ia2 = 0
    remaining_tokens = 42
    turn_count = 0

    while not game_over:
        start_time = time.time()

        # Vérifier si le total des points est de 42
        if total_points(board) == MAXIMUM_TOKEN:
            print("La partie est terminée, le total de points est de 42.")
            break

        # Player 1 (Human) input
        if turn == HUMAN_TOKEN and game_mode == "1":
            col = int(input("Joueur 1, fait ton choix entre (1-12): ")) - 1

            if is_slot_availabe(board, col):
                row = get_next_open_row(board, col)
                drop_token(board, row, col, HUMAN_TOKEN)

                if is_winner(board, HUMAN_TOKEN):
                    print(Fore.CYAN + "Joueur 1 wins!" + Style.RESET_ALL)
                    game_over = True

                turn = AI_TOKEN
                print_wall(board)

        # AI Player input
        elif turn == AI_TOKEN and not game_over and game_mode == "1":
            col, _ = minimax(board, 4, -math.inf, math.inf, True)

            if is_slot_availabe(board, col):
                row = get_next_open_row(board, col)
                drop_token(board, row, col, AI_TOKEN)

                if is_winner(board, AI_TOKEN):
                    print(Fore.MAGENTA + "AI wins!" + Style.RESET_ALL)
                    game_over = True

                turn = HUMAN_TOKEN if game_mode == "1" else AI_TOKEN
                print_wall(board)

        elif game_mode == "2":
            if turn == HUMAN_TOKEN:  # IA2 input
                col, _ = minimax(board, 4, -math.inf, math.inf, True)

                if is_slot_availabe(board, col):
                    row = get_next_open_row(board, col)
                    drop_token(board, row, col, HUMAN_TOKEN)

                    if is_winner(board, HUMAN_TOKEN):
                        print(Fore.CYAN + "AI 2 wins!" + Style.RESET_ALL)
                        game_over = True

                    turn = AI_TOKEN
                    print_wall(board)
                    print(
                        Fore.CYAN + "IA2 a joué la colonne :" + Style.RESET_ALL,
                        col + 1,
                    )

            elif turn == AI_TOKEN and not game_over:  # AI1 Player input
                col, _ = minimax(board, 4, -math.inf, math.inf, True)

                if is_slot_availabe(board, col):
                    row = get_next_open_row(board, col)
                    drop_token(board, row, col, AI_TOKEN)

                    if is_winner(board, AI_TOKEN):
                        print(Fore.MAGENTA + "AI 1 wins!" + Style.RESET_ALL)
                        game_over = True

                    turn = HUMAN_TOKEN
                    print_wall(board)
                    print(
                        Fore.MAGENTA + "IA1 a joué la colonne :" + Style.RESET_ALL,
                        col + 1,
                    )

        elapsed_time = time.time() - start_time

        # Mise à jour du temps total pour IA1 et IA2
        if turn == AI_TOKEN:
            total_time_ia1 += elapsed_time
        else:
            total_time_ia2 += elapsed_time

        # Mise à jour du nombre de jetons restants et du nombre de tours
        remaining_tokens -= 1
        turn_count += 1

        print(
            Fore.GREEN + "Temps écoulé pour ce tour :" + Style.RESET_ALL,
            elapsed_time,
            "secondes",
        )

    # Affichage des statistiques à la fin du jeu
    print("Statistiques de fin de jeu :")
    print(Fore.YELLOW + "Nombre de tours passés :" + Style.RESET_ALL, turn_count)
    print(Fore.YELLOW + "Jetons restants :" + Style.RESET_ALL, remaining_tokens)
    print(
        Fore.MAGENTA + "Temps total pour IA1 :" + Style.RESET_ALL,
        total_time_ia2,
        "secondes",
    )
    print(
        Fore.CYAN + "Temps total pour IA2 :" + Style.RESET_ALL,
        total_time_ia1,
        "secondes",
    )
