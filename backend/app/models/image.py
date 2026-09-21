from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.room import Room


class Image(Base):
    """Public image metadata model.

    Binary image data is stored outside the database. The database keeps a
    room-scoped storage reference and a semantic role used by the application.
    """

    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), index=True)
    storage_path: Mapped[str] = mapped_column(String(500), nullable=False)
    image_role: Mapped[str] = mapped_column(String(100), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    room: Mapped["Room"] = relationship(back_populates="images")
