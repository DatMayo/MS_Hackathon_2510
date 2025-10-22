import random
import textwrap
from src.config.settings import WIKI_MAX_DISPLAYED_CATEGORIES, CONSOLE_WIDTH
from src.game.classes.category import Category
from src.game.models.article import ArticleModel
from src.game.models.category import CategoryModel


class GameUI:
    @staticmethod
    def _wrap_text(text: str, width: int = None) -> str:
        """
        Wrap text to fit within console width.

        Args:
            text: The text to wrap.
            width: The width to wrap to. If None, uses CONSOLE_WIDTH.

        Returns:
            str: The wrapped text.
        """
        if width is None:
            width = CONSOLE_WIDTH
        return textwrap.fill(text, width=width - 4)  # -4 for indentation

    @staticmethod
    def draw_welcome() -> None:
        GameUI.clear_screen()
        print("Welcome to TruthPedia!\n")

    @staticmethod
    def clear_screen(lines: int = 100) -> None:
        """
        Clear the console screen by printing a specified number of blank lines.

        Args:
            lines (int): The number of blank lines to print. Defaults to 100.

        Returns:
            None
        """
        for x in range(lines):
            print("")

    @staticmethod
    def get_player_name() -> str:
        """
        Get the player's name from user input.

        Returns:
            str: The player's name.

        Raises:
            KeyboardInterrupt: If the user interrupts the input.
            EOFError: If the input stream ends unexpectedly.
        """
        try:
            user_name = input("So tell me, what's your name? ").strip()
            if not user_name:
                print("Please enter a valid name.")
                return GameUI.get_player_name()
            return user_name
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            exit(0)

    @staticmethod
    def print_basic_info() -> None:
        """
        Display basic information about the game.

        This method shows the player what the game is about and how to play.
        """
        print(
            "This game is about guessing the imposter summary.\n"
            "You will choose a category and get 3 summaries of random pages.\n"
            "1 out of the 3 is an imposter.\n"
            "Are you smart enough to identify it?\n"
        )

    @staticmethod
    def print_game_over(user_name: str , ai_article: ArticleModel) -> str:
        """
        Print a game over message to the user.

        Args:
            user_name: The name of the player who lost the game.
            ai_article: The article that was the Fakenews.

        Returns:
            str: The message that was printed.

        Note:
            This method clears the screen, prints the game over message,
            and displays the title and summary of the Fakenews article.
        """
        GameUI.clear_screen()
        message = f"Well {user_name}, you are pretty brainwashed...\nYou've lost!"
        print(message)
        print("The following summary was the Fakenews:\n")
        print(f"{ai_article['title']}")
        GameUI._wrap_text(f"{ai_article['summary']}")
        return message

    @staticmethod
    def print_random_categories(
        user_name: str,
        category_count: int = WIKI_MAX_DISPLAYED_CATEGORIES
    ) -> list[CategoryModel]:
        """
        Display and return a list of random categories for the player to choose from.

        Args:
            category_count: The number of categories to display. Defaults to WIKI_MAX_DISPLAYED_CATEGORIES.

        Returns:
            list[CategoryModel]: A list of randomly selected categories.

        Note:
            Categories are selected without replacement to ensure variety.
        """
        GameUI.clear_screen()
        print(f"Hello, {user_name}!")
        category_list: list[CategoryModel] = []
        print("Here you have your choices:")

        while len(category_list) < category_count:
            random_cat = Category.get_random_category()
            if random_cat.name not in [cat.name for cat in category_list]:
                category_list.append(random_cat)
                print(f"{len(category_list)}) {random_cat.name}")

        return category_list

    @staticmethod
    def get_user_category(category_list: list[CategoryModel]) -> CategoryModel:
        """
        Get the user's category selection.

        Args:
            category_list: List of available categories.

        Returns:
            CategoryModel: The selected category.

        Raises:
            ValueError: If input is invalid or category list is empty.
            KeyboardInterrupt: If the user interrupts the input.
            EOFError: If the input stream ends unexpectedly.
        """
        if not category_list:
            raise ValueError("No categories available for selection.")

        try:
            while True:
                user_input = input(
                    "\nChoose wisely... In which category do you wanna test your wits? "
                ).strip()

                if not user_input:
                    print("Please enter a number.")
                    continue

                try:
                    user_selection = int(user_input)
                except ValueError:
                    print(
                        f"Please enter a valid number between 1 and {len(category_list)}"
                    )
                    continue

                if user_selection < 1 or user_selection > len(category_list):
                    print(
                        f"Please enter a valid number between 1 and {len(category_list)}"
                    )
                    continue

                selected_category = category_list[user_selection - 1]
                print(
                    f"So you chose {selected_category.name}...\n"
                    f"Indeed a wise choice! We'll prepare the summaries now...\n"
                    f"Please wait... (eta: 15 seconds)"
                )
                return selected_category

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            exit(0)

    @staticmethod
    def get_user_answer() -> int:
        """
        Get the user's answer choice.

        Returns:
            int: The user's answer (1, 2, or 3).

        Raises:
            ValueError: If input is invalid.
            KeyboardInterrupt: If the user interrupts the input.
            EOFError: If the input stream ends unexpectedly.
        """
        try:
            while True:
                user_input = input("Choose the Fakenews!\nYour answer: ").strip()

                if not user_input:
                    print("Please enter a number.")
                    continue

                try:
                    user_answer = int(user_input)
                except ValueError:
                    print("Please enter a valid number between 1 and 3")
                    continue

                if user_answer < 1 or user_answer > 3:
                    print("Please enter a valid number between 1 and 3")
                    continue

                return user_answer

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            exit(0)

    @staticmethod
    def check_answer(article: ArticleModel) -> bool:
        """
        Check if the given article is fake news.

        Args:
            article: The article to check.

        Returns:
            bool: True if the article is fake news, False if it's real.

        Raises:
            ValueError: If the article doesn't have the required 'is_truth' field.
        """
        GameUI.clear_screen()
        if not isinstance(article, dict) or "is_truth" not in article:
            raise ValueError(
                "Invalid article provided. Article must be a dictionary with 'is_truth' field."
            )

        return not article["is_truth"]

    @staticmethod
    def _display_article(
        article: ArticleModel, index: int, total: int, console_width: int
    ) -> None:
        """
        Display a single article with proper formatting.

        Args:
            article: The article to display
            index: The 1-based index of the article
            total: Total number of articles
            console_width: Width of the console for formatting
        """
        print(f"\n{'=' * console_width}")
        print(f"Article {index} of {total}")
        print(f"{'=' * console_width}")

        # Wrap and print title
        wrapped_title = GameUI._wrap_text(article["title"])
        print(f"Title: {wrapped_title}")

        print()  # Empty line

        # Wrap and print summary
        wrapped_summary = GameUI._wrap_text(article["summary"])
        print(f"Summary: {wrapped_summary}")
        print(f"{'=' * console_width}\n")

    @staticmethod
    def print_articles(
        my_articles: list[ArticleModel], select_mode: bool = False
    ) -> int | None:
        """
        Displays articles one at a time with pagination controls.

        Args:
            my_articles (list[ArticleModel]): A list of articles to be displayed.
            select_mode (bool): If True, allows selecting an article to return its index.
                              If False, just for viewing (returns None).

        Returns:
            int | None: In select_mode, returns the 1-based index of the selected article.
                      In view mode, returns None.

        Raises:
            ValueError: If the input is not a list or if articles are invalid.
        """
        GameUI.clear_screen()
        if not isinstance(my_articles, list):
            raise ValueError("Articles must be provided as a list.")

        if not my_articles:
            print("No articles to display.")
            return None

        # Filter out invalid articles
        valid_articles = []
        for i, article in enumerate(my_articles):
            if not isinstance(article, dict):
                print(f"Warning: Skipping invalid article at position {i + 1}")
                continue
            if "title" not in article or "summary" not in article:
                print(f"Warning: Skipping article {i + 1} - missing title or summary")
                continue
            valid_articles.append(article)

        if not valid_articles:
            print("No valid articles to display.")
            return None

        console_width = CONSOLE_WIDTH
        current_index = 0
        total_articles = len(valid_articles)

        while True:
            GameUI.clear_screen()
            GameUI._display_article(
                valid_articles[current_index],
                current_index + 1,
                total_articles,
                console_width,
            )

            # Show navigation/selection instructions
            print("\nNavigation:")
            available_answers: list[str] = []
            if current_index > 0:
                available_answers.append("(P)revious")
                # print("  (P)revious")
            if current_index < total_articles - 1:
                available_answers.append("(N)ext")
                # print("  (N)ext")
            if select_mode:
                available_answers.append(f"(1-{total_articles}) Select this article")
                # print(f"  (1-{total_articles}) Select this article")
            available_answers.append("(Q)uit")
            print(" | ".join(available_answers))
            # print("  (Q)uit")

            # Get user input
            while True:
                try:
                    choice = input("\nYour choice: ").strip().lower()

                    # Navigation
                    if choice in ["n", "next"] and current_index < total_articles - 1:
                        current_index += 1
                        break
                    elif choice in ["p", "prev", "previous"] and current_index > 0:
                        current_index -= 1
                        break
                    # Article selection (only in select mode)
                    elif (
                        select_mode
                        and choice.isdigit()
                        and 1 <= int(choice) <= total_articles
                    ):
                        GameUI.clear_screen()
                        return int(choice)
                    # Quit
                    elif choice in ["q", "quit", "exit"]:
                        GameUI.clear_screen()
                        return None
                    else:
                        valid_choices = []
                        if current_index > 0:
                            valid_choices.extend(["p", "prev", "previous"])
                        if current_index < total_articles - 1:
                            valid_choices.extend(["n", "next"])
                        if select_mode:
                            valid_choices.extend(
                                [str(i + 1) for i in range(total_articles)]
                            )
                        valid_choices.extend(["q", "quit", "exit"])
                        print(
                            f"Please enter a valid choice: {', '.join(valid_choices)}"
                        )

                except (KeyboardInterrupt, EOFError):
                    GameUI.clear_screen()
                    return None

    @staticmethod
    def print_answer_correct(user_name: str) -> None:
        """
        Display congratulatory message when player answers correctly.

        Args:
            user_name: The name of the player who got the answer right.

        Note:
            Uses humorous Trump-inspired messages to celebrate correct answers.
        """
        GameUI.clear_screen()
        trump_praise = [
            f"TRUMPMENDOUS! {user_name}, you found the fake — nobody finds fakes better than you, believe me.",
            f"YUGE win, {user_name}! Correct answer. The other options? Total disasters.",
            f"Incredible job, {user_name}! Many people are saying this is the best guess they've ever seen.",
        ]

        trump_inform = [
            f"Fifteen seconds and we're right back—next round's going to be huge, believe me.",
            f"Give it 15 seconds—then we hit the next round. People say it's going to be incredible.",
            f"15 seconds and we roll again. Many, many people are saying it'll be the best yet.",
        ]

        print(random.choice(trump_praise))
        print(random.choice(trump_inform))

    @staticmethod
    def print_user_won(user_name: str) -> None:
        """
        Display victory message when player completes all rounds successfully.

        Args:
            user_name: The name of the player who won the game.

        Note:
            Uses humorous Trump-inspired victory messages to celebrate game completion.
        """
        trump_praise = [
            f"Huge win {user_name}. Almost as good as mine. Almost.",
            f"Tremendous job {user_name}. Everyone's talking. Mostly about me—and you.",
            f"You won {user_name}. Big league. The best—besides me, of course.",
            f"Legendary finish {user_name}. People are amazed. I'm impressed. That's rare.",
            f"Victory! Massive. You and I—real winners. The best.",
        ]
        GameUI.clear_screen()
        print(random.choice(trump_praise))

    @staticmethod
    def shuffle(articles: list[ArticleModel]):
        shuffled_list = []
        while articles:
            random_article = random.randint(0, len(articles)-1)
            popped_article = articles.pop(random_article)
            shuffled_list.append(popped_article)
        return shuffled_list
