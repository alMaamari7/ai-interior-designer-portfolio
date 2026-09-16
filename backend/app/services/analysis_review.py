from copy import deepcopy
from typing import Any

from app.schemas.analysis import AnalysisConfirmationResponse


class AnalysisReviewService:
    """Public example of the human-in-the-loop boundary.

    The AI result is treated as a proposal. A reviewer can accept it or provide
    corrections before the information is promoted to trusted room state.
    Production persistence and domain-specific validation remain private.
    """

    def confirm(
        self,
        analysis_id: int,
        ai_result: dict[str, Any],
        reviewed_result: dict[str, Any] | None = None,
    ) -> AnalysisConfirmationResponse:
        final_result = deepcopy(reviewed_result if reviewed_result is not None else ai_result)

        return AnalysisConfirmationResponse(
            analysis_id=analysis_id,
            confirmed=True,
            result=final_result,
        )
