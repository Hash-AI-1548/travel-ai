"""
Pydantic Schemas for Cultural Intelligence, Regional Attire, and Etiquette.
"""

from typing import List, Dict, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field


class AttireCategory(str, Enum):
    TRADITIONAL = "traditional"
    MODEST_CASUAL = "modest_casual"
    SPIRITUAL_TEMPLE = "spiritual_temple"
    FESTIVE = "festive"
    HERITAGE_WALK = "heritage_walk"


class RequirementLevel(str, Enum):
    STRICT = "strict"          # Enforced at entrance (e.g. temples, mosques)
    RECOMMENDED = "recommended" # Highly culturally appreciated
    OPTIONAL = "optional"      # General comfort


class AttireItem(BaseModel):
    """Specific clothing item recommended for cultural immersion."""
    id: str
    name: str = Field(..., description="Name of attire (e.g. 'Cotton Kurta with Stole', 'Linen Trousers')")
    local_name: Optional[str] = Field(default=None, description="Native language name (e.g. 'Kurti', 'Veshti')")
    category: AttireCategory
    description: str
    suitable_weather: List[str] = Field(default_factory=list, description="['Hot', 'Humid', 'Moderate', 'Cool', 'Rain']")
    fabric_recommendation: str = Field(default="100% Breathable Cotton / Linen")
    modesty_level: str = Field(default="High", description="High (knees & shoulders covered), Medium, Standard")
    cultural_significance: str
    styling_tips: List[str] = Field(default_factory=list)
    image_url: Optional[str] = None


class SiteDressCode(BaseModel):
    """Dress code and entry requirements for a specific monument or sacred site."""
    site_name: str
    requirement_level: RequirementLevel
    mandatory_rules: List[str] = Field(default_factory=list, description="Must-follow rules (e.g., 'Remove shoes at entrance')")
    recommended_clothing: str
    prohibited_items: List[str] = Field(default_factory=list, description="e.g. ['Shorts above knees', 'Sleeveless tops', 'Leather items']")
    shoe_policy: str = Field(default="Remove shoes before sanctum; shoe repository available")
    head_covering_required: bool = False


class EtiquetteRule(BaseModel):
    """Cultural etiquette guidelines and social norms."""
    category: str = Field(..., description="'temple_protocol', 'greetings', 'dining', 'bargaining', 'photography'")
    title: str
    description: str
    dos: List[str] = Field(default_factory=list)
    donts: List[str] = Field(default_factory=list)
    local_context: Optional[str] = None


class EssentialPhrase(BaseModel):
    """Key conversational phrases in the native destination language."""
    phrase: str = Field(..., description="English meaning (e.g. 'Thank you')")
    native_script: str = Field(..., description="Script in local language (e.g. 'धन्यवाद')")
    phonetic_pronunciation: str = Field(..., description="How to pronounce (e.g. 'Dhan-ya-vaad')")
    context: str = Field(..., description="When to use (e.g. 'After buying from an artisan')")


class AttireRecommendationRequest(BaseModel):
    """Request payload for generating tailored attire suggestions."""
    destination: str
    temperature_celsius: Optional[float] = Field(default=28.0, description="Forecast temperature")
    weather_condition: Optional[str] = Field(default="Sunny", description="'Sunny', 'Rainy', 'Hot', 'Humid', 'Cold'")
    planned_poi_categories: List[str] = Field(default_factory=list, description="['historic_temple', 'bazaar', 'fort', 'nature']")
    gender_preference: Optional[str] = Field(default="all", description="'unisex', 'male', 'female'")
    comfort_priority: str = Field(default="high", description="'high', 'balanced', 'traditional'")


class AttireRecommendationResponse(BaseModel):
    """Attire suggestions matching destination culture and weather."""
    destination: str
    weather_summary: str
    recommended_outfits: List[AttireItem] = Field(default_factory=list)
    site_dress_codes: List[SiteDressCode] = Field(default_factory=list)
    packing_checklist: List[str] = Field(default_factory=list)
    blendin_attire_boost: float = Field(default=15.0, description="Score increase in Blend-In calculation (+%)")


class CulturalGuideResponse(BaseModel):
    """Complete cultural guide response for a destination."""
    destination: str
    region_name: str
    primary_languages: List[str] = Field(default_factory=list)
    cultural_overview: str
    attire_recommendations: List[AttireItem] = Field(default_factory=list)
    site_dress_codes: List[SiteDressCode] = Field(default_factory=list)
    etiquette_rules: List[EtiquetteRule] = Field(default_factory=list)
    essential_phrases: List[EssentialPhrase] = Field(default_factory=list)
    cultural_events: List[str] = Field(default_factory=list)
