"""In-memory session state storage.

Phase 1A has no database yet (that's Phase 9/Supabase), so sessions live in a
process-local dict. This is intentionally the only place that knows sessions
are stored in memory — swapping this for a real DB-backed store later should
not require touching the API routes or the session engine logic.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class SessionState(BaseModel):
    session_id: str
    child_id: Optional[str] = None
    story_id: str
    language: str
    current_scene_id: str
    choices: list[str] = Field(default_factory=list)
    started_at: datetime
    completed_at: Optional[datetime] = None


_SESSIONS: dict[str, SessionState] = {}


def create_session(story_id: str, first_scene_id: str, child_id: Optional[str], language: str) -> SessionState:
    session = SessionState(
        session_id=str(uuid4()),
        child_id=child_id,
        story_id=story_id,
        language=language,
        current_scene_id=first_scene_id,
        started_at=datetime.now(timezone.utc),
    )
    _SESSIONS[session.session_id] = session
    return session


def get_session(session_id: str) -> Optional[SessionState]:
    return _SESSIONS.get(session_id)


def save_session(session: SessionState) -> None:
    _SESSIONS[session.session_id] = session


def clear_all() -> None:
    """Test-only helper to reset state between test runs."""
    _SESSIONS.clear()
