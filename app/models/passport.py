from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class TravelPassport(Base):
    __tablename__ = "travel_passports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)

    # Step 1: Personal Info
    full_name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    nationality = Column(String, nullable=True)
    home_city = Column(String, nullable=True)
    personal_notes = Column(Text, nullable=True)
    profile_picture_url = Column(String, nullable=True)
    languages_spoken = Column(JSON, default=list)

    # Step 2: Traveler Type
    traveler_type = Column(String, nullable=True)
    traveler_type_custom = Column(Text, nullable=True)

    # Step 3: Accessibility & Comfort
    accessibility_mobility = Column(Boolean, default=False)
    accessibility_visual = Column(Boolean, default=False)
    accessibility_hearing = Column(Boolean, default=False)
    accessibility_senior = Column(Boolean, default=False)
    accessibility_child = Column(Boolean, default=False)
    accessibility_none = Column(Boolean, default=False)
    accessibility_custom = Column(Text, nullable=True)

    # Step 4: Travel Styles
    travel_styles = Column(JSON, default=list)
    travel_styles_custom = Column(Text, nullable=True)

    # Step 5: Culinary & Food Preferences
    dietary_standards = Column(JSON, default=list)
    allergies_restrictions = Column(Text, nullable=True)
    food_custom = Column(Text, nullable=True)

    # Step 6: Clothing Preferences
    pack_styles = Column(JSON, default=list)
    modest_clothing = Column(Boolean, default=False)
    prioritize_hot_weather = Column(Boolean, default=False)
    clothing_custom = Column(Text, nullable=True)

    # Step 7: Budget Footprint & Multi-Currency Standardization
    budget_tier = Column(String, nullable=True)
    budget_currency = Column(String, default="INR")
    budget_custom = Column(Text, nullable=True)
    budget_standardized_usd = Column(String, nullable=True)

    # Progression & Metadata
    current_step = Column(Integer, default=1)
    is_completed = Column(Boolean, default=False)
    completion_percentage = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="passport")
