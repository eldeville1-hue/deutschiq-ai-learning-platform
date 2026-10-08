"""DeutschIQ 88 evaluation contract.

Pure evaluation data: this module does not award XP, update mastery or schedule reviews.
Confidence is an uncalibrated indicator, never a probability of correctness.
"""
from dataclasses import asdict, dataclass, field
from typing import Literal

EvaluationStatus = Literal["verified", "uncertain", "needs_review"]
AssistanceLevel = Literal["independent", "hinted", "guided_retry"]


@dataclass(frozen=True)
class LinguisticError:
    type: str
    span: str
    correction: str
    explanation: str


@dataclass(frozen=True)
class EvaluationResult:
    grammar_correct: bool | None
    meaning_correct: bool | None
    task_satisfied: bool | None
    correct: bool
    evaluation_status: EvaluationStatus
    evaluation_confidence: float | None = None
    errors: list[LinguisticError] = field(default_factory=list)
    error_type: str | None = None
    assistance_level: AssistanceLevel = "independent"
    feedback_focus: str | None = None
    retry_instruction: str | None = None

    def __post_init__(self):
        if self.evaluation_status != "verified" and self.correct:
            raise ValueError("Unverified answers must not be marked correct")
        if self.correct and self.task_satisfied is not True:
            raise ValueError("Successful answers must satisfy the task")
        if self.error_type and self.errors and self.error_type != self.errors[0].type:
            raise ValueError("Primary error must match first structured error")
        if self.evaluation_confidence is not None and not 0 <= self.evaluation_confidence <= 1:
            raise ValueError("Confidence indicator must be within [0, 1]")

    def to_dict(self) -> dict:
        return asdict(self)


def evidence_from_evaluation(result: EvaluationResult, *, skill: str, attempt_number: int) -> dict:
    """Record provenance separately from linguistic judgment, without side effects."""
    return {
        "skill": skill,
        "attempt_number": attempt_number,
        "assistance_level": result.assistance_level,
        "evaluation_status": result.evaluation_status,
        "independent_verified_success": (
            result.evaluation_status == "verified"
            and result.correct
            and result.assistance_level == "independent"
            and attempt_number == 1
        ),
    }
