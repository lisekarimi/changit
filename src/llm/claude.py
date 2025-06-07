"""Claude API integration for changit."""

import os

import requests

from src.constants import API_TIMEOUT, CHANGELOG_PROMPT
from src.llm.base import BaseLLM


class ClaudeLLM(BaseLLM):
    """Claude API implementation for changelog generation."""

    def __init__(self):
        """Initialize Claude LLM with API key from environment."""
        super().__init__("claude")
        self.api_key = os.getenv(self.config["env_var"])

    def process_commits(self, commits):
        """Process commits with Claude API."""
        if not self.api_key:
            print(f"❌ {self.config['env_var']} not found")
            return None

        commits_text = "\n".join(commits)
        prompt = CHANGELOG_PROMPT.format(commits=commits_text)

        try:
            response = requests.post(
                self.config["api_url"],
                headers={"x-api-key": self.api_key, **self.config["headers"]},
                json={
                    "model": self.config["model"],
                    "max_tokens": 1500,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=API_TIMEOUT,
            )

            if response.status_code == 200:
                return response.json()["content"][0]["text"]
            elif response.status_code in [401, 403]:
                print("❌ Invalid Claude API key")
                return "INVALID_API_KEY"
            else:
                print(f"Claude API error: {response.status_code}")
                return None

        except Exception as e:
            print(f"Error calling Claude: {e}")
            return None
