from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from api import auth_routes, journal_routes
from ml.sentiment_analyzer import SentimentAnalyzer

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MindCare API",
    description="AI-powered mental wellness journal with sentiment analysis",
    version="1.0.0"
)

# CORS middleware for React frontend
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
        "message": "Welcome to MindCare API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
@app.on_event("startup")
def load_ml_models():
    app.state.sentiment_analyzer = SentimentAnalyzer()
    print("🧠 ML Models loaded successfully!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
