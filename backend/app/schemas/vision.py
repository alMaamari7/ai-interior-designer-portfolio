from pydantic import BaseModel

from app.ai.public_outputs import PublicRoomAnalysis
from app.schemas.image import TechnicalQualityResult


class VisionAnalysisResponse(BaseModel):
    quality: TechnicalQualityResult
    analysis: PublicRoomAnalysis


class VisionAnalysisRejectedResponse(BaseModel):
    detail: str
    quality: TechnicalQualityResult
