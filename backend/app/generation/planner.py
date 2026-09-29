from __future__ import annotations

from app.generation.models import (
    StoryGenerationContext,
    StoryGenerationRequest,
)


DEFAULT_LEARNING_OBJECTIVE = "problem_solving.options"


class StoryPlanner:
    """
    Converts a raw story-generation request into normalized
    generation context.

    The planner is deterministic. It does not generate the story.
    """

    def determine_age_band(self, age: int) -> str:
        if age <= 6:
            return "4-6"

        return "7-8"

    def determine_language(
        self,
        request: StoryGenerationRequest,
    ) -> str:
        return request.preferred_language or request.child.language

    def determine_learning_objective(
        self,
        request: StoryGenerationRequest,
    ) -> str:
        if request.learning_objective:
            return request.learning_objective

        return DEFAULT_LEARNING_OBJECTIVE

    def plan(
        self,
        request: StoryGenerationRequest,
    ) -> StoryGenerationContext:
        age_band = self.determine_age_band(request.child.age)

        language = self.determine_language(request)

        learning_objective = self.determine_learning_objective(
            request
        )

        return StoryGenerationContext(
            child_id=request.child.child_id,
            age_band=age_band,
            language=language,
            idea=request.idea.strip(),
            interests=request.child.interests,
            learning_objective=learning_objective,
        )