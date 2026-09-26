from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.analysis.create_capture_room.outputs.overviewimage_analysis_output import (
    InitialEntitySpatialMap,
)
from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.room import Room
from app.models.user import User
from app.services.overview_image_analysis import OverviewImageAnalysis

router = APIRouter(
    prefix="/overview-image-analysis",
    tags=["overview image analysis"],
)


def _require_owned_room(db: Session, room_id: int, user_id: int) -> Room:
    room = db.scalar(
        select(Room).where(Room.id == room_id, Room.user_id == user_id)
    )
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found.")
    return room


@router.post("/{room_id}", response_model=InitialEntitySpatialMap)
def analyze_overview_image(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> InitialEntitySpatialMap:
    _require_owned_room(db, room_id, current_user.id)
    return OverviewImageAnalysis(db).analyze_overview_image(room_id)


@router.get(
    "/{room_id}/result",
    response_model=InitialEntitySpatialMap,
)
def get_overview_image_analysis_result(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> InitialEntitySpatialMap:
    _require_owned_room(db, room_id, current_user.id)
    result = OverviewImageAnalysis(db).get_overview_image_analysis_result(room_id)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Overview image analysis result not found or not ready for review.",
        )
    return result


@router.post("/{room_id}/confirm", status_code=status.HTTP_204_NO_CONTENT)
def confirm_overview_image_analysis(
    room_id: int,
    result: InitialEntitySpatialMap,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    _require_owned_room(db, room_id, current_user.id)
    OverviewImageAnalysis(db).confirm_overview_image_analysis(room_id, result)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
