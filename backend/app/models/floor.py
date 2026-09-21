from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums.room import VerificationStatus
from app.core.enums.spatial import FloorMaterial
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.room import Room


class Floor(Base):
    __tablename__ = "floors"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False, unique=True, index=True)
    floor_material: Mapped[FloorMaterial | None] = mapped_column(Enum(FloorMaterial), nullable=True)
    floor_color_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    floor_color_hex: Mapped[str | None] = mapped_column(String(7), nullable=True)
    floor_confidence_score: Mapped[float | None] = mapped_column(nullable=True, index=True)
    verification_status: Mapped[VerificationStatus] = mapped_column(Enum(VerificationStatus), nullable=False, default=VerificationStatus.AI_DETECTED)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    room: Mapped["Room"] = relationship(back_populates="floor")
