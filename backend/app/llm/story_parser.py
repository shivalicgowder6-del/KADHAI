from __future__ import annotations

import json

from pydantic import ValidationError

from app.models.story import Story


class StoryParseError(ValueError):
    """Raised when an LLM response cannot become a valid KADHAI Story."""


class StoryParser:
    """
    Converts raw LLM output into a validated KADHAI Story.

    The LLM output is treated as untrusted data.
    Pydantic validation is the structural source of truth.
    """

    def parse(self, raw_response: str) -> Story:
        if not raw_response.strip():
            raise StoryParseError("LLM response is empty.")

        try:
            data = json.loads(raw_response)
        except json.JSONDecodeError as exc:
            raise StoryParseError(
                f"LLM response is not valid JSON: {exc.msg}"
            ) from exc

        try:
            return Story.model_validate(data)
        except ValidationError as exc:
            raise StoryParseError(
                f"LLM response does not match the KADHAI Story schema: {exc}"
            ) from exc