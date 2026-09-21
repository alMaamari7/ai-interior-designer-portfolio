from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.image import ImageCreationResult
from app.services.image_capture import ImageCaptureService, RoomNotFoundError

router = APIRouter(prefix="/rooms", tags=["room capture"])


@router.post("/{room_id}/images", response_model=ImageCreationResult)
async def capture_room_image(
    room_id: int,
    image_role: str = Form(...),
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ImageCreationResult:
    """Authenticate ownership, run deterministic quality checks, then persist."""
    service = ImageCaptureService(db)
    try:
        result = await service.create(user=current_user, room_id=room_id, image_role=image_role, image=image)
    except RoomNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if result.created:
        db.commit()
    return result
