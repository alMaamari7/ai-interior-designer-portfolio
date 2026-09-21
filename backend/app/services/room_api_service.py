from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.enums.room import RoomStatus
from app.models.room import Room
from app.models.user import User
from app.schemas.room_api import CreateRoomRequest, RoomResponse


class RoomApiService:
    def __init__(self, db: Session):
        self.db = db

    def list_rooms(self, user: User) -> list[RoomResponse]:
        rooms = self.db.execute(select(Room).where(Room.user_id == user.id).order_by(Room.updated_at.desc())).scalars().all()
        return [RoomResponse.model_validate(room) for room in rooms]

    def get_room(self, user: User, room_id: int) -> RoomResponse | None:
        room = self.db.execute(select(Room).where(Room.id == room_id, Room.user_id == user.id)).scalar_one_or_none()
        return RoomResponse.model_validate(room) if room else None

    def create_room(self, user: User, data: CreateRoomRequest) -> RoomResponse:
        room = Room(user_id=user.id, room_name=data.room_name or data.current_room_type.value.replace("_", " ").title(), current_room_type=data.current_room_type, room_shape=data.room_shape, room_layout_type=data.room_layout_type, room_size=data.room_size, ceiling_height=data.ceiling_height, wall_count=data.wall_count, room_status=RoomStatus.UNDER_REVIEW)
        self.db.add(room)
        self.db.commit()
        self.db.refresh(room)
        return RoomResponse.model_validate(room)
