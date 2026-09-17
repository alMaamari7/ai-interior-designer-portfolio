import io
import json

import pytest
from fastapi import UploadFile
from PIL import Image

from app.ai.public_outputs import PublicVisionOutput
from app.services.image_quality import TechnicalImageQualityConfig
from app.services.vision_analysis import VisionAnalysisService


class PassingQualityService:
    async def evaluate(self, image):
        from app.schemas.image import TechnicalQualityResult

        return TechnicalQualityResult(passed=True, checks={})


class FakeAIClient:
    def send(self, request):
        assert request.images
        assert request.output_schema is PublicVisionOutput
        return json.dumps(
            {
                "summary": "Bright living space with visible seating.",
                "observations": [
                    {
                        "category": "furniture",
                        "label": "sofa",
                        "confidence": 0.93,
                    }
                ],
                "limitations": [],
            }
        )


def make_upload() -> UploadFile:
    buffer = io.BytesIO()
    Image.new("RGB", (800, 600), "gray").save(buffer, format="JPEG")
    buffer.seek(0)
    return UploadFile(filename="room.jpg", file=buffer)


@pytest.mark.asyncio
async def test_service_builds_multimodal_request_and_parses_structured_output():
    service = VisionAnalysisService(
        quality_service=PassingQualityService(),
        ai_client=FakeAIClient(),
    )

    quality, result = await service.analyze(
        make_upload(), room_context="Public demo context"
    )

    assert quality.passed is True
    assert result.observations[0].label == "sofa"
    assert result.observations[0].confidence == 0.93
