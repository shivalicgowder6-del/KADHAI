from fastapi import APIRouter, HTTPException

from app.services.story_registry import get_story

router = APIRouter(prefix="/api/stories", tags=["stories"])


@router.get("/fixture-elephant-moon")
def get_elephant_moon_story():
    """Kept as an explicit, stable route for backward compatibility with
    Phase 1's original endpoint, in addition to the generic /{story_id}
    route below."""
    story = get_story("fixture-elephant-moon")
    if story is None:
        raise HTTPException(status_code=404, detail="story not found")
    return story.model_dump()


@router.get("/{story_id}")
def get_story_by_id(story_id: str):
    story = get_story(story_id)
    if story is None:
        raise HTTPException(status_code=404, detail=f"story '{story_id}' not found")
    return story.model_dump()
