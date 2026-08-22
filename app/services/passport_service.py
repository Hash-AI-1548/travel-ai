import os
import re
import uuid
import json
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
from app.models.passport import TravelPassport
from app.schemas.passport import PassportSummaryResponse, SummaryItem
from app.core.config import settings

def sync_passport_to_disk(passport: TravelPassport):
    """Persists collected user profile/passport data to JSON files in the repo for GitHub and team access."""
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        data_dir = os.path.join(base_dir, "data", "processed")
        mock_dir = os.path.join(base_dir, "data", "mock")
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(mock_dir, exist_ok=True)

        record = {
            "user_id": passport.user_id,
            "full_name": passport.full_name,
            "age": passport.age,
            "gender": passport.gender,
            "nationality": passport.nationality,
            "home_city": passport.home_city,
            "personal_notes": passport.personal_notes,
            "profile_picture_url": passport.profile_picture_url,
            "languages_spoken": passport.languages_spoken,
            "traveler_type": passport.traveler_type,
            "traveler_type_custom": passport.traveler_type_custom,
            "accessibility_mobility": passport.accessibility_mobility,
            "accessibility_visual": passport.accessibility_visual,
            "accessibility_hearing": passport.accessibility_hearing,
            "accessibility_senior": passport.accessibility_senior,
            "accessibility_child": passport.accessibility_child,
            "accessibility_none": passport.accessibility_none,
            "accessibility_custom": passport.accessibility_custom,
            "travel_styles": passport.travel_styles,
            "travel_styles_custom": passport.travel_styles_custom,
            "dietary_standards": passport.dietary_standards,
            "allergies_restrictions": passport.allergies_restrictions,
            "food_custom": passport.food_custom,
            "pack_styles": passport.pack_styles,
            "modest_clothing": passport.modest_clothing,
            "prioritize_hot_weather": passport.prioritize_hot_weather,
            "clothing_custom": passport.clothing_custom,
            "budget_tier": passport.budget_tier,
            "budget_currency": passport.budget_currency,
            "budget_custom": passport.budget_custom,
            "budget_standardized_usd": passport.budget_standardized_usd,
            "is_completed": passport.is_completed,
            "completion_percentage": passport.completion_percentage,
            "updated_at": passport.updated_at.isoformat() if passport.updated_at else datetime.now(timezone.utc).isoformat()
        }

        user_file = os.path.join(data_dir, "user_profiles.json")
        profiles = []
        if os.path.exists(user_file):
            try:
                with open(user_file, "r", encoding="utf-8") as f:
                    profiles = json.load(f)
            except Exception:
                profiles = []
        profiles = [p for p in profiles if p.get("user_id") != passport.user_id]
        profiles.append(record)
        with open(user_file, "w", encoding="utf-8") as f:
            json.dump(profiles, f, indent=2)

        pass_file = os.path.join(mock_dir, "submitted_passports.json")
        with open(pass_file, "w", encoding="utf-8") as f:
            json.dump(profiles, f, indent=2)
    except Exception as e:
        print(f"Error syncing passport to disk: {e}")

# Global 160+ Currency conversion rates to USD (1 unit of currency in USD)
GLOBAL_CURRENCY_RATES = {
    "INR": 0.0119, "USD": 1.0, "EUR": 1.087, "GBP": 1.266, "AED": 0.272,
    "CAD": 0.735, "AUD": 0.658, "SGD": 0.746, "JPY": 0.00658, "SAR": 0.267,
    "QAR": 0.275, "KWD": 3.26, "BHD": 2.65, "OMR": 2.60, "CHF": 1.136,
    "CNY": 0.138, "HKD": 0.128, "NZD": 0.612, "THB": 0.0274, "MYR": 0.213,
    "IDR": 0.0000625, "PHP": 0.0175, "VND": 0.000039, "KRW": 0.000725,
    "TWD": 0.031, "PKR": 0.0036, "BDT": 0.0085, "LKR": 0.0033, "NPR": 0.0075,
    "AFN": 0.014, "ALL": 0.011, "AMD": 0.0026, "ANG": 0.556, "AOA": 0.0011,
    "ARS": 0.0011, "AWG": 0.556, "AZN": 0.588, "BAM": 0.555, "BBD": 0.50,
    "BGN": 0.555, "BIF": 0.00035, "BMD": 1.0, "BND": 0.746, "BOB": 0.145,
    "BRL": 0.183, "BSD": 1.0, "BTN": 0.0119, "BWP": 0.074, "BYN": 0.305,
    "BZD": 0.50, "CDF": 0.00036, "CLP": 0.00108, "COP": 0.00025, "CRC": 0.0019,
    "CUP": 0.042, "CVE": 0.0098, "CZK": 0.043, "DJF": 0.0056, "DKK": 0.145,
    "DOP": 0.017, "DZD": 0.0074, "EGP": 0.021, "ERN": 0.067, "ETB": 0.0084,
    "FJD": 0.445, "FKP": 1.266, "GEL": 0.37, "GHS": 0.065, "GIP": 1.266,
    "GMD": 0.014, "GNF": 0.00012, "GTQ": 0.129, "GYD": 0.0048, "HNL": 0.040,
    "HRK": 0.144, "HTG": 0.0076, "HUF": 0.0028, "ILS": 0.272, "IQD": 0.00076,
    "IRR": 0.000024, "ISK": 0.0073, "JMD": 0.0064, "JOD": 1.41, "KES": 0.0077,
    "KGS": 0.0116, "KHR": 0.00024, "KMF": 0.0022, "KYD": 1.20, "KZT": 0.0021,
    "LAK": 0.000046, "LBP": 0.000011, "LRD": 0.0051, "LSL": 0.054, "LYD": 0.207,
    "MAD": 0.10, "MDL": 0.056, "MGA": 0.00022, "MKD": 0.0176, "MMK": 0.00048,
    "MNT": 0.00029, "MOP": 0.124, "MRU": 0.025, "MUR": 0.0215, "MVR": 0.065,
    "MWK": 0.00057, "MXN": 0.0549, "MZN": 0.0156, "NAD": 0.054, "NGN": 0.00063,
    "NIO": 0.027, "NOK": 0.094, "PAB": 1.0, "PEN": 0.268, "PGK": 0.255,
    "PLN": 0.252, "PYG": 0.00013, "RON": 0.218, "RSD": 0.0093, "RUB": 0.011,
    "RWF": 0.00075, "SBD": 0.118, "SCR": 0.073, "SDG": 0.0017, "SEK": 0.096,
    "SOS": 0.00175, "SRD": 0.028, "SYP": 0.000077, "SZL": 0.054, "TJS": 0.092,
    "TMT": 0.286, "TND": 0.32, "TOP": 0.42, "TRY": 0.029, "TTD": 0.147,
    "TZS": 0.00038, "UAH": 0.024, "UGX": 0.00027, "UYU": 0.025, "UZS": 0.000079,
    "VES": 0.027, "VUV": 0.0083, "WST": 0.365, "XAF": 0.00165, "XCD": 0.370,
    "XOF": 0.00165, "XPF": 0.0091, "YER": 0.0040, "ZAR": 0.054, "ZMW": 0.038
}

def standardize_budget_to_usd(raw_custom: Optional[str], currency_code: Optional[str]) -> Optional[str]:
    """Extracts numbers from custom budget string, converts using exchange rate, and returns standardized USD estimate."""
    if not raw_custom:
        return None
    code = (currency_code or "INR").strip().upper()
    rate = GLOBAL_CURRENCY_RATES.get(code, 0.0119)

    # Find numbers or ranges in the string
    numbers = [float(n.replace(",", "")) for n in re.findall(r'\b\d+(?:,\d+)*(?:\.\d+)?\b', raw_custom)]
    if not numbers:
        return f"≈ {raw_custom} ({code})"
    
    if len(numbers) >= 2:
        low_usd = int(numbers[0] * rate)
        high_usd = int(numbers[1] * rate)
        return f"≈ ${low_usd:,} – ${high_usd:,} USD (Converted from {code})"
    else:
        val_usd = int(numbers[0] * rate)
        return f"≈ ${val_usd:,} USD (Converted from {code})"

def get_or_create_passport(db: Session, user_id: int) -> TravelPassport:
    passport = db.query(TravelPassport).filter(TravelPassport.user_id == user_id).first()
    if not passport:
        passport = TravelPassport(
            user_id=user_id,
            languages_spoken=["English"],
            travel_styles=[],
            dietary_standards=[],
            pack_styles=[],
            budget_currency="INR",
            current_step=1,
            is_completed=False,
            completion_percentage=0
        )
        db.add(passport)
        db.commit()
        db.refresh(passport)
    return passport

def calculate_progress(passport: TravelPassport) -> tuple[int, bool]:
    completed_steps = 0
    total_steps = 7

    # Step 1
    if passport.full_name and passport.age and passport.home_city:
        completed_steps += 1
    # Step 2
    if passport.traveler_type:
        completed_steps += 1
    # Step 3
    if (passport.accessibility_none or passport.accessibility_mobility or 
        passport.accessibility_visual or passport.accessibility_hearing or 
        passport.accessibility_senior or passport.accessibility_child or
        passport.accessibility_custom):
        completed_steps += 1
    # Step 4
    if (passport.travel_styles and len(passport.travel_styles) >= 1) or passport.travel_styles_custom:
        completed_steps += 1
    # Step 5
    if (passport.dietary_standards is not None and len(passport.dietary_standards) >= 1) or passport.food_custom:
        completed_steps += 1
    # Step 6
    if (passport.pack_styles is not None and len(passport.pack_styles) >= 1) or passport.clothing_custom:
        completed_steps += 1
    # Step 7
    if passport.budget_tier or passport.budget_custom:
        completed_steps += 1

    percentage = int((completed_steps / total_steps) * 100)
    is_completed = completed_steps >= 6
    return percentage, is_completed

def update_passport_step(db: Session, user_id: int, step_number: int, data: dict) -> TravelPassport:
    passport = get_or_create_passport(db, user_id)
    
    if step_number == 1:
        for k in ["full_name", "age", "gender", "nationality", "home_city", "personal_notes", "profile_picture_url", "languages_spoken"]:
            if k in data and data[k] is not None:
                setattr(passport, k, data[k])
    elif step_number == 2:
        if "traveler_type" in data:
            passport.traveler_type = data["traveler_type"]
        if "traveler_type_custom" in data:
            passport.traveler_type_custom = data["traveler_type_custom"]
    elif step_number == 3:
        for k in ["accessibility_mobility", "accessibility_visual", "accessibility_hearing", 
                  "accessibility_senior", "accessibility_child", "accessibility_none", "accessibility_custom"]:
            if k in data and data[k] is not None:
                setattr(passport, k, data[k])
    elif step_number == 4:
        if "travel_styles" in data and data["travel_styles"] is not None:
            passport.travel_styles = data["travel_styles"]
        if "travel_styles_custom" in data:
            passport.travel_styles_custom = data["travel_styles_custom"]
    elif step_number == 5:
        if "dietary_standards" in data and data["dietary_standards"] is not None:
            passport.dietary_standards = data["dietary_standards"]
        if "allergies_restrictions" in data:
            passport.allergies_restrictions = data["allergies_restrictions"]
        if "food_custom" in data:
            passport.food_custom = data["food_custom"]
    elif step_number == 6:
        if "pack_styles" in data and data["pack_styles"] is not None:
            passport.pack_styles = data["pack_styles"]
        if "modest_clothing" in data and data["modest_clothing"] is not None:
            passport.modest_clothing = data["modest_clothing"]
        if "prioritize_hot_weather" in data and data["prioritize_hot_weather"] is not None:
            passport.prioritize_hot_weather = data["prioritize_hot_weather"]
        if "clothing_custom" in data:
            passport.clothing_custom = data["clothing_custom"]
    elif step_number == 7:
        if "budget_tier" in data and data["budget_tier"] is not None:
            passport.budget_tier = data["budget_tier"]
        if "budget_currency" in data and data["budget_currency"] is not None:
            passport.budget_currency = data["budget_currency"]
        if "budget_custom" in data:
            passport.budget_custom = data["budget_custom"]
        
        # Calculate standardized USD
        passport.budget_standardized_usd = standardize_budget_to_usd(passport.budget_custom, passport.budget_currency)
    else:
        raise HTTPException(status_code=400, detail=f"Invalid step number: {step_number}. Must be 1-7.")

    percentage, is_comp = calculate_progress(passport)
    passport.completion_percentage = percentage
    passport.is_completed = is_comp
    passport.current_step = min(max(step_number + 1, passport.current_step), 8)
    passport.updated_at = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(passport)
    sync_passport_to_disk(passport)
    return passport

def update_full_passport(db: Session, user_id: int, data: dict) -> TravelPassport:
    passport = get_or_create_passport(db, user_id)
    for key, val in data.items():
        if hasattr(passport, key) and val is not None:
            setattr(passport, key, val)
    
    if passport.budget_custom:
        passport.budget_standardized_usd = standardize_budget_to_usd(passport.budget_custom, passport.budget_currency)

    percentage, is_comp = calculate_progress(passport)
    passport.completion_percentage = percentage
    passport.is_completed = is_comp
    passport.updated_at = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(passport)
    sync_passport_to_disk(passport)
    return passport

async def save_profile_avatar(db: Session, user_id: int, file: UploadFile) -> str:
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '{file.content_type}'. Allowed types: {settings.ALLOWED_IMAGE_TYPES}"
        )
    
    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB}MB"
        )
    
    ext = file.filename.split(".")[-1].lower() if file.filename and "." in file.filename else "jpg"
    safe_name = f"user_{user_id}_{uuid.uuid4().hex[:8]}.{ext}"
    avatars_dir = os.path.join(settings.UPLOAD_DIR, "avatars")
    os.makedirs(avatars_dir, exist_ok=True)
    file_path = os.path.join(avatars_dir, safe_name)
    
    with open(file_path, "wb") as f:
        f.write(content)
        
    avatar_url = f"/uploads/avatars/{safe_name}"
    passport = get_or_create_passport(db, user_id)
    passport.profile_picture_url = avatar_url
    db.commit()
    db.refresh(passport)
    return avatar_url

def generate_summary(passport: TravelPassport) -> PassportSummaryResponse:
    # 1. Personal Info
    name = passport.full_name or "Anonymous Traveler"
    age = f", {passport.age}" if passport.age else ""
    gender = f" • {passport.gender}" if passport.gender else ""
    nat = f" ({passport.nationality})" if passport.nationality else ""
    city = f"Home: {passport.home_city}" if passport.home_city else "Home: Not specified"
    langs = f" • {', '.join(passport.languages_spoken)}" if passport.languages_spoken else ""
    personal_headline = f"{name}{age}{gender}{nat}"
    personal_subtext = f"{city}{langs}"
    if passport.personal_notes:
        personal_subtext += f" • Note: {passport.personal_notes}"

    # 2. Traveler Type
    type_titles = {
        "solo": ("Solo Configuration", "Autonomous self-guided paths, flexible schedules, single rooms"),
        "couple": ("Couple Configuration", "Romantic stays, fine dining, intimate private tour routes"),
        "family": ("Family Configuration", "Kid-friendly attractions, multi-room suites, gentle transit pace"),
        "friends": ("Friends Configuration", "Shared budgets, multiple rooms, high-energy group spots"),
        "senior": ("Senior Traveler Configuration", "Comfortable transit, accessible walks, deep cultural pacing")
    }
    t_title, t_sub = type_titles.get(passport.traveler_type or "solo", ("Custom Traveler Configuration", "Flexible itinerary schedule"))
    if passport.traveler_type_custom:
        t_sub += f" • Custom: {passport.traveler_type_custom}"

    # 3. Accessibility
    acc_items = []
    if passport.accessibility_mobility:
        acc_items.append("Mobility & Wheelchair Access")
    if passport.accessibility_visual:
        acc_items.append("Visual Assistance")
    if passport.accessibility_hearing:
        acc_items.append("Hearing / Audio Support")
    if passport.accessibility_senior:
        acc_items.append("Elderly & Senior Friendly")
    if passport.accessibility_child:
        acc_items.append("Child-friendly Stays")
    
    if acc_items:
        acc_headline = ", ".join(acc_items[:2])
        acc_subtext = "Step-free entry, elevators, prioritized accessibility filters"
    else:
        acc_headline = "Standard Accommodations"
        acc_subtext = "No specific mobility or visual accommodations required"
    if passport.accessibility_custom:
        acc_subtext += f" • Note: {passport.accessibility_custom}"

    # 4. Travel Style
    styles = [s.replace("_", " ").title() for s in (passport.travel_styles or ["Adventure", "Culture"])]
    if passport.travel_styles_custom:
        styles.append(f"+ {passport.travel_styles_custom}")
    style_headline = ", ".join(styles) if styles else "Balanced Exploration"
    style_subtext = f"{len(styles)} style layers calibrated for POI selection & AI generator"

    # 5. Food Preferences
    diets = [d.replace("_", " ").title() for d in (passport.dietary_standards or ["Standard Dining"])]
    diet_headline = f"{', '.join(diets)} Standards" if diets else "Flexible Dining"
    allergy_parts = []
    if passport.allergies_restrictions:
        allergy_parts.append(f"Allergies: {passport.allergies_restrictions}")
    if passport.food_custom:
        allergy_parts.append(f"Custom: {passport.food_custom}")
    allergy_sub = " • ".join(allergy_parts) if allergy_parts else "No severe allergy restrictions flagged"

    # 6. Clothing Pack
    pack = [p.replace("_", " ").title() for p in (passport.pack_styles or ["Casual", "Western"])]
    pack_headline = f"{', '.join(pack)} wear"
    modesty_notes = []
    if passport.modest_clothing:
        modesty_notes.append("Modesty filters active (temple & custom friendly)")
    if passport.prioritize_hot_weather:
        modesty_notes.append("Hot weather comfort priority")
    if passport.clothing_custom:
        modesty_notes.append(f"Custom: {passport.clothing_custom}")
    pack_subtext = " • ".join(modesty_notes) if modesty_notes else "Standard travel checklist"

    # 7. Budget Footprint with Multi-Currency & USD Standardization
    curr = passport.budget_currency or "INR"
    custom_val = passport.budget_custom or "50,000"
    usd_note = f" [{passport.budget_standardized_usd}]" if passport.budget_standardized_usd else ""
    b_head = f"{curr} {custom_val}{usd_note}"
    b_sub = f"Currency: {curr} • Standardized USD conversion calibrated for global itinerary flights & hotels"

    return PassportSummaryResponse(
        is_ready=True,
        status_badge="Itinerary algorithm primed and ready to calculate.",
        personal_info=SummaryItem(
            title="Personal Info",
            headline=personal_headline,
            subtext=personal_subtext,
            step_number=1,
            data={
                "name": passport.full_name,
                "age": passport.age,
                "gender": passport.gender,
                "nationality": passport.nationality,
                "city": passport.home_city,
                "notes": passport.personal_notes,
                "languages": passport.languages_spoken
            }
        ),
        traveler_type=SummaryItem(
            title="Traveler Type",
            headline=t_title,
            subtext=t_sub,
            step_number=2,
            data={"type": passport.traveler_type, "custom": passport.traveler_type_custom}
        ),
        accessibility=SummaryItem(
            title="Accessibility",
            headline=acc_headline,
            subtext=acc_subtext,
            step_number=3,
            data={
                "mobility": passport.accessibility_mobility,
                "visual": passport.accessibility_visual,
                "hearing": passport.accessibility_hearing,
                "senior": passport.accessibility_senior,
                "child": passport.accessibility_child,
                "none": passport.accessibility_none,
                "custom": passport.accessibility_custom
            }
        ),
        travel_style=SummaryItem(
            title="Travel Style",
            headline=style_headline,
            subtext=style_subtext,
            step_number=4,
            data={"styles": passport.travel_styles, "custom": passport.travel_styles_custom}
        ),
        food_preferences=SummaryItem(
            title="Food Preferences",
            headline=diet_headline,
            subtext=allergy_sub,
            step_number=5,
            data={"standards": passport.dietary_standards, "allergies": passport.allergies_restrictions, "custom": passport.food_custom}
        ),
        clothing_pack=SummaryItem(
            title="Clothing Pack",
            headline=pack_headline,
            subtext=pack_subtext,
            step_number=6,
            data={"pack_styles": passport.pack_styles, "modest": passport.modest_clothing, "hot_weather": passport.prioritize_hot_weather, "custom": passport.clothing_custom}
        ),
        budget_footprint=SummaryItem(
            title="Budget Footprint",
            headline=b_head,
            subtext=b_sub,
            step_number=7,
            data={
                "tier": passport.budget_tier,
                "currency": passport.budget_currency,
                "custom": passport.budget_custom,
                "standardized_usd": passport.budget_standardized_usd
            }
        )
    )
