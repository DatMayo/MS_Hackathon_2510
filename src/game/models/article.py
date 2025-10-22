"""
Article data model definitions.

This module defines the data structures used for representing articles
in the TruthPedia game, including both real and AI-generated articles.
"""
# Article model definition
class ArticleModel:
    """
    Data model for representing articles in the game.

    This class defines the structure of articles used throughout the game,
    including real articles from Wikipedia and AI-generated fake articles.

    Attributes:
        title (str): The title of the article.
        summary (str): A brief summary of the article content.
        category (str): The category this article belongs to.
        is_truth (bool): Whether this article contains real information (True)
                        or is AI-generated fake news (False).
    """
    title: str
    summary: str
    category: str
    is_truth: bool
