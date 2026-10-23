from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine


def create_app() -> FastAPI:
    app = FastAPI(title="Car Dealership Inventory API")

    # Lets the React app (a different origin) call this API from the browser.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    return app


Base.metadata.create_all(bind=engine)

app = create_app()