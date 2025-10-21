import random
from src.game.models.category import CategoryModel


class Category:
    categories: list[CategoryModel] = [
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
        "April_Fools%27_Day",
        "Lists_of_reportedly_haunted_locations",
        "New_religious_movements",
        "Doomsday_scenarios",
        "Fake_news",
        "Prophecy",
    ]

    @staticmethod
    def get_category_by_name(category_name) -> CategoryModel | None:
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
        return CategoryModel(random.choice(Category.categories))
