
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


SupportedLanguage = Literal["en", "ta", "hi", "ml", "kn", "te"]


class ChildProfile(BaseModel):
    """
    Minimal child context used for age-adaptive story generation.
    """

    child_id: str
    age: int = Field(ge=4, le=8)
    language: SupportedLanguage
    interests: list[str] = Field(default_factory=list)


class StoryGenerationRequest(BaseModel):
    """
    Input received when KADHAI needs to generate a new story.
    """

    child: ChildProfile
    idea: str = Field(min_length=1, max_length=500)
    learning_objective: str | None = None
    preferred_language: SupportedLanguage | None = None


class StoryGenerationContext(BaseModel):
    """
    Normalized context passed from the planner to the story generator.
    """

    child_id: str
    age_band: Literal["4-6", "7-8"]
    language: SupportedLanguage
    idea: str
    interests: list[str] = Field(default_factory=list)
    learning_objective: str
