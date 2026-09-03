# backend/app/api/endpoints/referral.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/referral", tags=["referral"])

@router.post("/create")
async def create_referral(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.telegram_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    referral_link = f"https://t.me/DeutschIQ_bot?start=ref_{user_id}"
    return {"link": referral_link}

@router.post("/claim")
async def claim_referral(referrer_id: int, referee_id: int, db: Session = Depends(get_db)):
    referrer = db.query(User).filter(User.telegram_id == referrer_id).first()
    if not referrer:
        raise HTTPException(status_code=404, detail="Referrer not found")
    
    from app.models.diagnostic import DiagnosticResult
    referee_test = db.query(DiagnosticResult).filter(
        DiagnosticResult.user_id == referee_id
    ).first()
    if not referee_test:
        raise HTTPException(status_code=400, detail="Referee hasn't completed test")
    
    if referrer.subscription_status == 'pro':
        referrer.subscription_end_date = (referrer.subscription_end_date or datetime.now()) + timedelta(days=3)
    else:
        referrer.subscription_status = 'pro'
        referrer.subscription_end_date = datetime.now() + timedelta(days=3)
    
    db.commit()
    return {"status": "bonus_added", "bonus_days": 3}

