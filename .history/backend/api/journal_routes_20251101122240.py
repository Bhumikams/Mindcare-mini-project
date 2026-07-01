from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Journal, User
from schemas import JournalCreate, JournalResponse
from auth import get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/entries", response_model=JournalResponse, status_code=status.HTTP_201_CREATED)
def create_journal_entry(
    entry: JournalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new journal entry with basic sentiment analysis"""
    
    # Simple sentiment analysis (we'll replace this with ML model later)
    content_lower = entry.content.lower()
    
    # Basic keyword-based sentiment
    positive_words = ['happy', 'great', 'good', 'wonderful', 'excellent', 'amazing', 'love', 'joy']
    negative_words = ['sad', 'bad', 'terrible', 'awful', 'hate', 'angry', 'depressed', 'anxious']
    
    pos_count = sum(1 for word in positive_words if word in content_lower)
    neg_count = sum(1 for word in negative_words if word in content_lower)
    
    if pos_count > neg_count:
        sentiment = "positive"
        sentiment_score = 0.7 + (pos_count * 0.05)
        primary_emotion = "happy"
    elif neg_count > pos_count:
        sentiment = "negative"
        sentiment_score = 0.7 + (neg_count * 0.05)
        primary_emotion = "sad" if 'sad' in content_lower else "anxious"
    else:
        sentiment = "neutral"
        sentiment_score = 0.5
        primary_emotion = "calm"
    
    sentiment_score = min(sentiment_score, 0.99)  # Cap at 0.99
    
    # Create journal entry
    journal = Journal(
        user_id=current_user.id,
        content=entry.content,
        sentiment=sentiment,
        sentiment_score=sentiment_score,
        primary_emotion=primary_emotion,
        emotion_score=sentiment_score,
        created_at=datetime.utcnow()
    )
    
    db.add(journal)
    db.commit()
    db.refresh(journal)
    
    return journal

@router.get("/entries", response_model=List[JournalResponse])
def get_journal_entries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = 20
):
    """Get user's journal entries"""
    entries = db.query(Journal)\
        .filter(Journal.user_id == current_user.id)\
        .order_by(Journal.created_at.desc())\
        .limit(limit)\
        .all()
    return entries

@router.get("/entries/{entry_id}", response_model=JournalResponse)
def get_journal_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific journal entry"""
    entry = db.query(Journal)\
        .filter(Journal.id == entry_id, Journal.user_id == current_user.id)\
        .first()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Journal entry not found"
        )
    
    return entry

@router.delete("/entries/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_journal_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete journal entry"""
    entry = db.query(Journal)\
        .filter(Journal.id == entry_id, Journal.user_id == current_user.id)\
        .first()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Journal entry not found"
        )
    
    db.delete(entry)
    db.commit()
    
    return None
