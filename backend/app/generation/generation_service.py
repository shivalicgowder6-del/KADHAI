from __future__ import annotations

from app.generation.models import StoryGenerationRequest
from app.generation.planner import StoryPlanner
from app.generation.story_generator import StoryGenerator
from app.llm.ai_story_generator import AIStoryGenerator
from app.llm.factory import create_llm_provider
from app.models.story import Story
from app.safety.categories import SafetyDecision
from app.safety.safety_service import SafetyService


class GenerationResult:
    """
    Result returned by the generation orchestration layer.
    """

    def __init__(
        self,
        *,
        decision: SafetyDecision,
        story: Story | None = None,
        safe_response: str | None = None,
        used_ai: bool = False,
    ) -> None:
        self.decision = decision
        self.story = story
        self.safe_response = safe_response
        self.used_ai = used_ai


class StoryGenerationService:
    """
    Orchestrates KADHAI story generation.

    Pipeline:
        Safety → Planning → AI Generation → Validation

    If AI generation fails, the deterministic generator is used
    as a fallback so the application remains available.
    """

    def __init__(
        self,
        safety_service: SafetyService | None = None,
        planner: StoryPlanner | None = None,
        generator: StoryGenerator | None = None,
        ai_generator: AIStoryGenerator | None = None,
    ) -> None:
        self.safety_service = safety_service or SafetyService()
        self.planner = planner or StoryPlanner()
        self.generator = generator or StoryGenerator()

        self.ai_generator = ai_generator or AIStoryGenerator(
            provider=create_llm_provider()
        )

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

        try:
            story = self.ai_generator.generate(context)

            return GenerationResult(
                decision=SafetyDecision.ALLOW,
                story=story,
                used_ai=True,
            )

        except Exception:
            story = self.generator.generate(context)

            return GenerationResult(
                decision=SafetyDecision.ALLOW,
                story=story,
                used_ai=False,
            )