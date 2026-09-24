import io

import numpy as np
import pytest
from fastapi import UploadFile
from PIL import Image

from app.services.image_quality import TechnicalImageQuality


def upload_from_array(array: np.ndarray, filename: str = "room.jpg") -> UploadFile:
    buffer = io.BytesIO()
    Image.fromarray(array.astype(np.uint8), mode="RGB").save(buffer, format="JPEG")
    buffer.seek(0)
    return UploadFile(filename=filename, file=buffer)


def detailed_image(width: int = 800, height: int = 600) -> UploadFile:
    y, x = np.indices((height, width))
    checker = ((x // 8 + y // 8) % 2) * 100 + 80
    rgb = np.stack([checker, checker, checker], axis=-1)
    return upload_from_array(rgb)


@pytest.mark.asyncio
async def test_invalid_image_fails_integrity_check():
    service = TechnicalImageQuality()
    upload = UploadFile(filename="broken.jpg", file=io.BytesIO(b"not-an-image"))

    result = await service.evaluate(upload)

    assert result.passed is False
    assert result.checks["image_integrity"].code == "INVALID_IMAGE"


@pytest.mark.asyncio
async def test_low_resolution_image_is_rejected():
    service = TechnicalImageQuality()
    upload = detailed_image(320, 240)

    result = await service.evaluate(upload)

    assert result.passed is False
    assert result.checks["resolution"].code == "INSUFFICIENT_RESOLUTION"


@pytest.mark.asyncio
async def test_blurred_image_is_rejected():
    service = TechnicalImageQuality()
    uniform = np.full((600, 800, 3), 128, dtype=np.uint8)

    result = await service.evaluate(upload_from_array(uniform))

    assert result.passed is False
    assert result.checks["sharpness"].code == "INSUFFICIENT_SHARPNESS"


@pytest.mark.asyncio
async def test_underexposed_image_is_rejected_by_exposure_check():
    service = TechnicalImageQuality()
    dark = np.zeros((600, 800, 3), dtype=np.uint8)

    result = await service.check_exposure(upload_from_array(dark))

    assert result.passed is False
    assert result.code == "UNDEREXPOSED"


@pytest.mark.asyncio
async def test_overexposed_image_is_rejected_by_exposure_check():
    service = TechnicalImageQuality()
    bright = np.full((600, 800, 3), 255, dtype=np.uint8)

    result = await service.check_exposure(upload_from_array(bright))

    assert result.passed is False
    assert result.code == "OVEREXPOSED"


@pytest.mark.asyncio
async def test_valid_detailed_image_passes_quality_gate():
    service = TechnicalImageQuality()

    result = await service.evaluate(detailed_image())

    assert result.passed is True
    assert set(result.checks) == {
        "image_integrity",
        "resolution",
        "sharpness",
        "exposure",
    }
