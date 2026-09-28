"""
The Phase 1 fixture story.

This is deliberately hand-written, not LLM-generated — the whole point of
this phase is to prove the schema, the player state machine, and the video
pipeline work with data we know is correct, before we add an LLM that might
hand us data that *looks* correct but isn't.

Shape: n1 (setup, linear) -> n2 (branch point, one choice) -> n3a or n3b
(both endings). Both endings resolve the same premise (Ellie sees the moon)
through a different path, which is the smallest possible example of
"choice changes the story without needing unbounded branching."
"""

from app.models.story import (
    Character,
    Interaction,
    InteractionOption,
    LocalizedText,
    Scene,
    Story,
    StoryBible,
)

ELEPHANT_MOON = Story(
    story_id="fixture-elephant-moon",
    title=LocalizedText(
        en="The Elephant Who Wanted to See the Moon",
        ta="நிலவைப் பார்க்க விரும்பிய யானை",
    ),
    age_band="4-6",
    languages=["en", "ta"],
    learning_objectives=["problem_solving.options"],
    story_bible=StoryBible(
        characters=[
            Character(
                id="ellie",
                appearance="small grey elephant with a blue scarf",
                personality="curious, gentle",
            )
        ],
        setting="a quiet forest at dusk, leading to a river",
        established_facts=["Ellie has never seen the moon before"],
    ),
    scenes=[
        Scene(
            scene_id="n1",
            narration=LocalizedText(
                en=(
                    "Ellie the elephant looked up through the leaves and saw "
                    "a soft silver light. 'What is that?' she wondered. "
                    "'I want to see it properly.'"
                ),
                ta=(
                    "யானை எல்லி இலைகளுக்கிடையே ஒரு மென்மையான வெள்ளி ஒளியைப் "
                    "பார்த்தாள். 'அது என்ன?' என்று அவள் யோசித்தாள். 'நான் "
                    "அதை நன்றாகப் பார்க்க விரும்புகிறேன்.'"
                ),
            ),
            visual_prompt=(
                "a small grey elephant with a blue scarf looking up through "
                "forest leaves at moonlight, dusk, gentle storybook illustration"
            ),
            characters=["ellie"],
            next_scene="n2",
        ),
        Scene(
            scene_id="n2",
            narration=LocalizedText(
                en=(
                    "Ellie walked until she reached a wide river. On the "
                    "other side, the sky was clear and the moon was "
                    "waiting. But the old bridge was broken."
                ),
                ta=(
                    "எல்லி நடந்து ஒரு பரந்த ஆற்றை அடைந்தாள். மறுபுறம் வானம் "
                    "தெளிவாக இருந்தது, நிலவு காத்திருந்தது. ஆனால் பழைய "
                    "பாலம் உடைந்திருந்தது."
                ),
            ),
            visual_prompt=(
                "small grey elephant with a blue scarf standing before a "
                "wide river with a broken wooden bridge, evening sky"
            ),
            characters=["ellie"],
            interaction=Interaction(
                template="choice",
                skill_ids=["problem_solving.options"],
                options=[
                    InteractionOption(
                        id="ask_help",
                        label=LocalizedText(
                            en="Ask the birds for help",
                            ta="பறவைகளிடம் உதவி கேள்",
                        ),
                        next_scene="n3a",
                    ),
                    InteractionOption(
                        id="find_path",
                        label=LocalizedText(
                            en="Look for another path",
                            ta="வேறு வழியைத் தேடு",
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
                    "Ellie called out, and a flock of friendly birds "
                    "carried little twigs to patch the bridge. Together, "
                    "they crossed. Ellie finally saw the moon, round and "
                    "bright."
                ),
                ta=(
                    "எல்லி கூப்பிட்டாள், நட்பான பறவைகள் சிறு குச்சிகளைக் "
                    "கொண்டு வந்து பாலத்தைச் சரிசெய்தன. அவர்கள் இணைந்து "
                    "கடந்தனர். எல்லி இறுதியாக வட்டமான, பிரகாசமான நிலவைப் "
                    "பார்த்தாள்."
                ),
            ),
            visual_prompt=(
                "small grey elephant crossing a repaired wooden bridge with "
                "birds flying alongside, full moon rising, warm night sky"
            ),
            characters=["ellie"],
            is_ending=True,
        ),
        Scene(
            scene_id="n3b",
            narration=LocalizedText(
                en=(
                    "Ellie followed the riverbank until she found a "
                    "shallow, gentle crossing. She waded across carefully. "
                    "On the other side, the moon was even bigger than she "
                    "imagined."
                ),
                ta=(
                    "எல்லி ஆற்றின் கரையோரம் சென்று ஒரு ஆழம் குறைந்த, "
                    "மென்மையான கடவைக் கண்டுபிடித்தாள். அவள் கவனமாக அதைக் "
                    "கடந்தாள். மறுபுறம், நிலவு அவள் நினைத்ததை விட "
                    "பெரியதாக இருந்தது."
                ),
            ),
            visual_prompt=(
                "small grey elephant wading across a shallow river "
                "crossing, large bright moon reflected in the water"
            ),
            characters=["ellie"],
            is_ending=True,
        ),
    ],
)
