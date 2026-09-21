from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.design_request import DesignRequest


class Budget(Base):
    __tablename__ = "budgets"
    __table_args__ = (
        CheckConstraint("minimum_budget >= 0", name="ck_budget_minimum_non_negative"),
        CheckConstraint("maximum_budget >= minimum_budget", name="ck_budget_valid_range"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    design_request_id: Mapped[int] = mapped_column(ForeignKey("design_requests.id"), nullable=False, unique=True, index=True)
    minimum_budget: Mapped[int] = mapped_column(Integer, nullable=False)
    maximum_budget: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(50), nullable=False, default="EUR", server_default="EUR")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    design_request: Mapped["DesignRequest"] = relationship(back_populates="budget")
