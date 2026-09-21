from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums.room import ImageRole
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.room import Room
    from app.models.wall import Wall


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False, index=True)
    wall_id: Mapped[int | None] = mapped_column(ForeignKey("walls.id"), nullable=True, index=True)
    image_path: Mapped[str] = mapped_column(String(500), nullable=False)
    image_role: Mapped[ImageRole] = mapped_column(Enum(ImageRole), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    room: Mapped["Room"] = relationship(back_populates="images")
    wall: Mapped["Wall | None"] = relationship(back_populates="images")
