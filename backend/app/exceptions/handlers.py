from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.auth import EmailAlreadyExistsError, InvalidCredentialsError, InvalidTokenError, PasswordsDoNotMatchError, PasswordTooShortError


def register_exception_handlers(app: FastAPI) -> None:
    mapping = {
        EmailAlreadyExistsError: (409, "Email already exists."),
        PasswordsDoNotMatchError: (400, "Passwords do not match."),
        PasswordTooShortError: (400, "Password does not meet the minimum length."),
        InvalidCredentialsError: (401, "Invalid email or password."),
        InvalidTokenError: (401, "Invalid or expired access token."),
    }
    for exception_type, (status_code, message) in mapping.items():
        async def handler(request: Request, exc: Exception, code=status_code, detail=message):
            return JSONResponse(status_code=code, content={"detail": detail})
        app.add_exception_handler(exception_type, handler)
