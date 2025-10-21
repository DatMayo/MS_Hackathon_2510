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
        print(f"Well {user_name}, you are pretty brainwashed...\n" "You lost!")

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
    def get_user_answer(user_input):

        

        """
        user_answer = int(input("Choose the Fakenews!\n" "Your answer: "))
        if user_answer < 1 or user_answer > len(summaries):
            raise IndexError
        return user_answer
        """

    @staticmethod
    def check_answer(user_answer, score_count):
        if user_answer is False:
            score_count += 1
            print("Correct!")
        else:
            print("Wrong!\n" "No points for you. Try again!")

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
