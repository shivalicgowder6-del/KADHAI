"""Story lookup by story_id.

Phase 1A only has the one hand-written fixture, but this is the single seam
where Phase 5 (LLM-generated, published story packages) will plug in without
touching the API layer or the session engine at all.
"""

from __future__ import annotations

from app.fixtures.elephant_moon import ELEPHANT_MOON
from app.models.story import Story

_STORIES: dict[str, Story] = {
    ELEPHANT_MOON.story_id: ELEPHANT_MOON,
}


def get_story(story_id: str) -> Story | None:
    return _STORIES.get(story_id)


def list_stories() -> list[Story]:
    return list(_STORIES.values())
