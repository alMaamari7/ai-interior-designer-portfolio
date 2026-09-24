import json

import pytest
from pydantic import ValidationError

from app.ai.public_outputs import PublicRoomAnalysis
from app.ai.request import AIRequestBuilder


def test_valid_structured_ai_response_becomes_typed_model():
    builder = AIRequestBuilder()
    response = json.dumps(
        {
            "summary": "Room with seating and natural light.",
            "observations": [
                {"category": "furniture", "label": "sofa", "confidence": 0.94}
            ],
        }
    )

    result = builder.parse_response(response, PublicRoomAnalysis)

    assert isinstance(result, PublicRoomAnalysis)
    assert result.observations[0].label == "sofa"


def test_malformed_ai_response_is_rejected_by_schema_validation():
    builder = AIRequestBuilder()
    response = json.dumps(
        {
            "summary": "Invalid confidence example.",
            "observations": [
                {"category": "furniture", "label": "sofa", "confidence": 1.5}
            ],
        }
    )

    with pytest.raises(ValidationError):
        builder.parse_response(response, PublicRoomAnalysis)
