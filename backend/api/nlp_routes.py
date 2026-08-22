"""
Module 1 & 2: NLP API Routes
Owner: Satyajit
"""
from fastapi import APIRouter
from pydantic import BaseModel
from modules.nlp.nlp_service import extract_traveler_profile
from modules.nlp.ticket_parser import parse_booking_text

router = APIRouter(prefix="/api/v1/nlp", tags=["NLP & Ticket Parsing"])

class TextPayload(BaseModel):
    raw_text: str

@router.post("/profile")
def generate_profile(payload: TextPayload):
    """Converts natural language into a structured traveler profile."""
    profile = extract_traveler_profile(payload.raw_text)
    return {"status": "SUCCESS", "data": profile}

@router.post("/ticket")
def parse_ticket(payload: TextPayload):
    """Extracts travel details from pasted booking text."""
    ticket_data = parse_booking_text(payload.raw_text)
    return {"status": "SUCCESS", "data": ticket_data}
