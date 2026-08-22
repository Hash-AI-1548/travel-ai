from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict

class PersonalInfoStep(BaseModel):
    full_name: Optional[str] = Field(None, json_schema_extra={"example": "Evelyn Thorne"})
    age: Optional[int] = Field(None, ge=1, le=120, json_schema_extra={"example": 29})
    gender: Optional[str] = Field(None, json_schema_extra={"example": "Female"})
    nationality: Optional[str] = Field(None, json_schema_extra={"example": "Canadian"})
    home_city: Optional[str] = Field(None, json_schema_extra={"example": "Vancouver, BC"})
    personal_notes: Optional[str] = Field(None, json_schema_extra={"example": "Celebrating 5th wedding anniversary"})
    profile_picture_url: Optional[str] = None
    languages_spoken: List[str] = Field(default_factory=list, json_schema_extra={"example": ["English", "French"]})

class TravelerTypeStep(BaseModel):
    traveler_type: str = Field(..., description="solo, couple, family, friends, senior", json_schema_extra={"example": "couple"})
    traveler_type_custom: Optional[str] = Field(None, json_schema_extra={"example": "Traveling with a small golden retriever pet"})

    @field_validator("traveler_type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        valid = ["solo", "couple", "family", "friends", "senior"]
        if v.lower() not in valid:
            raise ValueError(f"traveler_type must be one of: {', '.join(valid)}")
        return v.lower()

class AccessibilityStep(BaseModel):
    accessibility_mobility: bool = False
    accessibility_visual: bool = False
    accessibility_hearing: bool = False
    accessibility_senior: bool = False
    accessibility_child: bool = False
    accessibility_none: bool = False
    accessibility_custom: Optional[str] = Field(None, json_schema_extra={"example": "Need room with power outlet near bed for CPAP device"})

class TravelStylesStep(BaseModel):
    travel_styles: List[str] = Field(..., min_length=1, json_schema_extra={"example": ["adventure", "nature", "culture", "food_wine", "photography"]})
    travel_styles_custom: Optional[str] = Field(None, json_schema_extra={"example": "Interested in pottery making and retro jazz bars"})

class FoodPreferencesStep(BaseModel):
    dietary_standards: List[str] = Field(default_factory=list, json_schema_extra={"example": ["vegetarian", "halal"]})
    allergies_restrictions: Optional[str] = Field(None, json_schema_extra={"example": "Severe peanut allergy, prefers gluten-free options where possible"})
    food_custom: Optional[str] = Field(None, json_schema_extra={"example": "Prefer organic farm-to-table restaurants and tea ceremonies"})

class ClothingStep(BaseModel):
    pack_styles: List[str] = Field(default_factory=list, json_schema_extra={"example": ["western", "casual"]})
    modest_clothing: bool = False
    prioritize_hot_weather: bool = False
    clothing_custom: Optional[str] = Field(None, json_schema_extra={"example": "Need formal cocktail outfit for one fine dining dinner"})

class BudgetStep(BaseModel):
    budget_tier: str = Field(..., description="budget, moderate, premium_luxury, flexible", json_schema_extra={"example": "moderate"})
    budget_currency: Optional[str] = Field("INR", json_schema_extra={"example": "INR"})
    budget_custom: Optional[str] = Field(None, json_schema_extra={"example": "₹6,000 – ₹8,000 / day per person"})
    budget_standardized_usd: Optional[str] = Field(None, json_schema_extra={"example": "$70 – $95 USD / day"})

    @field_validator("budget_tier")
    @classmethod
    def validate_tier(cls, v: str) -> str:
        valid = ["budget", "moderate", "premium_luxury", "flexible"]
        if v.lower() not in valid:
            raise ValueError(f"budget_tier must be one of: {', '.join(valid)}")
        return v.lower()

class PassportFullUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    nationality: Optional[str] = None
    home_city: Optional[str] = None
    personal_notes: Optional[str] = None
    profile_picture_url: Optional[str] = None
    languages_spoken: Optional[List[str]] = None
    traveler_type: Optional[str] = None
    traveler_type_custom: Optional[str] = None
    accessibility_mobility: Optional[bool] = None
    accessibility_visual: Optional[bool] = None
    accessibility_hearing: Optional[bool] = None
    accessibility_senior: Optional[bool] = None
    accessibility_child: Optional[bool] = None
    accessibility_none: Optional[bool] = None
    accessibility_custom: Optional[str] = None
    travel_styles: Optional[List[str]] = None
    travel_styles_custom: Optional[str] = None
    dietary_standards: Optional[List[str]] = None
    allergies_restrictions: Optional[str] = None
    food_custom: Optional[str] = None
    pack_styles: Optional[List[str]] = None
    modest_clothing: Optional[bool] = None
    prioritize_hot_weather: Optional[bool] = None
    clothing_custom: Optional[str] = None
    budget_tier: Optional[str] = None
    budget_currency: Optional[str] = None
    budget_custom: Optional[str] = None
    budget_standardized_usd: Optional[str] = None

class SummaryItem(BaseModel):
    title: str
    headline: str
    subtext: str
    step_number: int
    data: Dict[str, Any]

class PassportSummaryResponse(BaseModel):
    is_ready: bool
    status_badge: str
    personal_info: SummaryItem
    traveler_type: SummaryItem
    accessibility: SummaryItem
    travel_style: SummaryItem
    food_preferences: SummaryItem
    clothing_pack: SummaryItem
    budget_footprint: SummaryItem

class PassportResponse(BaseModel):
    id: int
    user_id: int
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    nationality: Optional[str] = None
    home_city: Optional[str] = None
    personal_notes: Optional[str] = None
    profile_picture_url: Optional[str] = None
    languages_spoken: List[str] = []
    traveler_type: Optional[str] = None
    traveler_type_custom: Optional[str] = None
    accessibility_mobility: bool = False
    accessibility_visual: bool = False
    accessibility_hearing: bool = False
    accessibility_senior: bool = False
    accessibility_child: bool = False
    accessibility_none: bool = False
    accessibility_custom: Optional[str] = None
    travel_styles: List[str] = []
    travel_styles_custom: Optional[str] = None
    dietary_standards: List[str] = []
    allergies_restrictions: Optional[str] = None
    food_custom: Optional[str] = None
    pack_styles: List[str] = []
    modest_clothing: bool = False
    prioritize_hot_weather: bool = False
    clothing_custom: Optional[str] = None
    budget_tier: Optional[str] = None
    budget_currency: Optional[str] = "INR"
    budget_custom: Optional[str] = None
    budget_standardized_usd: Optional[str] = None
    current_step: int = 1
    is_completed: bool = False
    completion_percentage: int = 0
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
