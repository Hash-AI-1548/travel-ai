from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    destination = Column(String, nullable=False)
    start_date = Column(String, nullable=True)
    duration_days = Column(Integer, default=5)
    custom_notes = Column(String, nullable=True)

    # Generated Output JSON
    itinerary = Column(JSON, nullable=False)
    dining_recommendations = Column(JSON, default=list)
    packing_checklist = Column(JSON, default=dict)
    budget_breakdown = Column(JSON, default=dict)
    applied_preferences = Column(JSON, default=dict)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="trips")
