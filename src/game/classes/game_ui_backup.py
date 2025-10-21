from src.config.settings import WIKI_MAX_DISPLAYED_CATEGORIES
from src.game.classes.category import Category


class GameUI:
    @staticmethod
    def draw_welcome():
        print("Welcome to TruthPedia!\n")
        pass

    @staticmethod
    def get_player_name():
        user_name = input("So tell me, what's your name? ")
        print(f"Hello {user_name}!")
        return user_name

    """@staticmethod
    def get_player_rounds():
        print(f"Okay {name}! I assume you are ready to test your wits!")
        #sleep(2)                                                   Time delay from the "time" dictionary
        round_count = int(input("How many rounds do you wanna play? "))
        return round_count
    """

    @staticmethod
    def print_basic_info():
        print(
            "This game is about guessing the imposter summary.\n"
            "You will choose a category and get 3 summaries of random pages.\n"
            "1 out of the 3 is an imposter.\n"
            "Are you smart enough to identify it?\n"
        )
        pass

    @staticmethod
    def print_game_over(user_name: str):
        print(f"Well {user_name}, you are pretty brainwashed...\n" "You lost!")
        pass

    @staticmethod
    def print_random_categories(category_count: int = WIKI_MAX_DISPLAYED_CATEGORIES):
        category_list = []
        print("Here you have your choices:")
        for i in range(category_count):
            category_list.append(Category.get_random_category())
            print(f"{i+1}) {category_list[i]}")
        return category_list

    @staticmethod
    def print_question(category_list):
        user_selection = int(
            input(
                "In which category do you wanna test your wits?\n" "Choose wisely...\n"
            )
        )
        if user_selection < 1 or user_selection > len(category_list):
            raise IndexError
        print(
            f"So you chose {category_list[user_selection - 1]}...\n"
            f"Indeed a wise choice!"
        )
        return user_selection

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
    def get_user_answer(summaries):
        user_answer = int(input("Choose the Fakenews!\n" "Your answer: "))
        if user_answer < 1 or user_answer > len(summaries):
            raise IndexError
        return user_answer

    @staticmethod
    def check_answer(user_answer, score_count):
        if user_answer is False:
            score_count += 1
            print("Correct!")
        else:
            print("Wrong!\n" "No points for you. Try again!")
        pass
