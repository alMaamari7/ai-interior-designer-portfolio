from fastapi import APIRouter

from app.schemas.analysis import (
    AnalysisConfirmationRequest,
    AnalysisConfirmationResponse,
)
from app.services.analysis_review import AnalysisReviewService

router = APIRouter(prefix="/analyses", tags=["AI Analysis"])
review_service = AnalysisReviewService()


@router.post(
    "/{analysis_id}/confirm",
    response_model=AnalysisConfirmationResponse,
)
def confirm_analysis(
    analysis_id: int,
    request: AnalysisConfirmationRequest,
) -> AnalysisConfirmationResponse:
    """Public demonstration endpoint for human review of AI output.

    Database lookup/authorization and proprietary domain validation are omitted
    from the portfolio layer. The endpoint exposes the architectural contract.
    """

    return review_service.confirm(
        analysis_id=analysis_id,
        ai_result=request.result,
    )
