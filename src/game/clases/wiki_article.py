from src.game.clases.local_article import ArticlesLocal
from src.game.models.question import QuestionModel


class ArticleWiki(ArticlesLocal):
    def load_article(self) -> bool:
        raise NotImplementedError("You can not call load_article() on ArticleWiki")

    def get_random_article(self, category: str = None) -> QuestionModel:

        # ToDo: Implement local articles on API error or no internet connection
        pass