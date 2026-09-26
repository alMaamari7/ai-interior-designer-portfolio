import mimetypes
from pathlib import Path
from typing import Any

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.ai_request_payload import AIRequestPayload
from app.core.enums.room import ImageRole
from app.models.image import Image
from app.schemas.image import ImageInput


class AIRequest:
    """Build multimodal AI requests from persisted room images and phase inputs."""

    def __init__(self, db: Session, analysis_root: Path | None = None):
        self.db = db
        self.analysis_root = analysis_root or Path("app/ai/analysis")

    def load_images(
        self,
        room_id: int,
        image_roles: list[ImageRole],
    ) -> list[ImageInput]:
        statement = select(Image).where(
            Image.room_id == room_id,
            Image.image_role.in_(image_roles),
        )
        images = self.db.execute(statement).scalars().all()
        image_inputs: list[ImageInput] = []

        for image in images:
            image_path = Path("uploads") / image.image_path
            if not image_path.exists():
                raise FileNotFoundError(f"Image file not found: {image_path}")

            image_inputs.append(
                ImageInput(
                    data=image_path.read_bytes(),
                    mime_type=mimetypes.guess_type(image_path)[0]
                    or "application/octet-stream",
                    image_type=image.image_role.value,
                )
            )

        return image_inputs

    def load_prompt(self, phase: str, prompt_name: str) -> str:
        path = self.analysis_root / phase / "prompt" / f"{prompt_name}.txt"
        return path.read_text(encoding="utf-8")

    def prepare_inputs(
        self,
        phase: str,
        inputs: dict[Any, object | None],
    ) -> str:
        prepared: list[str] = []
        for key, value in inputs.items():
            key_name = key.value if hasattr(key, "value") else str(key)
            if value is None:
                path = self.analysis_root / phase / "inputs" / f"{key_name}.txt"
                content = path.read_text(encoding="utf-8")
            else:
                content = str(value)
            prepared.append(f"{key_name}: {content}")
        return "\n".join(prepared)

    def prepare_output(self, output_schema: type[BaseModel]) -> type[BaseModel]:
        if not issubclass(output_schema, BaseModel):
            raise TypeError("output_schema must be a Pydantic BaseModel.")
        return output_schema

    def parse_response(
        self,
        response: str,
        output_schema: type[BaseModel],
    ) -> BaseModel:
        return output_schema.model_validate_json(response)

    def build(
        self,
        prompt: str,
        images: list[ImageInput],
        inputs: str,
        output_schema: type[BaseModel],
    ) -> AIRequestPayload:
        return AIRequestPayload(
            prompt=prompt,
            inputs=inputs,
            images=images,
            output_schema=output_schema,
        )
