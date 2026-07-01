from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import Optional




class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class JournalCreate(BaseModel):
    content: str


class JournalResponse(BaseModel):
    id: int
    content: str
    sentiment: str
    sentiment_score: float
    primary_emotion: str
    emotion_score: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
