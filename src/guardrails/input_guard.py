"""Input Guard: Prompt Injection Defense and Toxic/Abusive Language Sanitization."""
import re
from typing import Tuple, List, Optional, Any
from pydantic import BaseModel, Field

class InputGuardResult(BaseModel):
    is_safe: bool
    status: str  # "CLEAN", "MASKED_ABUSIVE", "BLOCKED_INJECTION"
    original_text: str
    sanitized_text: str
    detected_threats: List[str] = Field(default_factory=list)
    action_taken: str

# Prompt injection regex patterns aligned with Course LAB-06 and adversarial red-teaming
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+|any\s+)?(previous|prior|above|earlier)\s+(instructions|rules|guidelines)",
    r"disregard\s+(your|the|all)\s+(instructions|rules|policies|guidelines)",
    r"system\s*prompt\s*(override|reveal|leak|output)",
    r"\bdeveloper\s*mode\b",
    r"\bjailbreak\b",
    r"output\s+admin\s+(secret|password|key)",
    r"bypass\s+(safety|guardrail|security|filters)",
    r"assign\s+driver\s+.*without\s+checking\s+hours",
    r"\bact\s+as\s+(an?\s+)?unrestricted\b",
    r"\boverride\s+all\s+(rules|guidelines|limits|safety)\b",
    r"\bnew\s+instructions?\s*:\s*assign\b"
]

# Toxic, abusive, or hostile speech patterns
TOXIC_TERMS = [
    r"\bpathetic\b",
    r"\blazy\b",
    r"\bincompetent\b",
    r"\bidiots?\b",
    r"\bgarbage\b",
    r"\bclowns?\b",
    r"\bsue\s+your\s+service\b",
    r"\bstupid\b",
    r"\bustupid\s*machine\b",
    r"\bworthless\b",
    r"\btrash\b",
    r"\bscam(mers?)?\b",
    r"\buseless\b"
]

class InputGuard:
    """Pre-execution gateway checking and sanitizing external client inputs."""

    def __init__(self):
        self.injection_regexes = [re.compile(p, re.IGNORECASE) for p in INJECTION_PATTERNS]
        self.toxic_regexes = [re.compile(p, re.IGNORECASE) for p in TOXIC_TERMS]

    def evaluate(self, user_prompt: Any) -> InputGuardResult:
        """Scan prompt for injection attempts or toxic abusive language safely."""
        if user_prompt is None:
            clean_text = ""
        elif isinstance(user_prompt, str):
            clean_text = user_prompt
        else:
            clean_text = str(user_prompt)

        detected = []
        
        # 1. Check for prompt injection
        for reg in self.injection_regexes:
            match = reg.search(clean_text)
            if match:
                detected.append(f"Prompt Injection Pattern: '{match.group(0)}'")

        if detected:
            return InputGuardResult(
                is_safe=False,
                status="BLOCKED_INJECTION",
                original_text=clean_text,
                sanitized_text="[REQUEST_BLOCKED_DUE_TO_SECURITY_POLICY_VIOLATION]",
                detected_threats=detected,
                action_taken="IMMEDIATE_REFUSAL_AND_AUDIT_LOG"
            )

        # 2. Check for toxic / abusive content
        sanitized = clean_text
        toxic_found = []
        for reg in self.toxic_regexes:
            matches = reg.findall(clean_text)
            if matches:
                toxic_found.extend(matches)
                sanitized = reg.sub("[REDACTED_HOSTILE]", sanitized)

        if toxic_found:
            return InputGuardResult(
                is_safe=True,  # Safe to process once neutralized
                status="MASKED_ABUSIVE",
                original_text=clean_text,
                sanitized_text=sanitized,
                detected_threats=[f"Hostile phrasing: {t}" for t in toxic_found],
                action_taken="MASK_AND_FLAG_FOR_OPERATIONAL_DISPATCH"
            )

        return InputGuardResult(
            is_safe=True,
            status="CLEAN",
            original_text=clean_text,
            sanitized_text=clean_text,
            detected_threats=[],
            action_taken="ALLOW"
        )

