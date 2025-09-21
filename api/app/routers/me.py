from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.db import get_db
from app.models.models import User

router = APIRouter()

def get_current_user(authorization: str | None = Header(None), db: Session = Depends(get_db)) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, settings.APP_SECRET, algorithms=["HS256"])
        sub = payload.get("sub")
        if not sub:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.get(User, sub)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

class MeUpdate(BaseModel):
    name: str | None = None
    language: str | None = None
    consent_json: dict | None = None

@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return {
        "id": str(user.id),
        "name": user.name,
        "phone": user.phone,
        "email": user.email,
        "language": user.language,
        "consent_json": user.consent_json or {},
    }

@router.put("/me")
def update_me(payload: MeUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if payload.name is not None: user.name = payload.name
    if payload.language is not None: user.language = payload.language
    if payload.consent_json is not None: user.consent_json = payload.consent_json
    db.add(user); db.commit(); db.refresh(user)
    return {"ok": True}
