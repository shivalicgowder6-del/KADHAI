from __future__ import annotations

import os


class LLMConfig:
    """
    Configuration for the KADHAI language-model layer.

    No API key is required when using the MockLLMProvider.
    """

    def __init__(self) -> None:
        self.provider = os.getenv("KADHAI_LLM_PROVIDER", "mock")
        self.api_key = os.getenv("KADHAI_LLM_API_KEY")
        self.model = os.getenv(
            "KADHAI_LLM_MODEL",
            "default",
        )

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key)