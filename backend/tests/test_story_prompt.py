import json

from app.generation.models import StoryGenerationContext
from app.llm.story_prompt import StoryPromptBuilder


def test_story_prompt_contains_child_context():
    context = StoryGenerationContext(
        child_id="test-child",
        age_band="4-6",
        language="en",
        idea="A tiny star helps a lost firefly",
        interests=["stars", "animals"],
        learning_objective="problem_solving.options",
    )

    prompt = StoryPromptBuilder().build(context)

    data = json.loads(prompt)

    assert data["child"]["age_band"] == "4-6"
    assert data["child"]["language"] == "en"
    assert data["child"]["interests"] == ["stars", "animals"]


def test_story_prompt_contains_story_request():
    context = StoryGenerationContext(
        child_id="test-child",
        age_band="7-8",
        language="ta",
        idea="A rabbit discovers a rainbow",
        learning_objective="problem_solving.options",
    )

    prompt = StoryPromptBuilder().build(context)

    data = json.loads(prompt)

    assert data["story_request"] == "A rabbit discovers a rainbow"
    assert data["learning_objective"] == "problem_solving.options"


def test_story_prompt_contains_safety_requirements():
    context = StoryGenerationContext(
        child_id="test-child",
        age_band="4-6",
        language="en",
        idea="A friendly elephant explores a garden",
        learning_objective="problem_solving.options",
    )

    prompt = StoryPromptBuilder().build(context)

    data = json.loads(prompt)

    requirements = data["requirements"]

    assert "Do not include sexual content." in requirements
    assert "Do not include dangerous instructions." in requirements
    assert "Do not encourage secrecy from parents." in requirements


def test_story_prompt_requires_json_output():
    context = StoryGenerationContext(
        child_id="test-child",
        age_band="4-6",
        language="en",
        idea="A little bird finds a new friend",
        learning_objective="problem_solving.options",
    )

    prompt = StoryPromptBuilder().build(context)

    data = json.loads(prompt)

    instruction = data["output_format"]["instruction"]

    assert "valid JSON" in instruction
    assert "KADHAI Story Pydantic schema" in instruction