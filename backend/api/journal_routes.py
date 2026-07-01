from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, Journal
from schemas import JournalCreate, JournalResponse
from auth import get_current_user
from datetime import datetime, timedelta
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
    """Get mood trends analysis - Chart.js compatible format"""
    
    # Get entries from last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    entries = db.query(Journal).filter(
        Journal.user_id == current_user.id,
        Journal.created_at >= thirty_days_ago
    ).order_by(Journal.created_at).all()
    
    # Format data for Chart.js
    dates = [entry.created_at.strftime("%b %d") for entry in entries]
    scores = [entry.sentiment_score for entry in entries]
    
    return {
        "dates": dates,
        "scores": scores
    }


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


@router.get("/writing-prompt")
def get_writing_prompt(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate personalized AI writing prompts based on mood history"""
    import random
    
    # Get recent entries to understand user's mood
    recent_entries = db.query(Journal).filter(
        Journal.user_id == current_user.id
    ).order_by(Journal.created_at.desc()).limit(5).all()
    
    if not recent_entries:
        # First-time user prompts
        prompts = [
            "What made you smile today? Describe it in detail.",
            "If you could tell your past self one thing, what would it be?",
            "What are three things you're grateful for right now?",
            "Describe your perfect day from morning to night.",
            "What's a challenge you're currently facing? How do you feel about it?"
        ]
    else:
        # Convert to string explicitly (FIX for type error)
        latest_sentiment = str(recent_entries[0].sentiment)
        latest_emotion = str(recent_entries[0].primary_emotion)
        
        if latest_sentiment == 'negative':
            prompts = [
                "What's one small thing that could make today better?",
                "Write about a time you overcame a similar challenge. What helped you then?",
                "What would you tell a close friend who was feeling the same way?",
                "List 3 things that are still good in your life right now.",
                "What activity usually helps you feel better? Describe why it works."
            ]
        elif latest_sentiment == 'positive':
            prompts = [
                "What contributed most to your positive mood today?",
                "How can you recreate this feeling tomorrow?",
                "Who would you like to share this happiness with and why?",
                "What did you do today that you're proud of?",
                "Describe the moment when you felt most alive today."
            ]
        else:  # neutral
            prompts = [
                "What emotions did you notice in yourself today?",
                "If you could change one thing about today, what would it be?",
                "Describe your energy level today and what influenced it.",
                "What's something you're looking forward to?",
                "What's on your mind right now? Let it flow freely."
            ]
        
        # Add emotion-specific prompts
        emotion_prompts = {
            'happy': ["What made you laugh today?", "Describe a moment of joy in detail."],
            'sad': ["What do you need right now to feel better?", "Write a letter to your sadness."],
            'anxious': ["What's worrying you most? Break it down.", "What can you control right now?"],
            'grateful': ["What are you most thankful for?", "Who made your day better today?"],
            'excited': ["What are you most excited about?", "Describe your ideal future."],
            'angry': ["What triggered this feeling?", "How can you express this healthily?"]
        }
        
        if latest_emotion in emotion_prompts:
            prompts.extend(emotion_prompts[latest_emotion])
    
    selected_prompt = random.choice(prompts)
    
    return {
        "prompt": selected_prompt,
        "category": "personalized" if recent_entries else "getting_started"
    }
