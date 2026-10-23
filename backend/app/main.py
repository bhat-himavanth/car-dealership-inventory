"""Application entry point. Run with:  uvicorn app.main:app --reload"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import auth, vehicles


def create_app() -> FastAPI:
    app = FastAPI(title="Car Dealership Inventory API")

    # Lets the React app (a different origin) call this API from the browser.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router)
    app.include_router(vehicles.router)

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    return app


# Creates the tables if they don't exist yet (fine for a project this size;
# a bigger app would use migrations, e.g. Alembic).
Base.metadata.create_all(bind=engine)

app = create_app()