import random
from src.game.models.category import CategoryModel

class Category:
    categories: list[CategoryModel] = [
        'Sport',
        'Geschichte',
        'Kultur',
        'Politik',
        'Wissenschaft',
        'Technik',
        'Kunst'
    ]

    @staticmethod
    def get_category_by_name(category_name) -> CategoryModel | None:
        return next(
            (category for category in Category.categories if category.name == category_name), None
        )

    @staticmethod
    def get_random_category() -> str:
        return random.choice(Category.categories)
