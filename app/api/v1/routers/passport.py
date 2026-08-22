from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Body
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user_id
from app.schemas.passport import (
    PassportResponse, PassportFullUpdate, PassportSummaryResponse,
    PersonalInfoStep, TravelerTypeStep, AccessibilityStep,
    TravelStylesStep, FoodPreferencesStep, ClothingStep, BudgetStep
)
from app.services.passport_service import (
    get_or_create_passport, update_passport_step, update_full_passport,
    save_profile_avatar, generate_summary
)

router = APIRouter(prefix="/passport", tags=["Travel Passport & Onboarding"])

@router.get("", response_model=PassportResponse)
def get_passport(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Retrieve current user's Travel Passport profile."""
    return get_or_create_passport(db, user_id)

@router.put("", response_model=PassportResponse)
def update_passport(
    update_data: PassportFullUpdate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Full or partial update of the Travel Passport."""
    data = update_data.model_dump(exclude_unset=True)
    return update_full_passport(db, user_id, data)

@router.patch("/step/{step_number}", response_model=PassportResponse)
def patch_step(
    step_number: int,
    step_data: dict = Body(...),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Save/update data for a specific onboarding step (1 to 7)."""
    return update_passport_step(db, user_id, step_number, step_data)

@router.post("/step/1-personal-info", response_model=PassportResponse)
def save_step_1(step: PersonalInfoStep, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Save Step 1: Personal Info (Name, Age, City, Languages)."""
    return update_passport_step(db, user_id, 1, step.model_dump(exclude_unset=True))

@router.post("/step/2-traveler-type", response_model=PassportResponse)
def save_step_2(step: TravelerTypeStep, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Save Step 2: Traveler Type (Solo, Couple, Family, Friends, Senior)."""
    return update_passport_step(db, user_id, 2, step.model_dump(exclude_unset=True))

@router.post("/step/3-accessibility", response_model=PassportResponse)
def save_step_3(step: AccessibilityStep, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Save Step 3: Accessibility & Comfort options."""
    return update_passport_step(db, user_id, 3, step.model_dump(exclude_unset=True))

@router.post("/step/4-travel-styles", response_model=PassportResponse)
def save_step_4(step: TravelStylesStep, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Save Step 4: Travel Styles (min 3 styles recommended)."""
    return update_passport_step(db, user_id, 4, step.model_dump(exclude_unset=True))

@router.post("/step/5-food-preferences", response_model=PassportResponse)
def save_step_5(step: FoodPreferencesStep, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Save Step 5: Culinary standards & allergies."""
    return update_passport_step(db, user_id, 5, step.model_dump(exclude_unset=True))

@router.post("/step/6-clothing-preferences", response_model=PassportResponse)
def save_step_6(step: ClothingStep, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Save Step 6: Clothing styles, modesty & weather options."""
    return update_passport_step(db, user_id, 6, step.model_dump(exclude_unset=True))

@router.post("/step/7-budget", response_model=PassportResponse)
def save_step_7(step: BudgetStep, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Save Step 7: Budget Footprint calibration."""
    return update_passport_step(db, user_id, 7, step.model_dump(exclude_unset=True))

@router.get("/summary", response_model=PassportSummaryResponse)
def get_passport_summary(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Retrieve Step 8 compiled Travel Passport review cards."""
    passport = get_or_create_passport(db, user_id)
    return generate_summary(passport)

@router.post("/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Upload profile picture for Travel Passport (JPG/PNG, up to 5MB)."""
    avatar_url = await save_profile_avatar(db, user_id, file)
    return {"status": "success", "profile_picture_url": avatar_url}
