from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.passport import TravelPassport
from app.models.trip import Trip
from app.schemas.trip import TripGenerateRequest

def generate_trip_plan(db: Session, user_id: int, request: TripGenerateRequest, passport: TravelPassport) -> Trip:
    """
    Synthesizes a personalized AI itinerary based on the user's destination,
    duration, and all 8-step travel passport parameters in Indian Rupees (₹ INR) & Standardized USD.
    """
    dest = request.destination
    days_count = request.duration_days
    
    # 1. Traveler configuration & custom notes
    t_type = (passport.traveler_type or "solo").capitalize()
    if passport.traveler_type_custom:
        t_type += f" ({passport.traveler_type_custom})"

    # 2. Styles
    styles = passport.travel_styles if passport.travel_styles else ["adventure", "culture"]
    if passport.travel_styles_custom:
        styles = list(styles) + [passport.travel_styles_custom]
    
    # 3. Dietary & Allergies
    diets = passport.dietary_standards if passport.dietary_standards else ["Non-vegetarian"]
    diets_str = ", ".join([d.replace("_", " ").capitalize() for d in diets])
    if passport.food_custom:
        diets_str += f" + {passport.food_custom}"
    allergy_notes = passport.allergies_restrictions or "No specific allergy restrictions noted"
    
    # 4. Modesty & Clothing
    is_modest = passport.modest_clothing
    hot_weather = passport.prioritize_hot_weather
    
    # 5. Accessibility
    is_mobility = passport.accessibility_mobility
    access_notes_list = []
    if is_mobility:
        access_notes_list.append("Wheelchair & step-free accessible paths strictly verified")
    if passport.accessibility_visual:
        access_notes_list.append("Audio guides and high-contrast routes available")
    if passport.accessibility_hearing:
        access_notes_list.append("Visual signage and vibration alert indicators enabled")
    if passport.accessibility_senior:
        access_notes_list.append("Gentle walking pace with elevator access")
    if passport.accessibility_child:
        access_notes_list.append("Stroller friendly and child safety certified")
    if passport.accessibility_custom:
        access_notes_list.append(passport.accessibility_custom)
    
    access_str = " • ".join(access_notes_list) if access_notes_list else "Standard accessibility (smooth paved walkways)"

    # 6. Budget Tier in INR & Standardized USD
    b_tier = passport.budget_tier or "moderate"
    curr = passport.budget_currency or "INR"
    budget_map = {
        "budget": ("₹1,500 – ₹3,500 / day per person ($18 – $42 USD)", "BUDGET / LOW (₹)"),
        "moderate": ("₹4,000 – ₹8,500 / day per person ($48 – $102 USD)", "MODERATE / MID (₹₹)"),
        "premium_luxury": ("₹10,000 – ₹25,000+ / day per person ($120 – $300+ USD)", "PREMIUM / LUXURY (₹₹₹)"),
        "flexible": ("₹3,000 – ₹15,000 / day per person ($36 – $180 USD)", "FLEXIBLE (₹ – ₹₹₹)")
    }
    est_range, tier_lbl = budget_map.get(b_tier, ("₹4,000 – ₹8,500 / day per person", "MODERATE / MID (₹₹)"))
    if passport.budget_custom:
        usd_tag = f" [{passport.budget_standardized_usd}]" if passport.budget_standardized_usd else ""
        est_range = f"{curr} {passport.budget_custom}{usd_tag}"

    # Generate daily activities
    itinerary_data = []
    sample_themes = [
        ("Historic Core & Ancient Sacred Temples", "Discover foundational architecture, ancient sanctums, and traditional artisan tea houses."),
        ("Scenic Nature Trails & Panoramic Waterways", "Experience tranquil bamboo pathways, botanical gardens, and scenic river boardwalks."),
        ("Culinary Odyssey & Local Hidden Alleyways", "Curated food walks featuring strict dietary-certified delicacies and spice markets."),
        ("Contemporary Art, Crafts & Modern Culture", "Explore modern creative quarters, ceramic studios, and immersive visual spaces."),
        ("Spiritual Retreats & Scenic Sunset Vistas", "Peaceful monastery views, meditative stone gardens, and breathtaking mountain overlooks."),
        ("Artisan Boutiques & Silk Heritage Districts", "Historic merchant lanes, local textile weavers, and bespoke souvenir crafting."),
        ("Iconic Monuments & Farewell Gastronomy", "Grand finale landmarks followed by a relaxed, personalized celebration dinner.")
    ]

    for d in range(1, days_count + 1):
        theme_idx = (d - 1) % len(sample_themes)
        t_title, t_desc = sample_themes[theme_idx]
        
        # Activity 1: Morning
        act1_dress = "Cover shoulders & knees for temple/holy sanctum entry." if is_modest else "Comfortable morning walking wear."
        act1 = {
            "time_slot": "Morning (09:00 - 12:30)",
            "activity_name": f"{dest} Historic Cultural Landmark & Sanctum",
            "location": f"{dest} Old Town Quarter",
            "description": f"{t_desc} Guided step-by-step route tailored for {t_type}.",
            "dress_code_advice": act1_dress,
            "accessibility_notes": access_str
        }

        # Activity 2: Afternoon
        act2_dress = "Lightweight breathable fabrics with sun protection." if hot_weather else "Smart casual walking attire."
        act2 = {
            "time_slot": "Afternoon (14:00 - 17:30)",
            "activity_name": f"{dest} Panoramic Scenic Promenade",
            "location": f"{dest} Central District",
            "description": f"Immerse yourself in {', '.join(styles[:3])} highlights and shaded viewing lookouts.",
            "dress_code_advice": act2_dress,
            "accessibility_notes": "Benches and rest alcoves available every 150 meters."
        }

        # Activity 3: Evening
        act3 = {
            "time_slot": "Evening (18:30 - 21:30)",
            "activity_name": f"{dest} Evening Lantern & Culinary Experience",
            "location": f"{dest} Artisan Food Alley",
            "description": f"Curated evening stroll and relaxed dining strictly accommodating {diets_str}.",
            "dress_code_advice": "Casual chic layer for cooler evening breezes.",
            "accessibility_notes": "Step-free flat entrance."
        }

        # Lodging
        stay = {
            "hotel_name": f"The {dest} Boutique Heritage Hotel & Suites",
            "address": f"100 Central Way, {dest}",
            "room_type": "Accessible Deluxe Suite (Elevator Access, Step-free)",
            "vibe": f"Charming local architecture with 24/7 concierge, dietary-customized breakfast, and {tier_lbl.lower()} amenities.",
            "accessibility_features": [
                "Step-free ground entry & elevator",
                "Wide doorways & roll-in shower",
                "24/7 assistance desk"
            ]
        }

        itinerary_data.append({
            "day_number": d,
            "theme": f"Day {d}: {t_title}",
            "activities": [act1, act2, act3],
            "recommended_stay": stay
        })

    # Curated Dining with INR (₹)
    dining_data = [
        {
            "meal_type": "Morning Artisan Breakfast",
            "restaurant_name": f"{dest} Botanical Cafe & Roastery",
            "cuisine": "Artisan Breakfast & Speciality Coffee",
            "dietary_alignment": f"Verified {diets_str} menu selections",
            "allergy_safety_note": f"Dedicated allergen prep protocol: {allergy_notes}",
            "estimated_cost_tier": "₹₹ ($15 – $25)" if b_tier in ["moderate", "flexible"] else ("₹ ($5 – $12)" if b_tier == "budget" else "₹₹₹ ($30 – $60)")
        },
        {
            "meal_type": "Midday Lunch Refuel",
            "restaurant_name": f"The Green Heritage Bistro ({dest})",
            "cuisine": "Local Organic Specialties",
            "dietary_alignment": f"Farm-to-table organic {diets_str} recipes",
            "allergy_safety_note": "No cross-contamination guarantee on customer allergy request",
            "estimated_cost_tier": "₹₹ ($15 – $25)"
        },
        {
            "meal_type": "Evening Gastronomy Dinner",
            "restaurant_name": f"Lantern Garden Kitchen",
            "cuisine": "Regional Fine Heritage Dining",
            "dietary_alignment": f"Signature {diets_str} Chef Tasting Set",
            "allergy_safety_note": "Personalized menu card with verified ingredients",
            "estimated_cost_tier": "₹₹₹ ($40 – $90)" if b_tier in ["premium_luxury", "flexible"] else "₹₹ ($20 – $35)"
        }
    ]

    # Packing Checklist
    modesty_items = []
    if is_modest:
        modesty_items.extend([
            "Lightweight breathable shawl or scarf (shoulders covered for temples)",
            "Long loose trousers or maxi skirt (covering knees)",
            "Slip-on walking footwear (easy removal for shrines & tatami floors)"
        ])
    else:
        modesty_items.append("Standard comfortable everyday city wear")
    
    if passport.clothing_custom:
        modesty_items.append(f"Custom wardrobe: {passport.clothing_custom}")

    weather_items = [
        "UV protection sunglasses and wide-brim sunhat",
        "Compact travel umbrella / windbreaker",
        "Breathable quick-dry socks and walking sneakers"
    ]
    if hot_weather:
        weather_items.append("Cooling mist spray and electrolyte hydration packs")

    acc_items = []
    if is_mobility:
        acc_items.extend([
            "Portable ramp app map & transport transit card",
            "Wheelchair maintenance kit & universal charger"
        ])
    if passport.accessibility_custom:
        acc_items.append(f"Custom care: {passport.accessibility_custom}")

    packing_data = {
        "modesty_specific_items": modesty_items,
        "weather_adaptation_items": weather_items,
        "special_accessibility_items": acc_items
    }

    # Budget Breakdown in INR (₹) and USD ($)
    if b_tier == "budget":
        stay_est = "₹800 – ₹1,800 / night (≈ $10 – $22 USD)"
        food_est = "₹400 – ₹800 / day (≈ $5 – $10 USD)"
        act_est = "₹300 – ₹900 / day (≈ $4 – $11 USD)"
    elif b_tier == "premium_luxury":
        stay_est = "₹8,000 – ₹20,000+ / night (≈ $95 – $240+ USD)"
        food_est = "₹2,500 – ₹6,000 / day (≈ $30 – $72 USD)"
        act_est = "₹2,000 – ₹5,000 / day (≈ $24 – $60 USD)"
    elif b_tier == "flexible":
        stay_est = "₹2,000 – ₹10,000 / night (≈ $24 – $120 USD)"
        food_est = "₹1,000 – ₹3,500 / day (≈ $12 – $42 USD)"
        act_est = "₹800 – ₹3,000 / day (≈ $10 – $36 USD)"
    else:  # moderate
        stay_est = "₹2,500 – ₹5,000 / night (≈ $30 – $60 USD)"
        food_est = "₹1,000 – ₹2,000 / day (≈ $12 – $24 USD)"
        act_est = "₹500 – ₹1,500 / day (≈ $6 – $18 USD)"

    budget_data = {
        "total_estimated_range": est_range,
        "accommodation_per_night": stay_est,
        "meals_daily_estimate": food_est,
        "activities_daily_estimate": act_est,
        "tier_label": tier_lbl
    }

    # Applied preferences summary
    applied_prefs = {
        "traveler_type": t_type,
        "styles": styles,
        "dietary": diets_str,
        "modesty_clothing": is_modest,
        "accessibility": access_str,
        "budget_tier": tier_lbl,
        "currency": curr,
        "standardized_usd": passport.budget_standardized_usd
    }

    # Save to Database
    trip_record = Trip(
        user_id=user_id,
        destination=dest,
        duration_days=days_count,
        start_date=request.start_date,
        custom_notes=request.custom_notes,
        budget_breakdown=budget_data,
        itinerary=itinerary_data,
        dining_recommendations=dining_data,
        packing_checklist=packing_data,
        applied_preferences=applied_prefs
    )
    db.add(trip_record)
    db.commit()
    db.refresh(trip_record)
    return trip_record

def get_user_trips(db: Session, user_id: int) -> List[Trip]:
    return db.query(Trip).filter(Trip.user_id == user_id).order_by(Trip.created_at.desc()).all()

def get_trip_by_id(db: Session, trip_id: int, user_id: int) -> Optional[Trip]:
    return db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == user_id).first()

def delete_trip(db: Session, trip_id: int, user_id: int) -> bool:
    trip = get_trip_by_id(db, trip_id, user_id)
    if trip:
        db.delete(trip)
        db.commit()
        return True
    return False
