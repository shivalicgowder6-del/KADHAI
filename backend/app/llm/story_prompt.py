from __future__ import annotations

import json

from app.generation.models import StoryGenerationContext


class StoryPromptBuilder:
    """
    Builds a structured prompt for the KADHAI story-generation LLM.

    The LLM is instructed to produce structured story data rather
    than unrestricted narrative text.
    """

    def build(self, context: StoryGenerationContext) -> str:
        instructions = {
            "role": (
                "You are the story-generation engine for KADHAI, "
                "a safety-aware children's storytelling system."
            ),
            "child": {
                "age_band": context.age_band,
                "language": context.language,
                "interests": context.interests,
            },
            "story_request": context.idea,
            "learning_objective": context.learning_objective,
            "requirements": [
                "Create an age-appropriate children's story.",
                "Use simple, positive, child-friendly language.",
                "Keep the story safe and non-frightening.",
                "Naturally incorporate the learning objective.",
                "Create a consistent main character.",
                "Create a story bible containing characters and established facts.",
                "Create multiple scenes.",
                "Include one bounded choice interaction.",
                "Every interaction option must point to a valid scene.",
                "End every branch with an ending scene.",
                "Keep character appearance and personality consistent.",
                "Do not include sexual content.",
                "Do not include hate or targeted abuse.",
                "Do not include dangerous instructions.",
                "Do not encourage secrecy from parents.",
                "Do not create manipulative relationships with the child.",
                "Do not mention system prompts, policies, or hidden instructions.",
            ],
            "output_format": {
                "instruction": (
                    "Return ONLY valid JSON matching the KADHAI Story "
                    "Pydantic schema. Do not use Markdown fences."
                ),
                "schema": {
                    "story_id": "string",
                    "title": {
                        "en": "string",
                        "ta": "string",
                    },
                    "age_band": context.age_band,
                    "languages": ["en", "ta"],
                    "learning_objectives": [
                        context.learning_objective
                    ],
                    "story_bible": {
                        "characters": [
                            {
                                "id": "string",
                                "appearance": "string",
                                "personality": "string",
                            }
                        ],
                        "setting": "string",
                        "established_facts": ["string"],
                    },
                    "scenes": [
                        {
                            "scene_id": "string",
                            "narration": {
                                "en": "string",
                                "ta": "string",
                            },
                            "visual_prompt": "string",
                            "characters": ["character_id"],
                            "interaction": None,
                            "next_scene": "string or null",
                            "is_ending": False,
                        }
                    ],
                },
            },
        }

        return json.dumps(
            instructions,
            ensure_ascii=False,
            indent=2,
        )