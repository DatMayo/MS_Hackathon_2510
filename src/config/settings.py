"""
Game configuration and settings management.

This module handles all configuration settings for the TruthPedia game,
including API keys, game parameters, and display settings. It uses
environment variables for sensitive information like API keys.
"""
# Game settings and configuration
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Game settings
GAME_DEFAULT_ROUNDS = 2

WIKI_MAX_DISPLAYED_CATEGORIES = 3
WIKI_MAX_SENTENCE_LENGTH = 6

# Display settings
CONSOLE_WIDTH = 80
