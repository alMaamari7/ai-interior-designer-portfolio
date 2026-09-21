from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.room_api import CreateRoomRequest, RoomResponse
from app.services.room_api_service import RoomApiService

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("", response_model=list[RoomResponse])
def list_rooms(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return RoomApiService(db).list_rooms(current_user)


@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    room = RoomApiService(db).get_room(current_user, room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found.")
    return room


@router.post("", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(request: CreateRoomRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return RoomApiService(db).create_room(current_user, request)
