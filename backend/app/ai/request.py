from dataclasses import dataclass

from pydantic import BaseModel

from app.schemas.image import ImageInput


@dataclass(frozen=True)
class AIRequest:
    """Provider-facing multimodal request with a typed output contract."""

    instruction: str
    context: str
    images: list[ImageInput]
    output_schema: type[BaseModel]
