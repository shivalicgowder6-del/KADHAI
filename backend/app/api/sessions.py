from fastapi import APIRouter, HTTPException

from app.models.story import Scene
from app.schemas.session import (
    CreateSessionRequest,
    SceneOut,
    SessionOut,
    SessionWithSceneOut,
    TurnRequest,
    TurnResponse,
)
from app.services import session_engine
from app.services.session_store import SessionState

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


def _session_out(session: SessionState) -> SessionOut:
    return SessionOut(
        session_id=session.session_id,
        child_id=session.child_id,
        story_id=session.story_id,
        language=session.language,
        current_scene_id=session.current_scene_id,
        choices=session.choices,
        started_at=session.started_at,
        completed_at=session.completed_at,
    )


def _scene_out(scene: Scene) -> SceneOut:
    return SceneOut(
        scene_id=scene.scene_id,
        narration=scene.narration,
        visual_prompt=scene.visual_prompt,
        characters=scene.characters,
        interaction=scene.interaction,
        is_ending=scene.is_ending,
    )


@router.post("", response_model=SessionWithSceneOut)
def create_session(request: CreateSessionRequest):
    try:
        session, scene = session_engine.start_session(
            story_id=request.story_id,
            child_id=request.child_id,
            language=request.language,
        )
    except session_engine.StoryNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return SessionWithSceneOut(session=_session_out(session), scene=_scene_out(scene))


@router.get("/{session_id}", response_model=SessionOut)
def get_session(session_id: str):
    try:
        session = session_engine.get_session_state(session_id)
    except session_engine.SessionNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _session_out(session)


@router.get("/{session_id}/state", response_model=SceneOut)
def get_session_state(session_id: str):
    try:
        scene = session_engine.get_current_scene(session_id)
    except session_engine.SessionNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except session_engine.StoryNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _scene_out(scene)


@router.post("/{session_id}/turns", response_model=TurnResponse)
def take_turn(session_id: str, request: TurnRequest):
    try:
        session, scene = session_engine.advance(session_id, request.option_id)
    except session_engine.SessionNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except session_engine.StoryNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except session_engine.SessionAlreadyCompletedError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except session_engine.InvalidChoiceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return TurnResponse(session=_session_out(session), scene=_scene_out(scene))
