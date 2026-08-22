"""
Module 3: Traffic & Delay Estimation Service
Author: Satyajit
"""

# Road segment congestion multipliers (1.0 = clear, 2.0 = heavy traffic)
TRAFFIC_CONDITIONS = {
    ("hotel", "temple"): {"multiplier": 1.1, "condition": "Light Traffic"},
    ("temple", "museum"): {"multiplier": 1.8, "condition": "Heavy Congestion"},
    ("museum", "park"): {"multiplier": 1.0, "condition": "Clear Roads"},
    ("park", "hotel"): {"multiplier": 1.3, "condition": "Moderate Traffic"},
    ("hotel", "park"): {"multiplier": 1.2, "condition": "Moderate Traffic"},
    ("temple", "park"): {"multiplier": 1.4, "condition": "Moderate Traffic"}
}

DEFAULT_BASE_SPEED_KMH = 30.0  # Average city driving speed


def get_traffic_multiplier(origin_id: str, destination_id: str) -> float:
    """Returns the congestion multiplier between two stops."""
    key = (origin_id, destination_id)
    reverse_key = (destination_id, origin_id)
    
    if key in TRAFFIC_CONDITIONS:
        return TRAFFIC_CONDITIONS[key]["multiplier"]
    if reverse_key in TRAFFIC_CONDITIONS:
        return TRAFFIC_CONDITIONS[reverse_key]["multiplier"]
    return 1.0


def calculate_travel_time(distance_km: float, origin_id: str, destination_id: str) -> dict:
    """
    Calculates estimated travel time in minutes incorporating traffic slowdowns.
    """
    multiplier = get_traffic_multiplier(origin_id, destination_id)
    base_time_hours = distance_km / DEFAULT_BASE_SPEED_KMH
    adjusted_time_mins = round((base_time_hours * 60) * multiplier)
    
    return {
        "distance_km": distance_km,
        "traffic_multiplier": multiplier,
        "est_travel_time_mins": max(1, adjusted_time_mins)
    }
