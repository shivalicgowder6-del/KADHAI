from __future__ import annotations

from app.generation.models import StoryGenerationContext
from app.llm.base import LLMProvider
from app.llm.story_parser import StoryParser
from app.llm.story_prompt import StoryPromptBuilder
from app.models.story import Story


class AIStoryGenerator:
    """
    Generates a validated KADHAI Story through an LLM provider.

    The LLM is responsible for generation.
    The StoryParser is responsible for structural validation.
    """

    def __init__(
        self,
        provider: LLMProvider,
        prompt_builder: StoryPromptBuilder | None = None,
        parser: StoryParser | None = None,
    ) -> None:
        self.provider = provider
        self.prompt_builder = prompt_builder or StoryPromptBuilder()
        self.parser = parser or StoryParser()

    def generate(self, context: StoryGenerationContext) -> Story:
        prompt = self.prompt_builder.build(context)

        raw_response = self.provider.generate(prompt)

        return self.parser.parse(raw_response)