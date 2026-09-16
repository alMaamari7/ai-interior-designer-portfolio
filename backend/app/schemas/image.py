from pydantic import BaseModel


class TechnicalQualityCheckResult(BaseModel):
    """Result of one deterministic image-quality check."""

    passed: bool
    code: str | None = None
    message: str | None = None


class TechnicalQualityResult(BaseModel):
    """Aggregated result of the technical image-quality gate."""

    passed: bool
    checks: dict[str, TechnicalQualityCheckResult]


class ImageInput(BaseModel):
    """Provider-neutral in-memory image representation for AI clients."""

    data: bytes
    mime_type: str
    image_type: str | None = None
