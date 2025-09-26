"""
Sentiment analysis implementation using VADER and TextBlob.

This module provides sentiment analysis functionality for financial text data.
"""

from typing import Dict, List, Tuple
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob


class SentimentAnalyzer:
    """
    Sentiment analyzer for financial text using multiple models.
    
    Supports VADER (optimized for social media) and TextBlob
    for comprehensive sentiment analysis.
    """
    
    def __init__(self):
        """Initialize sentiment analyzer with models."""
        self.vader = SentimentIntensityAnalyzer()
        
    def analyze_text(self, text: str, model: str = "vader") -> Dict:
        """
        Analyze sentiment of given text.
        
        Args:
            text: Text to analyze
            model: Model to use ("vader" or "textblob")
            
        Returns:
            Dictionary with sentiment scores and metadata
        """
        start_time = time.time()
        
        if model == "vader":
            result = self._analyze_vader(text)
        elif model == "textblob":
            result = self._analyze_textblob(text)
        else:
            raise ValueError(f"Unknown model: {model}")
        
        # Add metadata
        result.update({
            "model_name": model,
            "text_length": len(text),
            "word_count": len(text.split()),
            "processing_time_ms": round((time.time() - start_time) * 1000, 2)
        })
        
        return result
    
    def _analyze_vader(self, text: str) -> Dict:
        """Analyze text using VADER sentiment analyzer."""
        scores = self.vader.polarity_scores(text)
        
        # Determine sentiment label
        compound = scores['compound']
        if compound >= 0.05:
            label = "positive"
        elif compound <= -0.05:
            label = "negative"
        else:
            label = "neutral"
            
        return {
            "compound_score": compound,
            "positive_score": scores['pos'],
            "negative_score": scores['neg'],
            "neutral_score": scores['neu'],
            "sentiment_label": label,
            "confidence": max(scores['pos'], scores['neg'], scores['neu'])
        }
    
    def _analyze_textblob(self, text: str) -> Dict:
        """Analyze text using TextBlob sentiment analyzer."""
        blob = TextBlob(text)
        
        polarity = blob.sentiment.polarity  # -1 to 1
        subjectivity = blob.sentiment.subjectivity  # 0 to 1
        
        # Convert to VADER-like format
        if polarity > 0:
            pos_score = polarity
            neg_score = 0
        else:
            pos_score = 0
            neg_score = abs(polarity)
        
        neu_score = 1 - abs(polarity)
        
        # Normalize scores
        total = pos_score + neg_score + neu_score
        if total > 0:
            pos_score /= total
            neg_score /= total
            neu_score /= total
        
        # Determine label
        if polarity >= 0.1:
            label = "positive"
        elif polarity <= -0.1:
            label = "negative"
        else:
            label = "neutral"
            
        return {
            "compound_score": polarity,
            "positive_score": pos_score,
            "negative_score": neg_score,
            "neutral_score": neu_score,
            "sentiment_label": label,
            "confidence": abs(polarity),
            "subjectivity": subjectivity
        }