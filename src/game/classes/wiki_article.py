import random

import wikipediaapi

from src.config.settings import WIKI_MAX_SENTENCE_LENGTH
from src.game.classes.local_article import ArticlesLocal
from src.game.models.article import ArticleModel
from src.game.models.category import CategoryModel


class ArticleWiki(ArticlesLocal):
    @staticmethod
    def load_articles() -> bool:
        raise NotImplementedError("You can not call load_article() on ArticleWiki")

    @staticmethod
    def get_random_article(
        category: CategoryModel, is_truth: bool = True
    ) -> ArticleModel:
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
        concatinated_summary = []
        if len(split_summary) > 6:
            for i in range(1, WIKI_MAX_SENTENCE_LENGTH + 1):
                concatinated_summary.append(split_summary[i].strip("\n").strip("\\"))

            chosen_article = {
                "title": article_page.title,
                "summary": ". ".join(concatinated_summary),
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
