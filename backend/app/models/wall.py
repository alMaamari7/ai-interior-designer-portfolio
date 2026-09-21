from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, DateTime, Enum, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums.room import VerificationStatus
from app.core.enums.spatial import WallType, WallUsability
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.building_element import BuildingElement
    from app.models.door import Door
    from app.models.image import Image
    from app.models.room import Room
    from app.models.window import Window


class Wall(Base):
    __tablename__ = "walls"
    __table_args__ = (
        CheckConstraint("wall_order > 0", name="ck_wall_order_positive"),
        CheckConstraint("wall_length > 0", name="ck_wall_length_positive"),
        UniqueConstraint("room_id", "wall_order", name="uq_wall_room_order"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False, index=True)
    wall_order: Mapped[int] = mapped_column(nullable=False)
    wall_type: Mapped[WallType | None] = mapped_column(Enum(WallType), nullable=True)
    wall_color_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    wall_color_hex: Mapped[str | None] = mapped_column(String(7), nullable=True)
    wall_length: Mapped[float] = mapped_column(nullable=False)
    wall_height: Mapped[float | None] = mapped_column(nullable=True)
    wall_usability: Mapped[WallUsability | None] = mapped_column(Enum(WallUsability), nullable=True)
    is_accent_wall: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    wall_confidence_score: Mapped[float | None] = mapped_column(nullable=True, index=True)
    verification_status: Mapped[VerificationStatus] = mapped_column(Enum(VerificationStatus), nullable=False, default=VerificationStatus.AI_DETECTED)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    room: Mapped["Room"] = relationship(back_populates="walls")
    windows: Mapped[list["Window"]] = relationship(back_populates="wall", cascade="all, delete-orphan")
    doors: Mapped[list["Door"]] = relationship(back_populates="wall", cascade="all, delete-orphan")
    images: Mapped[list["Image"]] = relationship(back_populates="wall", cascade="all, delete-orphan")
    building_elements: Mapped[list["BuildingElement"]] = relationship(back_populates="wall", cascade="all, delete-orphan")
