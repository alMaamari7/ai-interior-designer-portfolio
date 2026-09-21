from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums.design_request import DesiredAtmosphere
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.design_request import DesignRequest


class DesignGoal(Base):
    __tablename__ = "design_goals"
    __table_args__ = tuple(
        CheckConstraint(f"{field} BETWEEN 1 AND 10", name=f"ck_design_goal_{field}")
        for field in (
            "desired_brightness",
            "desired_warmth",
            "desired_naturalness",
            "desired_minimalism",
            "desired_color_intensity",
        )
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    design_request_id: Mapped[int] = mapped_column(ForeignKey("design_requests.id"), nullable=False, unique=True, index=True)
    goal_description: Mapped[str] = mapped_column(String(1000), nullable=False)
    desired_atmospheres: Mapped[list[DesiredAtmosphere]] = mapped_column(ARRAY(Enum(DesiredAtmosphere, name="desired_atmosphere_enum")), nullable=False)
    desired_brightness: Mapped[int] = mapped_column(Integer, nullable=False)
    desired_warmth: Mapped[int] = mapped_column(Integer, nullable=False)
    desired_naturalness: Mapped[int] = mapped_column(Integer, nullable=False)
    desired_minimalism: Mapped[int] = mapped_column(Integer, nullable=False)
    desired_color_intensity: Mapped[int] = mapped_column(Integer, nullable=False)
    preferred_style: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    design_request: Mapped["DesignRequest"] = relationship(back_populates="design_goal")
