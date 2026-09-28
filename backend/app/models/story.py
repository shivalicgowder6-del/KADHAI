"""
The KADHAI story graph schema.

This is the single most important file in the whole project. Every story —
whether we hand-write it (like the fixture in app/fixtures/elephant_moon.py)
or an LLM generates it later — must satisfy this schema. That's the point:
we're not trusting the LLM to produce a well-formed graph, we're *checking*
that it did, the same way we check this hand-written one.

Two kinds of rules live here, and it's worth noticing the difference:

1. Structural rules Pydantic enforces automatically just from the type
   annotations (a Scene must have a scene_id that's a string, an Interaction
   must have at least... well, we enforce that one explicitly below).
2. Graph-integrity rules we have to write ourselves, because Pydantic has no
   way to know that "next_scene points at a scene_id that actually exists"
   without us telling it to check.

The `model_validator` methods below are all rule #2. If you delete them,
every individual field still validates fine, but you could build a story
where a choice option points at scene "n99" that doesn't exist — and you'd
only find out when a child hit that choice and the player crashed. That's
exactly the class of bug we want to catch at *publish* time, not *play* time.
"""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator


class LocalizedText(BaseModel):
    """Every piece of child-facing text is bilingual from day one.

    We could have made `language` a top-level story field and stored one
    language per story, but that would mean generating and validating each
    language as a completely separate story graph — double the LLM calls,
    double the safety checks, and no guarantee the two versions even have
    the same branch structure. Storing both languages on every text field
    means one story graph, one validation pass, two languages for free.
    """

    en: str
    ta: str


class InteractionOption(BaseModel):
    id: str
    label: LocalizedText
    next_scene: str


class Interaction(BaseModel):
    # Phase 1 only implements "choice". Counting, emotion-pick, etc. are
    # added the same way later: new Literal value, new Pydantic model,
    # nothing else in this file changes.
    template: Literal["choice"]
    skill_ids: list[str] = Field(default_factory=list)
    options: list[InteractionOption]

    @model_validator(mode="after")
    def must_have_at_least_two_options(self) -> "Interaction":
        if len(self.options) < 2:
            raise ValueError("a choice interaction needs at least 2 options")
        return self


class Character(BaseModel):
    id: str
    appearance: str
    personality: str


class StoryBible(BaseModel):
    """The fixed facts every generation call gets handed, so the elephant
    doesn't change color between scene 1 and scene 4."""

    characters: list[Character]
    setting: str
    established_facts: list[str] = Field(default_factory=list)


class Scene(BaseModel):
    scene_id: str
    narration: LocalizedText
    visual_prompt: str
    characters: list[str] = Field(default_factory=list)
    interaction: Optional[Interaction] = None
    next_scene: Optional[str] = None
    is_ending: bool = False

    @model_validator(mode="after")
    def must_have_exactly_one_way_out(self) -> "Scene":
        """A scene is one of three things, never a combination:
        - an ending (no interaction, no next_scene)
        - a linear beat (next_scene set, no interaction)
        - a branch point (interaction set, no next_scene — the branch
          options themselves carry the next_scene)
        """
        has_interaction = self.interaction is not None
        has_next = self.next_scene is not None

        if self.is_ending:
            if has_interaction or has_next:
                raise ValueError(
                    f"scene '{self.scene_id}': is_ending=True but also has "
                    f"an interaction or next_scene — an ending must have neither"
                )
        elif has_interaction == has_next:
            # both True (ambiguous exit) or both False (dead end) are invalid
            raise ValueError(
                f"scene '{self.scene_id}': must have exactly one of "
                f"next_scene or interaction, or be marked is_ending"
            )
        return self


class Story(BaseModel):
    story_id: str
    title: LocalizedText
    age_band: Literal["4-6", "7-8"]
    languages: list[str]
    learning_objectives: list[str] = Field(default_factory=list)
    story_bible: StoryBible
    scenes: list[Scene]

    @model_validator(mode="after")
    def every_reference_must_point_at_a_real_scene(self) -> "Story":
        """The check that matters most. A Scene on its own has no way to
        know whether the scene_id it points to exists elsewhere in the
        list — only the full Story object can see the whole graph."""
        scene_ids = {s.scene_id for s in self.scenes}

        for scene in self.scenes:
            if scene.next_scene is not None and scene.next_scene not in scene_ids:
                raise ValueError(
                    f"scene '{scene.scene_id}': next_scene "
                    f"'{scene.next_scene}' does not exist in this story"
                )
            if scene.interaction is not None:
                for option in scene.interaction.options:
                    if option.next_scene not in scene_ids:
                        raise ValueError(
                            f"scene '{scene.scene_id}': option "
                            f"'{option.id}' points to missing scene "
                            f"'{option.next_scene}'"
                        )
        return self

    @model_validator(mode="after")
    def scene_ids_must_be_unique(self) -> "Story":
        ids = [s.scene_id for s in self.scenes]
        if len(ids) != len(set(ids)):
            duplicates = {i for i in ids if ids.count(i) > 1}
            raise ValueError(f"duplicate scene_id(s): {duplicates}")
        return self
