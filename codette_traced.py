"""
Traced version of Codette class with OpenTelemetry instrumentation
Enables visualization of agent decision-making and multi-perspective reasoning
"""
import logging
import nltk
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import List, Dict, Any, Optional
from nltk.tokenize import word_tokenize
import os
import json
from datetime import datetime
import hashlib

# Import original Codette
from codette_new import Codette as BaseCodette

# Import tracing utilities
try:
    from src.utils.tracing_config import get_tracer, trace_perspective_generation
    from opentelemetry import trace
    from opentelemetry.trace import Status, StatusCode
    TRACING_AVAILABLE = True
except ImportError:
    TRACING_AVAILABLE = False
    get_tracer = None
    trace_perspective_generation = None

logger = logging.getLogger(__name__)


class TracedCodette(BaseCodette):
    """
    Codette with OpenTelemetry tracing for agent visualization
    
    Extends the base Codette class with distributed tracing to visualize:
    - Multi-perspective reasoning flows
    - Quantum spiderweb thought propagation
    - Memory operations and cocoon state changes
    - Response generation pipeline
    """
    
    def __init__(self, user_name="User", enable_tracing=True):
        """
        Initialize TracedCodette with optional tracing
        
        Args:
            user_name: Name of the user interacting with Codette
            enable_tracing: Enable OpenTelemetry tracing (default: True)
        """
        super().__init__(user_name)
        self.enable_tracing = enable_tracing and TRACING_AVAILABLE
        
        if self.enable_tracing:
            self.tracer = get_tracer()
            logger.info("✓ Tracing enabled for Codette instance")
        else:
            self.tracer = None
            if not TRACING_AVAILABLE:
                logger.debug("Tracing not available - install OpenTelemetry packages")
    
    def respond(self, prompt: str) -> str:
        """
        Generate traced response to user prompt
        
        Args:
            prompt: User input query
            
        Returns:
            Generated response with perspective synthesis
        """
        if not self.enable_tracing or self.tracer is None:
            # Fallback to base implementation
            return super().respond(prompt)
        
        # Create root span for the entire response generation
        with self.tracer.start_as_current_span(
            "codette.respond",
            attributes={
                "user.name": self.user_name,
                "prompt.length": len(prompt),
                "prompt.preview": prompt[:100],
            }
        ) as span:
            try:
                # Trace sentiment analysis
                sentiment = self._traced_sentiment_analysis(prompt)
                span.set_attribute("sentiment.compound", sentiment.get('compound', 0))
                span.set_attribute("sentiment.label", 
                    'positive' if sentiment.get('compound', 0) > 0.05 
                    else 'negative' if sentiment.get('compound', 0) < -0.05 
                    else 'neutral')
                
                # Trace key concept extraction
                concepts = self._traced_extract_concepts(prompt)
                span.set_attribute("concepts.count", len(concepts))
                span.set_attribute("concepts.list", ", ".join(concepts[:5]))
                
                # Trace perspective selection
                active_perspectives = self._traced_select_perspectives(prompt, concepts)
                span.set_attribute("perspectives.count", len(active_perspectives))
                span.set_attribute("perspectives.active", ", ".join(active_perspectives))
                
                # Generate response using base class logic
                response = super().respond(prompt)
                
                # Record response metadata
                span.set_attribute("response.length", len(response))
                span.set_attribute("response.success", True)
                span.set_status(Status(StatusCode.OK))
                
                return response
                
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                logger.error(f"Error in traced respond: {e}")
                raise
    
    def _traced_sentiment_analysis(self, text: str) -> Dict[str, float]:
        """Trace sentiment analysis operation"""
        with self.tracer.start_as_current_span(
            "codette.sentiment_analysis",
            attributes={"component": "sentiment_analyzer"}
        ) as span:
            sentiment = self.analyzer.polarity_scores(text)
            span.set_attribute("sentiment.positive", sentiment['pos'])
            span.set_attribute("sentiment.negative", sentiment['neg'])
            span.set_attribute("sentiment.neutral", sentiment['neu'])
            span.set_attribute("sentiment.compound", sentiment['compound'])
            return sentiment
    
    def _traced_extract_concepts(self, text: str) -> List[str]:
        """Trace concept extraction operation"""
        with self.tracer.start_as_current_span(
            "codette.extract_concepts",
            attributes={"component": "concept_extractor"}
        ) as span:
            try:
                tokens = word_tokenize(text.lower())
                keywords = [word for word in tokens if len(word) > 4 and word.isalnum()]
                span.set_attribute("tokens.count", len(tokens))
                span.set_attribute("keywords.count", len(keywords))
                return keywords[:10]
            except Exception as e:
                span.record_exception(e)
                return []
    
    def _traced_select_perspectives(self, prompt: str, concepts: List[str]) -> List[str]:
        """Trace perspective selection logic"""
        with self.tracer.start_as_current_span(
            "codette.select_perspectives",
            attributes={"component": "perspective_selector"}
        ) as span:
            # Simple perspective selection logic
            perspectives = []
            
            # Technical keywords -> Newton
            technical_keywords = ['how', 'why', 'explain', 'calculate', 'analyze']
            if any(kw in prompt.lower() for kw in technical_keywords):
                perspectives.append("Newton")
            
            # Creative keywords -> DaVinci
            creative_keywords = ['imagine', 'create', 'design', 'innovate']
            if any(kw in prompt.lower() for kw in creative_keywords):
                perspectives.append("DaVinci")
            
            # Ethical keywords -> Ethical
            ethical_keywords = ['should', 'ought', 'right', 'wrong', 'moral', 'ethical']
            if any(kw in prompt.lower() for kw in ethical_keywords):
                perspectives.append("Ethical")
            
            # Quantum/abstract keywords -> Quantum
            quantum_keywords = ['quantum', 'probability', 'superposition', 'possibility']
            if any(kw in prompt.lower() for kw in quantum_keywords):
                perspectives.append("Quantum")
            
            # Default perspectives if none matched
            if not perspectives:
                perspectives = ["Newton", "DaVinci", "Ethical"]
            
            # Ensure we have at least 3 perspectives
            available = ["Newton", "DaVinci", "Ethical", "Quantum", "Memory", 
                        "Philosophical", "Neural", "Psychological"]
            for p in available:
                if p not in perspectives and len(perspectives) < 3:
                    perspectives.append(p)
            
            span.set_attribute("perspectives.selected", ", ".join(perspectives))
            return perspectives


def create_traced_codette(user_name="User", enable_tracing=True):
    """
    Factory function to create TracedCodette instance
    
    Args:
        user_name: Name of the user
        enable_tracing: Enable tracing (default: True)
        
    Returns:
        TracedCodette instance with tracing enabled
    """
    return TracedCodette(user_name=user_name, enable_tracing=enable_tracing)
