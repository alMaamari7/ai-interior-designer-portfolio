from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums.room import ObjectCategory, VerificationStatus
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.constraint_room_object import ConstraintRoomObject
    from app.models.room import Room


class RoomObject(Base):
    __tablename__ = "room_objects"
    __table_args__ = (
        CheckConstraint("object_position_x_ratio BETWEEN 0 AND 1", name="ck_room_object_x_ratio"),
        CheckConstraint("object_position_y_ratio BETWEEN 0 AND 1", name="ck_room_object_y_ratio"),
        CheckConstraint("object_width_ratio > 0 AND object_width_ratio <= 1", name="ck_room_object_width_ratio"),
        CheckConstraint("object_depth_ratio > 0 AND object_depth_ratio <= 1", name="ck_room_object_depth_ratio"),
        CheckConstraint("object_rotation_angle >= 0 AND object_rotation_angle < 360", name="ck_room_object_rotation"),
        CheckConstraint("object_confidence_score BETWEEN 0 AND 1", name="ck_room_object_confidence"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False, index=True)
    object_category: Mapped[ObjectCategory | None] = mapped_column(Enum(ObjectCategory), nullable=True)
    object_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    object_material: Mapped[str | None] = mapped_column(String(100), nullable=True)
    object_color_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    object_color_hex: Mapped[str | None] = mapped_column(String(7), nullable=True)
    object_position_x_ratio: Mapped[float | None] = mapped_column(nullable=True)
    object_position_y_ratio: Mapped[float | None] = mapped_column(nullable=True)
    object_width_ratio: Mapped[float | None] = mapped_column(nullable=True)
    object_depth_ratio: Mapped[float | None] = mapped_column(nullable=True)
    object_rotation_angle: Mapped[float | None] = mapped_column(nullable=True, default=0.0, server_default="0")
    object_confidence_score: Mapped[float | None] = mapped_column(nullable=True, index=True)
    verification_status: Mapped[VerificationStatus] = mapped_column(Enum(VerificationStatus), nullable=False, default=VerificationStatus.AI_DETECTED)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    room: Mapped["Room"] = relationship(back_populates="room_objects")
    constraint_references: Mapped[list["ConstraintRoomObject"]] = relationship(back_populates="room_object", cascade="all, delete-orphan")
