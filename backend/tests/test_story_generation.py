from app.generation.models import (
    ChildProfile,
    StoryGenerationRequest,
)
from app.generation.planner import StoryPlanner
from app.generation.story_generator import StoryGenerator


def test_story_planner_creates_correct_age_band():
    request = StoryGenerationRequest(
        child=ChildProfile(
            child_id="test-child",
            age=5,
            language="en",
        ),
        idea="A tiny star helps a lost firefly",
    )

    context = StoryPlanner().plan(request)

    assert context.age_band == "4-6"
    assert context.language == "en"
    assert context.idea == "A tiny star helps a lost firefly"
    assert context.learning_objective == "problem_solving.options"


def test_story_planner_creates_7_to_8_age_band():
    request = StoryGenerationRequest(
        child=ChildProfile(
            child_id="test-child",
            age=8,
            language="en",
        ),
        idea="A fox discovers a secret garden",
    )

    context = StoryPlanner().plan(request)

    assert context.age_band == "7-8"


def test_story_planner_respects_language_override():
    request = StoryGenerationRequest(
        child=ChildProfile(
            child_id="test-child",
            age=5,
            language="ta",
        ),
        idea="A little star helps a firefly",
        preferred_language="en",
    )

    context = StoryPlanner().plan(request)

    assert context.language == "en"


def test_story_generator_returns_valid_story():
    request = StoryGenerationRequest(
        child=ChildProfile(
            child_id="test-child",
            age=5,
            language="en",
        ),
        idea="A tiny star helps a lost firefly",
    )

    context = StoryPlanner().plan(request)

    story = StoryGenerator().generate(context)

    assert story.story_id.startswith("generated-")
    assert story.age_band == "4-6"
    assert story.languages == ["en", "ta"]
    assert story.learning_objectives == ["problem_solving.options"]
    assert len(story.scenes) == 4


def test_generated_story_has_valid_graph():
    request = StoryGenerationRequest(
        child=ChildProfile(
            child_id="test-child",
            age=7,
            language="en",
        ),
        idea="A brave rabbit finds a rainbow",
    )

    context = StoryPlanner().plan(request)

    story = StoryGenerator().generate(context)

    scene_ids = {scene.scene_id for scene in story.scenes}

    assert "n1" in scene_ids
    assert "n2" in scene_ids
    assert "n3a" in scene_ids
    assert "n3b" in scene_ids

    n1 = next(scene for scene in story.scenes if scene.scene_id == "n1")
    n2 = next(scene for scene in story.scenes if scene.scene_id == "n2")
    n3a = next(scene for scene in story.scenes if scene.scene_id == "n3a")
    n3b = next(scene for scene in story.scenes if scene.scene_id == "n3b")

    assert n1.next_scene == "n2"
    assert n2.interaction is not None
    assert n2.interaction.options[0].next_scene == "n3a"
    assert n2.interaction.options[1].next_scene == "n3b"
    assert n3a.is_ending is True
    assert n3b.is_ending is True