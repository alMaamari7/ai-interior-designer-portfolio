from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.image import Image
from app.models.room import Room
from app.models.user import User
from app.schemas.image import ImageCreationResult
from app.services.image_quality import TechnicalImageQuality


class RoomNotFoundError(ValueError):
    pass


class ImageCaptureService:
    """Quality-check and persist an authenticated user's room image."""

    def __init__(self, db: Session, upload_root: Path | None = None, quality_service: TechnicalImageQuality | None = None) -> None:
        self.db = db
        self.upload_root = upload_root or Path("uploads")
        self.quality_service = quality_service or TechnicalImageQuality()

    async def create(self, *, user: User, room_id: int, image_role: str, image: UploadFile) -> ImageCreationResult:
        room = self.db.execute(select(Room).where(Room.id == room_id, Room.user_id == user.id)).scalar_one_or_none()
        if room is None:
            raise RoomNotFoundError(f"Room {room_id} was not found.")

        quality = await self.quality_service.evaluate(image)
        if not quality.passed:
            return ImageCreationResult(created=False, quality=quality)

        stored_image = await self._save(room_id=room_id, image_role=image_role, image=image)
        return ImageCreationResult(created=True, quality=quality, image_id=stored_image.id)

    async def _save(self, *, room_id: int, image_role: str, image: UploadFile) -> Image:
        room_directory = self.upload_root / "rooms" / f"room_{room_id}" / "images"
        room_directory.mkdir(parents=True, exist_ok=True)
        suffix = Path(image.filename or "").suffix.lower()
        filename = f"{uuid4()}{suffix}"
        destination = room_directory / filename
        content = await image.read()
        destination.write_bytes(content)
        await image.seek(0)
        relative_path = Path("rooms") / f"room_{room_id}" / "images" / filename
        entity = Image(room_id=room_id, image_path=relative_path.as_posix(), image_role=image_role)
        self.db.add(entity)
        self.db.flush()
        return entity
