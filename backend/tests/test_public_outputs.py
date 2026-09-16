import pytest
from pydantic import ValidationError

from app.ai.public_outputs import Observation, PublicRoomAnalysis


def test_structured_room_analysis_validates_confidence() -> None:
    analysis = PublicRoomAnalysis(
        summary="Example room analysis",
        observations=[Observation(category="opening", label="window", confidence=0.91)],
    )

    assert analysis.observations[0].confidence == 0.91


def test_confidence_outside_probability_range_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Observation(category="object", label="chair", confidence=1.5)
