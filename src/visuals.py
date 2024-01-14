from blessed import Terminal
from constants import COLUMNS_COUNT, PLAYER_1_TOKEN, PLAYER_2_TOKEN

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
        print()
        print("[ Connect Four: Configuration ] ")
        print()
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
    col_nums = [str(i + 1) for i in range(COLUMNS_COUNT)]
    print()
    print(f" ──────────────────────── [ turn {turn} ] ────────────────────────")
    print()
    formatted_col_nums = ["  " + num.rjust(2) for num in col_nums]
    print(" " + " ".join(formatted_col_nums))
    print(" " + "├" + "┼".join("────" for _ in range(COLUMNS_COUNT)) + "┤")
    for i, row in enumerate(flipped_wall):
        row_repr = []
        for cell in row:
            if cell == PLAYER_1_TOKEN:
                row_repr.append(term.red("🔴"))
            elif cell == PLAYER_2_TOKEN:
                row_repr.append(term.yellow("🟡"))
            else:
                row_repr.append(" ")
        print(
            " │" + "│".join(" " + cell.center(3 - 1) + " " for cell in row_repr) + "│",
        )
        if i < len(flipped_wall) - 1:
            print(" " + "├" + "┼".join("────" for _ in range(COLUMNS_COUNT)) + "┤")
    print(" " + "└" + "┴".join("────" for _ in range(COLUMNS_COUNT)) + "┘")


def print_statistics(
    turn_count: int,
    remaining_tokens: int,
    total_time_player_1: float,
    total_time_player_2: float,
    player_1_name: str,
    player_2_name: str,
    result_of_the_game: str,
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
    result_of_the_game (str): result of the game

    Returns:
    -------
    None
    """
    max_length = max(
        len(" Token left: " + str(remaining_tokens)),
        len(" Last turn number: " + str(turn_count)),
        len(
            f" Total time for {player_1_name}: {total_time_player_1:.2f} seconds",
        ),
        len(
            f" Total time for {player_2_name}: {total_time_player_2:.2f} seconds",
        ),
        len(" Result: " + result_of_the_game),
    )
    print()
    print(" ───────────────────── [ End of the game] ────────────────────")
    print()

    print("┌" + "─" * max_length + "┐")
    print("│" + " Statistics".ljust(max_length) + "│")
    print("│" + "─" * max_length + "│")
    print("│" + (" Result: " + result_of_the_game).ljust(max_length) + "│")
    print("│" + (" ").ljust(max_length) + "│")
    print("│" + (" Token left: " + str(remaining_tokens)).ljust(max_length) + "│")
    print(
        "│" + (" Last turn number: " + str(turn_count)).ljust(max_length) + "│",
    )
    print(
        "│"
        + f" Total time for {player_1_name}: {total_time_player_1:.2f} seconds".ljust(
            max_length,
        )
        + "│",
    )
    print(
        "│"
        + f" Total time for {player_2_name}: {total_time_player_2:.2f} seconds".ljust(
            max_length,
        )
        + "│",
    )
    print("└" + "─" * max_length + "┘")
