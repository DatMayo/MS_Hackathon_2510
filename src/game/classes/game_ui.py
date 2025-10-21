import random
from src.config.settings import WIKI_MAX_DISPLAYED_CATEGORIES
from src.game.classes.category import Category
from src.game.models.article import ArticleModel
from src.game.models.category import CategoryModel


class GameUI:
    @staticmethod
    def draw_welcome():
        print("Welcome to TruthPedia!\n")

    @staticmethod
    def get_player_name():
        user_name = input("So tell me, what's your name? ")
        print(f"Hello {user_name}!")
        return user_name

    @staticmethod
    def print_basic_info():
        print(
            "This game is about guessing the imposter summary.\n"
            "You will choose a category and get 3 summaries of random pages.\n"
            "1 out of the 3 is an imposter.\n"
            "Are you smart enough to identify it?\n"
        )

    @staticmethod
    def print_game_over(user_name: str):
        print(f"Well {user_name}, you are pretty brainwashed...\n" "You've lost!")

    @staticmethod
    def print_random_categories(
        category_count: int = WIKI_MAX_DISPLAYED_CATEGORIES,
    ) -> list[CategoryModel]:
        category_list: list[CategoryModel] = []
        print("Here you have your choices:")

        while len(category_list) < category_count:
            random_cat = Category.get_random_category()
            if random_cat not in category_list:
                category_list.append(random_cat)
                print(f"{len(category_list)}) {random_cat.name}")

        return category_list

    @staticmethod
    def get_user_category(category_list: list[CategoryModel]) -> CategoryModel:
        # ToDo: Check if user_selection is int
        user_selection = int(
            input("\nChoose wisely... In which category do you wanna test your wits? ")
        )

        if user_selection < 1 or user_selection > len(category_list):
            print(
                "FAKENEWS: Please enter a valid number between 1 and {WIKI_MAX_DISPLAYED_CATEGORIES}"
            )
            return GameUI.get_user_category(category_list)

        print(
            f"So you chose {category_list[user_selection - 1].name}...\n"
            f"Indeed a wise choice! We'll prepare the summaries now...\n"
            f"Please wait... (eta: 15 seconds)"
        )
        return category_list[user_selection - 1]

    # TODO: change 'summaries' argument to specified argument

    @staticmethod
    def get_summaries(summaries):
        pass

    @staticmethod
    def print_summaries(summaries):
        for i in range(len(summaries)):
            print(f"{i+1}) {summaries[i]}")
        return summaries

    @staticmethod
    def get_user_answer() -> int:
        user_answer = int(input("Choose the Fakenews!\n" "Your answer: "))
        if user_answer < 1 or user_answer > 3:
            print("FAKENEWS: Please enter a valid number between 1 and 3")
            return GameUI.get_user_answer()
        return user_answer

    @staticmethod
    def check_answer(article: ArticleModel):
        if not article['is_truth']:
            return True
        return False

    @staticmethod
    def print_articles(my_articles: list[ArticleModel]):
        """
        Prints out the articles in the given list.

        Args:
            my_articles (list[ArticleModel]): A list of articles to be printed.

        Returns:
            None
        """
        for i, article in enumerate(my_articles):
            print(f"\nArticle No.{i + 1}\n")
            print(f"{article['title']}\n")
            print(f"{article['summary']}\n")

    @staticmethod
    def print_answer_correct(user_name: str):
        trump_praise = [
            f"TRUMPMENDOUS! {user_name}, you found the fake — nobody finds fakes better than you, believe me.",
            f"YUGE win, {user_name}! Correct answer. The other options? Total disasters.",
            f"Incredible job, {user_name}! Many people are saying this is the best guess they've ever seen."
        ]

        trump_inform = [
            f'Fifteen seconds and we’re right back—next round’s going to be huge, believe me.',
            f'Give it 15 seconds—then we hit the next round. People say it’s going to be incredible.',
            f'15 seconds and we roll again. Many, many people are saying it’ll be the best yet.'
        ]

        print(random.choice(trump_praise))
        print(random.choice(trump_inform))

    @staticmethod
    def print_user_won(user_name):
        trump_praise = [
            f'Huge win {user_name}. Almost as good as mine. Almost.',
            f'Tremendous job {user_name}. Everyone’s talking. Mostly about me—and you.',
            f'You won {user_name}. Big league. The best—besides me, of course.',
            f'Legendary finish {user_name}. People are amazed. I’m impressed. That’s rare.',
            f'Victory! Massive. You and I—real winners. The best.'
        ]

        print(random.choice(trump_praise))


