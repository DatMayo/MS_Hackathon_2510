import json
import time
from openai import OpenAI

from src.config.settings import OPENAI_API_KEY, WIKI_MAX_SENTENCE_LENGTH
from src.game.models.article import ArticleModel


class FakeNewsGenerator:
    @staticmethod
    def _generate_from_api(client, category: str) -> ArticleModel | None:
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
            )
            data = json.loads(response.choices[0].message.content)
            article: ArticleModel = {
                "title": data.get("title"),
                "summary": data.get("summary"),
                "category": category,
                "is_truth": False,
            }
            return article
        except Exception as e:
            print(f"API Error: {e}")
            return None

    @staticmethod
    def generate(category: str):
        if not OPENAI_API_KEY:
            print("Error: OPENAI_API_KEY not found.")
            return None, None

        client = OpenAI(api_key=OPENAI_API_KEY)
        return FakeNewsGenerator._generate_from_api(client, category)


def main():
    try:
        category = input("Enter a category to test: ")
        if not category:
            print("No category provided. Exiting.")
            return

        print("\nGenerating...")

        start_time = time.monotonic()
        title, summary = FakeNewsGenerator.generate(category)
        end_time = time.monotonic()

        if title and summary:
            print(f"Title: {title}")
            print(f"Summary: {summary}")
            duration = end_time - start_time
            print(f"\nTime taken: {duration:.2f} seconds")
        else:
            print("\nFailed to generate trivia.")

    except (KeyboardInterrupt, EOFError):
        print("\n\nExiting test.")


if __name__ == "__main__":
    main()
