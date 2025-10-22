"""
Category management functionality.

This module provides functionality for managing game categories,
including predefined categories and methods for selecting random
categories or finding categories by name.
"""

import random

from src.config.settings import WIKI_MAX_DISPLAYED_CATEGORIES
from src.game.models.category import CategoryModel


class Category:
    """
    Manages game categories for the TruthPedia game.

    This class provides a collection of predefined categories and
    utility methods for working with categories throughout the game.
    Categories are used to organize articles by topic.

    Class Attributes:
        categories: A list of predefined category names as strings.
    """

    categories: list[str] = [
        "Urban_legends",
        "Conspiracy_theories",
        "Hoaxes",
        "Internet_memes",
        "Cryptids",
        "Secret_societies",
        "Paranormal",
        "UFO_sightings",
        "Alien_abduction",
        "Occult",
        "Alternative_medicine",
        "Pseudoscience",
        "Fringe_theories",
        "Mass_psychogenic_illness",
        "April_Fools'_Day",
        "Basketball",
        "New_religious_movements",
        "Doomsday_scenarios",
        "Fake_news",
        "Prophecy",
    ]

    @staticmethod
    def get_random_category() -> CategoryModel:
        """
        Get a random category from the predefined list.

        Returns:
            CategoryModel: A randomly selected category.

        Example:
            >>> random_cat = Category.get_random_category()
            >>> print(f"Random category: {random_cat.name}")
        """
        return CategoryModel(random.choice(Category.categories))

    @staticmethod
    def get_random_categories() -> list[CategoryModel]:
        """
        Get a list of random categories from the predefined list.

        Returns:
            list[CategoryModel]: A list of randomly selected categories.

        Example:
            >>> random_cats = Category.get_random_categories()
            >>> print(f"Random categories: {random_cats}")
        """
        return [CategoryModel(random.choice(Category.categories)) for _ in range(WIKI_MAX_DISPLAYED_CATEGORIES)]
