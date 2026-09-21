from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions.auth import EmailAlreadyExistsError
from app.models.user import User
from app.schemas.user import UpdateUserRequest, UserResponse


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def update(self, current_user: User, data: UpdateUserRequest) -> UserResponse:
        if data.email != current_user.email:
            existing = self.db.execute(select(User).where(User.email == data.email)).scalar_one_or_none()
            if existing is not None and existing.id != current_user.id:
                raise EmailAlreadyExistsError()
        current_user.first_name = data.first_name
        current_user.last_name = data.last_name
        current_user.email = data.email
        try:
            self.db.commit()
            self.db.refresh(current_user)
        except Exception:
            self.db.rollback()
            raise
        return UserResponse.model_validate(current_user)
