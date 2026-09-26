from google import genai
from google.genai import types

from app.ai.ai_request_payload import AIRequestPayload
from app.core.settings import settings


class GeminiClient:
    """Thin Gemini adapter with schema-constrained multimodal output."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        resolved_key = api_key or settings.AI_API_KEY
        if not resolved_key:
            raise ValueError("AI_API_KEY is not configured")
        self.client = genai.Client(api_key=resolved_key)
        self.model = model or settings.AI_MODEL

    def send_request(self, request: AIRequestPayload) -> str:
        parts: list[object] = [
            f"{request.prompt}\n\nContext:\n{request.inputs}"
        ]
        for image in request.images:
            parts.append(
                types.Part.from_bytes(
                    data=image.data,
                    mime_type=image.mime_type,
                )
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
