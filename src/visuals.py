from blessed import Terminal


def print_menu(term: Terminal, selected_index: int) -> None:
    """Print the menu.

    Args:
    ----
    term (Terminal): blessed Terminal object
    selected_index (int): index of the selected menu item

    Returns:
    -------
    None
    """
    menu_items = ["Joueur VS IA", "IA VS IA"]
    print(term.home + term.clear)
    print(term.move_y(term.height // 2))
    for i, item in enumerate(menu_items):
        if i == selected_index:
            print(term.center(term.cyan_on_black(item)))
        else:
            print(term.center(item))
