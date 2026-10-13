from __future__ import annotations

from app.llm.base import LLMProvider


class MockLLMProvider(LLMProvider):
    """
    Development provider used when no external LLM is configured.

    This keeps KADHAI runnable without a paid API.
    """

    def generate(self, prompt: str) -> str:
        return '{"status": "mock_response"}'