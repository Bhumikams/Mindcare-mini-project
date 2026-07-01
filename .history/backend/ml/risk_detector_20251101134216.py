class MentalHealthRiskDetector:
    """Detects mental health risks in journal entries"""
    
    def __init__(self):
        self.crisis_keywords = [
            'suicide', 'kill myself', 'end it all', 'no reason to live',
            'better off dead', 'want to die'
        ]
        
        self.high_risk_keywords = [
            'depressed', 'can\'t go on', 'no one cares', 'give up',
            'harm myself', 'hurt myself', 'hopeless', 'worthless'
        ]
        
        self.moderate_risk_keywords = [
            'anxious', 'panic', 'overwhelmed', 'can\'t cope',
            'stressed', 'exhausted', 'lonely', 'isolated'
        ]
    
    def assess_risk(self, text):
        text_lower = text.lower()
        
        if any(keyword in text_lower for keyword in self.crisis_keywords):
            return {
                'risk_level': 'crisis',
                'severity': 5,
                'message': 'Your entry shows signs of crisis. Please reach out immediately.',
                'show_alert': True
            }
        
        high_risk_count = sum(1 for keyword in self.high_risk_keywords if keyword in text_lower)
        if high_risk_count >= 2:
            return {
                'risk_level': 'high',
                'severity': 4,
                'message': 'You may need support. Consider reaching out to someone.',
                'show_alert': True
            }
        
        moderate_risk_count = sum(1 for keyword in self.moderate_risk_keywords if keyword in text_lower)
        if moderate_risk_count >= 3:
            return {
                'risk_level': 'moderate',
                'severity': 3,
                'message': 'Take care of yourself. Self-care is important.',
                'show_alert': False
            }
        
        return {
            'risk_level': 'low',
            'severity': 1,
            'message': 'Keep journaling! You\'re doing great.',
            'show_alert': False
        }
