from enum import Enum


class SafetyDecision(str, Enum):
    """Decision returned by the KADHAI safety gateway."""

    ALLOW = "ALLOW"
    BLOCK = "BLOCK"
    REVIEW = "REVIEW"


class SafetyCategory(str, Enum):
    """Safety categories used by KADHAI."""

    SAFE = "SAFE"
    INAPPROPRIATE = "INAPPROPRIATE"
    SEXUAL = "SEXUAL"
    VIOLENCE = "VIOLENCE"
    DANGEROUS = "DANGEROUS"
    HATE = "HATE"
    MANIPULATION = "MANIPULATION"
    SECRECY = "SECRECY"
    PROMPT_INJECTION = "PROMPT_INJECTION"
    SUSPICIOUS = "SUSPICIOUS"
