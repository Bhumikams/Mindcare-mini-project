from ml.ensemble_analyzer import EnsembleAnalyzer
from ml.risk_detector import MentalHealthRiskDetector
from ml.trend_analyzer import MoodTrendAnalyzer
from ml.activity_recommender import ActivityRecommender
from typing import Dict, Any

class SentimentAnalyzer:
    """
    Main ML System - Combines 4 unique ML features:
    1. Ensemble model (3 different algorithms)
    2. Mental health risk detection
    3. Mood trend analysis
    4. AI-powered activity recommendations
    """
    
    def __init__(self):
        """Initialize all ML components"""
        print("🔧 Initializing ML components...")
        
        self.ensemble = EnsembleAnalyzer()
        self.risk_detector = MentalHealthRiskDetector()
        self.trend_analyzer = MoodTrendAnalyzer()
        self.activity_recommender = ActivityRecommender()
        
        print("✅ Advanced ML System with Activity Recommendations initialized!")
        print("📊 Features: Ensemble Analysis, Risk Detection, Trend Analysis, Activity Recommendations")
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Full ML analysis with ensemble + risk detection + activity recommendations
        
        Args:
            text: Journal entry text to analyze
            
        Returns:
            Dictionary containing sentiment, emotions, risk, and recommended activities
        """
        # Get ensemble prediction from 3 models
        sentiment_result = self.ensemble.ensemble_predict(text)
        
        # Detect mental health risks
        risk_assessment = self.risk_detector.assess_risk(text)
        
        # Get personalized activity recommendations
        activities = self.activity_recommender.get_activity_with_context(
            emotion=sentiment_result['primary_emotion'],
            sentiment=sentiment_result['sentiment'],
            risk_level=risk_assessment['risk_level']
        )
        
        # Combine all results
        return {
            # Sentiment analysis results
            'sentiment': sentiment_result['sentiment'],
            'confidence': sentiment_result['confidence'],
            'polarity': sentiment_result['polarity'],
            'primary_emotion': sentiment_result['primary_emotion'],
            'emotion_score': sentiment_result['emotion_score'],
            
            # Model breakdown (for transparency)
            'model_breakdown': sentiment_result['model_breakdown'],
            'detected_keywords': sentiment_result['detected_keywords'],
            
            # Risk assessment
            'risk_assessment': risk_assessment,
            
            # Activity recommendations (NEW!)
            'recommended_activities': activities
        }
    
    def analyze_trends(self, entries) -> Dict[str, Any]:
        """
        Analyze mood trends over time from multiple journal entries
        
        Args:
            entries: List of journal entries with sentiment data
            
        Returns:
            Dictionary containing trend analysis and statistics
        """
        return self.trend_analyzer.analyze_trends(entries)
    
    def get_quick_recommendations(self, emotion: str, sentiment: str, num: int = 3):
        """
        Quick method to get activity recommendations without full analysis
        
        Args:
            emotion: Detected emotion
            sentiment: Sentiment (positive/negative/neutral)
            num: Number of recommendations to return
            
        Returns:
            List of activity recommendations
        """
        return self.activity_recommender.recommend_activities(emotion, sentiment, num)
