from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.auth import router as auth_router
from app.api.routes.diagnosis import router as diagnosis_router
from app.api.routes.health import router as health_router
from app.api.routes.market import router as market_router
from app.core.config import settings
from app.db import initialize_database


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Diagnosis_Xpo API",
    version="0.3.0",
    description="Market intelligence API with deterministic quantitative diagnosis.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(market_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(diagnosis_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"name": settings.app_name, "status": "ok", "version": "0.3.0", "docs": "/docs"}
