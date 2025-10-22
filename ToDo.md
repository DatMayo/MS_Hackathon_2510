# Code Refactoring and Improvement Plan

## Type Safety and Code Quality
- [x] Add return type hints to all methods in `game_ui.py`
- [x] Fix return type hint in `ai_gen.py`'s `generate()` method to match actual return (ArticleModel | None)
- [x] Add return type hints to `get_random_article()` in `local_article.py`
- [x] Fix `count(ArticlesLocal.local_articles == 0)` to `len(ArticlesLocal.local_articles) == 0` in `local_article.py`
- [x] Simplify `check_answer()` in `game_ui.py` to a one-liner
- [x] Fix typo in variable name `concatinated_summary` in `wiki_article.py`

## Error Handling
- [x] Add input validation for user selections in `game_ui.py`
- [x] Add retry logic for API failures in `ai_gen.py`
- [x] Add error handling for Wikipedia API failures in `wiki_article.py`
- [x] Add error handling for file operations in `local_article.py`
- [x] Add proper error handling for JSON parsing in `local_article.py`

## Code Organization
- [x] Move `main()` from `ai_gen.py` to a separate test file
- [ ] Implement singleton pattern in `local_article.py` instead of static methods
- [ ] ~~Move hardcoded categories in `category.py` to a configuration file~~
- [ ] Create a common base class/interface for `wiki_article.py` and `local_article.py`
- [ ] Move duplicate input validation logic in `game_ui.py` to a helper method

## Performance Improvements
- [ ] Implement caching for Wikipedia API responses in `wiki_article.py`
- [x] Load articles only once in `local_article.py`
- [ ] Add lazy loading for articles in `local_article.py`
- [ ] Implement proper singleton pattern to prevent multiple loads

## Configuration
- [ ] Make OpenAI model name configurable in `ai_gen.py`
- [ ] Make Wikipedia language configurable in `wiki_article.py`
- [ ] Move API keys and other sensitive data to environment variables
- [ ] Add configuration validation

## Testing
- [ ] Add unit tests for all classes and methods
- [ ] Add integration tests for game flow
- [ ] Add mock tests for external API calls
- [ ] Add end-to-end tests for the complete application

## Documentation
- [x] Add docstrings to all public methods
- [x] Add module-level docstrings
- [ ] Document the expected JSON structure for `responses.json`
- [x] Add a README with setup and usage instructions

## Security
- [ ] Remove API key exposure in error messages in `ai_gen.py`
- [ ] Add input validation for JSON in `local_article.py`
- [ ] Add rate limiting for API calls
- [ ] Add input sanitization for user inputs

## Code Quality
- [x] Add text wrapping for console output to improve readability
- [ ] Replace print statements with proper logging
- [ ] Add type checking with mypy
- [ ] Add code formatting with black
- [ ] Add linting with flake8 or pylint
- [ ] Add pre-commit hooks for code quality checks

## Features
- [ ] Add difficulty levels
- [ ] Add score tracking
- [ ] Add multiplayer support
- [ ] Add more categories and articles
- [ ] Add a web interface

## Technical Debt
- [ ] Remove commented code
- [ ] Fix TODOs in the codebase
- [ ] Update dependencies
- [ ] Add version compatibility checks
