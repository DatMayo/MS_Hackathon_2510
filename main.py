"""
Main entry point for the console-based quiz game.
"""
from src.game.classes.category import Category
from src.game.models.player import PlayerModel
from src.game.classes.game_ui import GameUI

def main():
    GameUI.draw_welcome()
    GameUI.print_basic_info()
    name = GameUI.get_player_name()
    GameUI.print_random_categories()
    GameUI.print_question()

    pass

if __name__ == "__main__":
    main()