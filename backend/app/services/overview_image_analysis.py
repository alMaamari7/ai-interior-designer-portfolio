from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.ai_request import AIRequest
from app.ai.analysis.create_capture_room.outputs.overviewimage_analysis_output import (
    InitialEntitySpatialMap,
)
from app.ai.gemini_client import GeminiClient
from app.core.enums.analysis import AnalysisStatus, AnalysisType
from app.core.enums.room import ImageRole
from app.models.ai_analysis import AIAnalysis
from app.models.confirmed_ai_analysis import ConfirmedAIAnalysis
from app.models.room import Room


class OverviewImageAnalysis:
    """Initial multi-view room understanding from accepted overview images."""

    PHASE = "create_capture_room"
    PROMPT_NAME = "overview_image_analysis"

    def __init__(self, db: Session, gemini_client: GeminiClient | None = None):
        self.db = db
        self.gemini_client = gemini_client

    def analyze_overview_image(self, room_id: int) -> InitialEntitySpatialMap:
        ai_request = AIRequest(self.db)
        prompt = ai_request.load_prompt(self.PHASE, self.PROMPT_NAME)
        images = ai_request.load_images(room_id, [ImageRole.OVERVIEW])

        room = self.db.get(Room, room_id)
        if room is None:
            raise ValueError("Room does not exist.")

        inputs = ai_request.prepare_inputs(
            self.PHASE,
            {
                "rules": None,
                "hints": None,
                "entity_scope": None,
                "Room Context": room,
            },
        )
        output_schema = ai_request.prepare_output(InitialEntitySpatialMap)
        request = ai_request.build(prompt, images, inputs, output_schema)

        analysis = AIAnalysis(
            room_id=room_id,
            analysis_type=AnalysisType.VISION,
            status=AnalysisStatus.IN_PROGRESS,
        )
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)

        client = self.gemini_client or GeminiClient()
        response = client.send_request(request)
        parsed = ai_request.parse_response(response, InitialEntitySpatialMap)

        analysis.result = parsed.model_dump()
        analysis.status = AnalysisStatus.TO_REVIEW
        analysis.completed_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(analysis)
        return parsed

    def get_overview_image_analysis_result(
        self,
        room_id: int,
    ) -> InitialEntitySpatialMap | None:
        statement = (
            select(AIAnalysis)
            .where(
                AIAnalysis.room_id == room_id,
                AIAnalysis.analysis_type == AnalysisType.VISION,
            )
            .order_by(AIAnalysis.created_at.desc())
        )
        analysis = self.db.scalar(statement)
        if (
            analysis is None
            or analysis.status != AnalysisStatus.TO_REVIEW
            or analysis.result is None
        ):
            return None
        return InitialEntitySpatialMap.model_validate(analysis.result)

    def confirm_overview_image_analysis(
        self,
        room_id: int,
        result: InitialEntitySpatialMap,
    ) -> None:
        statement = (
            select(AIAnalysis)
            .where(
                AIAnalysis.room_id == room_id,
                AIAnalysis.analysis_type == AnalysisType.VISION,
            )
            .order_by(AIAnalysis.created_at.desc())
        )
        analysis = self.db.scalar(statement)
        if analysis is None:
            raise ValueError("No overview image analysis exists.")
        if analysis.status != AnalysisStatus.TO_REVIEW:
            raise ValueError("The overview image analysis is not ready for review.")

        self.db.add(
            ConfirmedAIAnalysis(
                ai_analysis_id=analysis.id,
                result=result.model_dump(),
            )
        )
        analysis.status = AnalysisStatus.COMPLETED
        analysis.completed_at = datetime.now(timezone.utc)
        self.db.commit()
