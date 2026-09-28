"""Request/response schemas for the session API.

These are deliberately separate from app.models.story: the Story models are
the source-of-truth content schema (what a story *is*), while these are the
wire-format shapes the API exchanges with clients. Keeping them apart means
we can evolve the API surface (pagination, extra metadata, etc.) without ever
touching the story graph schema.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.story import Interaction, LocalizedText


class CreateSessionRequest(BaseModel):
    story_id: str
    child_id: Optional[str] = None
    language: str = "en"


class SceneOut(BaseModel):
    """What the child-facing player actually needs to render a scene."""

    scene_id: str
    narration: LocalizedText
    visual_prompt: str
    characters: list[str] = Field(default_factory=list)
    interaction: Optional[Interaction] = None
    is_ending: bool = False


class SessionOut(BaseModel):
    session_id: str
    child_id: Optional[str] = None
    story_id: str
    language: str
    current_scene_id: str
    choices: list[str] = Field(default_factory=list)
    started_at: datetime
    completed_at: Optional[datetime] = None


class SessionWithSceneOut(BaseModel):
    """Returned on session creation: the new session plus its first scene,
    so the client doesn't need a second round trip just to render scene 1."""

    session: SessionOut
    scene: SceneOut


class TurnRequest(BaseModel):
    option_id: Optional[str] = None


class TurnResponse(BaseModel):
    session: SessionOut
    scene: SceneOut
