from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user_id
from app.schemas.trip import TripGenerateRequest, TripResponse
from app.services.passport_service import get_or_create_passport
from app.services.ai_travel_service import generate_trip_plan, get_user_trips, get_trip_by_id, delete_trip
from app.models.trip import Trip

router = APIRouter(prefix="/trips", tags=["AI Trip Planner & Itineraries"])

@router.post("/generate", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def generate_trip(
    req: TripGenerateRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Generate a personalized AI travel itinerary and packing guide using the user's Travel Passport."""
    passport = get_or_create_passport(db, user_id)
    trip = generate_trip_plan(db, user_id, req, passport)
    return trip

@router.get("", response_model=List[TripResponse])
def list_trips(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """List all trips generated for the current user."""
    return get_user_trips(db, user_id)

@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(trip_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Retrieve details of a generated trip."""
    trip = get_trip_by_id(db, trip_id, user_id)
    if not trip:
        raise HTTPException(status_code=404, detail=f"Trip with ID {trip_id} not found")
    return trip

@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_trip(trip_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Delete a saved trip."""
    success = delete_trip(db, trip_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Trip with ID {trip_id} not found")
    return None
