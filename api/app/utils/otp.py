from app.core.config import settings
from redis import Redis

def store_code(r: Redis, identifier: str, code: str):
    r.setex(f"otp:{identifier}", settings.OTP_TTL_SECONDS, code)

def verify_code(r: Redis, identifier: str, code: str) -> bool:
    val = r.get(f"otp:{identifier}")
    if not val:
        return False
    return val.decode() == code
