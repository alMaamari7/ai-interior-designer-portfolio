from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums.room import RoomLayoutType, RoomShape, RoomStatus, RoomType


class CreateRoomRequest(BaseModel):
    room_name: str | None = None
    current_room_type: RoomType
    room_shape: RoomShape
    room_layout_type: RoomLayoutType
    room_size: float = Field(gt=0)
    ceiling_height: float | None = Field(default=None, gt=0)
    wall_count: int = Field(gt=0)


class RoomResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    room_name: str | None
    current_room_type: RoomType
    room_shape: RoomShape
    room_layout_type: RoomLayoutType
    room_size: float
    ceiling_height: float | None
    room_status: RoomStatus
    wall_count: int
    created_at: datetime
    updated_at: datetime
