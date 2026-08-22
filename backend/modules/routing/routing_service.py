"""
Module 3: Dynamic POI Ingestion & Route Optimization
Author: Satyajit
"""
import math
from modules.routing.traffic_service import calculate_travel_time

# Fallback default locations if none are supplied in the request payload
DEFAULT_LOCATIONS = {
    "hotel": {"name": "Basecamp Grand Hotel", "lat": 13.08, "lon": 80.27, "wheelchair": True, "min_age": 0, "category": "stay", "visit_mins": 0},
    "temple": {"name": "Ancient Heritage Temple", "lat": 13.09, "lon": 80.28, "wheelchair": True, "min_age": 0, "category": "culture", "visit_mins": 60},
    "museum": {"name": "City History & Art Museum", "lat": 13.07, "lon": 80.26, "wheelchair": True, "min_age": 5, "category": "culture", "visit_mins": 90},
    "mountain_hike": {"name": "Steep Scenic Peak", "lat": 13.10, "lon": 80.29, "wheelchair": False, "min_age": 12, "category": "adventure", "visit_mins": 120},
    "park": {"name": "Central Botanical Park", "lat": 13.11, "lon": 80.30, "wheelchair": True, "min_age": 0, "category": "nature", "visit_mins": 45}
}


def calculate_distance(p1, p2):
    """Calculates approximate distance between two geographical points."""
    return round(math.sqrt((p1["lat"] - p2["lat"])**2 + (p1["lon"] - p2["lon"])**2) * 100, 2)


def compute_optimal_route(blocked_stops=None, traveler_profile=None, custom_pois=None):
    """
    Sequences locations, filters constraints (wheelchair/age),
    applies preference discounts, and incorporates traffic delays.
    """
    blocked_stops = blocked_stops or []
    traveler_profile = traveler_profile or {"wheelchair": False, "min_age": 18, "preferences": []}
    locations = custom_pois or DEFAULT_LOCATIONS
    
    user_prefs = traveler_profile.get("preferences", [])
    current = "hotel" if "hotel" in locations else list(locations.keys())[0]
    route = [current]
    total_travel_distance = 0.0
    total_travel_time_mins = 0
    total_activity_time = 0
    legs = []
    
    # 1. Filter out stops based on constraints and disruptions
    valid_stops = [
        k for k, v in locations.items()
        if k != current
        and k not in blocked_stops
        and not (traveler_profile.get("wheelchair", False) and not v.get("wheelchair", True))
        and traveler_profile.get("min_age", 18) >= v.get("min_age", 0)
    ]
    
    # 2. Sequence stops using Distance + Preference Weights
    while valid_stops:
        best_candidate = None
        lowest_score = float("inf")
        
        for candidate in valid_stops:
            dist = calculate_distance(locations[current], locations[candidate])
            score = dist
            if locations[candidate].get("category") in user_prefs:
                score -= 3.0
            if score < lowest_score:
                lowest_score = score
                best_candidate = candidate
                
        dist_traveled = calculate_distance(locations[current], locations[best_candidate])
        traffic_info = calculate_travel_time(dist_traveled, current, best_candidate)
        
        legs.append({
            "from": locations[current]["name"],
            "to": locations[best_candidate]["name"],
            "distance_km": dist_traveled,
            "est_travel_time_mins": traffic_info["est_travel_time_mins"],
            "traffic_multiplier": traffic_info["traffic_multiplier"]
        })
        
        total_travel_distance += dist_traveled
        total_travel_time_mins += traffic_info["est_travel_time_mins"]
        total_activity_time += locations[best_candidate].get("visit_mins", 30)
        
        route.append(best_candidate)
        valid_stops.remove(best_candidate)
        current = best_candidate
        
    # 3. Return leg back to starting point
    origin_key = route[0]
    return_dist = calculate_distance(locations[current], locations[origin_key])
    return_traffic = calculate_travel_time(return_dist, current, origin_key)
    legs.append({
        "from": locations[current]["name"],
        "to": locations[origin_key]["name"],
        "distance_km": return_dist,
        "est_travel_time_mins": return_traffic["est_travel_time_mins"],
        "traffic_multiplier": return_traffic["traffic_multiplier"]
    })
    total_travel_distance += return_dist
    total_travel_time_mins += return_traffic["est_travel_time_mins"]
    route.append(origin_key)
    
    itinerary_details = [
        {
            "id": step,
            "name": locations[step]["name"],
            "category": locations[step].get("category", "general"),
            "est_visit_mins": locations[step].get("visit_mins", 0)
        }
        for step in route
    ]
    
    return {
        "route_sequence": [locations[step]["name"] for step in route],
        "itinerary": itinerary_details,
        "legs": legs,
        "total_distance_km": round(total_travel_distance, 2),
        "total_travel_time_mins": total_travel_time_mins,
        "total_activity_time_mins": total_activity_time
    }
