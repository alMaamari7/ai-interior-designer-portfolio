from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums.room import RoomLayoutType, RoomShape, RoomStatus, RoomType
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.ai_analysis import AIAnalysis
    from app.models.building_element import BuildingElement
    from app.models.design_request import DesignRequest
    from app.models.floor import Floor
    from app.models.image import Image
    from app.models.room_object import RoomObject
    from app.models.user import User
    from app.models.wall import Wall


class Room(Base):
    __tablename__ = "rooms"
    __table_args__ = (
        CheckConstraint("room_size > 0", name="ck_room_size_positive"),
        CheckConstraint("ceiling_height > 0", name="ck_room_ceiling_height_positive"),
        CheckConstraint("wall_count >= 1", name="ck_room_wall_count_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    room_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    current_room_type: Mapped[RoomType] = mapped_column(Enum(RoomType), nullable=False)
    room_shape: Mapped[RoomShape] = mapped_column(Enum(RoomShape), nullable=False)
    room_layout_type: Mapped[RoomLayoutType] = mapped_column(Enum(RoomLayoutType), nullable=False)
    room_size: Mapped[float] = mapped_column(nullable=False)
    ceiling_height: Mapped[float | None] = mapped_column(nullable=True)
    room_status: Mapped[RoomStatus] = mapped_column(Enum(RoomStatus), nullable=False)
    wall_count: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user: Mapped["User"] = relationship(back_populates="rooms")
    floor: Mapped["Floor | None"] = relationship(back_populates="room", uselist=False, cascade="all, delete-orphan")
    walls: Mapped[list["Wall"]] = relationship(back_populates="room", cascade="all, delete-orphan")
    building_elements: Mapped[list["BuildingElement"]] = relationship(back_populates="room", cascade="all, delete-orphan")
    room_objects: Mapped[list["RoomObject"]] = relationship(back_populates="room", cascade="all, delete-orphan")
    images: Mapped[list["Image"]] = relationship(back_populates="room", cascade="all, delete-orphan")
    design_requests: Mapped[list["DesignRequest"]] = relationship(back_populates="room", cascade="all, delete-orphan")
    ai_analyses: Mapped[list["AIAnalysis"]] = relationship(back_populates="room", cascade="all, delete-orphan")
