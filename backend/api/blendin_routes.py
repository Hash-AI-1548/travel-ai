"""
FastAPI Routes for Blend-In Scoring, Evaluation, and Target Fine-Tuning.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Query, status
import logging

from backend.schemas.blendin import (
    BlendInScoreResponse,
    BlendInEvaluationRequest,
    BlendInTargetRequest,
    BlendInOptimizationResult,
    BlendInRecommendation
)
from backend.modules.blendin.blendin_engine import BlendInEngine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/blendin", tags=["Blend-In Score"])
blendin_engine = BlendInEngine()


@router.post(
    "/evaluate",
    response_model=BlendInScoreResponse,
    summary="Evaluate Itinerary Blend-In Score",
    description="Calculates composite Blend-In Score (0-100%), authenticity, familiarity, dimensional breakdowns, and recommendations."
)
def evaluate_blendin(request: BlendInEvaluationRequest) -> BlendInScoreResponse:
    try:
        response = blendin_engine.evaluate_itinerary(request)
        return response
    except Exception as e:
        logger.error(f"Error evaluating blend-in score: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate blend-in score: {str(e)}"
        )


@router.post(
    "/optimize-target",
    response_model=BlendInOptimizationResult,
    summary="Re-plan for Target Blend-In Score",
    description="Triggered when the user adjusts the Blend-In slider. Generates fine-tuning modifiers and candidate swaps."
)
def optimize_for_target(request: BlendInTargetRequest) -> BlendInOptimizationResult:
    try:
        result = blendin_engine.optimize_for_target_blendin(request)
        return result
    except Exception as e:
        logger.error(f"Error optimizing for target blend-in score: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fine-tune for target blend-in score: {str(e)}"
        )


@router.get(
    "/tiers",
    summary="Get Blend-In Tiers Metadata",
    description="Returns metadata, thresholds, and descriptions for each blend-in persona level."
)
def get_blendin_tiers() -> List[Dict[str, Any]]:
    return [
        {
            "tier": "Tourist Bubble",
            "min_score": 0,
            "max_score": 25,
            "icon": "🏖️",
            "color": "#3B82F6",
            "title": "Tourist Bubble",
            "description": "Standard international sights, resort comforts, and minimal cultural friction."
        },
        {
            "tier": "Comfort Explorer",
            "min_score": 26,
            "max_score": 50,
            "icon": "🧭",
            "color": "#10B981",
            "title": "Comfort Explorer",
            "description": "Popular iconic landmarks combined with accessible introductions to local culture."
        },
        {
            "tier": "Cultural Immersion",
            "min_score": 51,
            "max_score": 75,
            "icon": "🕌",
            "color": "#F59E0B",
            "title": "Cultural Immersion",
            "description": "Rich heritage experiences, traditional dining, cultural attire, and respectful etiquette."
        },
        {
            "tier": "Local Insider",
            "min_score": 76,
            "max_score": 100,
            "icon": "✨",
            "color": "#8B5CF6",
            "title": "Local Insider",
            "description": "Off-the-beaten-path hidden gems, artisan quarters, morning markets, and native daily rhythm."
        }
    ]


@router.get(
    "/tips/{destination}",
    response_model=List[BlendInRecommendation],
    summary="Get Destination Blend-In Tips",
    description="Quick cultural, attire, food, and etiquette tips for a specific destination."
)
def get_destination_tips(destination: str) -> List[BlendInRecommendation]:
    tips = [
        BlendInRecommendation(
            category="attire",
            title="Respectful Temple & Heritage Attire",
            description=f"In {destination.title()}, cover knees and shoulders when entering sanctums. Slip-on footwear is convenient.",
            impact_score_boost=6.0,
            difficulty="Easy",
            cultural_context="Standard religious and cultural respect observed by locals."
        ),
        BlendInRecommendation(
            category="timing",
            title="Embrace Morning Rhythm",
            description="Start early at 7:00 AM to catch traditional flower markets and cooler morning tranquility.",
            impact_score_boost=7.5,
            difficulty="Moderate",
            cultural_context="Local commerce and spiritual life thrives in early morning hours."
        ),
        BlendInRecommendation(
            category="food",
            title="Heritage Street Breakfast",
            description="Seek out legendary local breakfast spots for freshly made regional snacks and hot chai.",
            impact_score_boost=8.0,
            difficulty="Easy",
            cultural_context="Every neighborhood has a generational tea/snack stall cherished by residents."
        ),
        BlendInRecommendation(
            category="etiquette",
            title="Warm Greetings & Courtesies",
            description="Greet shopkeepers and artisans with a warm local greeting. Bargaining should always remain friendly and smiling.",
            impact_score_boost=4.5,
            difficulty="Easy",
            cultural_context="Builds instant connection and mutual respect."
        )
    ]
    return tips
