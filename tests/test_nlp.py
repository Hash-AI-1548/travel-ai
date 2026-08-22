"""
Module 1 & 2 Unit Tests: NLP and Ticket Parsing
Author: Satyajit
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

# pyrefly: ignore [missing-import]
from modules.nlp.nlp_service import extract_traveler_profile
# pyrefly: ignore [missing-import]
from modules.nlp.ticket_parser import parse_booking_text

def test_nlp_extraction():
    """Verify natural language extraction of preferences, age, and accessibility."""
    sample_text = "Looking for a culture and temple trip with kids and wheelchair access."
    profile = extract_traveler_profile(sample_text)
    
    assert profile["wheelchair"] is True
    assert profile["min_age"] == 5
    assert "culture" in profile["preferences"]

def test_ticket_parser():
    """Verify parsing of flight/train booking details."""
    sample_ticket = "Flight INDIGO arriving in Chennai on 2026-09-15 for a family vacation."
    ticket = parse_booking_text(sample_ticket)
    
    assert ticket["destination"] == "Chennai"
    assert ticket["arrival_date"] == "2026-09-15"
    assert ticket["traveler_count"] == 4
