from __future__ import annotations

from pydantic import BaseModel, Field

from app.safety.categories import SafetyCategory, SafetyDecision


class SafetyResult(BaseModel):
    """Structured result returned by the KADHAI safety gateway."""

    decision: SafetyDecision
    category: SafetyCategory
    reason: str
    safe_response: str | None = None
    matched_rules: list[str] = Field(default_factory=list)


class SafetyEvent(BaseModel):
    """Safety event that can later be persisted for monitoring and auditing."""

    input_text: str
    decision: SafetyDecision
    category: SafetyCategory
    reason: str
    matched_rules: list[str] = Field(default_factory=list)
