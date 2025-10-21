"""
Main entry point for the console-based quiz game.
"""
from src.config.settings import GAME_DEFAULT_ROUNDS
from src.game.classes.game_ui import GameUI

from src.game.classes.ai_gen import FakeNewsGenerator
from src.game.classes.wiki_article import ArticleWiki
from src.game.models.article import ArticleModel


def main():
    GameUI.draw_welcome()
    GameUI.print_basic_info()
    user_name = GameUI.get_player_name()
    user_choice_category = GameUI.print_random_categories()
    user_selected_category = GameUI.get_user_category(user_choice_category)
    current_round = 0
    while current_round <= GAME_DEFAULT_ROUNDS:
        ai_article = FakeNewsGenerator.generate(user_selected_category.name)

        articles: list[ArticleModel] = []
        for article in range(2):
            articles.append(ArticleWiki.get_random_article(user_selected_category))

        articles.append(ai_article)
        GameUI.print_articles(articles)
        user_answer =  GameUI.get_user_answer()
        user_answer_correct = GameUI.check_answer(articles[user_answer - 1])
        if user_answer_correct is False:
            GameUI.print_game_over(user_name)
            break

        current_round += 1
        if current_round < GAME_DEFAULT_ROUNDS:
            GameUI.print_answer_correct(user_name)
    GameUI.print_user_won(user_name)



    #Walter testing
    # print(f"AI Title, Summary:{FakeNewsGenerator.generate(user_selected_category.name)}")


if __name__ == "__main__":
    main()



