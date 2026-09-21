from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.constraint import Constraint
    from app.models.room_object import RoomObject


class ConstraintRoomObject(Base):
    __tablename__ = "constraint_room_objects"
    __table_args__ = (UniqueConstraint("constraint_id", "room_object_id", name="uq_constraint_room_object"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    constraint_id: Mapped[int] = mapped_column(ForeignKey("constraints.id"), nullable=False, index=True)
    room_object_id: Mapped[int] = mapped_column(ForeignKey("room_objects.id"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    constraint: Mapped["Constraint"] = relationship(back_populates="constraint_room_objects")
    room_object: Mapped["RoomObject"] = relationship(back_populates="constraint_references")
