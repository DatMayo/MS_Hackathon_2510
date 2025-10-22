"""
Category data model definitions.

This module defines the data structures used for representing categories
in the TruthPedia game, which are used to organize articles by topic.
"""
class CategoryModel:
    """
    Data model for representing categories in the game.

    Categories are used to organize articles by topic and help players
    choose which type of content they want to test their fake news
    detection skills on.

    Attributes:
        name (str): The name of the category (e.g., "Science", "History").
    """

    def __init__(self, name: str):
        """
        Initialize a new category.

        Args:
            name: The name of the category.

        Raises:
            ValueError: If the category name is empty or invalid.
        """
        if not name or not isinstance(name, str):
            raise ValueError("Category name must be a non-empty string.")

        self.name = name
