from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.image import ImageCreationResult
from app.services.image_capture import ImageCaptureService, RoomNotFoundError

router = APIRouter(prefix="/rooms", tags=["Room Capture"])


@router.post("/{room_id}/images", response_model=ImageCreationResult)
async def capture_room_image(
    room_id: int,
    image_role: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> ImageCreationResult:
    """Run deterministic quality checks before persisting a room image."""

    service = ImageCaptureService(db)

    try:
        result = await service.create(
            room_id=room_id,
            image_role=image_role,
            image=image,
        )
    except RoomNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    if result.created:
        db.commit()

    return result
