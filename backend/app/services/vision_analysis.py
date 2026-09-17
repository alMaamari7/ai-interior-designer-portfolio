import json

from fastapi import UploadFile

from app.ai.gemini_client import GeminiClient
from app.ai.public_outputs import PublicRoomAnalysis
from app.ai.request import AIRequest
from app.schemas.image import ImageInput, TechnicalQualityResult
from app.services.image_quality import TechnicalImageQuality


class ImageQualityRejectedError(ValueError):
    def __init__(self, quality: TechnicalQualityResult) -> None:
        super().__init__("Image failed technical quality checks")
        self.quality = quality


class VisionAnalysisService:
    """Public end-to-end orchestration boundary for one captured image.

    The service demonstrates the production engineering pattern without
    exposing proprietary evidence requirements, capture policies, prompts or
    the complete private output model.
    """

    PUBLIC_INSTRUCTION = (
        "Analyze the room image and return a concise structured description "
        "using the supplied response schema. Do not infer details that are "
        "not visually supported."
    )

    def __init__(
        self,
        quality_service: TechnicalImageQuality | None = None,
        ai_client: GeminiClient | None = None,
    ) -> None:
        self.quality_service = quality_service or TechnicalImageQuality()
        self.ai_client = ai_client

    async def analyze(
        self,
        image: UploadFile,
        room_context: str = "",
    ) -> tuple[TechnicalQualityResult, PublicRoomAnalysis]:
        quality = await self.quality_service.evaluate(image)
        if not quality.passed:
            raise ImageQualityRejectedError(quality)

        image_bytes = await image.read()
        await image.seek(0)

        client = self.ai_client or GeminiClient()
        request = AIRequest(
            instruction=self.PUBLIC_INSTRUCTION,
            context=room_context,
            images=[
                ImageInput(
                    data=image_bytes,
                    mime_type=image.content_type or "image/jpeg",
                    image_type="room_capture",
                )
            ],
            output_schema=PublicRoomAnalysis,
        )

        raw_result = client.send(request)
        structured_result = PublicRoomAnalysis.model_validate(json.loads(raw_result))
        return quality, structured_result
