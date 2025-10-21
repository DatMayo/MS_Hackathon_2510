# TruthPedia: The Fake News Detection Game

A Python-based game that challenges players to identify fake news articles among real ones. Built during a hackathon coding challenge, this project features AI-generated fake articles, Wikipedia integration, and a fun, engaging interface with a political satire theme.

## Features

- 🤖 **AI-Generated Fake News** - Uses OpenAI's API to generate convincing fake articles
- 🌐 **Wikipedia Integration** - Fetches real articles from Wikipedia for comparison
- 🏆 **Multiple Categories** - Play with various topics from Urban Legends to Conspiracy Theories
- 🎭 **Satirical Theme** - Fun, political satire theme with humorous responses
- 📊 **Type-Safe Python** - Full type hints and comprehensive docstrings for better maintainability
- 🎮 **Interactive CLI** - Clean, user-friendly command-line interface
## Project Structure

```
├── src/
│   ├── config/
│   │   ├── __init__.py          # Package initialization
│   │   └── settings.py          # Application configuration and constants
│   ├── data/
│   │   └── responses.json       # Game data (true and false articles)
│   └── game/
│       ├── classes/             # Core game logic
│       │   ├── __init__.py
│       │   ├── ai_gen.py        # AI article generation
│       │   ├── category.py      # Category management
│       │   ├── game_ui.py       # User interface and game flow
│       │   ├── local_article.py # Local article handling
│       │   └── wiki_article.py  # Wikipedia integration
│       └── models/              # Data models
│           ├── __init__.py
│           ├── article.py       # Article data structure
│           └── category.py      # Category data structure
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore patterns
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── ToDo.md                      # Development roadmap and tasks
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

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key for AI article generation (optional)

## 🎮 How to Play

1. Start the game:
```bash
python main.py
```

2. Enter your name when prompted
3. Choose a category from the list
4. Read the articles carefully - one of them is AI-generated fake news!
5. Select which article you think is fake
6. See if you can spot all the fakes and become a true Fake News Detective!

### Game Modes
- **Single Player**: Test your fake news detection skills
- **Categories**: Various topics from Urban Legends to Conspiracy Theories
- **AI-Generated Fakes**: Each game features unique AI-generated fake articles

## 🛠️ Development Status

### Completed Features
- [x] Core game loop and user interface
- [x] Wikipedia article fetching and processing
- [x] Local article storage and management
- [x] AI-generated fake news with OpenAI integration
- [x] Comprehensive type hints and documentation
- [x] Error handling and input validation

### In Progress
- [ ] Unit tests and test coverage
- [ ] Additional article categories
- [ ] Score tracking and leaderboards
- [ ] Enhanced AI prompt engineering

### Technical Highlights
- **Type Safety**: Full Python type hints for better code reliability
- **Modular Design**: Clean separation of concerns between components
- **Documentation**: Comprehensive docstrings and module documentation
- **Error Handling**: Robust error handling and user feedback

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Report bugs or suggest features by opening an issue
2. Fork the repository and submit a pull request
3. Improve documentation or add more article categories
4. Help improve the AI prompt engineering

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built during the 2025 Hackathon Challenge
- Uses the [Wikipedia-API](https://pypi.org/project/Wikipedia-API/) for article fetching
- AI capabilities powered by OpenAI's API
- Inspired by the need for better media literacy in the digital age
