"""
travel-ai - Main Backend Entry Point (FastAPI)
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

# 1. Sabarri's Routing Engine (which you built)
from modules.routing.routing_service import compute_optimal_route

# 2. YOUR NLP Module Routes
from api.nlp_routes import router as nlp_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("travel-ai")

app = FastAPI(
    title="Travel AI - Unified API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Register your new NLP router here
app.include_router(nlp_router)

@app.get("/")
def read_root():
    return {"status": "ONLINE", "message": "Backend is running!"}

# 4. The Routing Endpoint (Already working)
@app.post("/api/v1/trip/plan")
def generate_trip_plan(payload: dict):
    logger.info("Received trip generation request...")
    try:
        blocked_locations = payload.get("blocked_stops", [])
        profile = payload.get("traveler_profile", {"wheelchair": False, "min_age": 18, "preferences": []})
        
        route_result = compute_optimal_route(
            blocked_stops=blocked_locations, 
            traveler_profile=profile
        )
        
        return {
            "status": "SUCCESS",
            "message": "Personalized route generated successfully.",
            "data": {
                "traveler_profile_used": profile,
                "disruptions_avoided": blocked_locations,
                "itinerary": route_result["itinerary"],
                "metrics": {
                    "total_distance_km": route_result["total_distance_km"],
                    "total_activity_time_mins": route_result["total_activity_time_mins"]
                }
            }
        }
    except Exception as e:
        logger.error(f"Error processing trip: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
