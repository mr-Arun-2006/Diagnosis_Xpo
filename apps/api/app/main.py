from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.health import router as health_router
from app.api.routes.market import router as market_router

app = FastAPI(title="Diagnosis_Xpo API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(market_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"name": "Diagnosis_Xpo", "status": "ok", "docs": "/docs"}
