"""
Blend-In Engine (Core Optimization and Scoring Module).
"""

from typing import List, Dict, Any, Optional, Tuple
import logging

from backend.schemas.blendin import (
    BlendInTier,
    ScoreDimension,
    BlendInBreakdown,
    BlendInRecommendation,
    BlendInScoreResponse,
    BlendInEvaluationRequest,
    BlendInTargetRequest,
    BlendInOptimizationResult,
    POISwapSuggestion
)
from backend.modules.blendin.authenticity_score import AuthenticityScorer
from backend.modules.blendin.familiarity_score import FamiliarityScorer

logger = logging.getLogger(__name__)


def _determine_tier_and_tagline(score: float) -> Tuple[BlendInTier, str]:
    if score >= 76.0:
        return BlendInTier.LOCAL_INSIDER, "Local Insider: Deeply integrated with native rhythms and hidden gems."
    elif score >= 51.0:
        return BlendInTier.CULTURAL_IMMERSION, "Cultural Immersion: Balanced blend of regional heritage and authentic flavor."
    elif score >= 26.0:
        return BlendInTier.COMFORT_EXPLORER, "Comfort Explorer: Iconic landmarks with gentle cultural discoveries."
    else:
        return BlendInTier.TOURIST_BUBBLE, "Tourist Bubble: High-comfort familiar itinerary with standard sightseeing."


class BlendInEngine:
    def __init__(self):
        self.authenticity_scorer = AuthenticityScorer()
        self.familiarity_scorer = FamiliarityScorer()

    def evaluate_itinerary(self, request: BlendInEvaluationRequest) -> BlendInScoreResponse:
        poi_list = request.poi_list or []
        restaurant_list = request.restaurant_list or []
        user_prefs = request.user_preferences or {}
        destination = request.destination or "Destination"

        auth_eval = self.authenticity_scorer.evaluate(
            poi_list=poi_list,
            restaurant_list=restaurant_list,
            destination=destination
        )
        auth_score = auth_eval["score"]

        fam_eval = self.familiarity_scorer.evaluate(
            poi_list=poi_list,
            restaurant_list=restaurant_list,
            preferences=user_prefs,
            selected_attire_count=request.selected_attire_count,
            etiquette_acknowledgement=request.etiquette_acknowledgement
        )
        fam_score = fam_eval["score"]

        culinary_score = auth_eval["culinary_authenticity"]
        cultural_adaptation_score = round(
            (auth_eval["cultural_depth"] * 0.5) + (fam_eval["cultural_readiness"] * 0.5), 1
        )
        local_interaction_score = round(
            (auth_eval["local_rhythm"] * 0.6) + (auth_eval["poi_authenticity"] * 0.4), 1
        )

        composite_score = round((auth_score * 0.55) + (fam_score * 0.45), 1)
        composite_score = max(5.0, min(100.0, composite_score))

        tier, tagline = _determine_tier_and_tagline(composite_score)

        dimensions = [
            ScoreDimension(
                name="Authentic Heritage & Activities",
                score=auth_eval["poi_authenticity"],
                weight=0.30,
                description="Selection of traditional sights and artisan quarters vs commercial tourist attractions.",
                strengths=auth_eval["strengths"][:2],
                opportunities=auth_eval["opportunities"][:2]
            ),
            ScoreDimension(
                name="Regional Culinary Exploration",
                score=culinary_score,
                weight=0.25,
                description="Enjoying authentic local cuisine while honoring dietary comfort.",
                strengths=[s for s in auth_eval["strengths"] if "cuisine" in s.lower() or "dining" in s.lower()][:2],
                opportunities=[o for o in auth_eval["opportunities"] if "eatery" in o.lower() or "kitchen" in o.lower()][:2]
            ),
            ScoreDimension(
                name="Pacing & Physiological Comfort",
                score=fam_eval["pacing_compatibility"],
                weight=0.20,
                description="Schedule density, walking endurance, and daily rest intervals.",
                strengths=fam_eval["strengths"][:2],
                opportunities=fam_eval["opportunities"][:2]
            ),
            ScoreDimension(
                name="Accessibility & Inclusivity",
                score=fam_eval["accessibility_safety"],
                weight=0.15,
                description="Wheelchair access, elder-friendly terrain, and child pacing safety.",
                strengths=[s for s in fam_eval["strengths"] if "access" in s.lower() or "mobility" in s.lower()][:2],
                opportunities=[o for o in fam_eval["opportunities"] if "lacks" in o.lower() or "stairs" in o.lower()][:2]
            ),
            ScoreDimension(
                name="Cultural Attire & Etiquette Readiness",
                score=fam_eval["cultural_readiness"],
                weight=0.10,
                description="Adoption of regional dress norms and awareness of local social customs.",
                strengths=[s for s in fam_eval["strengths"] if "attire" in s.lower() or "customs" in s.lower()][:2],
                opportunities=[o for o in fam_eval["opportunities"] if "attire" in o.lower() or "etiquette" in o.lower()][:2]
            )
        ]

        breakdown = BlendInBreakdown(
            authenticity_score=auth_score,
            familiarity_score=fam_score,
            cultural_adaptation_score=cultural_adaptation_score,
            culinary_immersion_score=culinary_score,
            local_interaction_score=local_interaction_score,
            dimensions=dimensions
        )

        recommendations = self.generate_recommendations(
            destination=destination,
            auth_eval=auth_eval,
            fam_eval=fam_eval,
            selected_attire_count=request.selected_attire_count,
            etiquette_acknowledgement=request.etiquette_acknowledgement,
            user_prefs=user_prefs
        )

        local_percentile = round(min(100.0, (composite_score / 90.0) * 100.0), 1)

        return BlendInScoreResponse(
            overall_score=composite_score,
            tier=tier,
            tagline=tagline,
            breakdown=breakdown,
            recommendations=recommendations,
            local_comparison_percentile=local_percentile
        )

    def generate_recommendations(
        self,
        destination: str,
        auth_eval: Dict[str, Any],
        fam_eval: Dict[str, Any],
        selected_attire_count: int,
        etiquette_acknowledgement: bool,
        user_prefs: Dict[str, Any]
    ) -> List[BlendInRecommendation]:
        recs = []

        if selected_attire_count == 0:
            recs.append(
                BlendInRecommendation(
                    category="attire",
                    title="Adopt Regional Modest Attire",
                    description=f"Wear breathable linen, cotton Kurta, or modest covered shoulders when visiting heritage precincts in {destination}.",
                    impact_score_boost=6.5,
                    difficulty="Easy",
                    cultural_context="Shows respect at cultural landmarks and blends naturally into local neighborhoods."
                )
            )
        else:
            recs.append(
                BlendInRecommendation(
                    category="attire",
                    title="Cultural Attire Synergy",
                    description=f"Your selected regional attire for {destination} helps you comfortably blend in at heritage sites and temples.",
                    impact_score_boost=3.0,
                    difficulty="Easy",
                    cultural_context="Respects regional traditions and aesthetics."
                )
            )

        if not etiquette_acknowledgement:
            recs.append(
                BlendInRecommendation(
                    category="etiquette",
                    title="Review Sacred Site Protocol",
                    description="Remember to remove shoes before entering temple sanctums and use your right hand for greetings and offerings.",
                    impact_score_boost=5.0,
                    difficulty="Easy",
                    cultural_context="Core cultural etiquette observed by residents across traditional sites."
                )
            )
        else:
            recs.append(
                BlendInRecommendation(
                    category="etiquette",
                    title="Temple & Bazaar Etiquette",
                    description="Maintain courteous, unhurried interactions with temple priests and artisan shopkeepers.",
                    impact_score_boost=2.5,
                    difficulty="Easy",
                    cultural_context="Fosters mutual respect in traditional communities."
                )
            )

        recs.append(
            BlendInRecommendation(
                category="food",
                title="Explore a Heritage Breakfast / Tea Stall",
                description=f"Start your morning with freshly brewed chai and local specialties at a historic neighborhood eatery in {destination}.",
                impact_score_boost=8.0,
                difficulty="Easy",
                cultural_context="Locals gather for morning tea and community conversations at heritage stalls."
            )
        )

        recs.append(
            BlendInRecommendation(
                category="timing",
                title="Experience Morning Wholesale Markets",
                description="Schedule an early morning walk (7:00 AM - 8:30 AM) to experience vibrant local flower/spice markets before tourist crowds arrive.",
                impact_score_boost=7.5,
                difficulty="Moderate",
                cultural_context="Authentic trading hours when local vendors and residents interact."
            )
        )

        recs.append(
            BlendInRecommendation(
                category="phrase",
                title="Use Local Courtesies",
                description="Learn 3 key local phrases: greeting ('Namaste' / 'Vanakkam'), thank you ('Dhanyavad' / 'Nandri'), and 'How much?' for bazaar interactions.",
                impact_score_boost=4.0,
                difficulty="Easy",
                cultural_context="Instantly creates warmth and rapport with artisans and locals."
            )
        )

        return recs

    def optimize_for_target_blendin(self, request: BlendInTargetRequest) -> BlendInOptimizationResult:
        current_score = request.current_score
        target_score = request.target_score
        delta = target_score - current_score

        candidate_pois = request.candidate_pois or []
        selected_poi_ids = set(request.current_selected_poi_ids or [])
        user_prefs = request.user_preferences or {}

        if target_score >= current_score:
            shift_factor = (target_score - current_score) / 50.0
            auth_weight_mod = round(1.0 + (shift_factor * 0.8), 2)
            density_penalty_mod = round(1.0 + (shift_factor * 0.6), 2)
            icon_weight_mod = round(max(0.3, 1.0 - (shift_factor * 0.5)), 2)
        else:
            shift_factor = (current_score - target_score) / 50.0
            auth_weight_mod = round(max(0.4, 1.0 - (shift_factor * 0.7)), 2)
            density_penalty_mod = round(max(0.2, 1.0 - (shift_factor * 0.6)), 2)
            icon_weight_mod = round(1.0 + (shift_factor * 0.7), 2)

        poi_weight_modifiers = {
            "authenticity_multiplier": auth_weight_mod,
            "tourist_density_penalty_multiplier": density_penalty_mod,
            "popular_icon_multiplier": icon_weight_mod,
            "cultural_depth_multiplier": round(auth_weight_mod * 1.1, 2)
        }

        suggested_swaps: List[POISwapSuggestion] = []
        if delta > 10.0 and candidate_pois and selected_poi_ids:
            currently_selected_pois = [p for p in candidate_pois if p.get("id") in selected_poi_ids or p.get("poi_id") in selected_poi_ids]
            unselected_candidates = [p for p in candidate_pois if (p.get("id") not in selected_poi_ids and p.get("poi_id") not in selected_poi_ids)]

            currently_selected_pois.sort(key=lambda p: float(p.get("authenticity_index", 0.5)))
            unselected_candidates.sort(key=lambda p: float(p.get("authenticity_index", 0.5)), reverse=True)

            for low_poi in currently_selected_pois:
                low_auth = float(low_poi.get("authenticity_index", 0.5))
                if low_auth < 0.60:
                    for high_poi in unselected_candidates:
                        high_auth = float(high_poi.get("authenticity_index", 0.5))
                        if high_auth >= 0.75:
                            handicap = user_prefs.get("handicap_accommodations", [])
                            req_wheelchair = any("wheelchair" in str(h).lower() for h in handicap)
                            if req_wheelchair and not high_poi.get("is_wheelchair_accessible", True):
                                continue

                            score_boost = round((high_auth - low_auth) * 20.0, 1)
                            suggested_swaps.append(
                                POISwapSuggestion(
                                    current_poi_id=low_poi.get("id") or low_poi.get("poi_id") or "curr_poi",
                                    current_poi_name=low_poi.get("name") or low_poi.get("poi_name") or "Standard Sights",
                                    suggested_poi_id=high_poi.get("id") or high_poi.get("poi_id") or "sugg_poi",
                                    suggested_poi_name=high_poi.get("name") or high_poi.get("poi_name") or "Authentic Gem",
                                    reason=f"Swaps crowded tourist hub with an artisan/heritage cultural site to reach {target_score:.0f}% blend-in.",
                                    blendin_score_delta=score_boost
                                )
                            )
                            unselected_candidates.remove(high_poi)
                            break
                if len(suggested_swaps) >= 3:
                    break

        fine_tuning_params = {
            "target_blendin_score": target_score,
            "poi_weight_modifiers": poi_weight_modifiers,
            "target_tier": _determine_tier_and_tagline(target_score)[0].value,
            "prioritize_local_food": target_score >= 60.0,
            "include_morning_market": target_score >= 70.0,
            "suggested_swap_ids": [s.suggested_poi_id for s in suggested_swaps]
        }

        projected_score = round(target_score, 1)

        actionable_tips = []
        if target_score >= 75:
            actionable_tips.append(
                BlendInRecommendation(
                    category="activity",
                    title="Immerse in Artisan Quarters",
                    description="Spend time in traditional block-printing or pottery workshops engaging directly with craft masters.",
                    impact_score_boost=10.0,
                    difficulty="Moderate"
                )
            )
        elif target_score <= 40:
            actionable_tips.append(
                BlendInRecommendation(
                    category="activity",
                    title="Comfort Sightseeing Mode",
                    description="Itinerary optimized for premier monuments, air-conditioned transit, and familiar international dining.",
                    impact_score_boost=0.0,
                    difficulty="Easy"
                )
            )

        return BlendInOptimizationResult(
            target_score=target_score,
            projected_score=projected_score,
            poi_weight_modifiers=poi_weight_modifiers,
            suggested_swaps=suggested_swaps,
            fine_tuning_parameters=fine_tuning_params,
            actionable_tips=actionable_tips
        )
