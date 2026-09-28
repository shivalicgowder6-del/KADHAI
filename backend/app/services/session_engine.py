"""Deterministic story session state machine.

No LLM involved: this module purely walks the Story graph that has already
been validated by app.models.story. Given a scene and a child's choice, there
is exactly one correct next scene, and this module is the only place that
decides it.
"""

from __future__ import annotations

from datetime import datetime, timezone

from app.models.story import Scene, Story
from app.services import session_store
from app.services.session_store import SessionState
from app.services.story_registry import get_story


class SessionEngineError(Exception):
    """Base class for engine errors that API routes translate to HTTP codes."""


class StoryNotFoundError(SessionEngineError):
    pass


class SessionNotFoundError(SessionEngineError):
    pass


class SessionAlreadyCompletedError(SessionEngineError):
    pass


class InvalidChoiceError(SessionEngineError):
    pass


def _scene_by_id(story: Story, scene_id: str) -> Scene:
    for scene in story.scenes:
        if scene.scene_id == scene_id:
            return scene
    # Unreachable if the story passed Story's own validators, but guards
    # against future bugs rather than crashing with a bare KeyError.
    raise SessionEngineError(f"scene '{scene_id}' not found in story '{story.story_id}'")


def start_session(story_id: str, child_id: str | None, language: str) -> tuple[SessionState, Scene]:
    story = get_story(story_id)
    if story is None:
        raise StoryNotFoundError(f"story '{story_id}' does not exist")

    first_scene = story.scenes[0]
    session = session_store.create_session(
        story_id=story_id,
        first_scene_id=first_scene.scene_id,
        child_id=child_id,
        language=language,
    )
    return session, first_scene


def get_session_state(session_id: str) -> SessionState:
    session = session_store.get_session(session_id)
    if session is None:
        raise SessionNotFoundError(f"session '{session_id}' does not exist")
    return session


def get_current_scene(session_id: str) -> Scene:
    session = get_session_state(session_id)
    story = get_story(session.story_id)
    if story is None:
        raise StoryNotFoundError(f"story '{session.story_id}' does not exist")
    return _scene_by_id(story, session.current_scene_id)


def advance(session_id: str, option_id: str | None) -> tuple[SessionState, Scene]:
    session = get_session_state(session_id)

    if session.completed_at is not None:
        raise SessionAlreadyCompletedError(f"session '{session_id}' is already completed")

    story = get_story(session.story_id)
    if story is None:
        raise StoryNotFoundError(f"story '{session.story_id}' does not exist")

    current_scene = _scene_by_id(story, session.current_scene_id)

    if current_scene.is_ending:
        raise SessionAlreadyCompletedError(f"session '{session_id}' is already completed")

    if current_scene.interaction is not None:
        # Branch point: option_id is required and must be one of the
        # closed-set options. The LLM never decides this — the graph does.
        if option_id is None:
            raise InvalidChoiceError(
                f"scene '{current_scene.scene_id}' requires an option_id"
            )
        option = next(
            (o for o in current_scene.interaction.options if o.id == option_id),
            None,
        )
        if option is None:
            raise InvalidChoiceError(
                f"'{option_id}' is not a valid option for scene '{current_scene.scene_id}'"
            )
        next_scene_id = option.next_scene
        session.choices.append(option_id)
    else:
        # Linear beat: no option_id expected, next_scene is fixed.
        if option_id is not None:
            raise InvalidChoiceError(
                f"scene '{current_scene.scene_id}' is linear and does not accept an option_id"
            )
        next_scene_id = current_scene.next_scene

    next_scene = _scene_by_id(story, next_scene_id)
    session.current_scene_id = next_scene.scene_id
    if next_scene.is_ending:
        session.completed_at = datetime.now(timezone.utc)

    session_store.save_session(session)
    return session, next_scene
