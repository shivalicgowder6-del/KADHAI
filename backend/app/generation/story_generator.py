
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
    """Generates a structured KADHAI story in six languages."""

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

        scenes = self._create_scenes(context, character)

        return Story(
            story_id=story_id,
            title=self._create_title(context),
            age_band=context.age_band,
            languages=["en", "ta", "hi", "ml", "kn", "te"],
            learning_objectives=[context.learning_objective],
            story_bible=story_bible,
            scenes=scenes,
        )

    def _create_story_id(self, idea: str) -> str:
        words = re.findall(r"[a-zA-Z0-9]+", idea.lower())

        if not words:
            return "generated-story"

        return f"generated-{'-'.join(words[:5])}"

    def _create_title(
        self,
        context: StoryGenerationContext,
    ) -> LocalizedText:
        return LocalizedText(
            en="The Little Forest Adventure",
            ta="சிறிய காட்டு சாகசம்",
            hi="जंगल का छोटा रोमांच",
            ml="കാട്ടിലെ ചെറിയ സാഹസികയാത്ര",
            kn="ಕಾಡಿನ ಪುಟ್ಟ ಸಾಹസ",
            te="చిన్న అడవి సాహసం",
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
                        "and noticed something unusual. What could it be?"
                    ),
                    ta=(
                        "ஒரு சிறிய நண்பன் அமைதியான காட்டில் நடந்து சென்றபோது "
                        "வித்தியாசமான ஒன்றைக் கவனித்தான். அது என்னவாக இருக்கும்?"
                    ),
                    hi=(
                        "एक छोटा दोस्त शांत जंगल में टहल रहा था। "
                        "तभी उसे कुछ अनोखा दिखाई दिया। वह क्या हो सकता है?"
                    ),
                    ml=(
                        "ഒരു ചെറിയ കൂട്ടുകാരൻ ശാന്തമായ കാട്ടിലൂടെ നടക്കുമ്പോൾ "
                        "വിചിത്രമായ ഒന്നിനെ കണ്ടു. അത് എന്തായിരിക്കും?"
                    ),
                    kn=(
                        "ಒಬ್ಬ ಪುಟ್ಟ ಗೆಳೆಯನು ಶಾಂತವಾದ ಕಾಡಿನಲ್ಲಿ ನಡೆಯುತ್ತಿದ್ದಾಗ "
                        "ಒಂದು ವಿಚಿತ್ರವಾದದ್ದನ್ನು ಗಮನಿಸಿದನು. ಅದು ಏನಿರಬಹುದು?"
                    ),
                    te=(
                        "ఒక చిన్న స్నేహితుడు ప్రశాంతమైన అడవిలో నడుస్తూ "
                        "ఒక వింత విషయాన్ని గమనించాడు. అది ఏమై ఉండవచ్చు?"
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
                    hi=(
                        "छोटा दोस्त एक छोटी नदी के पास पहुँचा। "
                        "आगे बढ़ने के लिए दो रास्ते थे।"
                    ),
                    ml=(
                        "ചെറിയ കൂട്ടുകാരൻ ഒരു ചെറിയ അരുവിയുടെ അരികിലെത്തി. "
                        "മുന്നോട്ട് പോകാൻ രണ്ട് വഴികളുണ്ടായിരുന്നു."
                    ),
                    kn=(
                        "ಪುಟ್ಟ ಗೆಳೆಯನು ಒಂದು ಚಿಕ್ಕ ತೊರೆಯ ಬಳಿಗೆ ಬಂದನು. "
                        "ಮುಂದುವರಿಯಲು ಎರಡು ದಾರಿಗಳಿದ್ದವು."
                    ),
                    te=(
                        "చిన్న స్నేహితుడు ఒక చిన్న వాగు దగ్గరకు చేరుకున్నాడు. "
                        "ముందుకు సాగడానికి రెండు మార్గాలు ఉన్నాయి."
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
                                hi="किसी दोस्त से मदद माँगें",
                                ml="ഒരു കൂട്ടുകാരനോട് സഹായം ചോദിക്കാം",
                                kn="ಒಬ್ಬ ಗೆಳೆಯನ ಸಹಾಯ ಕೇಳೋಣ",
                                te="ఒక స్నేహితుడి సహాయం అడుగుదాం",
                            ),
                            next_scene="n3a",
                        ),
                        InteractionOption(
                            id="explore",
                            label=LocalizedText(
                                en="Look for another way",
                                ta="வேறு வழியைத் தேடலாம்",
                                hi="दूसरा रास्ता खोजें",
                                ml="മറ്റൊരു വഴി അന്വേഷിക്കാം",
                                kn="ಬೇರೆ ದಾರಿಯನ್ನು ಹುಡುಕೋಣ",
                                te="మరో మార్గాన్ని వెతుకుదాం",
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
                        "The little friend asked for help. Together, "
                        "they found a safe way across the stream. "
                        "Solving problems can be easier when we work together."
                    ),
                    ta=(
                        "சிறிய நண்பன் உதவி கேட்டான். அவர்கள் சேர்ந்து "
                        "ஓடையைப் பாதுகாப்பாகக் கடக்க ஒரு வழியைக் கண்டுபிடித்தார்கள். "
                        "ஒன்றாகச் செயல்பட்டால் பிரச்சினைகளைத் தீர்ப்பது எளிதாகும்."
                    ),
                    hi=(
                        "छोटे दोस्त ने मदद माँगी। दोनों ने मिलकर "
                        "नदी पार करने का सुरक्षित रास्ता खोज लिया। "
                        "मिलकर काम करने से समस्याएँ हल करना आसान होता है।"
                    ),
                    ml=(
                        "ചെറിയ കൂട്ടുകാരൻ സഹായം ചോദിച്ചു. ഇരുവരും ചേർന്ന് "
                        "അരുവി സുരക്ഷിതമായി കടക്കാനുള്ള വഴി കണ്ടെത്തി. "
                        "ഒരുമിച്ച് പ്രവർത്തിച്ചാൽ പ്രശ്നങ്ങൾ പരിഹരിക്കാൻ എളുപ്പമാണ്."
                    ),
                    kn=(
                        "ಪುಟ್ಟ ಗೆಳೆಯನು ಸಹಾಯ ಕೇಳಿದನು. ಇಬ್ಬರೂ ಸೇರಿ "
                        "ತೊರೆಯನ್ನು ಸುರಕ್ಷಿತವಾಗಿ ದಾಟುವ ದಾರಿಯನ್ನು ಕಂಡುಕೊಂಡರು. "
                        "ಒಟ್ಟಾಗಿ ಕೆಲಸ ಮಾಡಿದರೆ ಸಮಸ್ಯೆಗಳನ್ನು ಪರಿಹರಿಸುವುದು ಸುಲಭ."
                    ),
                    te=(
                        "చిన్న స్నేహితుడు సహాయం అడిగాడు. ఇద్దరూ కలిసి "
                        "వాగును సురక్షితంగా దాటే మార్గాన్ని కనుగొన్నారు. "
                        "కలిసి పనిచేస్తే సమస్యలను పరిష్కరించడం సులభం."
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
                        "சில நேரங்களில் புதிய வழி நல்ல தீர்வுக்கு அழைத்துச் செல்லும்."
                    ),
                    hi=(
                        "छोटे दोस्त ने सावधानी से दूसरा रास्ता खोजा "
                        "और एक छोटा लकड़ी का पुल पाया। "
                        "कभी-कभी नया रास्ता अच्छा समाधान दे सकता है।"
                    ),
                    ml=(
                        "ചെറിയ കൂട്ടുകാരൻ ശ്രദ്ധയോടെ മറ്റൊരു വഴി അന്വേഷിച്ച് "
                        "ഒരു ചെറിയ മരപ്പാലം കണ്ടെത്തി. "
                        "ചിലപ്പോൾ പുതിയൊരു വഴി നല്ല പരിഹാരത്തിലേക്ക് നയിക്കും."
                    ),
                    kn=(
                        "ಪುಟ್ಟ ಗೆಳೆಯನು ಎಚ್ಚರಿಕೆಯಿಂದ ಬೇರೆ ದಾರಿಯನ್ನು ಹುಡುಕಿ "
                        "ಒಂದು ಚಿಕ್ಕ ಮರದ ಸೇತುವೆಯನ್ನು ಕಂಡುಕೊಂಡನು. "
                        "ಕೆಲವೊಮ್ಮೆ ಹೊಸ ದಾರಿ ಒಳ್ಳೆಯ ಪರಿಹಾರಕ್ಕೆ ಕರೆದೊಯ್ಯುತ್ತದೆ."
                    ),
                    te=(
                        "చిన్న స్నేహితుడు జాగ్రత్తగా మరో దారిని వెతికి "
                        "ఒక చిన్న చెక్క వంతెనను కనుగొన్నాడు. "
                        "కొన్నిసార్లు కొత్త మార్గం మంచి పరిష్కారాన్ని చూపిస్తుంది."
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
