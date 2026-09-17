from pydantic import BaseModel

from app.ai.public_outputs import PublicVisionOutput
from app.schemas.image import TechnicalQualityResult


class VisionAnalysisResponse(BaseModel):
    quality: TechnicalQualityResult
    analysis: PublicVisionOutput


class VisionAnalysisRejectedResponse(BaseModel):
    detail: str
    quality: TechnicalQualityResult
