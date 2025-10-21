import random
from itertools import count

from src.game.models.question import QuestionModel
import json

class ArticlesLocal:
    local_articles: list[QuestionModel] = []

    @staticmethod
    def load_articles() -> bool:
        """
        Loads articles from a JSON file and stores them in the local_articles list.

        Returns:
            bool: True if the articles were loaded successfully, False otherwise.
        """
        try:
            with open("../../data/responses.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                for article in data:
                    current_artice: QuestionModel = article
                    ArticlesLocal.local_articles.append(current_artice)
                return True
        except Exception as e:
            print(f"Error loading articles: {e}")
            return False

    @staticmethod
    def get_random_article(is_truth: bool, category: str):
        """
        Returns a random article from the list of local articles, filtered by the given is_truth and category parameters.

        Args:
            is_truth (bool): Whether the article is true or not.
            category (str): The category of the article.

        Returns:
            QuestionModel: A random article from the list of local articles, filtered by the given is_truth and category parameters.
        """
        if count(ArticlesLocal.local_articles == 0):
            ArticlesLocal.load_articles()

        # Generate a new list and filter truth and category
        filtered_list: list[QuestionModel] = []
        for article in ArticlesLocal.local_articles:
            if article['is_truth'] == is_truth and article['category'] == category:
                filtered_list.append(article)

        return random.choice(filtered_list)
