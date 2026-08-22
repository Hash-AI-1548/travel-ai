"""
Pydantic Schemas for Blend-In Scoring and Dynamic Optimization.

The Blend-In Score quantifies how effectively a traveler immerses into the
local culture, habits, and lifestyle of the destination while respecting
personal comfort, dietary needs, accessibility, and pacing.
"""

from typing import List, Dict, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field


class BlendInTier(str, Enum):
    """Tier/persona classification based on Blend-In Score percentage."""
    TOURIST_BUBBLE = "Tourist Bubble"          # 0 - 25%: Standard international sights, zero local friction
    COMFORT_EXPLORER = "Comfort Explorer"      # 26 - 50%: Popular landmarks with gentle cultural touches
    CULTURAL_IMMERSION = "Cultural Immersion"  # 51 - 75%: High local flavor, traditional food & customs
    LOCAL_INSIDER = "Local Insider"            # 76 - 100%: Deep authenticity, off-the-beaten-path, native rhythm


class ScoreDimension(BaseModel):
    """Detailed score and rationale for a single dimension of blending in."""
    name: str = Field(..., description="Dimension name (e.g., 'Authentic Dining', 'Heritage Immersion')")
    score: float = Field(..., ge=0.0, le=100.0, description="Score on 0-100 scale")
    weight: float = Field(..., ge=0.0, le=1.0, description="Weight of this dimension in composite calculation")
    description: str = Field(..., description="Explanation of why this score was assigned")
    strengths: List[str] = Field(default_factory=list, description="Positives that boosted the score")
    opportunities: List[str] = Field(default_factory=list, description="Ways to increase blending in this dimension")


class BlendInBreakdown(BaseModel):
    """Component-level breakdown of the Blend-In evaluation."""
    authenticity_score: float = Field(..., ge=0.0, le=100.0, description="POI & activity local authenticity")
    familiarity_score: float = Field(..., ge=0.0, le=100.0, description="Personal comfort and habit compatibility")
    cultural_adaptation_score: float = Field(..., ge=0.0, le=100.0, description="Attire, etiquette, and customs alignment")
    culinary_immersion_score: float = Field(..., ge=0.0, le=100.0, description="Local food exploration vs familiar bridge")
    local_interaction_score: float = Field(..., ge=0.0, le=100.0, description="Engagement with local markets and community")
    dimensions: List[ScoreDimension] = Field(default_factory=list, description="Granular dimensional breakdowns")


class BlendInRecommendation(BaseModel):
    """Specific actionable tip for the traveler to blend in better or adjust comfort."""
    category: str = Field(..., description="Category: 'attire', 'food', 'etiquette', 'timing', 'phrase', 'activity'")
    title: str = Field(..., description="Short catchy recommendation title")
    description: str = Field(..., description="Actionable detail for the traveler")
    impact_score_boost: float = Field(default=0.0, description="Estimated score increase percentage (+%) if adopted")
    difficulty: str = Field(default="Easy", description="Level of effort: 'Easy', 'Moderate', 'Adventurous'")
    cultural_context: Optional[str] = Field(default=None, description="Why locals do this / background etiquette")


class POIBlendinProfile(BaseModel):
    """Blend-in characteristics of a specific POI or activity."""
    poi_id: str
    poi_name: str
    authenticity_index: float = Field(..., ge=0.0, le=1.0, description="0.0 = commercial tourist trap, 1.0 = deep local spot")
    tourist_density: float = Field(..., ge=0.0, le=1.0, description="0.0 = zero tourists, 1.0 = heavy tourist crowds")
    cultural_depth: float = Field(..., ge=0.0, le=1.0, description="Cultural engagement potential")
    local_etiquette_required: bool = False
    recommended_attire: Optional[str] = None


class POISwapSuggestion(BaseModel):
    """Recommended POI replacement when shifting towards target blend-in score."""
    current_poi_id: str
    current_poi_name: str
    suggested_poi_id: str
    suggested_poi_name: str
    reason: str
    blendin_score_delta: float = Field(..., description="Score change (+/- %) from this swap")


class BlendInScoreResponse(BaseModel):
    """Complete evaluation response returned by Blend-In engine."""
    overall_score: float = Field(..., ge=0.0, le=100.0, description="Composite Blend-In percentage (0-100%)")
    tier: BlendInTier = Field(..., description="Persona level based on overall score")
    tagline: str = Field(..., description="Short descriptive tagline (e.g., 'Authentic Cultural Explorer')")
    breakdown: BlendInBreakdown
    recommendations: List[BlendInRecommendation] = Field(default_factory=list)
    local_comparison_percentile: float = Field(
        ..., ge=0.0, le=100.0,
        description="How close this itinerary is to a true local's weekend/day (% vs native benchmark)"
    )


class BlendInEvaluationRequest(BaseModel):
    """Request payload for evaluating an existing itinerary's Blend-In Score."""
    destination: str
    source: Optional[str] = None
    poi_list: List[Dict[str, Any]] = Field(default_factory=list, description="List of scheduled POIs")
    restaurant_list: List[Dict[str, Any]] = Field(default_factory=list, description="List of scheduled restaurants/food stops")
    user_preferences: Dict[str, Any] = Field(default_factory=dict, description="Dietary, habits, cultural, demographic preferences")
    selected_attire_count: int = Field(default=0, description="Number of culturally tailored outfits adopted")
    etiquette_acknowledgement: bool = Field(default=False, description="Whether traveler reviewed local etiquette")


class BlendInTargetRequest(BaseModel):
    """Request to re-tune an itinerary according to a target Blend-In Score slider."""
    destination: str
    current_score: float = Field(..., ge=0.0, le=100.0, description="Current itinerary blend-in score")
    target_score: float = Field(..., ge=0.0, le=100.0, description="Target blend-in score (0-100) set by traveler")
    candidate_pois: List[Dict[str, Any]] = Field(default_factory=list, description="All available candidate POIs")
    candidate_restaurants: List[Dict[str, Any]] = Field(default_factory=list, description="All available candidate restaurants")
    current_selected_poi_ids: List[str] = Field(default_factory=list, description="Currently selected POI IDs")
    user_preferences: Dict[str, Any] = Field(default_factory=dict, description="Traveler demographic, dietary, and habit profile")


class BlendInOptimizationResult(BaseModel):
    """Optimization parameters generated when adjusting to a target Blend-In Score."""
    target_score: float
    projected_score: float
    poi_weight_modifiers: Dict[str, float] = Field(
        default_factory=dict,
        description="Weight multipliers (e.g. {'authenticity_weight': 1.4, 'tourist_icon_weight': 0.6})"
    )
    suggested_swaps: List[POISwapSuggestion] = Field(default_factory=list, description="Recommended POI swaps")
    fine_tuning_parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Parameters passed back into ItineraryOptimizer to regenerate the plan"
    )
    actionable_tips: List[BlendInRecommendation] = Field(default_factory=list)
