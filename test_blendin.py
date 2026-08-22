"""
Unit and Integration Tests for Blend-In Scoring Engine, Components, and Routes.
"""

import pytest
from backend.schemas.blendin import (
    BlendInEvaluationRequest,
    BlendInTargetRequest,
    BlendInTier
)
from backend.modules.blendin.authenticity_score import AuthenticityScorer
from backend.modules.blendin.familiarity_score import FamiliarityScorer
from backend.modules.blendin.blendin_engine import BlendInEngine
from backend.api.blendin_routes import evaluate_blendin, optimize_for_target, get_blendin_tiers, get_destination_tips


@pytest.fixture
def sample_pois():
    return [
        {
            "id": "poi_1",
            "name": "Amber Palace & Fort",
            "category": "historic_temple",
            "authenticity_index": 0.85,
            "tourist_density": 0.70,
            "cultural_depth": 0.90,
            "duration_minutes": 120,
            "start_time": "08:00",
            "is_wheelchair_accessible": True,
            "is_elder_friendly": True,
            "is_child_friendly": True,
            "walking_distance_km": 1.2
        },
        {
            "id": "poi_2",
            "name": "Anokhi Hand-Block Printing Workshop",
            "category": "heritage_craft",
            "authenticity_index": 0.92,
            "tourist_density": 0.30,
            "cultural_depth": 0.95,
            "duration_minutes": 90,
            "start_time": "11:00",
            "is_wheelchair_accessible": True,
            "is_elder_friendly": True,
            "is_child_friendly": True,
            "walking_distance_km": 0.5
        },
        {
            "id": "poi_3",
            "name": "Old City Bapu Bazaar Evening Walk",
            "category": "bazaar",
            "authenticity_index": 0.88,
            "tourist_density": 0.60,
            "cultural_depth": 0.85,
            "duration_minutes": 90,
            "start_time": "17:30",
            "is_wheelchair_accessible": False,
            "is_elder_friendly": True,
            "is_child_friendly": True,
            "walking_distance_km": 1.5
        }
    ]


@pytest.fixture
def sample_commercial_pois():
    return [
        {
            "id": "comm_1",
            "name": "Celebrity Wax Museum",
            "category": "wax_museum",
            "authenticity_index": 0.20,
            "tourist_density": 0.90,
            "cultural_depth": 0.10,
            "duration_minutes": 60,
            "is_wheelchair_accessible": True,
            "is_elder_friendly": True,
            "is_child_friendly": True,
            "walking_distance_km": 0.3
        },
        {
            "id": "comm_2",
            "name": "Mega Shopping Mall & Arcade",
            "category": "commercial_mall",
            "authenticity_index": 0.15,
            "tourist_density": 0.85,
            "cultural_depth": 0.05,
            "duration_minutes": 90,
            "is_wheelchair_accessible": True,
            "is_elder_friendly": True,
            "is_child_friendly": True,
            "walking_distance_km": 0.8
        }
    ]


@pytest.fixture
def sample_restaurants():
    return [
        {
            "name": "Laxmi Mishtan Bhandar (LMB)",
            "cuisine": "Traditional Rajasthani Thali",
            "is_local_authentic": True,
            "authentic_score": 0.90,
            "dietary_options": ["Vegetarian", "Vegan", "Jain"]
        },
        {
            "name": "Gulab Ji Chai Wale",
            "cuisine": "Heritage Masala Chai & Maska Bun",
            "is_local_authentic": True,
            "authentic_score": 0.95,
            "dietary_options": ["Vegetarian"]
        }
    ]


@pytest.fixture
def sample_preferences():
    return {
        "food_preferences": ["Vegetarian"],
        "handicap_accommodations": ["wheelchair_accessible"],
        "elders_count": 1,
        "children_count": 0,
        "habits": {
            "pacing": "moderate",
            "walking_tolerance_km": 5.0
        }
    }


def test_authenticity_scorer_high(sample_pois, sample_restaurants):
    scorer = AuthenticityScorer()
    eval_result = scorer.evaluate(
        poi_list=sample_pois,
        restaurant_list=sample_restaurants,
        destination="Jaipur"
    )
    assert eval_result["score"] >= 65.0
    assert eval_result["poi_authenticity"] >= 60.0
    assert eval_result["culinary_authenticity"] >= 80.0
    assert len(eval_result["strengths"]) > 0


def test_authenticity_scorer_commercial(sample_commercial_pois):
    scorer = AuthenticityScorer()
    eval_result = scorer.evaluate(
        poi_list=sample_commercial_pois,
        restaurant_list=[{
            "name": "Global Fast Food Burger Hub",
            "cuisine": "Fast Food",
            "is_local_authentic": False,
            "authentic_score": 0.20,
            "dietary_options": []
        }],
        destination="Jaipur"
    )
    assert eval_result["score"] < 40.0
    assert len(eval_result["opportunities"]) > 0


def test_familiarity_scorer(sample_pois, sample_restaurants, sample_preferences):
    scorer = FamiliarityScorer()
    eval_result = scorer.evaluate(
        poi_list=sample_pois,
        restaurant_list=sample_restaurants,
        preferences=sample_preferences,
        selected_attire_count=2,
        etiquette_acknowledgement=True
    )
    assert eval_result["score"] >= 60.0
    assert eval_result["dietary_comfort"] == 100.0  # Vegetarian accommodated
    assert eval_result["cultural_readiness"] == 100.0


def test_blendin_engine_full_evaluation(sample_pois, sample_restaurants, sample_preferences):
    engine = BlendInEngine()
    req = BlendInEvaluationRequest(
        destination="Jaipur",
        poi_list=sample_pois,
        restaurant_list=sample_restaurants,
        user_preferences=sample_preferences,
        selected_attire_count=1,
        etiquette_acknowledgement=True
    )
    response = engine.evaluate_itinerary(req)
    
    assert 0.0 <= response.overall_score <= 100.0
    assert response.tier in [BlendInTier.CULTURAL_IMMERSION, BlendInTier.LOCAL_INSIDER, BlendInTier.COMFORT_EXPLORER]
    assert len(response.breakdown.dimensions) == 5
    assert len(response.recommendations) >= 3
    assert response.local_comparison_percentile > 0.0


def test_blendin_engine_target_optimization(sample_pois, sample_commercial_pois, sample_preferences):
    engine = BlendInEngine()
    all_candidates = sample_pois + sample_commercial_pois
    current_selected_ids = ["comm_1", "comm_2"]  # currently selected low authenticity spots

    req = BlendInTargetRequest(
        destination="Jaipur",
        current_score=35.0,
        target_score=85.0,  # Traveler drags slider from 35% to 85%
        candidate_pois=all_candidates,
        current_selected_poi_ids=current_selected_ids,
        user_preferences=sample_preferences
    )
    result = engine.optimize_for_target_blendin(req)

    assert result.target_score == 85.0
    assert result.poi_weight_modifiers["authenticity_multiplier"] > 1.0
    assert result.poi_weight_modifiers["popular_icon_multiplier"] < 1.0
    assert len(result.suggested_swaps) > 0
    # Checks that commercial POIs are suggested to be replaced with authentic ones
    assert result.suggested_swaps[0].suggested_poi_id in ["poi_1", "poi_2", "poi_3"]


def test_blendin_api_endpoints(sample_pois, sample_restaurants, sample_preferences):
    eval_req = BlendInEvaluationRequest(
        destination="Jaipur",
        poi_list=sample_pois,
        restaurant_list=sample_restaurants,
        user_preferences=sample_preferences,
        selected_attire_count=1,
        etiquette_acknowledgement=False
    )
    eval_resp = evaluate_blendin(eval_req)
    assert eval_resp.overall_score > 0

    opt_req = BlendInTargetRequest(
        destination="Jaipur",
        current_score=40.0,
        target_score=75.0,
        candidate_pois=sample_pois,
        current_selected_poi_ids=["poi_1"],
        user_preferences=sample_preferences
    )
    opt_resp = optimize_for_target(opt_req)
    assert opt_resp.target_score == 75.0

    tiers = get_blendin_tiers()
    assert len(tiers) == 4
    assert tiers[0]["tier"] == "Tourist Bubble"
    assert tiers[3]["tier"] == "Local Insider"

    tips = get_destination_tips("Varanasi")
    assert len(tips) >= 3
