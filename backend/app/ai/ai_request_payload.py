from dataclasses import dataclass

from pydantic import BaseModel

from app.schemas.image import ImageInput


@dataclass(frozen=True)
class AIRequestPayload:
    prompt: str
    inputs: str
    images: list[ImageInput]
    output_schema: type[BaseModel]
