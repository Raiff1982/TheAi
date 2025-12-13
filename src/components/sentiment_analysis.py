"""
This module provides enhanced sentiment analysis capabilities.
"""

from typing import Dict, Any

try:
    from transformers import pipeline
except Exception:
    pipeline = None

class EnhancedSentimentAnalyzer:
    """Advanced sentiment analysis with additional techniques"""
    def __init__(self):
        if pipeline is not None:
            try:
                self.sentiment_pipeline = pipeline('sentiment-analysis')
            except Exception:
                self.sentiment_pipeline = None
        else:
            self.sentiment_pipeline = None

    def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment with advanced techniques"""
        if self.sentiment_pipeline is None:
            # Fallback simple heuristic
            score = 0.5
            label = 'NEUTRAL'
            if any(w in text.lower() for w in ['good', 'great', 'excellent', 'happy']):
                score = 0.9
                label = 'POSITIVE'
            elif any(w in text.lower() for w in ['bad', 'sad', 'terrible', 'awful']):
                score = 0.1
                label = 'NEGATIVE'
            return {'label': label, 'score': score}
        analysis = self.sentiment_pipeline(text)
        return analysis[0]

    def detailed_analysis(self, text: str) -> Dict[str, Any]:
        """Provide a more detailed sentiment analysis"""
        if self.sentiment_pipeline is None:
            base = self.analyze(text)
            scores = base
        else:
            scores = self.sentiment_pipeline(text)[0]
        if scores['label'] == 'POSITIVE':
            sentiment = "Positive"
        elif scores['label'] == 'NEGATIVE':
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        return {
            "scores": scores,
            "sentiment": sentiment
        }