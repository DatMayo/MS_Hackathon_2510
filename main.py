"""
Main entry point for the console-based quiz game.
"""
import sys
from src.config.settings import GAME_DEFAULT_ROUNDS
from src.game.classes.game_ui import GameUI

from src.game.classes.ai_gen import FakeNewsGenerator
from src.game.classes.wiki_article import ArticleWiki
from src.game.classes.local_article import ArticlesLocal
from src.game.models.article import ArticleModel


def main():
    """
    Main game loop with comprehensive error handling.

    This function runs the complete game flow, handling various potential errors
    that might occur during gameplay, API calls, or user interactions.
    """
    try:
        # Initialize game
        GameUI.draw_welcome()
        GameUI.print_basic_info()

        # Get player information
        user_name = GameUI.get_player_name()

        # Get and select category
        category_list = GameUI.print_random_categories(user_name)
        selected_category = GameUI.get_user_category(category_list)

        # Main game loop
        current_round = 0
        while current_round < GAME_DEFAULT_ROUNDS:
            try:
                # Generate AI fake article
                ai_article = FakeNewsGenerator.generate(selected_category.name)
                if not ai_article:
                    #Get pre-generated fake article
                    print("Error: Failed to generate fake article. Using pre-generated.")
                    ai_article = ArticlesLocal.get_random_article(selected_category, False)
                    if not ai_article:
                        print("Error: Failed to fetch pre-generated fake article.")
                        return
                # Get real articles
                articles: list[ArticleModel] = []
                for attempt in range(2):
                    real_article = ""

                    try:
                        # Get real article from Wikipedia
                        real_article = ArticleWiki.get_random_article(selected_category)
                    except (ValueError, ConnectionError) as e:
                        print(f"Warning: Failed to fetch real article (attempt {attempt + 1}): {e}")
                        if attempt == 1:  # Last attempt
                            # Get real article from local
                            print("Error: Unable to fetch articles from Wikipedia. Using pre-fetched.")
                            real_article = ArticlesLocal.get_random_article(selected_category, True)
                            if not real_article:
                                print("Error: Failed to fetch pre-generated real article.")
                                return
                    # Add real artice
                    articles.append(real_article)

                # Add fake article
                articles.append(ai_article)

                # Shuffle articles
                shuffled_list = GameUI.shuffle(articles)
                articles = shuffled_list

                # Display articles and get user answer
                user_answer = GameUI.print_articles(articles, select_mode=True)
                if user_answer is None:  # User chose to quit
                    print("Game ended by user.")
                    return

                # Check answer
                if user_answer < 1 or user_answer > len(articles):
                    print(f"Error: Invalid answer. Please select a number between 1 and {len(articles)}")
                    continue

                user_answer_correct = GameUI.check_answer(articles[user_answer - 1])

                if not user_answer_correct:
                    GameUI.print_game_over(user_name, ai_article)
                    return

                current_round += 1

                # Show success message if not the last round
                if current_round < GAME_DEFAULT_ROUNDS:
                    GameUI.print_answer_correct(user_name)

            except (ValueError, IndexError) as e:
                print(f"Error in round {current_round + 1}: {e}")
                print("Skipping this round and continuing...")
                continue
            except Exception as e:
                print(f"Unexpected error in round {current_round + 1}: {e}")
                print("Ending game due to unexpected error.")
                return

        # Game completed successfully
        if current_round >= GAME_DEFAULT_ROUNDS:
            GameUI.print_user_won(user_name)

    except KeyboardInterrupt:
        print("\n\nGame interrupted by user. Goodbye!")
    except Exception as e:
        print(f"Unexpected error starting game: {e}")
        print("Please check your configuration and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()



