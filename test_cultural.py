"""
Unit and Integration Tests for Cultural & Attire Module and Endpoints.
"""

import pytest
from backend.schemas.cultural import (
    AttireRecommendationRequest,
    AttireCategory,
    RequirementLevel
)
from backend.modules.cultural.attire_bridge import AttireBridge
from backend.modules.cultural.weather_attire import WeatherAttireAdvisor
from backend.modules.cultural.occasion_matcher import OccasionMatcher
from backend.modules.cultural.cultural_context import CulturalContextManager
from backend.modules.cultural.attire_similarity import AttireSimilarityScorer
from backend.api.cultural_routes import (
    get_attire_recommendations,
    get_cultural_guide,
    get_standard_dress_codes
)


def test_attire_bridge_recommendations():
    bridge = AttireBridge()
    req = AttireRecommendationRequest(
        destination="Jaipur",
        temperature_celsius=33.0,
        weather_condition="Sunny",
        planned_poi_categories=["historic_temple", "bazaar"]
    )
    resp = bridge.recommend_attire(req)

    assert resp.destination == "Jaipur"
    assert len(resp.recommended_outfits) > 0
    assert any("Kurta" in o.name for o in resp.recommended_outfits)
    assert len(resp.site_dress_codes) > 0
    assert len(resp.packing_checklist) >= 4
    assert resp.blendin_attire_boost == 15.0


def test_weather_attire_advisor_hot():
    advisor = WeatherAttireAdvisor()
    summary, _ = advisor.filter_by_weather(
        outfits=[],
        temp_c=36.0,
        condition="Sunny"
    )
    assert "High heat" in summary or "36" in summary


def test_occasion_matcher_dress_codes():
    matcher = OccasionMatcher()
    codes = matcher.get_dress_codes("Jaipur", ["historic_temple"])
    assert len(codes) >= 2
    assert any(c.requirement_level == RequirementLevel.STRICT for c in codes)


def test_cultural_context_guide():
    manager = CulturalContextManager()
    guide = manager.get_guide("Jaipur")

    assert guide.destination == "Jaipur"
    assert len(guide.etiquette_rules) >= 3
    assert len(guide.essential_phrases) >= 4
    assert any("Nam" in p.phonetic_pronunciation or "Hello" in p.phrase for p in guide.essential_phrases)


def test_attire_similarity_scorer():
    scorer = AttireSimilarityScorer()
    assert scorer.compute_attire_match_score(selected_attire_count=2) == 95.0
    assert scorer.compute_attire_match_score(selected_attire_count=0, has_sacred_sites=True) == 45.0


def test_cultural_api_endpoints():
    req = AttireRecommendationRequest(destination="Varanasi", temperature_celsius=26.0)
    attire_resp = get_attire_recommendations(req)
    assert attire_resp.destination == "Varanasi"
    assert len(attire_resp.recommended_outfits) > 0

    guide_resp = get_cultural_guide("Varanasi")
    assert guide_resp.destination == "Varanasi"
    assert len(guide_resp.essential_phrases) > 0

    dress_codes = get_standard_dress_codes()
    assert len(dress_codes) >= 2
