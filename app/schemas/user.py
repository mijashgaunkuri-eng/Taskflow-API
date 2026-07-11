from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"        

class UpdateUser(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    full_name: str | None = None
    password: str | None = None    