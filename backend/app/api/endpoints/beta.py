from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.core.telegram_auth import assert_owner, telegram_user_id
from app.models.beta import BetaEnrollment, BetaInvite
from app.models.event import ProductEvent
from app.models.user import User

router = APIRouter(prefix="/api/beta", tags=["beta"])

class Claim(BaseModel):
    user_id: int
    code: str = Field(min_length=4, max_length=32)
    language: str = "en"

class Onboarding(BaseModel):
    user_id: int
    goal: str = Field(max_length=40)
    study_minutes: int = Field(ge=5, le=120)
    consent: bool

class Issue(BaseModel):
    user_id: int
    category: str = Field(default="problem", max_length=40)
    message: str = Field(min_length=1, max_length=800)
    page: str = Field(default="unknown", max_length=120)

@router.post("/claim")
async def claim(data: Claim, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, data.user_id)
    # Lock while claiming so simultaneous requests cannot consume the same
    # final seat.
    invite = db.query(BetaInvite).filter(BetaInvite.code == data.code.strip().upper(), BetaInvite.active == True).with_for_update().first()
    if not invite or invite.uses >= invite.max_uses:
        raise HTTPException(status_code=422, detail="Invite is invalid or full")
    user = db.query(User).filter(User.telegram_id == data.user_id).first()
    if not user:
        user = User(telegram_id=data.user_id, language_code=data.language if data.language in {"ru","de","en"} else "en")
        db.add(user); db.flush()
    enrollment = db.query(BetaEnrollment).filter(BetaEnrollment.user_id == user.id).first()
    if not enrollment:
        enrollment = BetaEnrollment(user_id=user.id, invite_id=invite.id)
        db.add(enrollment); invite.uses += 1
    db.commit()
    return {"access": True, "onboarding_completed": bool(enrollment.consent and enrollment.goal)}

@router.put("/onboarding")
async def onboarding(data: Onboarding, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, data.user_id)
    if not data.consent: raise HTTPException(status_code=422, detail="Consent is required")
    user = db.query(User).filter(User.telegram_id == data.user_id).first()
    enrollment = db.query(BetaEnrollment).filter(BetaEnrollment.user_id == user.id).first() if user else None
    if not enrollment: raise HTTPException(status_code=403, detail="Beta access required")
    enrollment.goal, enrollment.study_minutes, enrollment.consent = data.goal, data.study_minutes, True
    db.add(ProductEvent(user_id=user.id, event_name="beta_feedback", properties={"message":"Beta onboarding completed","page":"beta_onboarding","language":user.language_code,"goal":data.goal,"study_minutes":data.study_minutes}))
    db.commit(); return {"onboarding_completed": True}

@router.post("/issue")
async def report_issue(data: Issue, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, data.user_id)
    user = db.query(User).filter(User.telegram_id == data.user_id).first()
    if not user: raise HTTPException(status_code=403, detail="Beta access required")
    db.add(ProductEvent(user_id=user.id, event_name="beta_feedback", properties={"kind":"issue","category":data.category,"message":data.message.strip(),"page":data.page,"language":user.language_code,"release":"beta-readiness"}))
    db.commit(); return {"ok": True}
