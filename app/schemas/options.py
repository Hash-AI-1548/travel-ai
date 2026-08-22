from typing import List, Optional
from pydantic import BaseModel

class OptionItem(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    icon: Optional[str] = None
    symbol: Optional[str] = None

class CurrencyOption(BaseModel):
    code: str
    name: str
    symbol: str
    usd_rate: float

class OptionsMetadataResponse(BaseModel):
    traveler_types: List[OptionItem]
    accessibility_options: List[OptionItem]
    travel_styles: List[OptionItem]
    dietary_standards: List[OptionItem]
    clothing_pack_styles: List[str]
    clothing_toggles: List[OptionItem]
    budget_tiers: List[OptionItem]
    languages: List[str]
    nationalities: List[str] = []
    currencies: List[CurrencyOption] = []
