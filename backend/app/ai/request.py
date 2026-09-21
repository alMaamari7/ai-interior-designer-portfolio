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


class AIRequestBuilder:
    """Build provider-neutral requests without exposing product prompt policy."""

    def build(
        self,
        *,
        instruction: str,
        context: str,
        images: list[ImageInput],
        output_schema: type[BaseModel],
    ) -> AIRequest:
        if not issubclass(output_schema, BaseModel):
            raise TypeError("output_schema must be a Pydantic BaseModel")

        return AIRequest(
            instruction=instruction,
            context=context,
            images=images,
            output_schema=output_schema,
        )

    def parse_response(
        self,
        response: str,
        output_schema: type[BaseModel],
    ) -> BaseModel:
        return output_schema.model_validate_json(response)
