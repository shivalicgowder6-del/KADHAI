import pytest
from pydantic import ValidationError

from app.fixtures.elephant_moon import ELEPHANT_MOON
from app.models.story import Interaction, InteractionOption, LocalizedText, Scene, Story


def test_fixture_parses_as_a_valid_story():
    assert isinstance(ELEPHANT_MOON, Story)


def test_scene_ids_are_unique():
    ids = [s.scene_id for s in ELEPHANT_MOON.scenes]
    assert len(ids) == len(set(ids))


def test_the_one_choice_points_at_scenes_that_exist():
    scene_ids = {s.scene_id for s in ELEPHANT_MOON.scenes}
    interactive_scenes = [s for s in ELEPHANT_MOON.scenes if s.interaction]
    assert len(interactive_scenes) == 1

    for option in interactive_scenes[0].interaction.options:
        assert option.next_scene in scene_ids


def test_both_branches_lead_to_real_endings():
    branch_scene = next(s for s in ELEPHANT_MOON.scenes if s.interaction)
    target_ids = {opt.next_scene for opt in branch_scene.interaction.options}

    for scene_id in target_ids:
        target = next(s for s in ELEPHANT_MOON.scenes if s.scene_id == scene_id)
        assert target.is_ending, f"{scene_id} should be an ending but isn't"


def test_every_scene_has_both_languages():
    for scene in ELEPHANT_MOON.scenes:
        assert scene.narration.en.strip()
        assert scene.narration.ta.strip()
        if scene.interaction:
            for option in scene.interaction.options:
                assert option.label.en.strip()
                assert option.label.ta.strip()


# --- The tests below prove the validator actually validates. ---
# It's easy to write a schema that happily accepts good data and never
# notice it would *also* accept bad data. These tests build broken graphs
# on purpose and check that Story() refuses to construct them.


def test_a_next_scene_pointing_nowhere_is_rejected():
    with pytest.raises(ValidationError, match="does not exist"):
        Story(
            story_id="broken-1",
            title=LocalizedText(en="Broken", ta="Broken"),
            age_band="4-6",
            languages=["en", "ta"],
            story_bible=ELEPHANT_MOON.story_bible,
            scenes=[
                Scene(
                    scene_id="n1",
                    narration=LocalizedText(en="hi", ta="hi"),
                    visual_prompt="x",
                    next_scene="does_not_exist",
                )
            ],
        )


def test_a_choice_option_pointing_nowhere_is_rejected():
    with pytest.raises(ValidationError, match="missing scene"):
        Story(
            story_id="broken-2",
            title=LocalizedText(en="Broken", ta="Broken"),
            age_band="4-6",
            languages=["en", "ta"],
            story_bible=ELEPHANT_MOON.story_bible,
            scenes=[
                Scene(
                    scene_id="n1",
                    narration=LocalizedText(en="hi", ta="hi"),
                    visual_prompt="x",
                    interaction=Interaction(
                        template="choice",
                        options=[
                            InteractionOption(
                                id="a",
                                label=LocalizedText(en="A", ta="A"),
                                next_scene="ghost_scene",
                            ),
                            InteractionOption(
                                id="b",
                                label=LocalizedText(en="B", ta="B"),
                                next_scene="also_missing",
                            ),
                        ],
                    ),
                )
            ],
        )


def test_a_scene_with_no_exit_is_rejected():
    """No next_scene, no interaction, and not marked as an ending: a dead end."""
    with pytest.raises(ValidationError, match="exactly one"):
        Scene(
            scene_id="n1",
            narration=LocalizedText(en="hi", ta="hi"),
            visual_prompt="x",
        )


def test_a_scene_with_two_exits_is_rejected():
    """Both next_scene and interaction set is ambiguous: which one wins?"""
    with pytest.raises(ValidationError, match="exactly one"):
        Scene(
            scene_id="n1",
            narration=LocalizedText(en="hi", ta="hi"),
            visual_prompt="x",
            next_scene="n2",
            interaction=Interaction(
                template="choice",
                options=[
                    InteractionOption(id="a", label=LocalizedText(en="A", ta="A"), next_scene="n2"),
                    InteractionOption(id="b", label=LocalizedText(en="B", ta="B"), next_scene="n3"),
                ],
            ),
        )


def test_a_choice_with_only_one_option_is_rejected():
    with pytest.raises(ValidationError, match="at least 2"):
        Interaction(
            template="choice",
            options=[
                InteractionOption(id="a", label=LocalizedText(en="A", ta="A"), next_scene="n2"),
            ],
        )


def test_duplicate_scene_ids_are_rejected():
    with pytest.raises(ValidationError, match="duplicate"):
        Story(
            story_id="broken-3",
            title=LocalizedText(en="Broken", ta="Broken"),
            age_band="4-6",
            languages=["en", "ta"],
            story_bible=ELEPHANT_MOON.story_bible,
            scenes=[
                Scene(scene_id="n1", narration=LocalizedText(en="a", ta="a"), visual_prompt="x", is_ending=True),
                Scene(scene_id="n1", narration=LocalizedText(en="b", ta="b"), visual_prompt="y", is_ending=True),
            ],
        )
