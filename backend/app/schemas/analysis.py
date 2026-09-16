from typing import Any

from pydantic import BaseModel, Field


class AnalysisCreate(BaseModel):
    room_id: int
    analysis_type: str = Field(min_length=1, max_length=100)


class AnalysisResponse(BaseModel):
    id: int
    room_id: int
    analysis_type: str
    status: str
    result: dict[str, Any] | None = None

    model_config = {"from_attributes": True}


class AnalysisConfirmationRequest(BaseModel):
    """Reviewed result accepted or corrected by a human."""

    result: dict[str, Any]


class AnalysisConfirmationResponse(BaseModel):
    analysis_id: int
    confirmed: bool
    result: dict[str, Any]
