import json

import pytest

from app.llm.story_parser import StoryParseError, StoryParser


def valid_story_data() -> dict:
    return {
        "story_id": "test-story",
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


def test_parser_returns_valid_story():
    raw_response = json.dumps(valid_story_data())

    story = StoryParser().parse(raw_response)

    assert story.story_id == "test-story"
    assert story.age_band == "4-6"
    assert len(story.scenes) == 2


def test_parser_rejects_empty_response():
    with pytest.raises(StoryParseError, match="empty"):
        StoryParser().parse("")


def test_parser_rejects_invalid_json():
    with pytest.raises(StoryParseError, match="not valid JSON"):
        StoryParser().parse("This is not JSON")


def test_parser_rejects_invalid_story_schema():
    data = valid_story_data()
    del data["story_bible"]

    with pytest.raises(StoryParseError, match="does not match"):
        StoryParser().parse(json.dumps(data))