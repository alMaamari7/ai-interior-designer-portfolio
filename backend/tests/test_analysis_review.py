from app.services.analysis_review import AnalysisReviewService


def test_review_can_accept_ai_result():
    service = AnalysisReviewService()
    ai_result = {"room_type": "living_room", "confidence": 0.91}

    confirmed = service.confirm(analysis_id=12, ai_result=ai_result)

    assert confirmed.confirmed is True
    assert confirmed.result == ai_result


def test_review_can_replace_ai_result_with_human_correction():
    service = AnalysisReviewService()
    ai_result = {"room_type": "bedroom"}
    correction = {"room_type": "living_room"}

    confirmed = service.confirm(
        analysis_id=12,
        ai_result=ai_result,
        reviewed_result=correction,
    )

    assert confirmed.result == correction
    assert ai_result == {"room_type": "bedroom"}
