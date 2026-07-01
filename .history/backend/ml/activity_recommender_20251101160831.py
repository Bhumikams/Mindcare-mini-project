from typing import Dict, List, Any
import random

class ActivityRecommender:
    """
    AI-powered activity recommendation system
    Suggests personalized activities based on detected mood and emotion
    """
    
    def __init__(self):
        self.activity_database = self._build_activity_database()
        print("✅ Activity Recommender initialized")
    
    def _build_activity_database(self) -> Dict[str, List[Dict[str, str]]]:
        """Comprehensive activity database mapped to emotions"""
        return {
            # Positive emotions
            'happy': [
                {'activity': 'Share your happiness', 'description': 'Call a friend or family member and share your joy', 'icon': '📞'},
                {'activity': 'Celebrate yourself', 'description': 'Treat yourself to something you enjoy', 'icon': '🎉'},
                {'activity': 'Express gratitude', 'description': 'Write down 3 things you\'re grateful for', 'icon': '🙏'},
                {'activity': 'Creative expression', 'description': 'Draw, paint, or create something', 'icon': '🎨'},
                {'activity': 'Physical activity', 'description': 'Go for a joyful walk or dance', 'icon': '💃'}
            ],
            'joyful': [
                {'activity': 'Spread positivity', 'description': 'Do something kind for someone else', 'icon': '💝'},
                {'activity': 'Capture the moment', 'description': 'Take photos or journal about what makes you joyful', 'icon': '📸'},
                {'activity': 'Social connection', 'description': 'Spend time with loved ones', 'icon': '👨‍👩‍👧‍👦'},
                {'activity': 'Outdoor time', 'description': 'Enjoy nature - park, garden, or outdoor space', 'icon': '🌳'},
                {'activity': 'Try something new', 'description': 'Learn a new skill or hobby', 'icon': '✨'}
            ],
            'grateful': [
                {'activity': 'Gratitude journal', 'description': 'Write detailed gratitude entries', 'icon': '📔'},
                {'activity': 'Thank someone', 'description': 'Express appreciation to someone who helped you', 'icon': '💌'},
                {'activity': 'Meditation', 'description': 'Practice gratitude meditation', 'icon': '🧘'},
                {'activity': 'Pay it forward', 'description': 'Help someone or volunteer', 'icon': '🤝'},
                {'activity': 'Reflect', 'description': 'Think about your journey and growth', 'icon': '🌟'}
            ],
            
            # Negative emotions
            'anxious': [
                {'activity': 'Deep breathing', 'description': '4-7-8 breathing: Inhale 4s, hold 7s, exhale 8s', 'icon': '🌬️'},
                {'activity': 'Grounding exercise', 'description': '5-4-3-2-1: Name 5 things you see, 4 you touch, 3 you hear, 2 you smell, 1 you taste', 'icon': '🧭'},
                {'activity': 'Physical release', 'description': 'Go for a walk or do light exercise', 'icon': '🚶'},
                {'activity': 'Progressive relaxation', 'description': 'Tense and relax each muscle group', 'icon': '💆'},
                {'activity': 'Limit stimulants', 'description': 'Reduce caffeine, take a break from screens', 'icon': '☕'},
                {'activity': 'Talk it out', 'description': 'Share your worries with a trusted person', 'icon': '💬'}
            ],
            'stressed': [
                {'activity': 'Take a break', 'description': 'Step away from stressors for 10-15 minutes', 'icon': '⏸️'},
                {'activity': 'Organize', 'description': 'Make a to-do list and prioritize tasks', 'icon': '📝'},
                {'activity': 'Physical activity', 'description': 'Exercise to release tension', 'icon': '🏃'},
                {'activity': 'Music therapy', 'description': 'Listen to calming or uplifting music', 'icon': '🎵'},
                {'activity': 'Self-care', 'description': 'Take a warm bath or practice skincare', 'icon': '🛁'},
                {'activity': 'Stretching', 'description': 'Do gentle yoga or stretches', 'icon': '🧘‍♀️'}
            ],
            'sad': [
                {'activity': 'Allow yourself to feel', 'description': 'It\'s okay to cry and process emotions', 'icon': '💙'},
                {'activity': 'Comfort activities', 'description': 'Watch a comfort show or read a favorite book', 'icon': '📺'},
                {'activity': 'Reach out', 'description': 'Connect with someone who makes you feel safe', 'icon': '🤗'},
                {'activity': 'Gentle movement', 'description': 'Take a slow walk in nature', 'icon': '🌿'},
                {'activity': 'Creative outlet', 'description': 'Write, draw, or express your feelings', 'icon': '✍️'},
                {'activity': 'Self-compassion', 'description': 'Be kind to yourself, practice self-love', 'icon': '❤️'}
            ],
            'depressed': [
                {'activity': 'Small wins', 'description': 'Do one small task - make your bed, shower, get dressed', 'icon': '✅'},
                {'activity': 'Sunlight', 'description': 'Spend 10 minutes in sunlight or by a window', 'icon': '☀️'},
                {'activity': 'Reach for help', 'description': 'Contact a mental health professional or helpline', 'icon': '🆘'},
                {'activity': 'Routine', 'description': 'Stick to a simple daily routine', 'icon': '📅'},
                {'activity': 'Social support', 'description': 'Ask someone to sit with you or check in', 'icon': '👥'},
                {'activity': 'Gentle activity', 'description': 'Do light stretches or a 5-minute walk', 'icon': '🚶‍♀️'}
            ],
            'lonely': [
                {'activity': 'Connect online', 'description': 'Video call a friend or join an online community', 'icon': '💻'},
                {'activity': 'Go to public spaces', 'description': 'Work from a cafe or visit a library', 'icon': '☕'},
                {'activity': 'Volunteer', 'description': 'Help others and build connections', 'icon': '🤲'},
                {'activity': 'Join a group', 'description': 'Find local clubs or meetups for your interests', 'icon': '👫'},
                {'activity': 'Self-companionship', 'description': 'Practice enjoying your own company', 'icon': '🪞'},
                {'activity': 'Pet therapy', 'description': 'Spend time with animals if possible', 'icon': '🐕'}
            ],
            'angry': [
                {'activity': 'Physical release', 'description': 'Punch a pillow, run, or do intense exercise', 'icon': '🥊'},
                {'activity': 'Cooling off', 'description': 'Take a timeout before responding', 'icon': '❄️'},
                {'activity': 'Express safely', 'description': 'Write an angry letter you won\'t send', 'icon': '✉️'},
                {'activity': 'Problem-solve', 'description': 'Identify what you can control and address it', 'icon': '🧩'},
                {'activity': 'Breathe', 'description': 'Practice anger management breathing techniques', 'icon': '🌬️'},
                {'activity': 'Creative destruction', 'description': 'Tear paper, squeeze stress ball', 'icon': '💢'}
            ],
            
            # Neutral emotions
            'calm': [
                {'activity': 'Maintain balance', 'description': 'Continue your healthy routines', 'icon': '⚖️'},
                {'activity': 'Mindfulness', 'description': 'Practice present-moment awareness', 'icon': '🧘'},
                {'activity': 'Plan ahead', 'description': 'Set goals and organize your week', 'icon': '📋'},
                {'activity': 'Learn something', 'description': 'Read or take an online course', 'icon': '📚'},
                {'activity': 'Creative hobby', 'description': 'Work on a personal project', 'icon': '🎨'}
            ],
            'neutral': [
                {'activity': 'Explore your mood', 'description': 'Journal more to understand how you\'re feeling', 'icon': '📖'},
                {'activity': 'Try new things', 'description': 'Experiment with activities to spark joy', 'icon': '🎯'},
                {'activity': 'Connect with others', 'description': 'Reach out to friends for social time', 'icon': '👋'},
                {'activity': 'Physical activity', 'description': 'Exercise can boost your mood', 'icon': '🏋️'},
                {'activity': 'Healthy habits', 'description': 'Focus on sleep, nutrition, hydration', 'icon': '💪'}
            ],
            
            # Additional specific emotions
            'hopeful': [
                {'activity': 'Set goals', 'description': 'Write down your hopes and create action plans', 'icon': '🎯'},
                {'activity': 'Vision board', 'description': 'Create a visual representation of your dreams', 'icon': '🖼️'},
                {'activity': 'Take action', 'description': 'Make one small step toward your goals', 'icon': '👣'},
                {'activity': 'Share your hopes', 'description': 'Tell someone about your positive outlook', 'icon': '💬'},
                {'activity': 'Inspire others', 'description': 'Share motivational content or support someone', 'icon': '✨'}
            ],
            'excited': [
                {'activity': 'Channel the energy', 'description': 'Start that project you\'ve been thinking about', 'icon': '🚀'},
                {'activity': 'Share excitement', 'description': 'Tell others about what excites you', 'icon': '🎉'},
                {'activity': 'Document it', 'description': 'Capture this moment in photos or writing', 'icon': '📸'},
                {'activity': 'Physical expression', 'description': 'Dance, jump, or move to express your energy', 'icon': '💃'},
                {'activity': 'Plan ahead', 'description': 'Make plans for what you\'re excited about', 'icon': '📅'}
            ]
        }
    
    def recommend_activities(self, emotion: str, sentiment: str, num_recommendations: int = 3) -> List[Dict[str, str]]:
        """
        Get personalized activity recommendations based on emotion
        
        Args:
            emotion: Primary detected emotion (e.g., 'anxious', 'happy')
            sentiment: Overall sentiment (positive/negative/neutral)
            num_recommendations: Number of activities to recommend
        
        Returns:
            List of recommended activities with descriptions
        """
        emotion_lower = emotion.lower()
        
        # Get activities for specific emotion
        if emotion_lower in self.activity_database:
            activities = self.activity_database[emotion_lower].copy()
        # Fallback to sentiment-based recommendations
        elif sentiment == 'positive':
            activities = self.activity_database['happy'].copy()
        elif sentiment == 'negative':
            activities = self.activity_database['sad'].copy()
        else:
            activities = self.activity_database['neutral'].copy()
        
        # Randomize and select recommendations
        random.shuffle(activities)
        recommendations = activities[:num_recommendations]
        
        return recommendations
    
    def get_activity_with_context(self, emotion: str, sentiment: str, risk_level: str = 'low') -> Dict[str, Any]:
        """
        Get activities with contextual message based on risk level
        """
        recommendations = self.recommend_activities(emotion, sentiment, num_recommendations=3)
        
        # Contextual message based on risk
        if risk_level == 'crisis' or risk_level == 'high':
            message = "⚠️ Please prioritize your safety. Consider these activities while seeking professional support."
            urgent = True
        elif risk_level == 'moderate':
            message = f"Based on your {emotion} feeling, here are some helpful activities:"
            urgent = False
        else:
            message = f"Great! Here are some activities to enhance your {emotion} mood:"
            urgent = False
        
        return {
            'message': message,
            'urgent': urgent,
            'recommendations': recommendations,
            'emotion': emotion,
            'additional_tip': self._get_general_tip(sentiment)
        }
    
    def _get_general_tip(self, sentiment: str) -> str:
        """Get a general wellness tip based on sentiment"""
        tips = {
            'positive': "💡 Keep up the good work! Consistency in self-care maintains positive mental health.",
            'negative': "💡 Remember: It's okay to not be okay. Reach out for support when needed.",
            'neutral': "💡 Regular journaling helps you understand your emotional patterns better."
        }
        return tips.get(sentiment, tips['neutral'])
