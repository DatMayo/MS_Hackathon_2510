"""
Main entry point for the console-based quiz game.
"""
from src.game.classes.game_ui import GameUI

from src.game.classes.ai_gen import FakeNewsGenerator
from src.game.classes.wiki_article import ArticleWiki
from src.game.models.article import ArticleModel


def main():
    GameUI.draw_welcome()
    GameUI.print_basic_info()
    # name = GameUI.get_player_name()
    user_choice_category = GameUI.print_random_categories()
    user_selected_category = GameUI.get_user_category(user_choice_category)
    ai_article = FakeNewsGenerator.generate(user_selected_category.name)

    articles: list[ArticleModel] = []
    for article in range(2):
        articles.append(ArticleWiki.get_random_article(user_selected_category))

    articles.append(ai_article)
    GameUI.print_articles(articles)

    #Walter testing
    # print(f"AI Title, Summary:{FakeNewsGenerator.generate(user_selected_category.name)}")


if __name__ == "__main__":
    main()



