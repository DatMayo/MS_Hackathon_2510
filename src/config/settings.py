# Game settings and configuration
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Game settings
GAME_DEFAULT_ROUNDS = 3

WIKI_MAX_DISPLAYED_CATEGORIES = 3
WIKI_MAX_SENTENCE_LENGTH = 6