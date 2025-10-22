"""
Utility script to populate the local JSON fallback data.

This script fetches real articles from Wikipedia and generates fake articles
using the OpenAI API to fill 'src/data/responses.json'. This JSON file is used
as a fallback by ArticlesLocal when live API calls fail.

This script is designed to be resumable. It checks the existing JSON
data before fetching new content for each category.

== HOW TO RUN ==
From the project's root directory (the one containing the 'src' folder):
python -m src.game.utils.helpers
"""

import sys
import json
import time
from pathlib import Path
from typing import List, Set, Callable, Union


try:
    PROJECT_ROOT = Path(__file__).resolve().parents[3]
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))

    JSON_FILE_PATH = PROJECT_ROOT / "src" / "data" / "responses.json"
except IndexError:
    print("Error: Could not determine project root.")
    print("Please ensure this script is located at 'src/game/utils/helpers.py'")
    sys.exit(1)


# Imports from project
try:
    from src.game.models.article import ArticleModel
    from src.game.models.category import CategoryModel
    from src.game.classes.category import Category
    from src.game.classes.wiki_article import ArticleWiki
    from src.game.classes.ai_gen import FakeNewsGenerator
except ImportError as e:
    print(f"Error: Failed to import project modules: {e}")
    print("Please ensure you are running this script from the project root, e.g.:")
    print("python -m src.game.utils.helpers")
    sys.exit(1)

# Configuration
TARGET_REAL_ARTICLES_PER_CAT = 8
TARGET_FAKE_ARTICLES_PER_CAT = 4
API_RETRY_DELAY = 5  # seconds to wait after a failed API call
WIKI_API_DELAY = 1   # seconds to wait between successful Wikipedia API calls
AI_API_DELAY = 2     # seconds to wait between successful OpenAI API calls


def _load_existing_articles() -> List[ArticleModel]:
    """Loads the existing articles from the JSON file."""
    if not JSON_FILE_PATH.exists():
        print("No existing 'responses.json' file found. Starting fresh.")
        return []
    try:
        with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                print(f"Loaded {len(data)} existing articles.")
                return data
            print("Warning: 'responses.json' does not contain a list. Starting fresh.")
            return []  # File contained invalid data
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not read existing JSON file: {e}. Starting fresh.")
        return []

def _save_articles(articles: List[ArticleModel]):
    """Saves the complete list of articles to the JSON file."""
    try:
        JSON_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(JSON_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"FATAL ERROR: Could not write to JSON file: {e}")
        raise

def _fetch_and_add_articles(
    num_needed: int,
    fetch_function: Callable,
    category_arg: Union[CategoryModel, str],
    existing_titles: Set[str],
    all_articles_list: List[ArticleModel],
    api_delay: int,
    article_type_label: str
):
    """
    A generic helper to fetch/generate articles, check duplicates, and handle retries.
    """
    if num_needed <= 0:
        return  # Nothing to do

    print(f"Fetching {num_needed} new {article_type_label} articles...")

    max_consecutive_duplicates = 20

    for i in range(num_needed):
        consecutive_duplicates_found = 0

        while True:
            try:
                new_article = fetch_function(category_arg)

                # Validate the response
                if not new_article or not new_article.get('title'):
                    print(f"  ! Failed to get valid article data. Retrying in {API_RETRY_DELAY}s...")
                    time.sleep(API_RETRY_DELAY)
                    continue

                # Check for duplicates
                if new_article['title'] not in existing_titles:
                    all_articles_list.append(new_article)
                    existing_titles.add(new_article['title'])
                    print(f"  [{i+1}/{num_needed}] Added {article_type_label}: {new_article['title'][:50]}...")
                    time.sleep(api_delay)
                    break
                else:
                    print(f"  ! Duplicate found, retrying: {new_article['title'][:50]}...")
                    consecutive_duplicates_found += 1
                    time.sleep(0.5)

                    if consecutive_duplicates_found > max_consecutive_duplicates:
                        print(f"  ! Found {max_consecutive_duplicates}+ duplicates in a row.")
                        print(f"  ! Assuming category is exhausted of new {article_type_label} articles. Moving on.")
                        return

            except Exception as e:
                print(f"  ! Error fetching {article_type_label} article: {e}. Retrying in {API_RETRY_DELAY}s...")
                time.sleep(API_RETRY_DELAY)


def populate_fallback_data():
    """
    Fetches and generates articles to meet the target counts for each category.
    """
    print("Starting fallback data population utility...")
    print(f"Target file: {JSON_FILE_PATH}")
    print(f"Targets: {TARGET_REAL_ARTICLES_PER_CAT} REAL, {TARGET_FAKE_ARTICLES_PER_CAT} FAKE per category\n")

    all_articles = _load_existing_articles()

    for category_name in Category.categories:
        category_model = CategoryModel(category_name)
        print(f"--- Processing Category: {category_name} ---")

        # 1. Get current counts and existing titles
        existing_titles_in_cat: Set[str] = set()
        current_real_count = 0
        current_fake_count = 0

        for article in all_articles:
            if article.get("category") == category_name:
                if article.get("title"):
                    existing_titles_in_cat.add(article["title"])

                # Default to False (fake) if 'is_truth' key is missing or False
                if article.get("is_truth", False):
                    current_real_count += 1
                else:
                    current_fake_count += 1

        needed_real = TARGET_REAL_ARTICLES_PER_CAT - current_real_count
        needed_fake = TARGET_FAKE_ARTICLES_PER_CAT - current_fake_count

        print(f"Status: {current_real_count} real (need {needed_real}), {current_fake_count} fake (need {needed_fake})")

        # 2. Fetch missing REAL articles
        _fetch_and_add_articles(
            num_needed=needed_real,
            fetch_function=ArticleWiki.get_random_article,
            category_arg=category_model,
            existing_titles=existing_titles_in_cat,
            all_articles_list=all_articles,
            api_delay=WIKI_API_DELAY,
            article_type_label="REAL"
        )

        # 3. Generate missing FAKE articles
        _fetch_and_add_articles(
            num_needed=needed_fake,
            fetch_function=FakeNewsGenerator.generate,
            category_arg=category_name,
            existing_titles=existing_titles_in_cat,
            all_articles_list=all_articles,
            api_delay=AI_API_DELAY,
            article_type_label="FAKE"
        )

        # 4. Save progress after each category
        if needed_real > 0 or needed_fake > 0:
            print(f"Saving progress for '{category_name}'...")
            _save_articles(all_articles)
        else:
            print(f"Category '{category_name}' is already complete.")

        print(f"--- Finished Category: {category_name} ---\n")

    print("======================================================")
    print("All categories processed. Data population complete.")
    print(f"Total articles saved: {len(all_articles)}")
    print("======================================================")


if __name__ == "__main__":
    try:
        populate_fallback_data()
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user. Exiting gracefully.")
        try:
            sys.exit(0)
        except SystemExit:
            pass