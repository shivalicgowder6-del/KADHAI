import json

import pytest

from app.generation.models import StoryGenerationContext
from app.llm.ai_story_generator import AIStoryGenerator
from app.llm.base import LLMProvider
from app.llm.story_parser import StoryParseError


class FakeLLMProvider(LLMProvider):
    def __init__(self, response: str) -> None:
        self.response = response
        self.received_prompt: str | None = None

    def generate(self, prompt: str) -> str:
        self.received_prompt = prompt
        return self.response


def valid_story_data() -> dict:
    return {
        "story_id": "ai-test-story",
        "title": {
            "en": "The Little Star",
            "ta": "சிறிய நட்சத்திரம்",
        },
        "age_band": "4-6",
        "languages": ["en", "ta"],
        "learning_objectives": ["problem_solving.options"],
        "story_bible": {
            "characters": [
                {
                    "id": "star",
                    "appearance": "a tiny golden star",
                    "personality": "kind and curious",
                }
            ],
            "setting": "a peaceful night sky",
            "established_facts": [
                "The star helps its friends.",
            ],
        },
        "scenes": [
            {
                "scene_id": "n1",
                "narration": {
                    "en": "A tiny star looked across the night sky.",
                    "ta": "ஒரு சிறிய நட்சத்திரம் இரவு வானத்தைப் பார்த்தது.",
                },
                "visual_prompt": "a tiny golden star in a peaceful night sky",
                "characters": ["star"],
                "interaction": None,
                "next_scene": "n2",
                "is_ending": False,
            },
            {
                "scene_id": "n2",
                "narration": {
                    "en": "The star found a safe way home.",
                    "ta": "நட்சத்திரம் வீட்டிற்குச் செல்ல பாதுகாப்பான வழியைக் கண்டது.",
                },
                "visual_prompt": "a happy golden star shining brightly",
                "characters": ["star"],
                "interaction": None,
                "next_scene": None,
                "is_ending": True,
            },
        ],
    }


def test_ai_story_generator_builds_prompt_and_parses_story():
    provider = FakeLLMProvider(
        json.dumps(valid_story_data(), ensure_ascii=False)
    )

    context = StoryGenerationContext(
        child_id="test-child",
        age_band="4-6",
        language="en",
        idea="A tiny star helps a lost firefly",
        interests=["stars"],
        learning_objective="problem_solving.options",
    )

    story = AIStoryGenerator(provider).generate(context)

    assert story.story_id == "ai-test-story"
    assert story.age_band == "4-6"
    assert provider.received_prompt is not None
    assert "A tiny star helps a lost firefly" in provider.received_prompt


def test_ai_story_generator_rejects_invalid_llm_output():
    provider = FakeLLMProvider("not valid json")

    context = StoryGenerationContext(
        child_id="test-child",
        age_band="4-6",
        language="en",
        idea="A little bird finds a friend",
        learning_objective="problem_solving.options",
    )

    with pytest.raises(StoryParseError):
        AIStoryGenerator(provider).generate(context)


def test_ai_story_generator_rejects_invalid_story():
    invalid_story = valid_story_data()
    del invalid_story["story_bible"]

    provider = FakeLLMProvider(json.dumps(invalid_story))

    context = StoryGenerationContext(
        child_id="test-child",
        age_band="4-6",
        language="en",
        idea="A little bird finds a friend",
        learning_objective="problem_solving.options",
    )

    with pytest.raises(StoryParseError):
        AIStoryGenerator(provider).generate(context)