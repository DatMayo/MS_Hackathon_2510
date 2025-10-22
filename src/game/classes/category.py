"""
Category management functionality.

This module provides functionality for managing game categories,
including predefined categories and methods for selecting random
categories or finding categories by name.
"""

import random
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
        "Lists_of_reportedly_haunted_locations",
        "New_religious_movements",
        "Doomsday_scenarios",
        "Fake_news",
        "Prophecy",
    ]

    @staticmethod
    def get_category_by_name(category_name: str) -> CategoryModel | None:
        """
        Find a category by its name.

        Args:
            category_name: The name of the category to find.

        Returns:
            CategoryModel or None: The category object if found, None otherwise.

        Example:
            >>> category = Category.get_category_by_name("Science")
            >>> if category:
            ...     print(f"Found category: {category.name}")
        """
        return next(
            (
                category
                for category in Category.categories
                if category.name == category_name
            ),
            None,
        )

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
