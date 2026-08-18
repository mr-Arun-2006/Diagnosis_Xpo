from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.ai import router as ai_router
from app.api.routes.auth import router as auth_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.diagnosis import router as diagnosis_router
from app.api.routes.eod import router as eod_router
from app.api.routes.health import router as health_router
from app.api.routes.ingestion import router as ingestion_router
from app.api.routes.instruments import router as instruments_router
from app.api.routes.market import router as market_router
from app.api.routes.screener import router as screener_router
from app.core.config import settings
from app.db import initialize_database


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Diagnosis_Xpo API",
    version="1.0.0",
    description="Evidence-first Indian market intelligence API.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in (
    health_router,
    market_router,
    instruments_router,
    ingestion_router,
    eod_router,
    dashboard_router,
    auth_router,
    diagnosis_router,
    screener_router,
    ai_router,
):
    app.include_router(router, prefix="/api/v1")


@app.get("/")
def root():
    return {"name": settings.app_name, "status": "ok", "version": "1.0.0", "docs": "/docs"}
