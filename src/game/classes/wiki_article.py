import random
import wikipedia as wp
wp.set_lang("en")
from src.game.classes.local_article import ArticlesLocal
from src.game.models.question import QuestionModel


class ArticleWiki(ArticlesLocal):
    def load_articles(self) -> bool:
        raise NotImplementedError("You can not call load_article() on ArticleWiki")

    def get_random_article(self, category: str = None) -> QuestionModel:

        # ToDo: Implement local articles on API error or no internet connection
        articles =  wikipedia.search("Category:History", results = 2, suggestion = False)
        return articles

    print(get_random_article())