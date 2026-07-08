from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from jose import jwt

password_hasher = PasswordHash.recommended()

def get_password_hash(password: str) -> str:
    return password_hasher.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hasher.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: int) -> str:
    to_encode = data.copy() #copy payload data to avoid modifying the original dictionary
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt