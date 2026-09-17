from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.schemas.vision import VisionAnalysisResponse
from app.services.vision_analysis import (
    ImageQualityRejectedError,
    VisionAnalysisService,
)

router = APIRouter(prefix="/vision", tags=["Multimodal Vision"])


@router.post("/analyze", response_model=VisionAnalysisResponse)
async def analyze_room_image(
    image: UploadFile = File(...),
    room_context: str = Form(default=""),
) -> VisionAnalysisResponse:
    """Quality-check a room image and run schema-constrained vision analysis."""

    service = VisionAnalysisService()

    try:
        quality, analysis = await service.analyze(
            image=image,
            room_context=room_context,
        )
    except ImageQualityRejectedError as exc:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Image failed technical quality checks.",
                "quality": exc.quality.model_dump(),
            },
        ) from exc

    return VisionAnalysisResponse(quality=quality, analysis=analysis)
