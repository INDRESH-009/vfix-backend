from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from app.core.config import settings

ALGO = "HS256"

def create_access_token(sub: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(days=7))
    to_encode = {"sub": sub, "exp": expire}
    return jwt.encode(to_encode, settings.APP_SECRET, algorithm=ALGO)
