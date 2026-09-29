from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ChildProfile(BaseModel):
    """
    Minimal child context used for age-adaptive story generation.

    We intentionally keep this small in the MVP.
    The learner model will be expanded later.
    """

    child_id: str
    age: int = Field(ge=4, le=8)
    language: Literal["en", "ta"]
    interests: list[str] = Field(default_factory=list)


class StoryGenerationRequest(BaseModel):
    """
    Input received when KADHAI needs to generate a new story.
    """

    child: ChildProfile

    idea: str = Field(min_length=1, max_length=500)

    learning_objective: str | None = None

    preferred_language: Literal["en", "ta"] | None = None


class StoryGenerationContext(BaseModel):
    """
    Normalized context passed from the planner to the story generator.

    At this point, safety has already been checked.
    """

    child_id: str
    age_band: Literal["4-6", "7-8"]
    language: Literal["en", "ta"]
    idea: str
    interests: list[str] = Field(default_factory=list)
    learning_objective: str