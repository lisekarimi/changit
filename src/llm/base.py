"""Base LLM interface and provider selection."""

import os

from src.constants import LLMS


class BaseLLM:
    """Base class for LLM implementations."""

    def __init__(self, llm_type):
        """Initialize LLM with configuration for specified type."""
        self.config = LLMS[llm_type]
        self.name = self.config["name"]

    def process_commits(self, commits):
        """Process commits - to be implemented by subclasses."""
        raise NotImplementedError


def get_available_llm():
    """Get first available LLM based on API keys."""
    # Import here to avoid circular import
    from src.llm.claude import ClaudeLLM
    from src.llm.openai import OpenAILLM

    # Check Claude first
    if os.getenv(LLMS["claude"]["env_var"]):
        return ClaudeLLM()

    # Check OpenAI
    if os.getenv(LLMS["openai"]["env_var"]):
        return OpenAILLM()

    print("❌ No LLM API keys found. Please set one of:")
    for config in LLMS.values():
        print(f"  - {config['env_var']} for {config['name']}")

    return None
