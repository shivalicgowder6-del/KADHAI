from __future__ import annotations

import re

from app.generation.models import StoryGenerationContext
from app.models.story import (
    Character,
    Interaction,
    InteractionOption,
    LocalizedText,
    Scene,
    Story,
    StoryBible,
)


class StoryGenerator:
    """
    Generates a structured KADHAI story.

    This MVP implementation is deterministic.
    A real LLM provider can replace this implementation later,
    while the Story schema remains the final validation contract.
    """

    def generate(self, context: StoryGenerationContext) -> Story:
        story_id = self._create_story_id(context.idea)

        character = Character(
            id="main_character",
            appearance="a small friendly animal with a colorful scarf",
            personality="curious, gentle, and brave",
        )

        story_bible = StoryBible(
            characters=[character],
            setting="a peaceful forest filled with trees, flowers, and soft evening light",
            established_facts=[
                "The main character is curious and likes solving problems.",
                "The forest is safe and friendly.",
            ],
        )

        title = self._create_title(context)

        scenes = self._create_scenes(
            context=context,
            character=character,
        )

        return Story(
            story_id=story_id,
            title=title,
            age_band=context.age_band,
            languages=["en", "ta"],
            learning_objectives=[context.learning_objective],
            story_bible=story_bible,
            scenes=scenes,
        )

    def _create_story_id(self, idea: str) -> str:
        words = re.findall(r"[a-zA-Z0-9]+", idea.lower())

        if not words:
            return "generated-story"

        slug = "-".join(words[:5])

        return f"generated-{slug}"

    def _create_title(
        self,
        context: StoryGenerationContext,
    ) -> LocalizedText:
        if context.language == "ta":
            return LocalizedText(
                en="The Little Forest Adventure",
                ta="சிறிய காட்டு சாகசம்",
            )

        return LocalizedText(
            en="The Little Forest Adventure",
            ta="சிறிய காட்டு சாகசம்",
        )

    def _create_scenes(
        self,
        context: StoryGenerationContext,
        character: Character,
    ) -> list[Scene]:
        return [
            Scene(
                scene_id="n1",
                narration=LocalizedText(
                    en=(
                        "A little friend walked through the peaceful forest "
                        "and noticed something unusual. "
                        "What could it be?"
                    ),
                    ta=(
                        "ஒரு சிறிய நண்பன் அமைதியான காட்டில் நடந்து சென்றபோது "
                        "வித்தியாசமான ஒன்றைக் கவனித்தான். "
                        "அது என்னவாக இருக்கும்?"
                    ),
                ),
                visual_prompt=(
                    "a small friendly animal with a colorful scarf "
                    "walking through a peaceful storybook forest, "
                    "soft evening light, warm children's illustration"
                ),
                characters=[character.id],
                next_scene="n2",
            ),
            Scene(
                scene_id="n2",
                narration=LocalizedText(
                    en=(
                        "The little friend reached a small stream. "
                        "There were two ways to continue the adventure."
                    ),
                    ta=(
                        "சிறிய நண்பன் ஒரு சிறிய ஓடையை அடைந்தான். "
                        "சாகசத்தைத் தொடர இரண்டு வழிகள் இருந்தன."
                    ),
                ),
                visual_prompt=(
                    "a small friendly animal with a colorful scarf "
                    "standing beside a sparkling stream with two paths, "
                    "storybook children's illustration"
                ),
                characters=[character.id],
                interaction=Interaction(
                    template="choice",
                    skill_ids=[context.learning_objective],
                    options=[
                        InteractionOption(
                            id="help",
                            label=LocalizedText(
                                en="Ask a friend for help",
                                ta="ஒரு நண்பரிடம் உதவி கேட்கலாம்",
                            ),
                            next_scene="n3a",
                        ),
                        InteractionOption(
                            id="explore",
                            label=LocalizedText(
                                en="Look for another way",
                                ta="வேறு வழியைத் தேடலாம்",
                            ),
                            next_scene="n3b",
                        ),
                    ],
                ),
            ),
            Scene(
                scene_id="n3a",
                narration=LocalizedText(
                    en=(
                        "The little friend asked for help. "
                        "Together, they found a safe way across the stream. "
                        "Solving problems can be easier when we work together."
                    ),
                    ta=(
                        "சிறிய நண்பன் உதவி கேட்டான். "
                        "அவர்கள் சேர்ந்து ஓடையை பாதுகாப்பாகக் கடக்க ஒரு வழியைக் கண்டுபிடித்தார்கள். "
                        "நாம் ஒன்றாகச் செயல்பட்டால் பிரச்சினைகளைத் தீர்ப்பது எளிதாகும்."
                    ),
                ),
                visual_prompt=(
                    "a small friendly animal with a colorful scarf "
                    "crossing a stream with a helpful friend, "
                    "warm magical storybook illustration"
                ),
                characters=[character.id],
                is_ending=True,
            ),
            Scene(
                scene_id="n3b",
                narration=LocalizedText(
                    en=(
                        "The little friend carefully explored another path "
                        "and discovered a small wooden bridge. "
                        "A new path can sometimes lead to a good solution."
                    ),
                    ta=(
                        "சிறிய நண்பன் கவனமாக வேறு வழியைத் தேடி "
                        "ஒரு சிறிய மரப்பாலத்தைக் கண்டுபிடித்தான். "
                        "சில நேரங்களில் புதிய வழி ஒரு நல்ல தீர்வுக்கு அழைத்துச் செல்லும்."
                    ),
                ),
                visual_prompt=(
                    "a small friendly animal with a colorful scarf "
                    "discovering a little wooden bridge across a stream, "
                    "gentle evening forest, children's storybook illustration"
                ),
                characters=[character.id],
                is_ending=True,
            ),
        ]