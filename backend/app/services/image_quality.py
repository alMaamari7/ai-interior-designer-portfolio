from io import BytesIO

import cv2
import numpy as np
from fastapi import UploadFile
from PIL import Image, UnidentifiedImageError

from app.schemas.image import TechnicalQualityCheckResult, TechnicalQualityResult


class TechnicalImageQualityConfig:
    """Configurable thresholds for deterministic pre-inference checks."""

    minimum_width: int = 640
    minimum_height: int = 480
    sharpness_threshold: float = 40.0
    dark_luminance_threshold: int = 25
    bright_luminance_threshold: int = 235
    max_dark_pixel_ratio: float = 0.65
    max_bright_pixel_ratio: float = 0.65


class TechnicalImageQuality:
    """Reject technically unusable images before multimodal inference."""

    def __init__(self, config: TechnicalImageQualityConfig | None = None) -> None:
        self.config = config or TechnicalImageQualityConfig()

    async def _read(self, image: UploadFile) -> bytes:
        content = await image.read()
        await image.seek(0)
        return content

    async def check_image_integrity(self, image: UploadFile) -> TechnicalQualityCheckResult:
        try:
            content = await self._read(image)
            if not content:
                return TechnicalQualityCheckResult(
                    passed=False,
                    code="EMPTY_IMAGE",
                    message="The uploaded image is empty.",
                )

            with Image.open(BytesIO(content)) as pil_image:
                pil_image.verify()

            return TechnicalQualityCheckResult(passed=True)
        except UnidentifiedImageError:
            return TechnicalQualityCheckResult(
                passed=False,
                code="INVALID_IMAGE",
                message="The uploaded file is not a valid image.",
            )
        except Exception:
            return TechnicalQualityCheckResult(
                passed=False,
                code="IMAGE_INTEGRITY_FAILURE",
                message="The image could not be decoded correctly.",
            )

    async def check_resolution(self, image: UploadFile) -> TechnicalQualityCheckResult:
        try:
            content = await self._read(image)
            with Image.open(BytesIO(content)) as pil_image:
                width, height = pil_image.size

            if width < self.config.minimum_width or height < self.config.minimum_height:
                return TechnicalQualityCheckResult(
                    passed=False,
                    code="INSUFFICIENT_RESOLUTION",
                    message="The image resolution is below the required minimum.",
                )
            return TechnicalQualityCheckResult(passed=True)
        except Exception:
            return TechnicalQualityCheckResult(
                passed=False,
                code="RESOLUTION_CHECK_FAILED",
                message="The image resolution could not be determined.",
            )

    async def check_sharpness(self, image: UploadFile) -> TechnicalQualityCheckResult:
        try:
            content = await self._read(image)
            with Image.open(BytesIO(content)) as pil_image:
                grayscale = np.array(pil_image.convert("L"), dtype=np.float64)

            sharpness_score = float(cv2.Laplacian(grayscale, cv2.CV_64F).var())
            if sharpness_score < self.config.sharpness_threshold:
                return TechnicalQualityCheckResult(
                    passed=False,
                    code="INSUFFICIENT_SHARPNESS",
                    message="The image is not sufficiently sharp.",
                )
            return TechnicalQualityCheckResult(passed=True)
        except Exception:
            return TechnicalQualityCheckResult(
                passed=False,
                code="SHARPNESS_CHECK_FAILED",
                message="The image sharpness could not be determined.",
            )

    async def check_exposure(self, image: UploadFile) -> TechnicalQualityCheckResult:
        try:
            content = await self._read(image)
            with Image.open(BytesIO(content)) as pil_image:
                grayscale = np.array(pil_image.convert("L"), dtype=np.uint8)

            if grayscale.size == 0:
                return TechnicalQualityCheckResult(
                    passed=False, code="EMPTY_IMAGE", message="The image contains no pixels."
                )

            dark_ratio = float(
                np.mean(grayscale <= self.config.dark_luminance_threshold)
            )
            bright_ratio = float(
                np.mean(grayscale >= self.config.bright_luminance_threshold)
            )

            if dark_ratio > self.config.max_dark_pixel_ratio:
                return TechnicalQualityCheckResult(
                    passed=False,
                    code="UNDEREXPOSED",
                    message="Too much of the image is underexposed.",
                )
            if bright_ratio > self.config.max_bright_pixel_ratio:
                return TechnicalQualityCheckResult(
                    passed=False,
                    code="OVEREXPOSED",
                    message="Too much of the image is overexposed.",
                )
            return TechnicalQualityCheckResult(passed=True)
        except Exception:
            return TechnicalQualityCheckResult(
                passed=False,
                code="EXPOSURE_CHECK_FAILED",
                message="The image exposure could not be determined.",
            )

    async def evaluate(self, image: UploadFile) -> TechnicalQualityResult:
        checks: dict[str, TechnicalQualityCheckResult] = {}
        pipeline = (
            ("image_integrity", self.check_image_integrity),
            ("resolution", self.check_resolution),
            ("sharpness", self.check_sharpness),
            ("exposure", self.check_exposure),
        )

        for name, check in pipeline:
            result = await check(image)
            checks[name] = result
            if not result.passed:
                return TechnicalQualityResult(passed=False, checks=checks)

        return TechnicalQualityResult(passed=True, checks=checks)
