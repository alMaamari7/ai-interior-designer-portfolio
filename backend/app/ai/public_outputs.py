from pydantic import BaseModel, Field


class Observation(BaseModel):
    """Deliberately generic public example of a structured vision observation."""

    category: str
    label: str
    confidence: float = Field(ge=0.0, le=1.0)


class PublicRoomAnalysis(BaseModel):
    """Reduced portfolio schema; not the production Digital Twin schema."""

    summary: str
    observations: list[Observation] = Field(default_factory=list)


class ReasoningContext(BaseModel):
    """Public boundary for downstream reasoning; production policy is private."""

    room_summary: str
    user_goals: list[str]
    constraints: list[str] = Field(default_factory=list)
    budget: str | None = None


class Recommendation(BaseModel):
    """Generic public result contract for an evaluated recommendation."""

    summary: str
    rationale: list[str] = Field(default_factory=list)
    considerations: list[str] = Field(default_factory=list)
