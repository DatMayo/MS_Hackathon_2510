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

                if not isinstance(data, list):
                    print("Error: JSON data is not a list of articles")
                    return False

                for article in data:
                    # Validate required fields
                    if not isinstance(article, dict):
                        print(
                            f"Warning: Skipping invalid article (not a dictionary): {article}"
                        )
                        continue

                    if not all(
                        key in article
                        for key in ["title", "summary", "category", "is_truth"]
                    ):
                        print(
                            f"Warning: Skipping article with missing required fields: {article}"
                        )
                        continue

                    # Validate field types
                    if not isinstance(article["title"], str) or not isinstance(
                        article["summary"], str
                    ):
                        print(
                            f"Warning: Skipping article with invalid title/summary types: {article}"
                        )
                        continue

                    if not isinstance(article["category"], str):
                        print(
                            f"Warning: Skipping article with invalid category type: {article}"
                        )
                        continue

                    if not isinstance(article["is_truth"], bool):
                        print(
                            f"Warning: Skipping article with invalid is_truth type: {article}"
                        )
                        continue

                    current_article: ArticleModel = article
                    ArticlesLocal.local_articles.append(current_article)

                if not ArticlesLocal.local_articles:
                    print("Error: No valid articles found in JSON file")
                    return False

                return True

        except FileNotFoundError:
            print(
                "Error: responses.json file not found. Please ensure the file exists in the correct location."
            )
            return False
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse JSON file: {e}")
            return False
        except PermissionError:
            print("Error: Permission denied when trying to read responses.json file")
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
            ValueError: If articles fail to load or if invalid parameters are provided.

        Note:
            This method will automatically load articles from the JSON file if
            they haven't been loaded yet. The method uses the category's name
            for comparison with the article's category field.
        """
        # Input validation
        if not category or not hasattr(category, "name"):
            raise ValueError(
                "Invalid category provided. Category must have a 'name' attribute."
            )

        if not isinstance(is_truth, bool):
            raise ValueError("is_truth parameter must be a boolean value.")

        if len(ArticlesLocal.local_articles) == 0:
            success = ArticlesLocal.load_articles()
            if not success:
                raise ValueError("Failed to load articles from file.")

        # Generate a new list and filter truth and category
        filtered_list: list[ArticleModel] = []
        for article in ArticlesLocal.local_articles:
            if (
                article.get("is_truth") == is_truth
                and article.get("category") == category.name
            ):
                filtered_list.append(article)

        if not filtered_list:
            raise IndexError(
                f"No articles found for category '{category.name}' with is_truth={is_truth}"
            )

        return random.choice(filtered_list)
