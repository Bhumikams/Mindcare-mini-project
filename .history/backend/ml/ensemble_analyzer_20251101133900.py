from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

class EnsembleAnalyzer:
    """3-model ensemble: TextBlob + VADER + Custom Mental Health Lexicon"""
    
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        self.mental_health_keywords = self._load_mental_health_lexicon()
        print("✅ Ensemble Analyzer initialized")
    
    def _load_mental_health_lexicon(self):
        return {
            'positive': {
                'grateful': 0.8, 'blessed': 0.7, 'peaceful': 0.7, 'hopeful': 0.6,
                'motivated': 0.7, 'confident': 0.6, 'relaxed': 0.6, 'energized': 0.7,
                'accomplished': 0.7, 'loved': 0.8, 'supported': 0.7, 'calm': 0.6,
                'inspired': 0.7, 'proud': 0.7, 'optimistic': 0.7, 'joyful': 0.8,
                'happy': 0.7, 'great': 0.6, 'wonderful': 0.7, 'amazing': 0.8,
                'fantastic': 0.7, 'excellent': 0.7, 'good': 0.5
            },
            'negative': {
                'anxious': -0.7, 'depressed': -0.8, 'stressed': -0.7, 'overwhelmed': -0.8,
                'lonely': -0.7, 'hopeless': -0.9, 'worthless': -0.9, 'exhausted': -0.6,
                'frustrated': -0.6, 'worried': -0.6, 'scared': -0.7, 'panicked': -0.8,
                'isolated': -0.7, 'defeated': -0.8, 'helpless': -0.8, 'miserable': -0.8,
                'sad': -0.6, 'terrible': -0.7, 'awful': -0.7, 'bad': -0.5
            }
        }
    
    def analyze_with_textblob(self, text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        return {
            'polarity': polarity,
            'subjectivity': blob.sentiment.subjectivity,
            'sentiment': self._polarity_to_label(polarity),
            'confidence': abs(polarity)
        }
    
    def analyze_with_vader(self, text):
        scores = self.vader.polarity_scores(text)
        compound = scores['compound']
        return {
            'polarity': compound,
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu'],
            'sentiment': self._vader_to_label(compound),
            'confidence': abs(compound)
        }
    
    def analyze_with_mental_health_lexicon(self, text):
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        scores = []
        detected_emotions = []
        
        for word in words:
            if word in self.mental_health_keywords['positive']:
                score = self.mental_health_keywords['positive'][word]
                scores.append(score)
                detected_emotions.append({'word': word, 'type': 'positive', 'score': score})
            elif word in self.mental_health_keywords['negative']:
                score = self.mental_health_keywords['negative'][word]
                scores.append(score)
                detected_emotions.append({'word': word, 'type': 'negative', 'score': abs(score)})
        
        avg_score = sum(scores) / len(scores) if scores else 0
        
        return {
            'polarity': avg_score,
            'detected_keywords': detected_emotions,
            'sentiment': self._polarity_to_label(avg_score),
            'confidence': abs(avg_score) if scores else 0.3
        }
    
    def ensemble_predict(self, text):
        textblob_result = self.analyze_with_textblob(text)
        vader_result = self.analyze_with_vader(text)
        lexicon_result = self.analyze_with_mental_health_lexicon(text)
        
        weights = {'textblob': 0.3, 'vader': 0.3, 'lexicon': 0.4}
        
        weighted_polarity = (
            textblob_result['polarity'] * weights['textblob'] +
            vader_result['polarity'] * weights['vader'] +
            lexicon_result['polarity'] * weights['lexicon']
        )
        
        final_sentiment = self._polarity_to_label(weighted_polarity)
        
        confidences = [
            textblob_result['confidence'],
            vader_result['confidence'],
            lexicon_result['confidence']
        ]
        avg_confidence = sum(confidences) / len(confidences)
        
        emotion = self._detect_emotion(text, weighted_polarity, lexicon_result)
        
        return {
            'sentiment': final_sentiment,
            'confidence': avg_confidence,
            'polarity': weighted_polarity,
            'primary_emotion': emotion['name'],
            'emotion_score': emotion['intensity'],
            'model_breakdown': {
                'textblob': textblob_result,
                'vader': vader_result,
                'mental_health_lexicon': lexicon_result
            },
            'detected_keywords': lexicon_result['detected_keywords']
        }
    
    def _polarity_to_label(self, polarity):
        if polarity > 0.15:
            return "positive"
        elif polarity < -0.15:
            return "negative"
        else:
            return "neutral"
    
    def _vader_to_label(self, compound):
        if compound >= 0.05:
            return "positive"
        elif compound <= -0.05:
            return "negative"
        else:
            return "neutral"
    
    def _detect_emotion(self, text, polarity, lexicon_result):
        text_lower = text.lower()
        
        emotions = {
            'joyful': ['grateful', 'blessed', 'love', 'amazing', 'wonderful', 'fantastic'],
            'anxious': ['anxious', 'worried', 'nervous', 'stress', 'panic'],
            'depressed': ['depressed', 'hopeless', 'worthless', 'sad', 'defeated'],
            'angry': ['angry', 'frustrated', 'furious', 'mad'],
            'peaceful': ['peaceful', 'calm', 'relaxed', 'serene'],
            'hopeful': ['hopeful', 'optimistic', 'inspired', 'motivated'],
            'lonely': ['lonely', 'isolated', 'alone'],
            'excited': ['excited', 'energized', 'thrilled']
        }
        
        detected = []
        for emotion, words in emotions.items():
            if any(word in text_lower for word in words):
                detected.append(emotion)
        
        if detected:
            return {'name': detected[0], 'intensity': abs(polarity)}
        
        if polarity > 0.3:
            return {'name': 'happy', 'intensity': polarity}
        elif polarity < -0.3:
            return {'name': 'sad', 'intensity': abs(polarity)}
        else:
            return {'name': 'calm', 'intensity': 0.5}
