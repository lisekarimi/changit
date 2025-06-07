"""OpenAI API integration for changit."""

import os

import requests

from src.constants import API_TIMEOUT, CHANGELOG_PROMPT
from src.llm.base import BaseLLM


class OpenAILLM(BaseLLM):
    """OpenAI API implementation for changelog generation."""

    def __init__(self):
        """Initialize OpenAI LLM with API key from environment."""
        super().__init__("openai")
        self.api_key = os.getenv(self.config["env_var"])

    def process_commits(self, commits):
        """Process commits with OpenAI API."""
        if not self.api_key:
            print(f"❌ {self.config['env_var']} not found")
            return None

        commits_text = "\n".join(commits)
        prompt = CHANGELOG_PROMPT.format(commits=commits_text)

        try:
            response = requests.post(
                self.config["api_url"],
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.config["model"],
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1500,
                },
                timeout=API_TIMEOUT,
            )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            elif response.status_code in [401, 403]:
                print("❌ Invalid OpenAI API key")
                return "INVALID_API_KEY"
            else:
                print(f"OpenAI API error: {response.status_code}")
                return None

        except Exception as e:
            print(f"Error calling OpenAI: {e}")
            return None
