import statistics
from datetime import datetime

class MoodTrendAnalyzer:
    """Analyzes mood trends over time"""
    
    def analyze_trends(self, entries):
        if not entries or len(entries) < 3:
            return {
                'trend': 'insufficient_data',
                'message': 'Keep journaling to see your mood trends!',
                'has_data': False
            }
        
        scores = [(e.created_at, self._sentiment_to_score(e.sentiment), e.sentiment_score) 
                  for e in entries]
        scores.sort(key=lambda x: x[0])
        
        recent_scores = [s[1] * s[2] for s in scores[-7:]]
        older_scores = [s[1] * s[2] for s in scores[:7]] if len(scores) > 7 else recent_scores
        
        recent_avg = statistics.mean(recent_scores)
        older_avg = statistics.mean(older_scores)
        
        if recent_avg > older_avg + 0.2:
            trend = 'improving'
            message = '📈 Your mood has been improving! Keep it up!'
            trend_emoji = '📈'
        elif recent_avg < older_avg - 0.2:
            trend = 'declining'
            message = '📉 Consider reaching out for support if needed.'
            trend_emoji = '📉'
        else:
            trend = 'stable'
            message = '➡️ Your mood has been relatively stable.'
            trend_emoji = '➡️'
        
        all_scores = [s[1] * s[2] for s in scores]
        
        return {
            'trend': trend,
            'trend_emoji': trend_emoji,
            'message': message,
            'has_data': True,
            'statistics': {
                'average_mood': round(statistics.mean(all_scores), 2),
                'recent_average': round(recent_avg, 2),
                'positive_entries': sum(1 for s in scores if s[1] > 0),
                'negative_entries': sum(1 for s in scores if s[1] < 0),
                'neutral_entries': sum(1 for s in scores if s[1] == 0),
                'total_entries': len(entries)
            }
        }
    
    def _sentiment_to_score(self, sentiment):
        mapping = {'positive': 1, 'neutral': 0, 'negative': -1}
        return mapping.get(sentiment, 0)
