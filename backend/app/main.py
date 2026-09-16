from fastapi import FastAPI

from app.api.analysis import router as analysis_router

app = FastAPI(
    title="AI Interior Designer — Public Engineering API",
    version="0.2.0",
    description=(
        "Curated public API surface demonstrating selected engineering "
        "components of a larger private multimodal AI project."
    ),
)

app.include_router(analysis_router)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}
