from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    journals = relationship("Journal", back_populates="owner")

class Journal(Base):
    __tablename__ = "journals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    sentiment = Column(String)  # positive, negative, neutral
    sentiment_score = Column(Float)
    primary_emotion = Column(String)  # happy, sad, anxious, angry, calm
    emotion_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="journals")
