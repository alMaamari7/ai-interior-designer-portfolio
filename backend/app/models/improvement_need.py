from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.design_request import DesignRequest


class ImprovementNeed(Base):
    __tablename__ = "improvement_needs"

    id: Mapped[int] = mapped_column(primary_key=True)
    design_request_id: Mapped[int] = mapped_column(ForeignKey("design_requests.id"), nullable=False, index=True)
    improvement_description: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    design_request: Mapped["DesignRequest"] = relationship(back_populates="improvement_needs")
