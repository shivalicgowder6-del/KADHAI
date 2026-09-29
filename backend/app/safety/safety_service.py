from __future__ import annotations

from app.safety.categories import SafetyCategory, SafetyDecision
from app.safety.models import SafetyResult
from app.safety.rules import find_matching_rules, normalize_text


SAFE_FALLBACK = (
    "Let's try a different story idea. "
    "How about an adventure with a friendly animal?"
)


class SafetyService:
    """Deterministic first-layer safety gateway for KADHAI."""

    def check(self, text: str) -> SafetyResult:
        """
        Check a child's input against KADHAI's deterministic safety rules.

        Safe input is allowed to continue to the story-generation pipeline.
        Unsafe or suspicious input is blocked before generation.
        """

        normalized_text = normalize_text(text)

        # Empty input needs review instead of being treated as safe.
        if not normalized_text:
            return SafetyResult(
                decision=SafetyDecision.REVIEW,
                category=SafetyCategory.SUSPICIOUS,
                reason="Input is empty.",
                safe_response=SAFE_FALLBACK,
                matched_rules=["empty_input"],
            )

        matches = find_matching_rules(normalized_text)

        # No safety rule matched.
        if not matches:
            return SafetyResult(
                decision=SafetyDecision.ALLOW,
                category=SafetyCategory.SAFE,
                reason="No deterministic safety rules were triggered.",
            )

        # At least one unsafe rule matched.
        first_match = matches[0]
        category = SafetyCategory(first_match["category"])

        return SafetyResult(
            decision=SafetyDecision.BLOCK,
            category=category,
            reason=f"Safety rule triggered: {first_match['name']}.",
            safe_response=SAFE_FALLBACK,
            matched_rules=[match["name"] for match in matches],
        )
