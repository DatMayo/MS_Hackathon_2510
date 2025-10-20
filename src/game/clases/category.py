from src.game.models.category import CategoryModel


class Category:
    categories: list[CategoryModel] = []

    def get_category_by_name(self) -> CategoryModel:
        pass

    def get_default_categories(self) -> list[str]:
        pass

    def get_random_category(self) -> str:
        pass
