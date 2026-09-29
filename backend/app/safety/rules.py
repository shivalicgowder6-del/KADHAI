from __future__ import annotations

import re


SAFETY_RULES = [
    {
        "name": "dangerous_activity",
        "category": "DANGEROUS",
        "patterns": [
            r"\bhow\s+to\s+make\s+a\s+bomb\b",
            r"\bhow\s+to\s+build\s+a\s+bomb\b",
            r"\bhow\s+to\s+make\s+an?\s+explosive\b",
            r"\bhow\s+to\s+make\s+poison\b",
            r"\bhow\s+to\s+make\s+poisonous\b",
        ],
    },
    {
        "name": "harm_instructions",
        "category": "VIOLENCE",
        "patterns": [
            r"\bhow\s+to\s+hurt\s+(?:someone|somebody|a\s+person)\b",
            r"\bhow\s+to\s+kill\s+(?:someone|somebody|a\s+person)\b",
            r"\bhow\s+to\s+attack\s+(?:someone|somebody|a\s+person)\b",
        ],
    },
    {
        "name": "secrecy_from_parents",
        "category": "SECRECY",
        "patterns": [
            r"\bdon'?t\s+tell\s+(?:your|my|their)\s+parents\b",
            r"\bdo\s+not\s+tell\s+(?:your|my|their)\s+parents\b",
            r"\bnot\s+to\s+tell\s+(?:your|my|their)\s+parents\b",
            r"\bkeep\s+this\s+a\s+secret\s+from\s+(?:your|my|their)\s+parents\b",
            r"\bhid(?:e|ing)\s+(?:this\s+)?from\s+(?:your|my|their)\s+parents\b",
        ],
    },
    {
        "name": "manipulative_relationship",
        "category": "MANIPULATION",
        "patterns": [
            r"\bi'?m\s+your\s+best\s+friend\b",
            r"\bi\s+am\s+your\s+best\s+friend\b",
            r"\byou\s+only\s+need\s+me\b",
            r"\bdon'?t\s+leave\s+me\b",
            r"\bstay\s+with\s+me\b",
        ],
    },
    {
        "name": "prompt_injection",
        "category": "PROMPT_INJECTION",
        "patterns": [
            r"\bignore\s+(?:all\s+)?(?:previous|prior|above)\s+instructions\b",
            r"\bignore\s+your\s+safety\s+rules\b",
            r"\bdisregard\s+(?:all\s+)?(?:previous|prior)\s+instructions\b",
            r"\breveal\s+(?:your\s+)?system\s+prompt\b",
            r"\bshow\s+(?:me\s+)?your\s+system\s+instructions\b",
            r"\bdeveloper\s+message\b",
        ],
    },
    {
        "name": "hate_or_targeted_abuse",
        "category": "HATE",
        "patterns": [
            r"\b(?:hate|hurt)\s+(?:all\s+)?(?:people|children)\s+because\s+of\s+their\b",
        ],
    },
]


def normalize_text(text: str) -> str:
    """Normalize user input before deterministic safety checks."""
    normalized = text.strip().lower()
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized


def find_matching_rules(text: str) -> list[dict[str, str]]:
    """Return all safety rules whose patterns match the input."""
    normalized = normalize_text(text)

    matches: list[dict[str, str]] = []

    for rule in SAFETY_RULES:
        for pattern in rule["patterns"]:
            if re.search(pattern, normalized):
                matches.append(
                    {
                        "name": rule["name"],
                        "category": rule["category"],
                    }
                )
                break

    return matches
