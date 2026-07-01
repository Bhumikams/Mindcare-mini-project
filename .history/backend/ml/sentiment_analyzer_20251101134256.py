from ml.ensemble_analyzer import EnsembleAnalyzer
from ml.risk_detector import MentalHealthRiskDetector
from ml.trend_analyzer import MoodTrendAnalyzer

class SentimentAnalyzer:
    """Main ML System with 3 unique features"""
    
    def __init__(self):
        self.ensemble = EnsembleAnalyzer()
        self.risk_detector = MentalHealthRiskDetector()
        self.trend_analyzer = MoodTrendAnalyzer()
        print("✅ Advanced ML System initialized!")
    
    def analyze_sentiment(self, text):
        sentiment_result = self.ensemble.ensemble_predict(text)
        risk_assessment = self.risk_detector.assess_risk(text)
        
        return {
            **sentiment_result,
            'risk_assessment': risk_assessment
        }
    
    def analyze_trends(self, entries):
        return self.trend_analyzer.analyze_trends(entries)
