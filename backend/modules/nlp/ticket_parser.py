"""
Module 1: Ticket Parser
Owner: Satyajit
"""
import re

def parse_booking_text(raw_text: str) -> dict:
    """
    Scans a raw ticket string and extracts key travel details for the MVP.
    """
    text = raw_text.lower()
    
    # 1. Extract Destination (Basic keyword matching for MVP)
    destination = "Unknown"
    if "chennai" in text or "maa" in text:
        destination = "Chennai"
    elif "delhi" in text or "del" in text:
        destination = "Delhi"
        
    # 2. Extract Dates using a simple Regex pattern (YYYY-MM-DD)
    dates_found = re.findall(r'\d{4}-\d{2}-\d{2}', raw_text)
    arrival_date = dates_found[0] if dates_found else "Not Found"
    
    # 3. Estimate number of travelers based on keywords
    pax_count = 1
    if "family" in text or "group" in text:
        pax_count = 4
        
    return {
        "destination": destination,
        "arrival_date": arrival_date,
        "traveler_count": pax_count
    }

if __name__ == "__main__":
    print("--- 🎫 Testing Ticket Parser ---")
    sample_ticket = "Flight INDIGO 6E-234. Arriving in Chennai on 2026-09-15. Passenger: 1 Adult."
    print(parse_booking_text(sample_ticket))
