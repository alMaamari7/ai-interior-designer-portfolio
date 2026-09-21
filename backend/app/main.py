from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analysis import router as analysis_router
from app.api.auth import router as auth_router
from app.api.capture import router as capture_router
from app.api.rooms import router as rooms_router
from app.api.users import router as users_router
from app.api.vision import router as vision_router
from app.core.settings import settings
from app.exceptions.handlers import register_exception_handlers

app = FastAPI(
    title=settings.APP_NAME,
    version="0.4.0",
    description="Curated public engineering API demonstrating the safe application path from authentication through deterministic image-quality validation.",
)
app.add_middleware(CORSMiddleware, allow_origins=[settings.FRONTEND_URL], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
register_exception_handlers(app)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(rooms_router)
app.include_router(capture_router)
app.include_router(vision_router)
app.include_router(analysis_router)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}
