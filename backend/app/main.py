"""
Flight Delay Predictor - FastAPI Backend
"""
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.routers import flights, data, predict
from app.services.database import init_db

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup
    print("[START] Starting Flight Delay Predictor API...")
    await init_db()
    print("[OK] Database initialized")
    yield
    # Shutdown
    print("[STOP] Shutting down...")


app = FastAPI(
    title="Flight Delay Predictor API",
    description="API for analyzing and predicting flight delays using ML",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Configuration
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
allowed_origins = [origin.strip() for origin in frontend_url.split(",")]
allowed_origins.append("http://localhost:5173")  # always allow local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(flights.router, prefix="/api/flights", tags=["Flights"])
app.include_router(data.router, prefix="/api/data", tags=["Data"])
app.include_router(predict.router, prefix="/api/predict", tags=["Prediction"])


@app.get("/api/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "success": True,
        "message": "Flight Delay Predictor API is running",
        "version": "1.0.0",
    }
