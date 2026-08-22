import io
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, engine, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use a clean test SQLite database
TEST_DB_URL = "sqlite:///./test_travel_ai.db"
test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "Travel AI" in data["service"]

def test_options_metadata():
    response = client.get("/api/v1/options")
    assert response.status_code == 200
    data = response.json()
    assert "traveler_types" in data
    assert "accessibility_options" in data
    assert "travel_styles" in data
    assert "dietary_standards" in data
    assert "clothing_pack_styles" in data
    assert "budget_tiers" in data
    assert "nationalities" in data
    assert "currencies" in data
    assert len(data["currencies"]) >= 15
    assert any(c["code"] == "INR" for c in data["currencies"])
    assert any(c["code"] == "USD" for c in data["currencies"])
    assert any(c["code"] == "EUR" for c in data["currencies"])

def test_auth_and_passport_lifecycle():
    # 1. Register new user
    reg_payload = {
        "email": "test_evelyn@travelai.com",
        "password": "securepassword123",
        "full_name": "Evelyn Thorne"
    }
    reg_res = client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_res.status_code == 201
    token = reg_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Check /auth/me
    me_res = client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "test_evelyn@travelai.com"

    # 3. Get initial passport
    pass_res = client.get("/api/v1/passport", headers=headers)
    assert pass_res.status_code == 200
    passport = pass_res.json()
    assert passport["full_name"] == "Evelyn Thorne"
    assert passport["current_step"] == 1

    # 4. Step 1: Save Personal Info with Nationality and Personal Notes
    step1_res = client.post("/api/v1/passport/step/1-personal-info", headers=headers, json={
        "full_name": "Evelyn Thorne",
        "age": 29,
        "gender": "Female",
        "nationality": "Indian",
        "home_city": "Mumbai",
        "personal_notes": "Celebrating 5th wedding anniversary",
        "languages_spoken": ["English", "Hindi"]
    })
    assert step1_res.status_code == 200
    assert step1_res.json()["age"] == 29
    assert step1_res.json()["nationality"] == "Indian"

    # 5. Step 2: Save Traveler Type with Custom Group Details
    step2_res = client.post("/api/v1/passport/step/2-traveler-type", headers=headers, json={
        "traveler_type": "couple",
        "traveler_type_custom": "Traveling with a friendly pet"
    })
    assert step2_res.status_code == 200
    assert step2_res.json()["traveler_type"] == "couple"

    # 6. Step 3: Save Accessibility Options with Custom Need
    step3_res = client.post("/api/v1/passport/step/3-accessibility", headers=headers, json={
        "accessibility_mobility": True,
        "accessibility_visual": False,
        "accessibility_hearing": False,
        "accessibility_senior": False,
        "accessibility_child": False,
        "accessibility_none": False,
        "accessibility_custom": "Need ground floor room"
    })
    assert step3_res.status_code == 200
    assert step3_res.json()["accessibility_mobility"] is True

    # 7. Step 4: Save Travel Styles with Custom Style
    step4_res = client.post("/api/v1/passport/step/4-travel-styles", headers=headers, json={
        "travel_styles": ["adventure", "nature", "culture", "food_wine", "photography"],
        "travel_styles_custom": "Heritage temple architecture"
    })
    assert step4_res.status_code == 200
    assert len(step4_res.json()["travel_styles"]) == 5

    # 8. Step 5: Save Food Preferences with Custom Cuisine
    step5_res = client.post("/api/v1/passport/step/5-food-preferences", headers=headers, json={
        "dietary_standards": ["vegetarian", "halal"],
        "allergies_restrictions": "Severe peanut allergy, prefers gluten-free options where possible",
        "food_custom": "Prefer authentic thali and street food stalls"
    })
    assert step5_res.status_code == 200
    assert "vegetarian" in step5_res.json()["dietary_standards"]

    # 9. Step 6: Save Clothing Preferences with Custom Packing
    step6_res = client.post("/api/v1/passport/step/6-clothing-preferences", headers=headers, json={
        "pack_styles": ["western", "casual"],
        "modest_clothing": True,
        "prioritize_hot_weather": True,
        "clothing_custom": "Traditional kurta for temple visits"
    })
    assert step6_res.status_code == 200
    assert step6_res.json()["modest_clothing"] is True

    # 10. Step 7: Save Budget Footprint with Currency Selection & USD Standardization
    step7_res = client.post("/api/v1/passport/step/7-budget", headers=headers, json={
        "budget_tier": "moderate",
        "budget_currency": "INR",
        "budget_custom": "50000"
    })
    assert step7_res.status_code == 200
    data7 = step7_res.json()
    assert data7["budget_tier"] == "moderate"
    assert data7["budget_currency"] == "INR"
    assert data7["budget_custom"] == "50000"
    assert "USD" in data7["budget_standardized_usd"]
    assert "595" in data7["budget_standardized_usd"]
    assert data7["completion_percentage"] == 100
    assert data7["is_completed"] is True

    # 11. Step 8: Passport Summary Card
    sum_res = client.get("/api/v1/passport/summary", headers=headers)
    assert sum_res.status_code == 200
    summary = sum_res.json()
    assert summary["is_ready"] is True
    assert "Indian" in summary["personal_info"]["headline"]
    assert "INR" in summary["budget_footprint"]["subtext"]
    assert "USD" in summary["budget_footprint"]["subtext"]

def test_avatar_upload():
    # Register user
    reg_res = client.post("/api/v1/auth/register", json={
        "email": "avatar_tester@travelai.com",
        "password": "mypassword123",
        "full_name": "Avatar Tester"
    })
    assert reg_res.status_code == 201
    token = reg_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Upload test PNG
    test_img = io.BytesIO(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82")
    files = {"file": ("avatar.png", test_img, "image/png")}
    
    upload_res = client.post("/api/v1/passport/avatar", headers=headers, files=files)
    assert upload_res.status_code == 200
    avatar_url = upload_res.json()["profile_picture_url"]
    assert avatar_url.startswith("/uploads/avatars/user_")

def test_ai_trip_generation_with_multi_currency():
    # Register & complete passport with EUR currency
    reg_res = client.post("/api/v1/auth/register", json={
        "email": "traveler_euro@travelai.com",
        "password": "mypassword123",
        "full_name": "Euro Traveler"
    })
    assert reg_res.status_code == 201
    token = reg_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Setup passport with EUR currency and custom range
    client.put("/api/v1/passport", headers=headers, json={
        "full_name": "Euro Traveler",
        "age": 32,
        "nationality": "French",
        "personal_notes": "Summer holiday trip",
        "traveler_type": "couple",
        "traveler_type_custom": "Couple vacation",
        "accessibility_mobility": False,
        "travel_styles": ["culture", "nature", "food_wine", "photography"],
        "dietary_standards": ["vegetarian"],
        "allergies_restrictions": "None",
        "pack_styles": ["casual"],
        "modest_clothing": True,
        "budget_tier": "moderate",
        "budget_currency": "EUR",
        "budget_custom": "1500 - 2000"
    })

    # Generate Trip
    gen_res = client.post("/api/v1/trips/generate", headers=headers, json={
        "destination": "Rome, Italy",
        "duration_days": 3,
        "start_date": "2026-09-10",
        "custom_notes": "Interested in historic sites and culinary dining."
    })
    assert gen_res.status_code == 201
    trip = gen_res.json()
    assert trip["destination"] == "Rome, Italy"
    assert trip["duration_days"] == 3
    assert len(trip["itinerary"]) == 3

    # Verify that itinerary contains both EUR and standardized USD
    assert "EUR" in trip["budget_breakdown"]["total_estimated_range"]
    assert "USD" in trip["budget_breakdown"]["total_estimated_range"]
    assert "MODERATE" in trip["budget_breakdown"]["tier_label"]

    # List trips
    list_res = client.get("/api/v1/trips", headers=headers)
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1
