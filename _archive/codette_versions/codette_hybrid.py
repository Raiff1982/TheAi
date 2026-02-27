#!/usr/bin/env python
"""
Codette Hybrid System - Best of Both Worlds
===========================================
Combines Codette's lightweight quantum consciousness with AICore's optimization techniques
"""

import logging
import sys
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

# Ensure Codette directory is in path
_current_dir = Path(__file__).parent
if str(_current_dir) not in sys.path:
    sys.path.insert(0, str(_current_dir))

# --- SAFE IMPORTS FOR CODFETTE AI MODULES ---
REAL_AICORE_AVAILABLE = False
REAL_COGNITIVE_AVAILABLE = False
REAL_DEFENSE_AVAILABLE = False
REAL_HEALTH_AVAILABLE = False
REAL_FRACTAL_AVAILABLE = False
SENTIMENT_AVAILABLE = False

AICore = None
CognitiveProcessor = None
DefenseSystem = None
HealthMonitor = None
FractalIdentity = None
sentiment_analyzer = None

try:
    from ai_core import AICore
    REAL_AICORE_AVAILABLE = True
    logger.info("AICore loaded (ai_core)")
except Exception:
    try:
        from Codette.src.components.ai_core import AICore
        REAL_AICORE_AVAILABLE = True
        logger.info("AICore loaded (Codette.src.components.ai_core)")
    except Exception:
        logger.debug("AICore not available")

try:
    from cognitive_processor import CognitiveProcessor
    REAL_COGNITIVE_AVAILABLE = True
    logger.info("CognitiveProcessor loaded")
except Exception:
    try:
        from Codette.src.components.cognitive_processor import CognitiveProcessor
        REAL_COGNITIVE_AVAILABLE = True
        logger.info("CognitiveProcessor loaded (Codette.src.components)")
    except Exception:
        logger.debug("CognitiveProcessor not available")

try:
    from defense_system import DefenseSystem
    REAL_DEFENSE_AVAILABLE = True
    logger.info("DefenseSystem loaded")
except Exception:
    try:
        from Codette.src.components.defense_system import DefenseSystem
        REAL_DEFENSE_AVAILABLE = True
        logger.info("DefenseSystem loaded (Codette.src.components)")
    except Exception:
        logger.debug("DefenseSystem not available")

try:
    from health_monitor import HealthMonitor
    REAL_HEALTH_AVAILABLE = True
    logger.info("HealthMonitor loaded")
except Exception:
    try:
        from Codette.src.components.health_monitor import HealthMonitor
        REAL_HEALTH_AVAILABLE = True
        logger.info("HealthMonitor loaded (Codette.src.components)")
    except Exception:
        logger.debug("HealthMonitor not available")

try:
    from fractal import FractalIdentity
    REAL_FRACTAL_AVAILABLE = True
    logger.info("FractalIdentity loaded")
except Exception:
    try:
        from Codette.src.components.fractal import FractalIdentity
        REAL_FRACTAL_AVAILABLE = True
        logger.info("FractalIdentity loaded (Codette.src.components)")
    except Exception:
        logger.debug("FractalIdentity not available")

# Sentiment (optional)
try:
    from nltk.sentiment import SentimentIntensityAnalyzer
    import nltk
    nltk.download('vader_lexicon', quiet=True)
    sentiment_analyzer = SentimentIntensityAnalyzer()
    SENTIMENT_AVAILABLE = True
    logger.info("Sentiment analyzer available")
except Exception:
    logger.debug("Sentiment analyzer not available")

# Import base systems - try multiple import strategies
CODETTE_ADVANCED_AVAILABLE = False
CodetteAdvanced = None
SentimentAnalyzer = None
ExplainableAI = None

# Strategy 1: Direct import (when running from Codette dir)
try:
    from codette_advanced import CodetteAdvanced, SentimentAnalyzer, ExplainableAI
    CODETTE_ADVANCED_AVAILABLE = True
    logger.info("Codette Advanced loaded (direct import)")
except ImportError:
    pass

# Strategy 2: Relative import with Codette prefix
if not CODETTE_ADVANCED_AVAILABLE:
    try:
        from Codette.codette_advanced import CodetteAdvanced, SentimentAnalyzer, ExplainableAI
        CODETTE_ADVANCED_AVAILABLE = True
        logger.info("Codette Advanced loaded (Codette prefix)")
    except ImportError:
        pass

# Strategy 3: Try importing from parent directory
if not CODETTE_ADVANCED_AVAILABLE:
    try:
        parent_dir = Path(__file__).parent.parent
        if str(parent_dir) not in sys.path:
            sys.path.insert(0, str(parent_dir))
        from Codette.codette_advanced import CodetteAdvanced, SentimentAnalyzer, ExplainableAI
        CODETTE_ADVANCED_AVAILABLE = True
        logger.info("Codette Advanced loaded (parent path)")
    except ImportError:
        pass

if not CODETTE_ADVANCED_AVAILABLE:
    logger.warning("Codette Advanced not available - using standalone mode")

# Optional heavy ML imports (only if needed)
TORCH_AVAILABLE = False
try:
    import torch
    TORCH_AVAILABLE = True
    logger.info("PyTorch available for ML optimization")
except ImportError:
    logger.info("PyTorch not available - using lightweight mode")

TRANSFORMERS_AVAILABLE = False
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    TRANSFORMERS_AVAILABLE = True
    logger.info("Transformers available for LLM integration")
except ImportError:
    logger.info("Transformers not available - using base Codette")


class DefenseModifierSystem:
    """
    Lightweight defense system from AICore adapted for Codette
    """
    
    def __init__(self):
        self.response_modifiers = []
        self.response_filters = []
        self.security_level = "high"
    
    def add_sanitization_filter(self):
        """Add input sanitization"""
        import re
        
        def sanitize(text: str) -> str:
            # Remove HTML tags
            text = re.sub(r'<[^>]+>', '', text)
            # Remove potential JS
            text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
            # Remove SQL injection attempts
            text = re.sub(r'(union|select|insert|update|delete|drop)\s+', '', text, flags=re.IGNORECASE)
            return text
        
        self.response_filters.append(sanitize)
    
    def add_tone_modifier(self, tone: str = "professional"):
        """Add tone adjustment modifier"""
        def adjust_tone(text: str) -> str:
            if tone == "professional":
                # Remove overly casual language
                text = text.replace(" gonna ", " going to ")
                text = text.replace(" wanna ", " want to ")
            elif tone == "friendly":
                # Add warmth
                if not text.endswith(("!", ".", "?")):
                    text += "!"
            return text
        
        self.response_modifiers.append(adjust_tone)
    
    def add_length_limiter(self, max_words: int = 300):
        """Limit response length"""
        def limit_length(text: str) -> str:
            words = text.split()
            if len(words) > max_words:
                text = " ".join(words[:max_words]) + "..."
            return text
        
        self.response_modifiers.append(limit_length)
    
    def apply_filters(self, text: str) -> str:
        """Apply all filters"""
        for filter_func in self.response_filters:
            text = filter_func(text)
        return text
    
    def apply_modifiers(self, text: str) -> str:
        """Apply all modifiers"""
        for modifier_func in self.response_modifiers:
            text = modifier_func(text)
        return text


class VectorSearchEngine:
    """
    Lightweight vector search from AICore for semantic similarity
    """
    
    def __init__(self):
        self.embeddings_cache = {}
        self.use_sklearn = False
        
        try:
            from sklearn.metrics.pairwise import cosine_similarity
            self.cosine_similarity = cosine_similarity
            self.use_sklearn = True
        except ImportError:
            logger.warning("sklearn not available - using basic similarity")
    
    def simple_similarity(self, query: str, documents: List[str]) -> List[int]:
        """Simple word-overlap similarity (no ML needed)"""
        query_words = set(query.lower().split())
        scores = []
        
        for doc in documents:
            doc_words = set(doc.lower().split())
            overlap = len(query_words & doc_words)
            scores.append(overlap)
        
        # Return indices sorted by score
        return sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    
    def find_similar_responses(self, query: str, response_history: List[str], top_k: int = 3) -> List[int]:
        """Find most similar previous responses"""
        if self.use_sklearn:
            # Use proper vector search if available
            # TODO: Implement with actual embeddings
            pass
        
        # Fallback to simple similarity
        return self.simple_similarity(query, response_history)[:top_k]


class PromptEngineer:
    """
    Prompt engineering utilities from AICore
    """
    
    def __init__(self):
        self.templates = {
            "daw_expert": "As an expert audio engineer, provide detailed guidance on: {query}",
            "creative": "Thinking creatively about music production, explore: {query}",
            "technical": "From a technical perspective, analyze: {query}",
            "beginner_friendly": "In simple, beginner-friendly terms, explain: {query}"
        }
    
    def engineer_prompt(self, query: str, style: str = "daw_expert") -> str:
        """Apply prompt engineering"""
        template = self.templates.get(style, self.templates["daw_expert"])
        return template.format(query=query)
    
    def add_context(self, query: str, context: Dict[str, Any]) -> str:
        """Add contextual information to prompt"""
        context_parts = []
        
        if context.get("tracks"):
            context_parts.append(f"User has {len(context['tracks'])} tracks")
        
        if context.get("selected_track"):
            track = context["selected_track"]
            context_parts.append(f"Currently working on: {track.get('name', 'track')}")
        
        if context.get("bpm"):
            context_parts.append(f"Project tempo: {context['bpm']} BPM")
        
        if context_parts:
            return f"Context: {', '.join(context_parts)}. Query: {query}"
        
        return query


class CodetteHybrid(CodetteAdvanced):
    """
    Hybrid Codette combining lightweight quantum consciousness with AICore optimizations
    """
    
    def __init__(self, user_name="User", use_ml_features: bool = True):
        super().__init__(user_name)
        
        # Lightweight enhancements
        self.defense_system = DefenseModifierSystem()
        self.defense_system.add_sanitization_filter()
        self.defense_system.add_tone_modifier("professional")
        self.defense_system.add_length_limiter(400)
        
        self.vector_search = VectorSearchEngine()
        self.prompt_engineer = PromptEngineer()
        
        # Optional ML features (only if dependencies available)
        self.use_ml = use_ml_features and TORCH_AVAILABLE and TRANSFORMERS_AVAILABLE
        self.ml_model = None
        self.ml_tokenizer = None
        
        if self.use_ml:
            self._initialize_ml_model()
        
        logger.info(f"Codette Hybrid initialized (ML: {self.use_ml})")
    
    def _initialize_ml_model(self):
        """Initialize ML model (optional heavy feature)"""
        try:
            # Use a lightweight model if needed
            model_name = "distilgpt2"  # Much smaller than Mistral
            self.ml_tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.ml_model = AutoModelForCausalLM.from_pretrained(model_name)
            
            # Apply quantization for efficiency
            if TORCH_AVAILABLE:
                self.ml_model = torch.quantization.quantize_dynamic(
                    self.ml_model, {torch.nn.Linear}, dtype=torch.qint8
                )
            
            logger.info("ML model initialized with quantization")
        except Exception as e:
            logger.warning(f"Could not initialize ML model: {e}")
            self.use_ml = False
    
    def respond(self, query: str, daw_context: Optional[Dict] = None) -> str:
        """Generate response using available systems"""
        # Apply input filtering
        filtered_query = self.defense_system.apply_filters(query)
        
        # Try advanced system first - pass ORIGINAL filtered query (not engineered)
        # This preserves follow-up detection in the underlying Codette
        if self._use_advanced:
            try:
                # Check if the underlying Codette supports daw_context parameter
                import inspect
                respond_sig = inspect.signature(self._advanced.respond)
                param_names = list(respond_sig.parameters.keys())
                
                if len(param_names) >= 2 or 'daw_context' in param_names:
                    # Supports daw_context - pass original filtered query to preserve follow-up detection
                    response = self._advanced.respond(filtered_query, daw_context)
                else:
                    # Doesn't support daw_context - only engineer if NOT a follow-up
                    # Check for follow-up patterns ourselves
                    is_followup = self._is_followup_query(filtered_query)
                    if daw_context and not is_followup:
                        engineered_query = self.prompt_engineer.add_context(filtered_query, daw_context)
                    else:
                        engineered_query = filtered_query
                    response = self._advanced.respond(engineered_query)
                # If real defense is available, apply it, otherwise use lightweight modifiers
                if self.real_defense:
                    try:
                        response = self.real_defense.apply_defenses(response, {"m_score": 0.7})
                    except Exception:
                        pass
                else:
                    response = self.defense_system.apply_modifiers(response)
                return response
            except TypeError as e:
                # Handle case where respond() doesn't accept daw_context
                if "positional arguments" in str(e):
                    logger.warning(f"Advanced Codette doesn't support daw_context, using query only")
                    try:
                        # Check for follow-up before engineering
                        is_followup = self._is_followup_query(filtered_query)
                        if daw_context and not is_followup:
                            engineered_query = self.prompt_engineer.add_context(filtered_query, daw_context)
                        else:
                            engineered_query = filtered_query
                        response = self._advanced.respond(engineered_query)
                        if self.real_defense:
                            try:
                                response = self.real_defense.apply_defenses(response, {"m_score": 0.7})
                            except Exception:
                                pass
                        else:
                            response = self.defense_system.apply_modifiers(response)
                        return response
                    except Exception as e2:
                        logger.warning(f"Advanced respond (no context) failed: {e2}")
                else:
                    logger.warning(f"Advanced respond failed: {e}")
            except Exception as e:
                logger.warning(f"Advanced respond failed: {e}")
        
        # Fallback to basic response
        return self._generate_basic_response(query, daw_context)
    
    def _is_followup_query(self, prompt: str) -> bool:
        """Detect if this is a follow-up question (duplicated from codette_enhanced)"""
        prompt_lower = prompt.lower().strip()
        
        # Common follow-up phrases
        followup_patterns = [
            'what else', 'anything else', 'more tips', 'more advice', 'tell me more',
            'go on', 'continue', 'and', 'also', 'what about', 'how about',
            'any other', 'other suggestions', 'other ideas', 'more ideas', 'next',
            'then what', 'what next', 'ok', 'okay', 'got it', 'thanks', 'thank you',
            'cool', 'nice', 'great', 'good', 'yes', 'yeah', 'yep', 'sure', 'right',
            'hmm', 'interesting',
        ]
        
        # Check if prompt is a short follow-up
        if len(prompt_lower.split()) <= 4:
            for pattern in followup_patterns:
                if pattern in prompt_lower:
                    return True
        
        # Check if prompt starts with follow-up words
        followup_starters = ['and ', 'also ', 'what else', 'anything else', 'more ', 'other ']
        for starter in followup_starters:
            if prompt_lower.startswith(starter):
                return True
        
        return False
    
    def _generate_basic_response(self, query: str, daw_context: Optional[Dict] = None) -> str:
        """Generate a basic DAW-focused response"""
        prompt_lower = query.lower()
        
        # Check for DAW-related keywords
        if any(kw in prompt_lower for kw in ['mix', 'eq', 'compress', 'reverb', 'delay', 'audio', 'track', 'vocal', 'drum', 'bass']):
            responses = []
            
            if 'eq' in prompt_lower or 'frequency' in prompt_lower:
                responses.append("**EQ Guidance**: Cut before boost. High-pass filter on non-bass elements at 80-100Hz. Cut mud at 200-400Hz, add presence at 3-5kHz.")
            
            if 'compress' in prompt_lower:
                responses.append("**Compression Tips**: Start with 4:1 ratio for vocals, 2-3:1 for instruments. Attack 10-30ms preserves transients, release to match tempo.")
            
            if 'reverb' in prompt_lower or 'delay' in prompt_lower:
                responses.append("**Spatial Effects**: Use sends instead of inserts. Short reverb for presence, long for depth. Sync delays to tempo.")
            
            if 'vocal' in prompt_lower:
                responses.append("**Vocal Chain**: High-pass ? EQ (cut mud) ? Compressor ? EQ (add presence) ? De-esser ? Reverb send")
            
            if 'bass' in prompt_lower:
                responses.append("**Bass Processing**: Keep centered, high-pass at 30Hz, focus on 60-100Hz for weight, sidechain to kick if needed.")
            
            if 'drum' in prompt_lower or 'kick' in prompt_lower or 'snare' in prompt_lower:
                responses.append("**Drum Processing**: Check phase alignment, use parallel compression for punch, gate to reduce bleed.")
            
            if responses:
                return "\n\n".join(responses)
        
        # Default response
        return f"I'm Codette, your AI mixing assistant! I can help with EQ, compression, reverb, and other mixing techniques. Ask me about specific tracks or processing!"
    
    async def generate_response(self, query: str, user_id: int = 0, daw_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Enhanced response generation with AICore techniques"""
        try:
            # 1. Apply input filtering
            filtered_query = self.defense_system.apply_filters(query)
            
            # 2. Engineer prompt with context
            if daw_context:
                engineered_query = self.prompt_engineer.add_context(filtered_query, daw_context)
            else:
                engineered_query = self.prompt_engineer.engineer_prompt(filtered_query)
            
            # 3. Check for similar previous responses (avoid repetition)
            if self.context_memory:
                similar_indices = self.vector_search.find_similar_responses(
                    engineered_query,
                    [c.get('input', '') for c in self.context_memory[-20:] if isinstance(c, dict)]
                )
                if similar_indices and similar_indices[0] < 2:
                    # Very similar recent query - add variation prompt
                    engineered_query += " (Please provide a fresh perspective.)"
            
            # 4. Generate base response
            if self.use_ml:
                # Use ML model for enhanced generation
                ml_response = await self._generate_ml_response(engineered_query)
                base_response = ml_response
            else:
                # Use lightweight respond method
                base_response = self.respond(engineered_query, daw_context)
            
            # 4b. Optionally enrich with AICore if available
            ai_enriched = False
            ai_insights = None
            try:
                if self.ai_core:
                    # Prefer async generate_response if available
                    if hasattr(self.ai_core, 'generate_response'):
                        gen = self.ai_core.generate_response
                        if asyncio.iscoroutinefunction(gen):
                            try:
                                ai_out = await gen(user_id, engineered_query)
                            except TypeError:
                                # try swapped args
                                ai_out = await gen(engineered_query, user_id)
                        else:
                            try:
                                ai_out = gen(user_id, engineered_query)
                            except TypeError:
                                ai_out = gen(engineered_query, user_id)

                        if isinstance(ai_out, dict):
                            ai_text = ai_out.get('response') or ai_out.get('message') or str(ai_out)
                        else:
                            ai_text = str(ai_out)
                    elif hasattr(self.ai_core, 'generate_text'):
                        try:
                            ai_text = self.ai_core.generate_text(engineered_query)
                        except Exception:
                            ai_text = None
                    else:
                        ai_text = None

                    if ai_text:
                        # Apply defenses to ai_text if real defense exists
                        if self.real_defense:
                            try:
                                ai_text = self.real_defense.apply_defenses(ai_text, {"m_score": 0.7})
                            except Exception:
                                pass
                        # Apply cognitive insights if available
                        if self.cognitive:
                            try:
                                ai_insights = self.cognitive.generate_insights(ai_text)
                            except Exception:
                                ai_insights = None

                        # Merge ai_text with base response
                        base_response = f"{base_response}\n\n[AI Core] {ai_text}"
                        ai_enriched = True
            except Exception as e:
                logger.debug(f"AICore enrichment failed: {e}")
            
            # 5. Apply response modifiers (prefer real defense if present)
            if self.real_defense:
                try:
                    final_response = self.real_defense.apply_defenses(base_response, {"m_score": 0.7})
                except Exception:
                    final_response = self.defense_system.apply_modifiers(base_response)
            else:
                final_response = self.defense_system.apply_modifiers(base_response)
            
            # 6. Store in context memory
            self.context_memory.append({
                'input': query,
                'response': final_response,
                'timestamp': datetime.now().isoformat()
            })
            
            # 7. Build result
            result = {
                "response": final_response,
                "engineered_prompt": engineered_query != query,
                "ml_enhanced": self.use_ml,
                "ai_enriched": ai_enriched,
                "ai_insights": ai_insights,
                "security_filtered": True,
                "source": "codette-hybrid",
                "timestamp": datetime.now().isoformat()
            }
            
            # Add advanced features if available
            if self._use_advanced:
                result["health_status"] = "healthy"
                if self.sentiment:
                    try:
                        result["sentiment"] = self.sentiment.polarity_scores(filtered_query)
                    except Exception:
                        result["sentiment"] = {"compound": 0.0}
                else:
                    result["sentiment"] = {"compound": 0.0}
            
            return result
            
        except Exception as e:
            logger.error(f"Hybrid response generation failed: {e}", exc_info=True)
            # Graceful fallback
            return {
                "response": self._generate_basic_response(query, daw_context),
                "fallback": True,
                "error": str(e),
                "source": "codette-hybrid-fallback"
            }
    
    async def _generate_ml_response(self, query: str) -> str:
        """Generate response using ML model (optional)"""
        if not self.ml_model or not self.ml_tokenizer:
            return self.respond(query)
        
        try:
            inputs = self.ml_tokenizer(query, return_tensors='pt', max_length=512, truncation=True)
            
            with torch.no_grad():
                outputs = self.ml_model.generate(
                    **inputs,
                    max_new_tokens=150,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9
                )
            
            ml_text = self.ml_tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Combine ML output with base response
            base_response = self.respond(query)
            
            return f"{base_response}\n\n[ML Insight] {ml_text}"
            
        except Exception as e:
            logger.error(f"ML generation failed: {e}")
            return self.respond(query)
    
    def optimize_for_production(self):
        """Apply production optimizations"""
        logger.info("Applying production optimizations...")
        
        # Clear old memory to save RAM
        if len(self.context_memory) > 100:
            self.context_memory = self.context_memory[-50:]
            logger.info("Trimmed context memory")
        
        # If ML model loaded, apply further optimization
        if self.use_ml and self.ml_model:
            try:
                # Apply pruning (remove low-magnitude weights)
                if TORCH_AVAILABLE:
                    import torch.nn.utils.prune as prune
                    
                    for module in self.ml_model.modules():
                        if isinstance(module, torch.nn.Linear):
                            prune.l1_unstructured(module, name='weight', amount=0.2)
                    
                    logger.info("Applied model pruning (20%)")
            except Exception as e:
                logger.warning(f"Could not apply pruning: {e}")


# Standalone test
if __name__ == "__main__":
    import asyncio
    
    async def test_hybrid():
        print("\n" + "="*60)
        print("CODETTE HYBRID SYSTEM TEST")
        print("="*60)
        
        # Test with ML features (if available)
        codette = CodetteHybrid(user_name="TestUser", use_ml_features=True)
        
        test_query = "How do I reduce harsh sibilance in my vocal recording?"
        daw_context = {
            "tracks": ["Vocals", "Drums", "Bass"],
            "selected_track": {"name": "Vocals", "type": "audio"},
            "bpm": 120
        }
        
        result = await codette.generate_response(
            query=test_query,
            user_id=12345,
            daw_context=daw_context
        )
        
        print(f"\n?? Query: {test_query}")
        print(f"\n?? Context: {daw_context}")
        print(f"\n?? Response:\n{result['response']}")
        print(f"\n?? Security: Filtered={result.get('security_filtered')}")
        print(f"?? ML Enhanced: {result.get('ml_enhanced')}")
        print(f"?? Source: {result.get('source')}")
        
        # Test optimization
        print("\n" + "-"*60)
        print("Applying production optimizations...")
        codette.optimize_for_production()
        print("? Optimization complete")
        
        print("\n" + "="*60)
    
    asyncio.run(test_hybrid())
