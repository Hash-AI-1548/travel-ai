"""
Authenticity Scoring Engine for Blend-In Evaluation.
"""

from typing import List, Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class AuthenticityScorer:
    """
    Evaluates how authentically local an itinerary's POIs, activities, and dining choices are.
    """

    POI_AUTHENTICITY_WEIGHT = 0.40
    CULINARY_AUTHENTICITY_WEIGHT = 0.30
    CULTURAL_DEPTH_WEIGHT = 0.20
    LOCAL_RHYTHM_WEIGHT = 0.10

    def __init__(self):
        self.authentic_categories = {
            "heritage_craft", "artisan_quarter", "local_market", "historic_temple",
            "neighborhood_walk", "cultural_workshop", "traditional_tea_stall",
            "folk_performance", "hidden_viewpoint", "bazaar", "ghat", "monastery"
        }
        self.commercial_categories = {
            "wax_museum", "commercial_mall", "theme_park", "hop_on_bus",
            "chain_resort", "commercial_souvenir_hub", "tourist_trap"
        }

    def compute_poi_authenticity(self, poi_list: List[Dict[str, Any]]) -> Tuple[float, List[str], List[str]]:
        if not poi_list:
            return 50.0, [], ["No POIs scheduled yet to assess authenticity."]

        total_weight = 0.0
        weighted_auth_sum = 0.0
        strengths = []
        opportunities = []

        for poi in poi_list:
            name = poi.get("name") or poi.get("poi_name") or "Attraction"
            category = (poi.get("category") or "").lower()
            auth_idx = float(poi.get("authenticity_index", 0.5))
            tourist_density = float(poi.get("tourist_density", 0.5))
            effective_auth = auth_idx * (1.0 - (tourist_density * 0.25))

            if category in self.authentic_categories or auth_idx >= 0.75:
                strengths.append(f"'{name}' offers rich local cultural immersion ({int(auth_idx*100)}% authenticity)")
            elif category in self.commercial_categories or auth_idx < 0.35:
                opportunities.append(f"'{name}' is heavily commercialized; swap with a neighborhood landmark")

            weighted_auth_sum += effective_auth
            total_weight += 1.0

        raw_score = (weighted_auth_sum / max(total_weight, 1.0)) * 100.0
        score = max(0.0, min(100.0, raw_score))
        return score, strengths[:3], opportunities[:3]

    def compute_culinary_authenticity(self, restaurant_list: List[Dict[str, Any]]) -> Tuple[float, List[str], List[str]]:
        if not restaurant_list:
            return 50.0, [], ["Add local eateries to boost culinary immersion."]

        scores = []
        strengths = []
        opportunities = []

        for rest in restaurant_list:
            name = rest.get("name") or rest.get("restaurant_name") or "Dining Spot"
            cuisine_type = (rest.get("cuisine") or rest.get("cuisine_type") or "").lower()
            is_local = rest.get("is_local_authentic", True)
            local_score = float(rest.get("authentic_score", 0.8 if is_local else 0.3))

            if "international" in cuisine_type or "fast food" in cuisine_type or "chain" in cuisine_type:
                local_score = min(local_score, 0.30)
                opportunities.append(f"Replace standard dining at '{name}' with a regional heritage specialty kitchen")
            elif local_score >= 0.75:
                strengths.append(f"'{name}' showcases genuine local cuisine ({cuisine_type.title() or 'Local Specialty'})")

            scores.append(local_score * 100.0)

        avg_score = sum(scores) / max(len(scores), 1)
        return max(0.0, min(100.0, avg_score)), strengths[:3], opportunities[:3]

    def compute_cultural_depth(self, poi_list: List[Dict[str, Any]]) -> float:
        if not poi_list:
            return 50.0

        depth_scores = []
        for poi in poi_list:
            duration_minutes = float(poi.get("duration_minutes", 60))
            cultural_depth = float(poi.get("cultural_depth", 0.5))
            time_factor = min(1.2, max(0.8, duration_minutes / 90.0))
            depth_scores.append(cultural_depth * time_factor * 100.0)

        avg_depth = sum(depth_scores) / max(len(depth_scores), 1)
        return max(0.0, min(100.0, avg_depth))

    def compute_local_rhythm_alignment(self, poi_list: List[Dict[str, Any]]) -> float:
        if not poi_list:
            return 60.0

        matched_slots = 0
        total_checks = 0

        for poi in poi_list:
            start_time = poi.get("start_time") or poi.get("timestamp") or ""
            category = (poi.get("category") or "").lower()

            if "06:" in start_time or "07:" in start_time or "08:" in start_time:
                total_checks += 1
                if any(k in category for k in ["market", "temple", "ghat", "walk", "nature"]):
                    matched_slots += 1

            if "17:" in start_time or "18:" in start_time or "19:" in start_time:
                total_checks += 1
                if any(k in category for k in ["bazaar", "sunset", "aarti", "street_food", "music"]):
                    matched_slots += 1

        if total_checks == 0:
            return 70.0
        
        ratio = matched_slots / total_checks
        return 50.0 + (ratio * 50.0)

    def evaluate(
        self,
        poi_list: List[Dict[str, Any]],
        restaurant_list: List[Dict[str, Any]],
        destination: str = ""
    ) -> Dict[str, Any]:
        poi_score, poi_strengths, poi_opps = self.compute_poi_authenticity(poi_list)
        culinary_score, food_strengths, food_opps = self.compute_culinary_authenticity(restaurant_list)
        depth_score = self.compute_cultural_depth(poi_list)
        rhythm_score = self.compute_local_rhythm_alignment(poi_list)

        composite_authenticity = (
            (poi_score * self.POI_AUTHENTICITY_WEIGHT) +
            (culinary_score * self.CULINARY_AUTHENTICITY_WEIGHT) +
            (depth_score * self.CULTURAL_DEPTH_WEIGHT) +
            (rhythm_score * self.LOCAL_RHYTHM_WEIGHT)
        )

        strengths = poi_strengths + food_strengths
        opportunities = poi_opps + food_opps

        return {
            "score": round(max(0.0, min(100.0, composite_authenticity)), 1),
            "poi_authenticity": round(poi_score, 1),
            "culinary_authenticity": round(culinary_score, 1),
            "cultural_depth": round(depth_score, 1),
            "local_rhythm": round(rhythm_score, 1),
            "strengths": strengths,
            "opportunities": opportunities,
            "description": (
                f"Authenticity in {destination or 'the region'} is driven by {len(poi_list)} POIs and "
                f"{len(restaurant_list)} dining selections."
            )
        }
