from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums.room import VerificationStatus
from app.core.enums.spatial import DoorOpeningType, DoorType
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.wall import Wall


class Door(Base):
    __tablename__ = "doors"
    __table_args__ = (UniqueConstraint("wall_id", "door_order", name="uq_door_wall_order"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    wall_id: Mapped[int] = mapped_column(ForeignKey("walls.id"), nullable=False, index=True)
    door_order: Mapped[int | None] = mapped_column(nullable=True)
    door_type: Mapped[DoorType | None] = mapped_column(Enum(DoorType), nullable=True)
    door_opening_type: Mapped[DoorOpeningType | None] = mapped_column(Enum(DoorOpeningType), nullable=True)
    door_position_x_ratio: Mapped[float | None] = mapped_column(nullable=True)
    door_width_ratio: Mapped[float | None] = mapped_column(nullable=True)
    door_height_ratio: Mapped[float | None] = mapped_column(nullable=True)
    door_confidence_score: Mapped[float | None] = mapped_column(nullable=True, index=True)
    verification_status: Mapped[VerificationStatus] = mapped_column(Enum(VerificationStatus), nullable=False, default=VerificationStatus.AI_DETECTED)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    wall: Mapped["Wall"] = relationship(back_populates="doors")
