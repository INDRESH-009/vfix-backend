from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from redis import Redis
import redis as redislib
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.db import get_db
from app.models.models import User
from app.core.security import create_access_token
from app.utils.otp import store_code, verify_code

router = APIRouter()

def get_redis() -> Redis:
    return redislib.Redis.from_url(settings.REDIS_URL)

class OTPStartIn(BaseModel):
    identifier: str  # phone or email

class OTPVerifyIn(BaseModel):
    identifier: str
    code: str

@router.post("/otp/start")
def otp_start(payload: OTPStartIn, r: Redis = Depends(get_redis)):
    store_code(r, payload.identifier, settings.OTP_CODE_DEV)  # send stub
    return {"ok": True, "message": "OTP sent (dev stub)."}

@router.post("/otp/verify")
def otp_verify(payload: OTPVerifyIn, r: Redis = Depends(get_redis), db: Session = Depends(get_db)):
    if not verify_code(r, payload.identifier, payload.code):
        raise HTTPException(status_code=400, detail="Invalid or expired code")
    user = db.query(User).filter(
        (User.phone == payload.identifier) | (User.email == payload.identifier)
    ).first()
    if not user:
        user = User(
            phone=payload.identifier if payload.identifier.startswith("+") else None,
            email=None if payload.identifier.startswith("+") else payload.identifier
        )
        db.add(user); db.commit(); db.refresh(user)
    token = create_access_token(str(user.id))
    return {"access_token": token, "token_type": "bearer"}
