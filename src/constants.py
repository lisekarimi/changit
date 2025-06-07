"""Configuration constants for changit."""

# LLM Configuration
LLMS = {
    "claude": {
        "name": "Claude 3.5 Sonnet",
        "env_var": "ANTHROPIC_API_KEY",
        "model": "claude-3-5-sonnet-20241022",
        "api_url": "https://api.anthropic.com/v1/messages",
        "headers": {
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    },
    "openai": {
        "name": "OpenAI GPT-4o",
        "env_var": "OPENAI_API_KEY",
        "model": "gpt-4o",
        "api_url": "https://api.openai.com/v1/chat/completions",
    },
}

# Git Configuration
GIT_LOG_FORMAT = "--oneline --no-merges"
GIT_BRANCH = "main"

# Changelog Configuration
CHANGELOG_FILE = "CHANGELOG.md"

# API Configuration
API_TIMEOUT = 30
MAX_TOKENS = 1500

# Prompt Template
CHANGELOG_PROMPT = """Please categorize these git commits into a clean changelog format.

Git commits:
{commits}

Please organize them into these categories with emojis:

### ✨ Added
- New features or functionality

### 🔄 Changed
- Changes to existing functionality

### 🐛 Fixed
- Bug fixes

### 🗑️ Removed
- Removed features

Rules:
- Remove commit hashes and technical prefixes
- Make descriptions clear for end users
- Only include categories that have items
- Be concise but descriptive
- Use ### for category headers with emojis
- Do not add explanations or notes
- Return only the categorized content
"""
