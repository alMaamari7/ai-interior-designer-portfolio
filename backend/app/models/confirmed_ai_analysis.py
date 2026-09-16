from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.ai_analysis import AIAnalysis


class ConfirmedAIAnalysis(Base):
    """Human-confirmed version of an AI result."""

    __tablename__ = "confirmed_ai_analyses"

    id: Mapped[int] = mapped_column(primary_key=True)
    ai_analysis_id: Mapped[int] = mapped_column(
        ForeignKey("ai_analyses.id"), unique=True, nullable=False
    )
    result: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    ai_analysis: Mapped["AIAnalysis"] = relationship(
        back_populates="confirmed_analysis"
    )
