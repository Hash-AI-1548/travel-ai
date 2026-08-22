from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict

class TripGenerateRequest(BaseModel):
    destination: str = Field(..., json_schema_extra={"example": "Kyoto, Japan"})
    start_date: Optional[str] = Field(None, json_schema_extra={"example": "2026-10-15"})
    duration_days: int = Field(default=3, ge=1, le=14, json_schema_extra={"example": 3})
    custom_notes: Optional[str] = Field(None, json_schema_extra={"example": "Looking for peaceful morning walks and scenic tea houses"})

class DayActivity(BaseModel):
    time_slot: str
    activity_name: str
    location: str
    description: str
    style_tags: List[str] = []
    accessibility_notes: str
    dress_code_advice: str

class AccommodationRecommendation(BaseModel):
    hotel_name: str
    tier: str
    accessibility_features: List[str]
    vibe: str
    neighborhood: str

class DayItinerary(BaseModel):
    day_number: int
    theme: str
    activities: List[DayActivity]
    recommended_stay: Optional[AccommodationRecommendation] = None

class DiningSpot(BaseModel):
    meal_type: str
    restaurant_name: str
    cuisine: str
    dietary_alignment: str
    allergy_safety_note: str
    estimated_cost_tier: str

class PackingChecklist(BaseModel):
    essentials: List[str]
    clothing_items: List[str]
    modesty_specific_items: List[str]
    weather_adaptation_items: List[str]
    special_accessibility_items: List[str]

class BudgetBreakdown(BaseModel):
    total_estimated_range: str
    tier_label: str
    accommodation_share: str
    dining_share: str
    activities_share: str
    transit_share: str

class TripResponse(BaseModel):
    id: int
    user_id: int
    destination: str
    start_date: Optional[str] = None
    duration_days: int
    custom_notes: Optional[str] = None
    itinerary: List[Dict[str, Any]]
    dining_recommendations: List[Dict[str, Any]]
    packing_checklist: Dict[str, Any]
    budget_breakdown: Dict[str, Any]
    applied_preferences: Dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
