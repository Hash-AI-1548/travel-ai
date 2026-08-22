"""
Travel AI Backend Application Entrypoint.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from backend.api.blendin_routes import router as blendin_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("travel_ai")

app = FastAPI(
    title="Travel AI Planner API",
    description="AI-Powered Personalized Travel Itinerary & Cultural Intelligence Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(blendin_router)


@app.get("/", tags=["Health"])
def root():
    return {
        "status": "online",
        "service": "Travel AI Planner API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "blendin": "/api/blendin"
        }
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}
