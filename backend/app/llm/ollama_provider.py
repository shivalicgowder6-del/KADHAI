
from __future__ import annotations

import ollama

from app.llm.base import LLMProvider


class OllamaProvider(LLMProvider):
    def __init__(
        self,
        model: str = "qwen2.5:3b",
        host: str = "http://localhost:11434",
        timeout: float = 90.0,
    ) -> None:
        self.model = model
        self.client = ollama.Client(
            host=host,
            timeout=timeout,
        )

    def generate(self, prompt: str) -> str:
        response = self.client.generate(
            model=self.model,
            prompt=prompt,
        )
        return response.response
