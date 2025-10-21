"""
Module for fetching and processing Wikipedia articles.

This module provides functionality to retrieve random articles from Wikipedia
categories and process them for use in the game.
"""

import random
from typing import List, Dict, Any
import wikipediaapi

from src.config.settings import WIKI_MAX_SENTENCE_LENGTH
from src.game.classes.local_article import ArticlesLocal
from src.game.models.article import ArticleModel
from src.game.models.category import CategoryModel


class ArticleWiki(ArticlesLocal):
    """
    A class to handle Wikipedia article retrieval and processing.

    This class extends ArticlesLocal and provides methods to fetch random
    articles from Wikipedia categories, process their content, and format
    them for use in the game.
    """

    @staticmethod
    def load_articles() -> bool:
        """
        Placeholder method to maintain interface compatibility.

        Raises:
            NotImplementedError: Always, as this method should not be called on ArticleWiki.

        Note:
            This method is required to maintain compatibility with the ArticlesLocal
            interface but is not implemented as ArticleWiki fetches articles
            directly from Wikipedia's API.
        """
        raise NotImplementedError("You can not call load_article() on ArticleWiki")

    @staticmethod
    def get_random_article(
        category: CategoryModel, is_truth: bool = True
    ) -> ArticleModel:
        """
        Retrieve a random article from the specified Wikipedia category.

        Args:
            category: The category from which to fetch a random article.
            is_truth: Whether the article is considered true (always True for Wikipedia articles).

        Returns:
            ArticleModel: A dictionary containing the article's title, summary,
                        category, and truth status.

        Note:
            The method processes the article summary to ensure it's an appropriate
            length for the game, typically limiting it to WIKI_MAX_SENTENCE_LENGTH
            sentences.
        """
        wiki_handle = wikipediaapi.Wikipedia(user_agent="TruthPedia/1.0", language="en")
        wiki_page = wiki_handle.page(f"Category:{category.name}")

        article_list = []
        for entry in wiki_page.categorymembers.values():
            entry_name = entry.title
            if entry_name.startswith("Category") or entry_name.startswith("List"):
                continue

            article_list.append(entry_name)

        chosen_article: ArticleModel
        random_article = random.choice(article_list)
        article_page = wiki_handle.page(random_article)

        split_summary = article_page.summary.split(".")
        concatenated_summary = []
        if len(split_summary) > 6:
            for i in range(1, WIKI_MAX_SENTENCE_LENGTH + 1):
                concatenated_summary.append(split_summary[i].strip("\n").strip("\\"))

            chosen_article = {
                "title": article_page.title,
                "summary": ". ".join(concatenated_summary),
                "category": category.name,
                "is_truth": True,
            }
        else:
            chosen_article: ArticleModel = {
                "title": article_page.title,
                "summary": article_page.summary,
                "category": category.name,
                "is_truth": True,
            }

        return chosen_article
