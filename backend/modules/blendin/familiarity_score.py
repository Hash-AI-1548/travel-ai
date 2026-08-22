"""
Familiarity and Comfort Adaptation Scoring Engine.
"""

from typing import List, Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class FamiliarityScorer:
    """
    Evaluates traveler comfort, psychological ease, and physiological safety
    when experiencing local culture.
    """

    DIETARY_WEIGHT = 0.30
    PACING_WEIGHT = 0.25
    ACCESSIBILITY_WEIGHT = 0.25
    READINESS_WEIGHT = 0.20

    def compute_dietary_comfort(
        self,
        restaurant_list: List[Dict[str, Any]],
        preferences: Dict[str, Any]
    ) -> Tuple[float, List[str], List[str]]:
        dietary_prefs = preferences.get("food_preferences", [])
        if isinstance(dietary_prefs, str):
            dietary_prefs = [dietary_prefs]
        
        diet_set = {d.lower() for d in dietary_prefs if d}
        
        if not diet_set:
            return 90.0, ["No restrictive dietary constraints; flexible dining."], []

        if not restaurant_list:
            return 70.0, [], ["No restaurants selected yet to verify dietary match."]

        compliant_count = 0
        strengths = []
        opportunities = []

        for rest in restaurant_list:
            name = rest.get("name") or rest.get("restaurant_name") or "Eatery"
            rest_dietary = [d.lower() for d in rest.get("dietary_options", [])]
            
            is_compliant = all(
                any(req in opt for opt in rest_dietary)
                for req in diet_set
            ) if rest_dietary else True

            if is_compliant:
                compliant_count += 1
                strengths.append(f"'{name}' accommodates your {', '.join(diet_set)} preferences")
            else:
                opportunities.append(f"'{name}' may have limited options for {', '.join(diet_set)}")

        compliance_rate = compliant_count / max(len(restaurant_list), 1)
        score = compliance_rate * 100.0
        return max(30.0, min(100.0, score)), strengths[:2], opportunities[:2]

    def compute_pacing_compatibility(
        self,
        poi_list: List[Dict[str, Any]],
        preferences: Dict[str, Any]
    ) -> Tuple[float, List[str], List[str]]:
        habits = preferences.get("habits", {})
        if not isinstance(habits, dict):
            habits = {}

        pacing = (habits.get("pacing") or "moderate").lower()
        max_walking_km = float(habits.get("walking_tolerance_km", 6.0))
        
        pacing_poi_targets = {
            "relaxed": 3,
            "moderate": 5,
            "packed": 7,
            "fast": 8
        }
        target_pois = pacing_poi_targets.get(pacing, 4)
        actual_pois = len(poi_list)

        strengths = []
        opportunities = []

        if actual_pois <= target_pois:
            pacing_score = 95.0
            strengths.append(f"Pacing is comfortable with {actual_pois} POIs (Target for {pacing}: {target_pois})")
        else:
            overflow = actual_pois - target_pois
            pacing_score = max(40.0, 95.0 - (overflow * 15.0))
            opportunities.append(f"Itinerary has {actual_pois} POIs, which may feel rushed for a '{pacing}' pace")

        estimated_walking = sum(float(poi.get("walking_distance_km", 0.8)) for poi in poi_list)
        if estimated_walking > max_walking_km:
            pacing_score -= 15.0
            opportunities.append(
                f"Est. walking ({estimated_walking:.1f} km) exceeds preferred limit ({max_walking_km:.1f} km)"
            )
        else:
            strengths.append(f"Est. walking ({estimated_walking:.1f} km) is within comfort limit")

        return max(20.0, min(100.0, pacing_score)), strengths[:2], opportunities[:2]

    def compute_accessibility_safety(
        self,
        poi_list: List[Dict[str, Any]],
        preferences: Dict[str, Any]
    ) -> Tuple[float, List[str], List[str]]:
        handicap = preferences.get("handicap_accommodations", [])
        if isinstance(handicap, str):
            handicap = [handicap]
        
        elders_count = int(preferences.get("elders_count", 0))
        children_count = int(preferences.get("children_count", 0))

        requires_wheelchair = any("wheelchair" in str(h).lower() or "step_free" in str(h).lower() for h in handicap)
        has_vulnerable_group = requires_wheelchair or (elders_count > 0) or (children_count > 0)

        if not has_vulnerable_group:
            return 95.0, ["No special mobility or demographic constraints; full flexibility."], []

        if not poi_list:
            return 80.0, [], []

        accessible_count = 0
        strengths = []
        opportunities = []

        for poi in poi_list:
            name = poi.get("name") or poi.get("poi_name") or "Location"
            is_wheelchair_ok = poi.get("is_wheelchair_accessible", poi.get("wheelchair_accessible", True))
            elder_friendly = poi.get("is_elder_friendly", True)
            kid_friendly = poi.get("is_child_friendly", poi.get("kid_friendly", True))

            poi_ok = True
            if requires_wheelchair and not is_wheelchair_ok:
                poi_ok = False
                opportunities.append(f"'{name}' lacks wheelchair/step-free access")
            if elders_count > 0 and not elder_friendly:
                poi_ok = False
                opportunities.append(f"'{name}' has steep stairs/excessive standing unsuitable for seniors")
            if children_count > 0 and not kid_friendly:
                opportunities.append(f"'{name}' may not engage toddlers/children")

            if poi_ok:
                accessible_count += 1

        ratio = accessible_count / max(len(poi_list), 1)
        base_score = ratio * 100.0
        
        if ratio >= 0.85:
            strengths.append("High accessibility across scheduled points of interest")

        return max(10.0, min(100.0, base_score)), strengths[:2], opportunities[:2]

    def compute_cultural_readiness(
        self,
        preferences: Dict[str, Any],
        selected_attire_count: int = 0,
        etiquette_acknowledgement: bool = False
    ) -> Tuple[float, List[str], List[str]]:
        score = 50.0
        strengths = []
        opportunities = []

        if selected_attire_count > 0:
            score += 25.0
            strengths.append(f"Selected {selected_attire_count} culturally appropriate attire recommendations")
        else:
            opportunities.append("Review destination attire advice to blend in naturally")

        if etiquette_acknowledgement:
            score += 25.0
            strengths.append("Reviewed regional etiquette, temple protocols, and social customs")
        else:
            opportunities.append("Check local etiquette tips to prevent social faux pas")

        return max(20.0, min(100.0, score)), strengths, opportunities

    def evaluate(
        self,
        poi_list: List[Dict[str, Any]],
        restaurant_list: List[Dict[str, Any]],
        preferences: Dict[str, Any],
        selected_attire_count: int = 0,
        etiquette_acknowledgement: bool = False
    ) -> Dict[str, Any]:
        diet_score, diet_str, diet_opp = self.compute_dietary_comfort(restaurant_list, preferences)
        pacing_score, pace_str, pace_opp = self.compute_pacing_compatibility(poi_list, preferences)
        access_score, acc_str, acc_opp = self.compute_accessibility_safety(poi_list, preferences)
        readiness_score, read_str, read_opp = self.compute_cultural_readiness(
            preferences, selected_attire_count, etiquette_acknowledgement
        )

        composite_familiarity = (
            (diet_score * self.DIETARY_WEIGHT) +
            (pacing_score * self.PACING_WEIGHT) +
            (access_score * self.ACCESSIBILITY_WEIGHT) +
            (readiness_score * self.READINESS_WEIGHT)
        )

        strengths = diet_str + pace_str + acc_str + read_str
        opportunities = diet_opp + pace_opp + acc_opp + read_opp

        return {
            "score": round(max(0.0, min(100.0, composite_familiarity)), 1),
            "dietary_comfort": round(diet_score, 1),
            "pacing_compatibility": round(pacing_score, 1),
            "accessibility_safety": round(access_score, 1),
            "cultural_readiness": round(readiness_score, 1),
            "strengths": strengths,
            "opportunities": opportunities,
            "description": "Familiarity and comfort index measures seamless adaptation without cognitive or physical strain."
        }
