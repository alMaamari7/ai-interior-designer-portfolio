from enum import Enum


class AnalysisType(str, Enum):
    """Public categories; production analysis-stage taxonomy remains private."""

    VISION = "vision"
    REASONING = "reasoning"


class AnalysisStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    TO_REVIEW = "to_review"
    COMPLETED = "completed"
    FAILED = "failed"
