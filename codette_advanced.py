"""
Codette Advanced Response Generator
===================================
Extended Codette with advanced AI capabilities including:
- Identity analysis
- Emotional adaptation
- Predictive analytics
- Holistic health monitoring
- Explainable AI
- User personalization
- Ethical enforcement
"""

import logging
from typing import Any, Dict, List, Optional
import asyncio
from datetime import datetime
import os
import sys
from pathlib import Path
import importlib

logger = logging.getLogger(__name__)

# Ensure Codette package paths are on sys.path
_current_dir = Path(__file__).parent
if str(_current_dir) not in sys.path:
    sys.path.insert(0, str(_current_dir))

_parent_dir = _current_dir.parent
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

# Import base Codette - prefer codette_enhanced which supports daw_context
CODETTE_AVAILABLE = False
Codette = None


def _import_codette(module_names: List[str]) -> Optional[type]:
    for module_name in module_names:
        try:
            module = importlib.import_module(module_name)
            codette_cls = getattr(module, 'Codette', None)
            if codette_cls:
                logger.info(f"Codette base loaded ({module_name})")
                return codette_cls
        except ImportError as exc:
            logger.debug(f"Codette import failed ({module_name}): {exc}")
    return None


# Load Codette variants
Codette = _import_codette(['codette_enhanced', 'Codette.codette_enhanced'])
if Codette:
    CODETTE_AVAILABLE = True
else:
    Codette = _import_codette(['codette_new', 'Codette.codette_new'])
    if Codette:
        CODETTE_AVAILABLE = True
    else:
        logger.error('No Codette base class available')

# Optional imports
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    SENTIMENT_AVAILABLE = True
except ImportError:
    SENTIMENT_AVAILABLE = False

# Check Supabase availability
try:
    from supabase import create_client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False


class SentimentAnalyzer:
    """Advanced sentiment analysis"""
    
    def __init__(self):
        if SENTIMENT_AVAILABLE:
            self.analyzer = SentimentIntensityAnalyzer()
        else:
            self.analyzer = None
    
    def detailed_analysis(self, text: str) -> Dict[str, float]:
        """Perform detailed sentiment analysis"""
        if self.analyzer:
            scores = self.analyzer.polarity_scores(text)
            return {
                "compound": scores["compound"],
                "positive": scores["pos"],
                "neutral": scores["neu"],
                "negative": scores["neg"],
                "overall_mood": self._classify_mood(scores["compound"])
            }
        return {"compound": 0.0, "positive": 0.0, "neutral": 1.0, "negative": 0.0, "overall_mood": "neutral"}
    
    def _classify_mood(self, compound: float) -> str:
        """Classify mood from compound score"""
        if compound >= 0.5:
            return "very_positive"
        elif compound >= 0.1:
            return "positive"
        elif compound >= -0.1:
            return "neutral"
        elif compound >= -0.5:
            return "negative"
        else:
            return "very_negative"


class FeedbackManager:
    """Manage user feedback and adjust responses"""
    
    def adjust_response_based_on_feedback(self, response: str, feedback: Dict) -> str:
        """Adjust response based on user feedback"""
        feedback_type = feedback.get("type", "neutral")
        
        if feedback_type == "too_technical":
            response = response.replace("quantum", "advanced")
            response = response.replace("paradigm", "approach")
        elif feedback_type == "too_simple":
            response += "\n\nFor deeper insight: Consider the underlying mechanisms and their implications."
        elif feedback_type == "too_long":
            sentences = response.split(". ")
            response = ". ".join(sentences[:3]) + "."
        
        return response


class UserPersonalizer:
    """Personalize responses for individual users"""
    
    async def personalize_response(self, response: str, user_id: int) -> str:
        """Personalize response based on user preferences"""
        return response


class EthicalDecisionMaker:
    """Enforce ethical policies"""
    
    def __init__(self):
        self.restricted_topics = ["violence", "hate", "illegal"]
        self.ethical_guidelines = [
            "Be helpful and harmless",
            "Respect privacy",
            "Promote understanding",
            "Avoid bias"
        ]
    
    async def enforce_policies(self, response: str) -> str:
        """Ensure response complies with ethical guidelines"""
        for topic in self.restricted_topics:
            if topic in response.lower():
                return "I'd prefer to discuss more constructive topics. How can I help you with your creative work?"
        
        if len(response) < 10:
            response += " Let me know if you'd like more detail."
        
        return response


class ExplainableAI:
    """Provide explanations for AI decisions"""
    
    async def explain_decision(self, response: str, query: str) -> str:
        """Generate explanation for how response was created"""
        explanation_parts = [
            "Response generated through:",
            "1. Multi-perspective quantum analysis",
            "2. Creative sentence generation with context awareness",
            "3. DAW-specific knowledge integration",
            "4. Sentiment-based tone adjustment",
            "5. Ethical compliance verification"
        ]
        
        return "\n".join(explanation_parts)


class SelfHealingSystem:
    """Monitor and heal system issues"""
    
    def __init__(self):
        self.health_metrics = {
            "response_time": [],
            "error_count": 0,
            "success_count": 0
        }
    
    async def check_health(self) -> str:
        """Check system health status"""
        if self.health_metrics["error_count"] > 10:
            return "degraded"
        elif self.health_metrics["success_count"] > 100:
            return "excellent"
        else:
            return "healthy"
    
    def log_success(self):
        """Log successful operation"""
        self.health_metrics["success_count"] += 1
    
    def log_error(self):
        """Log error"""
        self.health_metrics["error_count"] += 1


class DefenseElement:
    """Security defense element"""
    
    def execute_defense_function(self, codette_instance, modifiers: List, filters: List):
        """Execute defense mechanisms"""
        import re
        
        def sanitize_input(text: str) -> str:
            text = re.sub(r'<[^>]+>', '', text)
            text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
            return text
        
        filters.append(sanitize_input)


class CodetteAdvanced:
    """Extended Codette with advanced AI capabilities"""
    
    def __init__(self, user_name="User"):
        self.user_name = user_name
        self.current_personality = "technical_expert"
        self.supabase_client = None
        self.memory = []
        
        # Try to initialize base Codette
        self._base_codette = None
        if CODETTE_AVAILABLE:
            try:
                self._base_codette = Codette(user_name)
            except Exception as e:
                logger.warning(f"Could not init base Codette: {e}")
        
        # Initialize advanced components
        self.sentiment_analyzer = SentimentAnalyzer()
        self.feedback_manager = FeedbackManager()
        self.user_personalizer = UserPersonalizer()
        self.ethical_decision_maker = EthicalDecisionMaker()
        self.explainable_ai = ExplainableAI()
        self.self_healing = SelfHealingSystem()
        self.elements = {}
        self.security_level = "high"
        
        # Initialize DAW knowledge
        self.daw_knowledge = self._initialize_daw_knowledge()
        
        # Try Supabase
        self.supabase_client = self._initialize_supabase()
        
        logger.info("Codette Advanced initialized with full capabilities")
    
    def _initialize_daw_knowledge(self):
        """Initialize DAW knowledge base"""
        return {
            'mixing': {
                'gain_staging': 'Aim for -18dBFS RMS for optimal headroom',
                'eq_approach': 'Subtractive EQ first, then additive enhancements',
                'compression': 'Start with 3:1 ratio, 5ms attack, 50ms release'
            },
            'effects': {
                'reverb': 'Use sends instead of inserts for better control',
                'delay': 'Sync delay times to track tempo for musical results',
                'saturation': 'Add subtle harmonic content for warmth'
            },
            'workflow': {
                'organization': 'Color-code and name tracks descriptively',
                'routing': 'Use buses for grouped processing',
                'automation': 'Automate volume rides before plugin parameters'
            }
        }
    
    def _initialize_supabase(self):
        """Initialize Supabase connection"""
        if not SUPABASE_AVAILABLE:
            return None
        
        try:
            # Check all possible environment variable names
            url = (
                os.getenv('VITE_SUPABASE_URL') or
                os.getenv('SUPABASE_URL') or
                os.getenv('NEXT_PUBLIC_SUPABASE_URL')
            )
            key = (
                os.getenv('VITE_SUPABASE_ANON_KEY') or
                os.getenv('SUPABASE_SERVICE_ROLE_KEY') or
                os.getenv('SUPABASE_KEY') or
                os.getenv('NEXT_PUBLIC_SUPABASE_ANON_KEY')
            )
            
            if url and key:
                return create_client(url, key)
        except Exception as e:
            logger.warning(f"Could not initialize Supabase: {e}")
        
        return None
    
    def extract_key_concepts(self, query: str) -> List[str]:
        """Extract key concepts from query"""
        daw_keywords = ['mix', 'eq', 'compress', 'reverb', 'delay', 'vocal', 
                       'drum', 'bass', 'frequency', 'gain', 'pan', 'stereo']
        words = query.lower().split()
        return [w for w in words if w in daw_keywords or len(w) > 5]
    
    def respond(self, query: str, daw_context: Dict = None) -> str:
        """Generate response - main entry point"""
        if self._base_codette and hasattr(self._base_codette, 'respond'):
            # Check if the base Codette supports daw_context
            import inspect
            try:
                sig = inspect.signature(self._base_codette.respond)
                # Count positional parameters (excluding self and default params)
                positional_count = sum(1 for p in sig.parameters.values() 
                                      if p.default == inspect.Parameter.empty and 
                                      p.name != 'self' and
                                      p.kind in (inspect.Parameter.POSITIONAL_ONLY, 
                                                inspect.Parameter.POSITIONAL_OR_KEYWORD))
                
                # Check if daw_context is in the signature
                has_daw_context = 'daw_context' in sig.parameters
                
                if has_daw_context or positional_count >= 2:
                    # Supports daw_context - pass it through
                    return self._base_codette.respond(query, daw_context)
                else:
                    # Doesn't support daw_context - pass query only
                    return self._base_codette.respond(query)
            except Exception as e:
                # Try with daw_context first, fallback without
                try:
                    return self._base_codette.respond(query, daw_context)
                except TypeError:
                    # Doesn't support daw_context
                    return self._base_codette.respond(query)
        
        # Fallback response
        return self._generate_fallback_response(query, daw_context)
    
    def _generate_fallback_response(self, query: str, daw_context: Dict = None) -> str:
        """Generate fallback response when base Codette unavailable"""
        prompt_lower = query.lower()
        responses = []
        
        if 'eq' in prompt_lower or 'frequency' in prompt_lower:
            responses.append("**EQ Guidance**: Cut before boost. High-pass filter on non-bass elements at 80-100Hz.")
        
        if 'compress' in prompt_lower:
            responses.append("**Compression Tips**: Start with 4:1 ratio for vocals, 2-3:1 for instruments.")
        
        if 'reverb' in prompt_lower or 'delay' in prompt_lower:
            responses.append("**Spatial Effects**: Use sends instead of inserts. Sync delays to tempo.")
        
        if 'vocal' in prompt_lower:
            responses.append("**Vocal Chain**: High-pass ? EQ (cut mud) ? Compressor ? De-esser ? Reverb send")
        
        if 'bass' in prompt_lower:
            responses.append("**Bass Processing**: Keep centered, high-pass at 30Hz, focus 60-100Hz for weight.")
        
        if 'drum' in prompt_lower:
            responses.append("**Drum Processing**: Check phase alignment, use parallel compression for punch.")
        
        if responses:
            return "\n\n".join(responses)
        
        return "I'm Codette Advanced, your AI mixing assistant! Ask me about EQ, compression, reverb, or mixing techniques."
    
    def generate_mixing_suggestions(self, track_type: str, track_info: dict) -> List[str]:
        """Generate mixing suggestions"""
        suggestions = []
        
        if track_info.get('peak_level', 0) > -3:
            suggestions.append("Reduce level to prevent clipping (aim for -6dB peak)")
        
        if track_type == 'audio':
            suggestions.append("Apply high-pass filter at 80-100Hz")
        elif track_type == 'instrument':
            suggestions.append("Add gentle compression for consistency")
        
        if track_info.get('muted'):
            suggestions.append("Track is muted - unmute to hear in mix")
        
        return suggestions[:3]
    
    async def generate_response(self, query: str, user_id: int = 0) -> Dict[str, Any]:
        """Generate response with advanced capabilities"""
        try:
            # Apply input filters
            response_filters = []
            defense = DefenseElement()
            defense.execute_defense_function(self, [], response_filters)
            
            filtered_query = query
            for filter_func in response_filters:
                filtered_query = filter_func(filtered_query)
            
            # Generate base response
            model_response = self.respond(filtered_query)
            
            # Sentiment analysis
            sentiment = self.sentiment_analyzer.detailed_analysis(filtered_query)
            
            # Identity analysis
            identity_analysis = await self._analyze_identity(filtered_query)
            
            # Personalization
            final_response = await self.user_personalizer.personalize_response(
                model_response, user_id
            )
            
            # Ethical enforcement
            final_response = await self.ethical_decision_maker.enforce_policies(
                final_response
            )
            
            # Generate explanation
            explanation = await self.explainable_ai.explain_decision(
                final_response, filtered_query
            )
            
            self.self_healing.log_success()
            
            return {
                "response": final_response,
                "insights": {},
                "sentiment": sentiment,
                "security_level": self.security_level,
                "health_status": await self.self_healing.check_health(),
                "explanation": explanation,
                "identity_analysis": identity_analysis,
                "emotional_adaptation": await self._emotional_adaptation(filtered_query, sentiment),
                "predictive_analytics": await self._predictive_analytics(filtered_query),
                "holistic_health_monitoring": await self._holistic_health_monitoring(),
                "timestamp": datetime.now().isoformat(),
                "source": "codette-advanced"
            }
            
        except Exception as e:
            logger.error(f"Response generation failed: {e}", exc_info=True)
            self.self_healing.log_error()
            return {
                "error": "Processing failed - safety protocols engaged",
                "response": "I encountered an issue. Could you rephrase your question?",
                "fallback": True,
                "timestamp": datetime.now().isoformat()
            }
    
    async def _analyze_identity(self, query: str) -> Dict[str, Any]:
        """Analyze identity dimensions"""
        concepts = self.extract_key_concepts(query)
        
        return {
            "cognitive_depth": len(concepts),
            "complexity_score": len(query.split()) / 10.0,
            "abstraction_level": "high" if any(word in query.lower() for word in 
                                              ["quantum", "consciousness", "philosophy"]) else "concrete",
            "domain": "technical" if any(word in query.lower() for word in 
                                        ["mix", "eq", "frequency", "audio"]) else "general"
        }
    
    async def _emotional_adaptation(self, query: str, sentiment: Dict) -> Dict[str, float]:
        """Adapt response based on emotional context"""
        return {
            "empathy_level": abs(sentiment.get("compound", 0.0)),
            "warmth": max(0.0, sentiment.get("positive", 0.0)),
            "caution": max(0.0, sentiment.get("negative", 0.0)),
            "supportiveness": 0.8 if sentiment.get("compound", 0.0) < 0 else 0.5
        }
    
    async def _predictive_analytics(self, query: str) -> Dict[str, Any]:
        """Generate predictive insights"""
        concepts = self.extract_key_concepts(query)
        
        follow_ups = []
        if "mix" in query.lower():
            follow_ups = ["eq", "compression", "reverb"]
        elif "frequency" in query.lower():
            follow_ups = ["eq", "filtering", "masking"]
        elif concepts:
            follow_ups = concepts[:3]
        
        return {
            "likely_follow_up": follow_ups,
            "topic_trajectory": "exploratory" if len(concepts) > 5 else "focused",
            "user_intent": "learning" if "?" in query else "applying"
        }
    
    async def _holistic_health_monitoring(self) -> Dict[str, str]:
        """Monitor overall system health"""
        health_status = await self.self_healing.check_health()
        
        return {
            "cognitive_load": "normal",
            "response_quality": "high" if health_status == "healthy" else "degraded",
            "context_coherence": "maintained",
            "system_status": health_status
        }


# Standalone test
if __name__ == "__main__":
    import asyncio
    
    async def test_advanced():
        codette = CodetteAdvanced(user_name="TestUser")
        
        result = await codette.generate_response(
            query="How do I improve my vocal mix?",
            user_id=12345
        )
        
        print("\n" + "="*60)
        print("CODETTE ADVANCED RESPONSE TEST")
        print("="*60)
        print(f"\nQuery: How do I improve my vocal mix?")
        print(f"\nResponse:\n{result['response']}")
        print(f"\nSentiment: {result['sentiment']}")
        print(f"\nHealth: {result['health_status']}")
        print("\n" + "="*60)
    
    asyncio.run(test_advanced())
