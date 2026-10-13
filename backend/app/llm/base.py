from __future__ import annotations

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """
    Common interface for any language model used by KADHAI.

    The rest of the application should depend on this interface,
    not on a specific AI provider.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a response from the language model.
        """
        raise NotImplementedError