"""
Module for managing local article storage and retrieval.

This module provides functionality to load articles from a JSON file,
store them in memory, and retrieve random articles based on specified
criteria such as category and truth status.
"""

import random
import json
from typing import List, Optional

from src.game.models.category import CategoryModel
from src.game.models.article import ArticleModel


class ArticlesLocal:
    """
    A class to manage local storage and retrieval of articles.

    This class provides methods to load articles from a JSON file and
    retrieve random articles based on specified criteria. It maintains
    an in-memory cache of articles for efficient access.

    Class Attributes:
        local_articles: A list of ArticleModel dictionaries stored in memory.
    """

    local_articles: list[ArticleModel] = []

    @staticmethod
    def load_articles() -> bool:
        """
        Load articles from a JSON file into the local_articles list.

        This method reads articles from a predefined JSON file path, parses them,
        and stores them in the class-level local_articles list. If articles have
        already been loaded, it returns immediately without reloading.

        Returns:
            bool: True if articles were loaded successfully or were already loaded,
                 False if an error occurred during loading.

        Note:
            The JSON file is expected to be in the ../../data/responses.json path
            relative to this file. The file should contain an array of article
            objects with 'title', 'summary', 'category', and 'is_truth' fields.
        """
        if len(ArticlesLocal.local_articles) > 0:
            return True

        try:
            with open("../../data/responses.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                for article in data:
                    current_artice: ArticleModel = article
                    ArticlesLocal.local_articles.append(current_artice)
                return True
        except Exception as e:
            print(f"Error loading articles: {e}")
            return False

    @staticmethod
    def get_random_article(
        category: CategoryModel, is_truth: bool = True
    ) -> ArticleModel:
        """
        Retrieve a random article matching the specified criteria.

        This method returns a random article from the locally stored articles
        that matches the given category and truth status. If no matching articles
        are found, it may raise an IndexError.

        Args:
            category: The category model containing the category name to filter by.
            is_truth: Whether to return true or false articles. Defaults to True.

        Returns:
            ArticleModel: A random article matching the specified criteria.

        Raises:
            IndexError: If no articles match the specified criteria.

        Note:
            This method will automatically load articles from the JSON file if
            they haven't been loaded yet. The method uses the category's name
            for comparison with the article's category field.
        """
        if len(ArticlesLocal.local_articles) == 0:
            ArticlesLocal.load_articles()

        # Generate a new list and filter truth and category
        filtered_list: list[ArticleModel] = []
        for article in ArticlesLocal.local_articles:
            if article["is_truth"] == is_truth and article["category"] == category.name:
                filtered_list.append(article)

        return random.choice(filtered_list)
