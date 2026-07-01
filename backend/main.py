from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from api import auth_routes, journal_routes
from ml.sentiment_analyzer import SentimentAnalyzer

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MindCare API - Advanced ML Mental Wellness",
    description="AI-powered journal with ML sentiment analysis and activity recommendations",
    version="2.0.0"
)

@app.on_event("startup")
def load_ml_models():
    """Load ML models when server starts"""
    app.state.sentiment_analyzer = SentimentAnalyzer()
    print("🧠 ML Models loaded successfully!")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(journal_routes.router, prefix="/api/journal", tags=["Journal"])

@app.get("/")
def root():
    return {
        "message": "Welcome to MindCare API - ML Mental Wellness Journal",
        "version": "2.0.0",
        "ml_features": [
            "3-Model Ensemble (TextBlob + VADER + Custom Lexicon)",
            "Mental Health Risk Detection",
            "Mood Trend Analysis",
            "AI Activity Recommendations"
        ],
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "ml_ready": hasattr(app.state, 'sentiment_analyzer')
    }
