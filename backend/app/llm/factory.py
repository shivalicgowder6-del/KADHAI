from __future__ import annotations

from app.llm.base import LLMProvider
from app.llm.config import LLMConfig
from app.llm.mock_provider import MockLLMProvider
from app.llm.ollama_provider import OllamaProvider


def create_llm_provider(config: LLMConfig | None = None) -> LLMProvider:
    """
    Create the configured LLM provider.

    KADHAI supports:
    - mock: deterministic provider for tests
    - ollama: local Ollama model
    """
    config = config or LLMConfig()

    if config.provider == "mock":
        return MockLLMProvider()

    if config.provider == "ollama":
        return OllamaProvider(
            model=config.model,
        )

    raise ValueError(
        f"Unsupported KADHAI LLM provider: {config.provider}"
    )