"""
Module 2: NLP Preference Extraction Service
Owner: Satyajit
"""

def extract_traveler_profile(user_prompt: str) -> dict:
    """
    Converts natural language input into a structured traveler profile
    that the Routing and POI modules can understand.
    """
    prompt = user_prompt.lower()
    
    # 1. Extract Preferences
    preferences = []
    if "culture" in prompt or "temple" in prompt:
        preferences.append("culture")
    if "nature" in prompt or "park" in prompt:
        preferences.append("nature")
    if "adventure" in prompt or "hike" in prompt:
        preferences.append("adventure")
        
    # 2. Extract Accessibility Constraints
    needs_wheelchair = "wheelchair" in prompt or "accessible" in prompt
    
    # 3. Extract Age Constraints
    min_age = 18 # Default to adult
    if "kid" in prompt or "child" in prompt or "family" in prompt:
        min_age = 5
    elif "toddler" in prompt or "baby" in prompt:
        min_age = 1
        
    return {
        "wheelchair": needs_wheelchair,
        "min_age": min_age,
        "preferences": preferences
    }

if __name__ == "__main__":
    print("--- 🧠 Testing NLP Extraction ---")
    test_prompt = "I want a relaxing nature trip for my family with kids. We need wheelchair access."
    profile = extract_traveler_profile(test_prompt)
    print(f"Raw Input: '{test_prompt}'")
    print(f"Extracted Profile: {profile}")
