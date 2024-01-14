from blessed import Terminal
from colorama import Fore, Style
from constants import AI_TOKEN, COLUMN_COUNT, HUMAN_TOKEN

term = Terminal()


def print_menu(question: str, menu_items: list) -> int:
    """Print the menu.

    Args:
    ----
    question (str): question to ask
    menu_items (list): list of menu items

    Returns:
    -------
    int: selection
    """
    with term.fullscreen():
        selection = 0
        display_screen(selection, menu_items, question)
        selection_inprogress = True
        with term.cbreak():
            while selection_inprogress:
                key = term.inkey()
                if key.is_sequence:
                    if key.name == "KEY_TAB":
                        selection += 1
                    if key.name == "KEY_DOWN":
                        selection += 1
                    if key.name == "KEY_UP":
                        selection -= 1
                    if key.name == "KEY_ENTER":
                        selection_inprogress = False
                elif key:
                    print(f"got {key}.")

                selection = selection % len(menu_items)

                display_screen(selection, menu_items, question)

    return selection


def display_screen(selection: int, menu: list, question: str) -> None:
    """Display the screen.

    Args:
    ----
    selection (int): index of the selected item
    menu (list): list of menu items
    question (str): question to ask

    Returns:
    -------
    None
    """
    with term.hidden_cursor():
        print(term.clear())
        print(question)
        print()

        for idx, m in enumerate(menu):
            if idx == selection:
                print(f"{term.bold_blue_reverse}{m}{term.normal}")
            else:
                print(f"{term.normal}{m}")
        print()
        print("Use the arrow keys to navigate, press enter to select an item.")


def print_wall(wall: list, turn: int) -> None:
    """Print the wall on the console.

    Args:
    ----
    wall (list): 2D array of zeros
    turn (int): current turn

    Returns:
    -------
    None
    """
    flipped_wall = list(reversed(wall))
    col_nums = [str(i + 1) for i in range(COLUMN_COUNT)]
    print()
    print(f" ──────────────────────── [ turn {turn} ] ────────────────────────")
    print()
    formatted_col_nums = ["  " + num.rjust(2) for num in col_nums]
    print(" " + " ".join(formatted_col_nums))
    print(" " + "├" + "┼".join("────" for _ in range(COLUMN_COUNT)) + "┤")
    for i, row in enumerate(flipped_wall):
        row_repr = []
        for cell in row:
            if cell == HUMAN_TOKEN:
                row_repr.append(Fore.RED + "🔴" + Style.RESET_ALL)
            elif cell == AI_TOKEN:
                row_repr.append(Fore.YELLOW + "🟡" + Style.RESET_ALL)
            else:
                row_repr.append(" ")
        print(
            " │" + "│".join(" " + cell.center(3 - 1) + " " for cell in row_repr) + "│",
        )
        if i < len(flipped_wall) - 1:
            print(" " + "├" + "┼".join("────" for _ in range(COLUMN_COUNT)) + "┤")
    print(" " + "└" + "┴".join("────" for _ in range(COLUMN_COUNT)) + "┘")


def print_statistics(
    turn_count: int,
    remaining_tokens: int,
    total_time_player_1: float,
    total_time_player_2: float,
    player_1_name: str,
    player_2_name: str,
) -> None:
    """Print the statistics.

    Args:
    ----
    turn_count (int): number of turns
    remaining_tokens (int): number of remaining tokens
    total_time_player_1 (float): total time for player 1
    total_time_player_2 (float): total time for player 2
    player_1_name (str): name of player 1
    player_2_name (str): name of player 2

    Returns:
    -------
    None
    """
    max_length = max(
        len(" Nombre de tours passés : " + str(turn_count)),
        len(" Jetons restants : " + str(remaining_tokens)),
        len(
            f" Temps total pour {player_1_name} : {total_time_player_1:.2f} secondes",
        ),
        len(
            f" Temps total pour {player_2_name} : {total_time_player_2:.2f} secondes",
        ),
    )

    print()
    # Print the statistics in a box with the calculated maximum length
    print("┌" + "─" * max_length + "┐")
    print("│" + " Statistiques de fin de jeu".ljust(max_length) + "│")
    print("│" + "─" * max_length + "│")
    print(
        "│" + (" Nombre de tours passés : " + str(turn_count)).ljust(max_length) + "│",
    )
    print("│" + (" Jetons restants : " + str(remaining_tokens)).ljust(max_length) + "│")
    print(
        "│"
        + f" Temps total pour {player_1_name} : {total_time_player_1:.2f} secondes".ljust(
            max_length,
        )
        + "│",
    )
    print(
        "│"
        + f" Temps total pour {player_2_name} : {total_time_player_2:.2f} secondes".ljust(
            max_length,
        )
        + "│",
    )
    print("└" + "─" * max_length + "┘")
