from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.budget import Budget
    from app.models.constraint import Constraint
    from app.models.design_goal import DesignGoal
    from app.models.household import Household
    from app.models.improvement_need import ImprovementNeed
    from app.models.room import Room
    from app.models.room_activity import RoomActivity
    from app.models.room_function import RoomFunction


class DesignRequest(Base):
    __tablename__ = "design_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False, index=True)
    design_request: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    room: Mapped["Room"] = relationship(back_populates="design_requests")
    design_goal: Mapped["DesignGoal | None"] = relationship(back_populates="design_request", uselist=False, cascade="all, delete-orphan")
    budget: Mapped["Budget | None"] = relationship(back_populates="design_request", uselist=False, cascade="all, delete-orphan")
    constraint: Mapped["Constraint | None"] = relationship(back_populates="design_request", uselist=False, cascade="all, delete-orphan")
    improvement_needs: Mapped[list["ImprovementNeed"]] = relationship(back_populates="design_request", cascade="all, delete-orphan")
    household: Mapped["Household | None"] = relationship(back_populates="design_request", uselist=False, cascade="all, delete-orphan")
    room_functions: Mapped[list["RoomFunction"]] = relationship(back_populates="design_request", cascade="all, delete-orphan")
    room_activities: Mapped[list["RoomActivity"]] = relationship(back_populates="design_request", cascade="all, delete-orphan")
