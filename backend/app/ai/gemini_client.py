import os

from google import genai
from google.genai import types

from app.ai.request import AIRequest


class GeminiClient:
    """Thin multimodal provider adapter with JSON-schema constrained output."""

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        resolved_key = api_key or os.getenv("AI_API_KEY")
        if not resolved_key:
            raise ValueError("AI_API_KEY is not configured")

        self.client = genai.Client(api_key=resolved_key)
        self.model = model or os.getenv("AI_MODEL", "gemini-2.5-flash")

    def send(self, request: AIRequest) -> str:
        text_part = f"{request.instruction}\n\nContext:\n{request.context}"
        parts: list[object] = [text_part]

        for image in request.images:
            parts.append(
                types.Part.from_bytes(data=image.data, mime_type=image.mime_type)
            )

        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=request.output_schema,
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=parts,
            config=config,
        )
        return response.text
