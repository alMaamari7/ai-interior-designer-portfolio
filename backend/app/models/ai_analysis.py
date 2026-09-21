from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums.analysis import AnalysisStatus, AnalysisType
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.confirmed_ai_analysis import ConfirmedAIAnalysis
    from app.models.room import Room


class AIAnalysis(Base):
    """Persisted AI run with intentionally abstract public analysis categories."""

    __tablename__ = "ai_analyses"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), index=True)
    analysis_type: Mapped[AnalysisType] = mapped_column(
        Enum(AnalysisType), nullable=False
    )
    status: Mapped[AnalysisStatus] = mapped_column(
        Enum(AnalysisStatus),
        nullable=False,
        default=AnalysisStatus.PENDING,
    )
    model_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    room: Mapped["Room"] = relationship(back_populates="ai_analyses")
    confirmed_analysis: Mapped["ConfirmedAIAnalysis | None"] = relationship(
        back_populates="ai_analysis",
        uselist=False,
        cascade="all, delete-orphan",
    )
