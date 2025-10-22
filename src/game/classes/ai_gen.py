"""
Module for generating fake news articles using OpenAI's API.

This module provides functionality to generate plausible-sounding but entirely
fictional articles that fit within specified categories, designed to be used
in a trivia game setting.
"""

import json
from typing import Optional
from openai import OpenAI

from src.config.settings import OPENAI_API_KEY, WIKI_MAX_SENTENCE_LENGTH
from src.game.models.article import ArticleModel


class FakeNewsGenerator:
    """
    A class to generate fake news articles using OpenAI's API.

    This class provides methods to generate fake news articles that are
    plausible-sounding but entirely fictional, designed to be used as
    distractors in a trivia game.
    """

    @staticmethod
    def _generate_from_api(client: OpenAI, category: str) -> Optional[ArticleModel]:
        """
        Generate a fake news article using the OpenAI API.

        Args:
            client: An instance of the OpenAI client.
            category: The category for which to generate a fake article.

        Returns:
            ArticleModel: A dictionary containing the generated article's title,
                        summary, category, and truth status, or None if an error occurs.

        Note:
            This is an internal method and should not be called directly.
            Use the `generate()` method instead.
        """
        system_prompt = f"""
        You are an AI assistant for a trivia game. You will create a plausible-sounding
        but entirely fictional subject that fits a given category.
        Generate a fake Wikipedia article "title" and a one-paragraph "summary".
        The summary must be about {WIKI_MAX_SENTENCE_LENGTH} sentences long and sound encyclopedic.
        Respond ONLY with a valid JSON object with "title" and "summary" keys. Respond only in English.
        """
        user_prompt = f"Category: {category}"

        try:
            response = client.chat.completions.create(
                model="gpt-5-nano",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=1,
                timeout=30,  # Add timeout for API calls
            )

            if not response.choices or not response.choices[0].message.content:
                print("Warning: Empty response from OpenAI API")
                return None

            data = json.loads(response.choices[0].message.content)

            # Validate required fields
            if not data.get("title") or not data.get("summary"):
                print(
                    "Warning: Incomplete response from OpenAI API - missing title or summary"
                )
                return None

            article: ArticleModel = {
                "title": data.get("title"),
                "summary": data.get("summary"),
                "category": category,
                "is_truth": False,
            }
            return article

        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse JSON response from OpenAI API: {e}")
            return None
        except Exception as e:
            print(f"API Error: {e}")
            return None

    @staticmethod
    def generate(category: str) -> Optional[ArticleModel]:
        """
        Generate a fake news article for the specified category.

        Args:
            category: The category for which to generate a fake article.

        Returns:
            Optional[ArticleModel]: A dictionary containing the generated article's
                                 details, or None if generation fails or if the
                                 API key is not configured.

        Example:
            >>> article = FakeNewsGenerator.generate("Science")
            >>> if article:
            ...     print(article['title'])
            ...     print(article['summary'])
        """
        # Input validation
        if not category or not isinstance(category, str):
            print(
                "Error: Invalid category provided. Category must be a non-empty string."
            )
            return None

        if not OPENAI_API_KEY:
            print(
                "Error: OPENAI_API_KEY not found. Please configure your OpenAI API key."
            )
            return None

        try:
            client = OpenAI(api_key=OPENAI_API_KEY)
            return FakeNewsGenerator._generate_from_api(client, category)
        except Exception as e:
            print(f"Error: Failed to initialize OpenAI client: {e}")
            return None
