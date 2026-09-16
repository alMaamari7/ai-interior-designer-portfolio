from fastapi import FastAPI

app = FastAPI(
    title="AI Interior Designer — Public Engineering API",
    version="0.1.0",
    description=(
        "Curated public API surface demonstrating selected engineering "
        "components of a larger private multimodal AI project."
    ),
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}
