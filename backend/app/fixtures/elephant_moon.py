
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
        hi="चाँद देखना चाहने वाला हाथी",
        ml="ചന്ദ്രനെ കാണാൻ ആഗ്രഹിച്ച ആന",
        kn="ಚಂದ್ರನನ್ನು ನೋಡಲು ಬಯಸಿದ ಆನೆ",
        te="చంద్రుడిని చూడాలనుకున్న ఏనుగు",
    ),
    age_band="4-6",
    languages=["en", "ta", "hi", "ml", "kn", "te"],
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
                    "யானை எல்லி இலைகளுக்கிடையே ஒரு மென்மையான வெள்ளி "
                    "ஒளியைப் பார்த்தாள். 'அது என்ன?' என்று அவள் யோசித்தாள். "
                    "'நான் அதை நன்றாகப் பார்க்க விரும்புகிறேன்.'"
                ),
                hi=(
                    "हाथी ऐली ने पत्तों के बीच से ऊपर देखा और चाँदी जैसी "
                    "नरम रोशनी देखी। उसने सोचा, 'यह क्या है?' "
                    "वह उसे अच्छी तरह देखना चाहती थी।"
                ),
                ml=(
                    "ആനയായ എല്ലി ഇലകൾക്കിടയിലൂടെ മുകളിലേക്ക് നോക്കിയപ്പോൾ "
                    "വെള്ളിനിറമുള്ള മൃദുവായ വെളിച്ചം കണ്ടു. "
                    "'അതെന്താണ്?' എന്ന് അവൾ ചിന്തിച്ചു. "
                    "'എനിക്ക് അത് നന്നായി കാണണം.'"
                ),
                kn=(
                    "ಆನೆ ಎಲ್ಲೀ ಎಲೆಗಳ ನಡುವೆ ಮೇಲಕ್ಕೆ ನೋಡಿದಾಗ ಬೆಳ್ಳಿಯಂತಹ "
                    "ಮೃದುವಾದ ಬೆಳಕನ್ನು ಕಂಡಳು. 'ಅದು ಏನು?' ಎಂದು ಅವಳು "
                    "ಯೋಚಿಸಿದಳು. 'ನಾನು ಅದನ್ನು ಚೆನ್ನಾಗಿ ನೋಡಬೇಕು.'"
                ),
                te=(
                    "ఏనుగు ఎల్లీ ఆకుల మధ్య నుంచి పైకి చూసి వెండి వంటి "
                    "మృదువైన వెలుగును చూసింది. 'అది ఏమిటి?' అని "
                    "ఆమె అనుకుంది. 'నేను దాన్ని బాగా చూడాలి.'"
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
                    "எல்லி நடந்து ஒரு பரந்த ஆற்றை அடைந்தாள். மறுபுறம் "
                    "வானம் தெளிவாக இருந்தது, நிலவு காத்திருந்தது. "
                    "ஆனால் பழைய பாலம் உடைந்திருந்தது."
                ),
                hi=(
                    "ऐली चलते-चलते एक चौड़ी नदी के पास पहुँची। "
                    "दूसरी ओर आसमान साफ़ था और चाँद दिखाई दे रहा था। "
                    "लेकिन पुराना पुल टूटा हुआ था।"
                ),
                ml=(
                    "എല്ലി നടന്ന് വിശാലമായ ഒരു നദിക്കരയിലെത്തി. "
                    "മറുവശത്ത് ആകാശം തെളിഞ്ഞിരുന്നു, ചന്ദ്രൻ കാത്തിരിക്കുന്നതുപോലെ "
                    "തോന്നി. പക്ഷേ പഴയ പാലം തകർന്നിരുന്നു."
                ),
                kn=(
                    "ಎಲ್ಲೀ ನಡೆದು ಒಂದು ವಿಶಾಲವಾದ ನದಿಯನ್ನು ತಲುಪಿದಳು. "
                    "ಇನ್ನೊಂದು ದಡದಲ್ಲಿ ಆಕಾಶ ಸ್ಪಷ್ಟವಾಗಿತ್ತು ಮತ್ತು ಚಂದ್ರನು "
                    "ಕಾಣಿಸುತ್ತಿದ್ದನು. ಆದರೆ ಹಳೆಯ ಸೇತುವೆ ಮುರಿದಿತ್ತು."
                ),
                te=(
                    "ఎల్లీ నడుచుకుంటూ ఒక విశాలమైన నది దగ్గరకు చేరుకుంది. "
                    "అవతలి వైపు ఆకాశం నిర్మలంగా ఉంది, చంద్రుడు కనిపిస్తున్నాడు. "
                    "కానీ పాత వంతెన విరిగిపోయింది."
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
                            hi="पक्षियों से मदद माँगो",
                            ml="പക്ഷികളോട് സഹായം ചോദിക്കുക",
                            kn="ಪಕ್ಷಿಗಳ ಸಹಾಯ ಕೇಳು",
                            te="పక్షులను సహాయం అడుగు",
                        ),
                        next_scene="n3a",
                    ),
                    InteractionOption(
                        id="find_path",
                        label=LocalizedText(
                            en="Look for another path",
                            ta="வேறு வழியைத் தேடு",
                            hi="दूसरा रास्ता ढूँढ़ो",
                            ml="മറ്റൊരു വഴി കണ്ടെത്തുക",
                            kn="ಬೇರೆ ದಾರಿಯನ್ನು ಹುಡುಕು",
                            te="మరో దారిని వెతుకు",
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
                    "எல்லி கூப்பிட்டாள். நட்பான பறவைகள் சிறு குச்சிகளைக் "
                    "கொண்டு வந்து பாலத்தைச் சரிசெய்தன. அவர்கள் இணைந்து "
                    "கடந்தனர். எல்லி இறுதியாக வட்டமான, பிரகாசமான நிலவைப் பார்த்தாள்."
                ),
                hi=(
                    "ऐली ने आवाज़ लगाई। दोस्ताना पक्षी छोटी-छोटी टहनियाँ "
                    "लेकर आए और पुल की मरम्मत करने लगे। सबने मिलकर नदी पार की। "
                    "आखिरकार ऐली ने गोल और चमकता चाँद देखा।"
                ),
                ml=(
                    "എല്ലി വിളിച്ചു. സൗഹൃദമുള്ള പക്ഷികൾ ചെറിയ ചില്ലകൾ "
                    "കൊണ്ടുവന്ന് പാലം നന്നാക്കി. എല്ലാവരും ഒരുമിച്ച് നദി കടന്നു. "
                    "ഒടുവിൽ എല്ലി വട്ടത്തിലും തിളക്കത്തിലും മനോഹരമായ ചന്ദ്രനെ കണ്ടു."
                ),
                kn=(
                    "ಎಲ್ಲೀ ಕೂಗಿದಳು. ಸ್ನೇಹಪರ ಪಕ್ಷಿಗಳು ಚಿಕ್ಕ ಕೊಂಬೆಗಳನ್ನು "
                    "ತಂದು ಸೇತುವೆಯನ್ನು ಸರಿಪಡಿಸಿದವು. ಎಲ್ಲರೂ ಒಟ್ಟಿಗೆ ನದಿ ದಾಟಿದರು. "
                    "ಕೊನೆಗೆ ಎಲ್ಲೀ ದುಂಡಗಿನ, ಹೊಳೆಯುವ ಚಂದ್ರನನ್ನು ಕಂಡಳು."
                ),
                te=(
                    "ఎల్లీ పిలిచింది. స్నేహపూర్వకమైన పక్షులు చిన్న కొమ్మలను "
                    "తీసుకొచ్చి వంతెనను బాగుచేశాయి. అందరూ కలిసి నది దాటారు. "
                    "చివరకు ఎల్లీ గుండ్రంగా మెరిసే చంద్రుడిని చూసింది."
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
                    "எல்லி ஆற்றின் கரையோரம் சென்று ஆழம் குறைந்த, "
                    "மென்மையான கடவைக் கண்டுபிடித்தாள். அவள் கவனமாக அதைக் "
                    "கடந்தாள். மறுபுறம், நிலவு அவள் நினைத்ததை விடப் பெரியதாக இருந்தது."
                ),
                hi=(
                    "ऐली नदी के किनारे चलती रही और उसे एक उथली, शांत जगह "
                    "मिली जहाँ से नदी पार की जा सकती थी। वह सावधानी से पानी "
                    "में उतरी और पार चली गई। दूसरी ओर चाँद उसकी कल्पना से भी बड़ा था।"
                ),
                ml=(
                    "എല്ലി നദിക്കരയിലൂടെ നടന്ന് ആഴം കുറഞ്ഞ, ശാന്തമായ ഒരു "
                    "കടവിലെത്തി. അവൾ സൂക്ഷിച്ച് വെള്ളത്തിലൂടെ നടന്ന് മറുകരയിലെത്തി. "
                    "അവിടെ ചന്ദ്രൻ അവൾ കരുതിയതിലും വലുതായിരുന്നു."
                ),
                kn=(
                    "ಎಲ್ಲೀ ನದಿಯ ದಡದ ಮೂಲಕ ನಡೆದು ಆಳವಿಲ್ಲದ, ಶಾಂತವಾದ ಒಂದು "
                    "ದಾಟುವ ಸ್ಥಳವನ್ನು ಕಂಡಳು. ಅವಳು ಎಚ್ಚರಿಕೆಯಿಂದ ನೀರಿನಲ್ಲಿ ನಡೆದು "
                    "ನದಿಯನ್ನು ದಾಟಿದಳು. ಇನ್ನೊಂದು ದಡದಲ್ಲಿ ಚಂದ್ರನು ಅವಳು ಊಹಿಸಿದ್ದಕ್ಕಿಂತ ದೊಡ್ಡದಾಗಿದ್ದನು."
                ),
                te=(
                    "ఎల్లీ నది ఒడ్డున నడుస్తూ లోతు తక్కువగా ఉన్న ప్రశాంతమైన "
                    "దాటే ప్రదేశాన్ని కనుగొంది. ఆమె జాగ్రత్తగా నీటిలో నడిచి "
                    "అవతలి ఒడ్డుకు చేరుకుంది. అక్కడ చంద్రుడు ఆమె ఊహించినదానికంటే పెద్దగా కనిపించాడు."
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
