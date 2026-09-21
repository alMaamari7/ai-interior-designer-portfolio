from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums.room import BuildingElementType, VerificationStatus
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.room import Room
    from app.models.wall import Wall


class BuildingElement(Base):
    __tablename__ = "building_elements"
    __table_args__ = (
        CheckConstraint("building_element_position_x_ratio BETWEEN 0 AND 1", name="ck_building_element_x_ratio"),
        CheckConstraint("building_element_position_y_ratio BETWEEN 0 AND 1", name="ck_building_element_y_ratio"),
        CheckConstraint("building_element_width_ratio > 0 AND building_element_width_ratio <= 1", name="ck_building_element_width_ratio"),
        CheckConstraint("building_element_height_ratio > 0 AND building_element_height_ratio <= 1", name="ck_building_element_height_ratio"),
        CheckConstraint("building_element_confidence_score BETWEEN 0 AND 1", name="ck_building_element_confidence"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False, index=True)
    wall_id: Mapped[int | None] = mapped_column(ForeignKey("walls.id"), nullable=True, index=True)
    building_element_type: Mapped[BuildingElementType | None] = mapped_column(Enum(BuildingElementType), nullable=True)
    building_element_position_x_ratio: Mapped[float | None] = mapped_column(nullable=True)
    building_element_position_y_ratio: Mapped[float | None] = mapped_column(nullable=True)
    building_element_width_ratio: Mapped[float | None] = mapped_column(nullable=True)
    building_element_height_ratio: Mapped[float | None] = mapped_column(nullable=True)
    building_element_confidence_score: Mapped[float | None] = mapped_column(nullable=True, index=True)
    verification_status: Mapped[VerificationStatus] = mapped_column(Enum(VerificationStatus), nullable=False, default=VerificationStatus.AI_DETECTED)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    room: Mapped["Room"] = relationship(back_populates="building_elements")
    wall: Mapped["Wall | None"] = relationship(back_populates="building_elements")
