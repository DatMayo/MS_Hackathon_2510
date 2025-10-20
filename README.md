# Hackathon Quiz Game

A Python-based trivia/quiz application built during a hackathon coding challenge. This project supports multiple article sources including local storage and Wikipedia integration, with a flexible category system for educational gaming experiences.

## Features

- 📚 **Multi-source article management** - Support for both local articles and Wikipedia content
- 🏷️ **Category-based organization** - Flexible categorization system for content management
- 🎯 **Question model system** - Structured approach to quiz questions and answers
- ⚙️ **Configurable settings** - Easy configuration management
- 🎮 **Game UI components** - User interface elements for the quiz game
## Project Structure

```
├── src/
│   ├── config/
│   │   ├── __init__.py          # Package initialization
│   │   └── settings.py          # Application configuration
│   ├── data/
│   │   ├── false_responses.json # Game data
│   │   └── true_responses.json  # Game data
│   └── game/
│       ├── clases/              # Main game classes
│       │   ├── __init__.py      # Package initialization
│       │   ├── category.py      # Category management
│       │   ├── game_ui.py       # Game interface
│       │   ├── local_article.py # Local article handling
│       │   └── wiki_article.py  # Wikipedia integration
│       ├── enums/               # Enumeration definitions
│       │   ├── __init__.py      # Package initialization
│       │   └── game_state.py    # Game state enumerations
│       ├── models/              # Data models
│       │   ├── __init__.py      # Package initialization
│       │   ├── category.py      # Category data model
│       │   ├── player.py        # Player data model
│       │   └── question.py      # Question data model
│       └── utils/               # Utility functions
│           ├── __init__.py      # Package initialization
│           └── helpers.py       # Helper functions
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore patterns
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── LICENSE                      # MIT License file
```

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd hackathon_2510
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

## Development

This project is developed as part of a hackathon challenge, focusing on creating an educational quiz game with multiple content sources and a modular architecture.

## Contributing

Contributions are welcome after hackathon (2025-10-25)! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
