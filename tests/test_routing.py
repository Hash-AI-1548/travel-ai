def test_standard_route_generation():
    """Verify standard itinerary contains all valid locations and metrics."""
    result = compute_optimal_route()
    stop_names = result["route_sequence"]
    
    assert "Basecamp Grand Hotel" in stop_names
    assert "Steep Scenic Peak" in stop_names
    assert result["total_distance_km"] > 0
    assert result["total_travel_time_mins"] > 0


def test_wheelchair_constraint():
    """Verify inaccessible locations are filtered out."""
    profile = {"wheelchair": True, "min_age": 25, "preferences": []}
    result = compute_optimal_route(traveler_profile=profile)
    stop_names = result["route_sequence"]
    
    assert "Steep Scenic Peak" not in stop_names
    assert "Central Botanical Park" in stop_names


def test_dynamic_rerouting_disruption():
    """Verify blocked stops are omitted and alternative paths calculated."""
    result = compute_optimal_route(blocked_stops=["temple"])
    stop_ids = [s["id"] for s in result["itinerary"]]
    
    assert "temple" not in stop_ids
    assert "museum" in stop_ids
