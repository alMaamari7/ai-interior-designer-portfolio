from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "AI Interior Designer — Public Engineering API"
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/ai_interior_designer"
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    MIN_PASSWORD_LENGTH: int = 8
    FRONTEND_URL: str = "http://localhost:5173"
    AI_API_KEY: str | None = None
    AI_MODEL: str = "gemini-2.5-flash"


settings = Settings()
