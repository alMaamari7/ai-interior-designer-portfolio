from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.core.settings import settings
from app.exceptions.auth import EmailAlreadyExistsError, InvalidCredentialsError, PasswordsDoNotMatchError, PasswordTooShortError
from app.models.user import User
from app.schemas.user import AuthResponse, LoginRequest, RegisterRequest, UserResponse


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, data: RegisterRequest) -> AuthResponse:
        if self.db.execute(select(User).where(User.email == data.email)).scalar_one_or_none():
            raise EmailAlreadyExistsError()
        if data.password != data.confirm_password:
            raise PasswordsDoNotMatchError()
        if len(data.password) < settings.MIN_PASSWORD_LENGTH:
            raise PasswordTooShortError()

        user = User(first_name=data.first_name, last_name=data.last_name, email=data.email, hashed_password=hash_password(data.password))
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return AuthResponse(access_token=create_access_token(user.id), user=UserResponse.model_validate(user))

    def login(self, data: LoginRequest) -> AuthResponse:
        user = self.db.execute(select(User).where(User.email == data.email)).scalar_one_or_none()
        if user is None or not verify_password(data.password, user.hashed_password):
            raise InvalidCredentialsError()
        return AuthResponse(access_token=create_access_token(user.id), user=UserResponse.model_validate(user))
