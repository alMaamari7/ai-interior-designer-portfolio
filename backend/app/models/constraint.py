from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums.design_request import ModifiableArea, OwnershipType, PropertyUsage
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.constraint_room_object import ConstraintRoomObject
    from app.models.design_request import DesignRequest


class Constraint(Base):
    __tablename__ = "constraints"

    id: Mapped[int] = mapped_column(primary_key=True)
    design_request_id: Mapped[int] = mapped_column(ForeignKey("design_requests.id"), nullable=False, unique=True, index=True)
    ownership_type: Mapped[OwnershipType] = mapped_column(Enum(OwnershipType), nullable=False)
    property_usage: Mapped[PropertyUsage] = mapped_column(Enum(PropertyUsage), nullable=False)
    allow_wall_mounting: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    modifiable_areas: Mapped[list[ModifiableArea]] = mapped_column(ARRAY(Enum(ModifiableArea, name="modifiable_area_enum")), nullable=False)
    additional_constraints: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    design_request: Mapped["DesignRequest"] = relationship(back_populates="constraint")
    constraint_room_objects: Mapped[list["ConstraintRoomObject"]] = relationship(back_populates="constraint", cascade="all, delete-orphan")
