from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, Journal
from schemas import JournalCreate, JournalResponse
from auth import get_current_user
from datetime import datetime
from typing import List

router = APIRouter()

@router.post("/entries", response_model=JournalResponse, status_code=status.HTTP_201_CREATED)
def create_journal_entry(
    entry: JournalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new journal entry with ML-powered sentiment analysis"""
    
    # Get ML sentiment analyzer from app state
    from main import app
    analyzer = app.state.sentiment_analyzer
    
    # Perform ML analysis
    analysis = analyzer.analyze_sentiment(entry.content)
    
    # Create journal entry with ML predictions
    journal = Journal(
        user_id=current_user.id,
        content=entry.content,
        sentiment=analysis['sentiment'],
        sentiment_score=analysis['confidence'],
        primary_emotion=analysis['primary_emotion'],
        emotion_score=analysis['emotion_score'],
        created_at=datetime.utcnow()
    )
    
    db.add(journal)
    db.commit()
    db.refresh(journal)
    
    return journal

@router.get("/entries", response_model=List[JournalResponse])
def get_journal_entries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all journal entries for current user"""
    entries = db.query(Journal).filter(
        Journal.user_id == current_user.id
    ).order_by(Journal.created_at.desc()).all()
    return entries

@router.get("/trends")
def get_mood_trends(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get mood trends analysis"""
    from main import app
    analyzer = app.state.sentiment_analyzer
    
    entries = db.query(Journal).filter(
        Journal.user_id == current_user.id
    ).order_by(Journal.created_at.desc()).all()
    
    trends = analyzer.analyze_trends(entries)
    return trends

@router.get("/activities/{entry_id}")
def get_activity_recommendations(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get activity recommendations for a specific journal entry"""
    from main import app
    analyzer = app.state.sentiment_analyzer
    
    # Get the journal entry
    entry = db.query(Journal).filter(
        Journal.id == entry_id,
        Journal.user_id == current_user.id
    ).first()
    
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    # Get activity recommendations
    activities = analyzer.activity_recommender.get_activity_with_context(
        emotion=entry.primary_emotion,
        sentiment=entry.sentiment,
        risk_level='low'  # You can enhance this by storing risk level in DB
    )
    
    return activities

@router.get("/entries/{entry_id}", response_model=JournalResponse)
def get_journal_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific journal entry"""
    entry = db.query(Journal).filter(
        Journal.id == entry_id,
        Journal.user_id == current_user.id
    ).first()
    
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
    entry = db.query(Journal).filter(
        Journal.id == entry_id,
        Journal.user_id == current_user.id
    ).first()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Journal entry not found"
        )
    
    db.delete(entry)
    db.commit()
    
    return None
