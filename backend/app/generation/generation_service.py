from __future__ import annotations

from app.generation.models import StoryGenerationRequest
from app.generation.planner import StoryPlanner
from app.generation.story_generator import StoryGenerator
from app.models.story import Story
from app.safety.categories import SafetyDecision
from app.safety.safety_service import SafetyService


class GenerationResult:
    """
    Result returned by the generation orchestration layer.

    A story is returned only when the input passes the safety gateway.
    """

    def __init__(
        self,
        *,
        decision: SafetyDecision,
        story: Story | None = None,
        safe_response: str | None = None,
    ) -> None:
        self.decision = decision
        self.story = story
        self.safe_response = safe_response


class StoryGenerationService:
    """
    Orchestrates the complete story-generation pipeline.

    Safety is checked before planning and generation.
    """

    def __init__(
        self,
        safety_service: SafetyService | None = None,
        planner: StoryPlanner | None = None,
        generator: StoryGenerator | None = None,
    ) -> None:
        self.safety_service = safety_service or SafetyService()
        self.planner = planner or StoryPlanner()
        self.generator = generator or StoryGenerator()

    def generate(
        self,
        request: StoryGenerationRequest,
    ) -> GenerationResult:
        safety_result = self.safety_service.check(request.idea)

        if safety_result.decision != SafetyDecision.ALLOW:
            return GenerationResult(
                decision=safety_result.decision,
                safe_response=safety_result.safe_response,
            )

        context = self.planner.plan(request)

        story = self.generator.generate(context)

        return GenerationResult(
            decision=SafetyDecision.ALLOW,
            story=story,
        )