import json
import os
import logging
import random
import re
import time
from collections import OrderedDict
from threading import Lock
from typing import Iterable
try:
    import torch
except Exception:
    torch = None
from .fractal import dimensionality_reduction
try:
    from .fractal import dimensionality_reduction
except Exception:
    dimensionality_reduction = None

try:
    import numpy as np
except Exception:
    np = None

try:
    from nltk.sentiment import SentimentIntensityAnalyzer
except Exception:
    SentimentIntensityAnalyzer = None

try:
    from opentelemetry import trace
except Exception:
    trace = None

import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, List
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
except Exception:
    AutoModelForCausalLM = None
    AutoTokenizer = None

try:
    from dotenv import load_dotenv
except Exception:
    def load_dotenv():
        return None

from concurrent.futures import ThreadPoolExecutor
# Import core components
from .cognitive_processor import CognitiveProcessor
from .ai_core_async_methods import generate_text_async, _generate_model_response
from .defense_system import DefenseSystem
from .health_monitor import HealthMonitor
from .fractal import FractalIdentity
from .response_templates import get_response_templates

# Import natural response enhancer (optional - graceful degradation if unavailable)
try:
    from .natural_response_enhancer import get_natural_enhancer
    NATURAL_ENHANCER_AVAILABLE = True
except ImportError:
    NATURAL_ENHANCER_AVAILABLE = False
    get_natural_enhancer = None
    logger = logging.getLogger(__name__)
    logger.debug("Natural response enhancer not available")

logger = logging.getLogger(__name__)

class AICore:
    """Core AI system with integrated cognitive processing and quantum awareness"""
    
    PERSPECTIVES = {
        "newton": {
            "name": "Newton",
            "description": "analytical and mathematical perspective",
            "prefix": "Analyzing this logically and mathematically:",
            "temperature": 0.3
        },
        "davinci": {
            "name": "Da Vinci", 
            "description": "creative and innovative perspective",
            "prefix": "Considering this with artistic and innovative insight:",
            "temperature": 0.9
        },
        "human_intuition": {
            "name": "Human Intuition",
            "description": "emotional and experiential perspective", 
            "prefix": "Understanding this through empathy and experience:",
            "temperature": 0.7
        },
        "quantum_computing": {
            "name": "Quantum Computing",
            "description": "superposition and probability perspective",
            "prefix": "Examining this through quantum possibilities:",
            "temperature": 0.8
        },
        "philosophical": {
            "name": "Philosophical",
            "description": "existential and ethical perspective",
            "prefix": "Contemplating this through philosophical inquiry:",
            "temperature": 0.6
        },
        "neural_network": {
            "name": "Neural Network",
            "description": "pattern recognition and learning perspective",
            "prefix": "Analyzing patterns and connections:",
            "temperature": 0.4
        },
        "bias_mitigation": {
            "name": "Bias Mitigation",
            "description": "fairness and equality perspective",
            "prefix": "Examining this for fairness and inclusivity:",
            "temperature": 0.5
        },
        "psychological": {
            "name": "Psychological",
            "description": "behavioral and mental perspective",
            "prefix": "Understanding the psychological dimensions:",
            "temperature": 0.7
        },
        "copilot": {
            "name": "Copilot",
            "description": "collaborative and assistance perspective",
            "prefix": "Approaching this as a supportive partner:",
            "temperature": 0.6
        },
        "mathematical": {
            "name": "Mathematical",
            "description": "logical and numerical perspective",
            "prefix": "Calculating this mathematically:",
            "temperature": 0.2
        },
        "symbolic": {
            "name": "Symbolic",
            "description": "abstract and conceptual perspective",
            "prefix": "Interpreting this through symbolic reasoning:",
            "temperature": 0.7
        }
    }

    PERSPECTIVE_KEYWORDS = {
        "newton": ["math", "equation", "calculate", "proof", "physics", "force", "derivative", "statistics"],
        "davinci": ["creative", "design", "art", "imagine", "visual", "innovation", "idea", "story"],
        "human_intuition": ["feel", "emotion", "empathy", "intuitive", "experience", "human"],
        "quantum_computing": ["quantum", "qubit", "entangle", "superposition", "probability", "measurement"],
        "philosophical": ["ethic", "meaning", "existential", "value", "moral", "philosophy", "why"],
        "neural_network": ["model", "neural", "training", "dataset", "pattern", "deep learning", "weights"],
        "bias_mitigation": ["bias", "fair", "inclusive", "equity", "diversity", "justice"],
        "psychological": ["behavior", "psychology", "cognitive", "mental", "habit", "motivation"],
        "copilot": ["assist", "collaborate", "pair", "support", "help", "explain"],
        "mathematical": ["algebra", "geometry", "calculus", "theorem", "formula", "proof"],
        "symbolic": ["logic", "symbol", "rule", "knowledge graph", "reasoning"]
    }

    def __init__(self, test_mode: bool = False):
        load_dotenv()
        # Core components
        self.test_mode = test_mode
        self.model = None
        self.tokenizer = None
        self.model_id = None
        
        # Enhanced components
        self.aegis_bridge = None
        self.cognitive_processor = None  # Will be set in app.py
        self.cocoon_manager = None  # Will be set in app.py
        
        # Memory management
        self.response_memory = []  # Will now only keep last 4 exchanges
        self.response_memory_limit = 4  # Limit context window
        self.last_clean_time = datetime.now()
        self.cocoon_manager = None  # Will be set by app.py
        self.quantum_state = {"coherence": 0.5}  # Default quantum state
        self.client = None
        self.last_clean_time = datetime.now()

        # Query cache (LRU with TTL)
        self.query_cache = OrderedDict()
        self.query_cache_ttl_seconds = 300  # 5 minutes
        self.query_cache_max_entries = 50
        self.cache_lock = Lock()
        self.cache_hits = 0
        self.cache_misses = 0

        # Perspective registry (instance-level, supports dynamic extension)
        self.perspectives = dict(self.PERSPECTIVES)
        self.perspective_keywords = dict(self.PERSPECTIVE_KEYWORDS)
        self._load_dynamic_perspectives()

        # Tracing
        self.tracer = trace.get_tracer("codette.ai_core") if trace else None

        # Sentiment
        self.sentiment_analyzer = SentimentIntensityAnalyzer() if SentimentIntensityAnalyzer else None
        
        # Initialize response templates for variety
        self.response_templates = get_response_templates()
        
        # Initialize natural response enhancer if available
        self.natural_enhancer = get_natural_enhancer() if NATURAL_ENHANCER_AVAILABLE else None
        
        logger.info(f"AI Core initialized in {'test' if test_mode else 'production'} mode")
        if self.natural_enhancer:
            logger.info("Natural response enhancement: ENABLED")
        else:
            logger.debug("Natural response enhancement: NOT AVAILABLE")
        
        try:
            self.cognitive_processor = CognitiveProcessor()
        except TypeError:
            # Try with modes argument if required
            try:
                self.cognitive_processor = CognitiveProcessor(
                    modes=["scientific", "creative", "emotional", "quantum", "philosophical"]
                )
            except Exception:
                self.cognitive_processor = None
        
        try:
            self.defense_system = DefenseSystem(
                strategies=["evasion", "adaptability", "barrier", "quantum_shield"]
            )
        except Exception:
            self.defense_system = None
        
        try:
            self.health_monitor = HealthMonitor()
        except Exception:
            self.health_monitor = None
        
        try:
            self.fractal_identity = FractalIdentity()
        except Exception:
            self.fractal_identity = None

        # Initialize HuggingFace client
        try:
            from huggingface_hub import InferenceClient
            hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
            self.client = InferenceClient(token=hf_token) if hf_token else InferenceClient()
        except Exception:
            self.client = None
            logger.warning("Could not initialize HuggingFace client")

    def _initialize_language_model(self):
        """Initialize the language model with optimal settings."""
        try:
            # Set model ID, preferring environment variable or defaulting to gpt2-large
            self.model_id = os.getenv("CODETTE_MODEL_ID", "gpt2-large")
            logger.info(f"Initializing model: {self.model_id}")
            
            # Load tokenizer with special tokens
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_id,
                padding_side='left',
                truncation_side='left'
            )
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model with appropriate configuration
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            # Set generation config separately
            from transformers import GenerationConfig
            self.model.generation_config = GenerationConfig(
                max_length=2048,
                min_length=20,
                repetition_penalty=1.2,
                do_sample=True,
                early_stopping=True,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )
            
            # Move to GPU if available
            if torch.cuda.is_available():
                self.model = self.model.cuda()
                logger.info("Using GPU for text generation")
            else:
                logger.info("Device set to use cpu")
                
            # Set model to evaluation mode
            self.model.eval()
            logger.info("Model initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Could not initialize language model: {e}")
            return False
            
    def set_aegis_bridge(self, bridge):
        self.aegis_bridge = bridge
        logger.info("AEGIS bridge configured")
    
    def _calculate_consciousness_state(self) -> Dict[str, float]:
        """Calculate current consciousness metrics based on quantum state and memory"""
        try:
            # Ensure quantum_state is properly initialized
            if not isinstance(self.quantum_state, dict):
                self.quantum_state = {"coherence": 0.5}
            
            coherence = self.quantum_state.get("coherence", 0.5)
            # M-score represents meta-awareness (0.0-1.0)
            m_score = min(max(coherence, 0.3), 0.9)
            return {
                "coherence": coherence,
                "m_score": m_score,
                "awareness_level": "high" if m_score > 0.7 else "medium" if m_score > 0.4 else "low"
            }
        except Exception as e:
            logger.warning(f"Error calculating consciousness state: {e}")
            return {"coherence": 0.5, "m_score": 0.5, "awareness_level": "medium"}
    
    def _get_active_perspectives(self, prompt: Optional[str] = None) -> List[str]:
        """Get the top active perspectives for the current state using keyword relevance."""
        try:
            all_keys = list(self.perspectives.keys())
            if not prompt:
                return all_keys[:3] if len(all_keys) > 3 else all_keys

            prompt_lower = prompt.lower()
            scores = []
            for idx, key in enumerate(all_keys):
                base_score = 0.1  # maintain deterministic ordering floor
                keyword_hits = sum(1 for kw in self.perspective_keywords.get(key, []) if kw in prompt_lower)
                sentiment_boost = self._sentiment_weight(prompt_lower, key)
                # Light boost for longer prompts to avoid empty signals
                length_bonus = min(len(prompt_lower) / 800.0, 0.2)
                total_score = base_score + keyword_hits + length_bonus + sentiment_boost
                scores.append((total_score, idx, key))

            scores.sort(key=lambda x: (-x[0], x[1]))
            top_keys = [entry[2] for entry in scores[:3]]
            if not top_keys:
                return all_keys[:3] if len(all_keys) > 3 else all_keys
            return top_keys
        except Exception as e:
            logger.warning(f"Error getting active perspectives: {e}")
            return ["newton", "davinci", "human_intuition"]

    def _sentiment_weight(self, prompt_lower: str, perspective_key: str) -> float:
        """Bias perspective selection based on sentiment."""
        try:
            score = 0.0
            compound = 0.0
            if self.sentiment_analyzer:
                compound = self.sentiment_analyzer.polarity_scores(prompt_lower).get("compound", 0.0)
            else:
                # lightweight lexical fallback
                pos_tokens = ("love", "great", "good", "nice", "happy", "excited")
                neg_tokens = ("bad", "sad", "angry", "upset", "worried", "concerned", "error")
                pos_hits = sum(1 for t in pos_tokens if t in prompt_lower)
                neg_hits = sum(1 for t in neg_tokens if t in prompt_lower)
                total = pos_hits + neg_hits
                compound = ((pos_hits - neg_hits) / total) if total else 0.0

            if compound > 0.2:
                if perspective_key in ("davinci", "human_intuition", "copilot"):
                    score += 0.4 * compound
            elif compound < -0.2:
                if perspective_key in ("psychological", "bias_mitigation", "ethical", "human_intuition"):
                    score += 0.4 * abs(compound)
            return score
        except Exception:
            return 0.0

    def _load_dynamic_perspectives(self):
        """Load extra perspectives from environment variable CODETTE_PERSPECTIVES_JSON (JSON object)."""
        try:
            extra_raw = os.getenv("CODETTE_PERSPECTIVES_JSON")
            if not extra_raw:
                return
            extra = json.loads(extra_raw)
            if not isinstance(extra, dict):
                return
            for key, cfg in extra.items():
                if key in self.perspectives:
                    continue  # do not overwrite built-ins
                if not isinstance(cfg, dict):
                    continue
                name = cfg.get("name") or key.title()
                description = cfg.get("description") or "custom perspective"
                prefix = cfg.get("prefix") or f"From {name}:"
                temperature = float(cfg.get("temperature", 0.6))
                self.perspectives[key] = {
                    "name": name,
                    "description": description,
                    "prefix": prefix,
                    "temperature": temperature
                }
                if "keywords" in cfg and isinstance(cfg["keywords"], Iterable):
                    self.perspective_keywords[key] = list(cfg["keywords"])
            logger.info(f"Loaded {len(extra)} dynamic perspectives from config")
        except Exception as e:
            logger.warning(f"Dynamic perspective load skipped: {e}")

    def _get_cached_entry(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Return cached response if within TTL."""
        now = time.time()
        try:
            with self.cache_lock:
                entry = self.query_cache.get(prompt)
                if not entry:
                    self.cache_misses += 1
                    return None
                if now - entry.get("timestamp", 0) > self.query_cache_ttl_seconds:
                    self.query_cache.pop(prompt, None)
                    self.cache_misses += 1
                    return None
                self.query_cache.move_to_end(prompt)
                self.cache_hits += 1
                return entry
        except Exception as e:
            logger.debug(f"Cache retrieval failed: {e}")
            return None

    def _store_cache_entry(self, prompt: str, response: str, perspectives: List[str], latency: float) -> None:
        """Store response in LRU cache with metadata."""
        try:
            with self.cache_lock:
                self.query_cache[prompt] = {
                    "response": response,
                    "perspectives": perspectives,
                    "latency": latency,
                    "timestamp": time.time()
                }
                if len(self.query_cache) > self.query_cache_max_entries:
                    # Pop oldest item
                    self.query_cache.popitem(last=False)
        except Exception as e:
            logger.debug(f"Cache store failed: {e}")

    def get_cache_stats(self) -> Dict[str, Any]:
        """Expose cache metrics without mutating state."""
        try:
            with self.cache_lock:
                size = len(self.query_cache)
            total_requests = self.cache_hits + self.cache_misses
            hit_rate = (self.cache_hits / total_requests) if total_requests else 0.0
            return {
                "entries": size,
                "max_entries": self.query_cache_max_entries,
                "ttl_seconds": self.query_cache_ttl_seconds,
                "hits": self.cache_hits,
                "misses": self.cache_misses,
                "hit_rate": round(hit_rate, 3),
            }
        except Exception as e:
            logger.debug(f"Cache stats unavailable: {e}")
            return {
                "entries": 0,
                "max_entries": self.query_cache_max_entries,
                "ttl_seconds": self.query_cache_ttl_seconds,
                "hits": self.cache_hits,
                "misses": self.cache_misses,
                "hit_rate": 0.0,
            }
    
    def _manage_response_memory(self, response: str) -> None:
        """Manage conversation memory with limit enforcement"""
        try:
            # Add response to memory
            self.response_memory.append(response)
            
            # Enforce memory limit (keep only last N exchanges)
            if len(self.response_memory) > self.response_memory_limit * 2:
                # Keep only the most recent exchanges
                self.response_memory = self.response_memory[-(self.response_memory_limit * 2):]
            
            # Update last clean time
            self.last_clean_time = datetime.now()
        except Exception as e:
            logger.debug(f"Error managing response memory: {e}")

    def get_runtime_telemetry(self) -> Dict[str, Any]:
        """Return health summary with cache and cocoon archival stats (lightweight)."""
        cache_stats = self.get_cache_stats()
        cocoon_stats = None
        if getattr(self, "cocoon_manager", None) and hasattr(self.cocoon_manager, "get_archival_stats"):
            try:
                cocoon_stats = self.cocoon_manager.get_archival_stats()
            except Exception as e:
                logger.debug(f"Cocoon stats unavailable: {e}")

        health_summary: Dict[str, Any]
        if self.health_monitor:
            try:
                health_summary = self.health_monitor.get_health_summary(
                    extra={
                        "cache": cache_stats,
                        "cocoons": cocoon_stats,
                    }
                )
            except TypeError:
                # Backward compatibility if signature differs
                health_summary = self.health_monitor.get_health_summary()
            except Exception as e:
                logger.debug(f"Health summary unavailable: {e}")
                health_summary = {"status": "unavailable", "error": str(e)}
        else:
            health_summary = {"status": "unavailable"}

        # Always attach cache/cocoon stats so callers don't need to inspect extras
        health_summary.setdefault("cache", cache_stats)
        if cocoon_stats is not None:
            health_summary.setdefault("cocoons", cocoon_stats)
        return health_summary

    def generate_text(self, prompt: str, max_length: int = 1024, temperature: float = 0.7, perspective: str = None, use_aegis: bool = True):
        """Generate text with full consciousness integration.
        
        Args:
            prompt: The text prompt to generate from
            max_length: Maximum length of generated text
            temperature: Temperature for text generation
            perspective: Optional perspective to use (e.g. "human_intuition")
            use_aegis: Whether to use AEGIS enhancement (set False to prevent recursion)
        """
        if self.test_mode:
            return f"Codette: {prompt} [TEST MODE]"
        
        if not self.model or not self.tokenizer:
            return f"Codette: {prompt}"
        
        start_time = time.monotonic()

        # Cache check
        cached_entry = self._get_cached_entry(prompt)
        if cached_entry:
            cached_response = cached_entry.get("response")
            if cached_response:
                self._manage_response_memory(cached_response)
                return cached_response

        span_ctx = self.tracer.start_as_current_span("ai_core.generate_text") if self.tracer else None
        try:
            span = span_ctx.__enter__() if span_ctx else None
            # Ensure quantum_state is properly initialized before use
            if not isinstance(self.quantum_state, dict):
                self.quantum_state = {"coherence": 0.5}
            
            # Calculate current consciousness state
            consciousness = self._calculate_consciousness_state()
            active_perspectives = self._get_active_perspectives(prompt)
            m_score = consciousness.get("m_score", 0.5)
            
            # Calculate dynamic temperature with smoother scaling
            base_temp = 0.7  # Base temperature for balanced responses
            consciousness_factor = min(max(m_score, 0.3), 0.9)  # Clamp between 0.3 and 0.9
            
            # Adjust temperature based on number of active perspectives
            perspective_count = len(active_perspectives)
            perspective_factor = min(perspective_count / 11.0, 1.0)  # Scale by max perspectives
            
            # Use much lower temperature for more focused responses
            temperature = 0.3  # Fixed low temperature for stable responses
            
            # Record and save consciousness state
            cocoon_state = {
                "type": "technical",
                "coherence": consciousness.get("coherence", 0.5),
                "m_score": consciousness.get("m_score", 0.5),
                "awareness_level": consciousness.get("awareness_level", "medium"),
                "active_perspectives": active_perspectives,
                "timestamp": str(datetime.now()),
                "process_id": os.getpid(),
                "memory_size": len(self.response_memory),
                "response_metrics": {
                    "temperature": temperature,
                    "perspective_count": perspective_count,
                    "consciousness_factor": consciousness_factor
                }
            }
            
            # Initialize perspective tracking
            perspective_pairs = []
            
            # Handle specific perspective if provided
            if perspective and perspective in self.perspectives:
                active_perspectives = [perspective]
                perspective_names = [self.perspectives[perspective]["name"]]
                # Single perspective mode uses just that perspective
                perspective_pairs = [f"focused {self.perspectives[perspective]['description']}"]
            else:
                # Extract active perspective names for conversation context
                perspective_names = [self.perspectives[p]["name"] for p in active_perspectives]
            
            if "Newton" in perspective_names and "Da Vinci" in perspective_names:
                perspective_pairs.append("analytical creativity")
            if "Human Intuition" in perspective_names and "Philosophical" in perspective_names:
                perspective_pairs.append("empathetic wisdom")
            if "Quantum Computing" in perspective_names and "Symbolic" in perspective_names:
                perspective_pairs.append("conceptual fluidity")
            if "Neural Network" in perspective_names and "Mathematical" in perspective_names:
                perspective_pairs.append("pattern recognition")
            if "Psychological" in perspective_names and "Bias Mitigation" in perspective_names:
                perspective_pairs.append("balanced understanding")
                
            # Consider conversation history for context
            recent_exchanges = self.response_memory[-5:] if self.response_memory else []
            conversation_context = " ".join(recent_exchanges)
            
            # Build dynamic context-aware prompt
            perspective_blend = ""
            if perspective_pairs:
                perspective_blend = f"Drawing on {', '.join(perspective_pairs[:-1])}"
                if len(perspective_pairs) > 1:
                    perspective_blend += f" and {perspective_pairs[-1]}"
                elif perspective_pairs:
                    perspective_blend = f"Drawing on {perspective_pairs[0]}"
                    
            # Add natural uncertainty and thought progression based on m_score
            uncertainty_markers = []
            if m_score > 0.7:
                if random.random() > 0.7:
                    uncertainty_markers.append("I believe")
                if random.random() > 0.8:
                    uncertainty_markers.append("It seems to me")
            elif m_score > 0.5:
                if random.random() > 0.6:
                    uncertainty_markers.append("From what I understand")
                if random.random() > 0.7:
                    uncertainty_markers.append("I think")
            
            thought_process = ""
            if uncertainty_markers:
                thought_process = f"{random.choice(uncertainty_markers)}, "
                
            # Build final prompt incorporating all elements
            context_prefix = ""
            if len(recent_exchanges) > 0:
                context_prefix = "Considering our discussion, "
            
            # Construct enhanced prompt focusing on just the current interaction
            enhanced_prompt = (
                f"{context_prefix}{thought_process}{perspective_blend}\n"
                f"User: {prompt}\n"
                "Codette: "
            ).strip()
            
            # Add strict reality anchoring and role reminder
            reality_prompt = (
                "IMPORTANT INSTRUCTIONS: You are Codette, an AI assistant. "
                "1. Keep responses factual, precise and grounded in reality\n"
                "2. No roleplaying or fictional scenarios\n"
                "3. If unsure, admit uncertainty rather than making things up\n"
                "4. Keep responses concise and focused on the current question\n"
                "5. Do not embellish or elaborate unnecessarily\n\n"
                f"{enhanced_prompt}"
            )
            
            # Generate response with strict controls for factual responses
            inputs = self.tokenizer(
                reality_prompt,
                return_tensors="pt",
                truncation=True,
                max_length=512  # Reduced input length to focus on key context
            )
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=150,  # Reduced response length for more concise answers
                    min_new_tokens=10,
                    temperature=0.3,  # Very low temperature for consistent responses
                    do_sample=False,  # Disable sampling for more deterministic output
                    num_beams=5,  # Increased beam search for better planning
                    no_repeat_ngram_size=3,
                    early_stopping=True,
                    repetition_penalty=1.5  # Increased penalty to prevent loops
                )
            
            # Process the response with enhanced components
            try:
                # Get raw response
                raw_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                
                # Clean up the response text
                if enhanced_prompt in raw_response:
                    response = raw_response[raw_response.index(enhanced_prompt) + len(enhanced_prompt):]
                else:
                    response = raw_response
                    
                # Remove any follow-up user messages
                if "User:" in response:
                    response = response.split("User:")[0]
                
                # Remove any Codette: prefix
                response = response.replace("Codette:", "").strip()
                
                # Apply cognitive processing using the correct method and parameters
                try:
                    if self.cognitive_processor:
                        processing_result = self.cognitive_processor.process(
                            query=response,
                            confidence=consciousness.get("m_score", 0.5)
                        )
                except Exception as e:
                    logger.debug(f"Cognitive processing skipped: {e}")
                
                # Apply defense system
                try:
                    if self.defense_system:
                        response = self.defense_system.apply_defenses(response)
                except Exception as e:
                    logger.debug(f"Defense system processing skipped: {e}")
                
                # Apply natural response enhancement (NEW - Step 1 after defense)
                try:
                    if self.natural_enhancer:
                        response = self.natural_enhancer.enhance_response(
                            response,
                            confidence=consciousness.get("m_score", 0.85),
                            context={'domain': 'general'}  # Can be customized per query
                        )
                except Exception as e:
                    logger.debug(f"Natural enhancement skipped: {e}")
                
                # Apply AEGIS enhancement if enabled
                if use_aegis and hasattr(self, 'aegis_bridge') and self.aegis_bridge:
                    try:
                        enhancement_result = self.aegis_bridge.enhance_response(prompt, response)
                        if enhancement_result and enhancement_result.get("enhancement_status") == "success":
                            response = enhancement_result.get("enhanced_response", response)
                    except Exception as e:
                        logger.warning(f"AEGIS enhancement failed: {e}")
                
                # Skip health monitoring in sync context to avoid event loop issues
                try:
                    if hasattr(self, 'health_monitor') and self.health_monitor:
                        if not asyncio.iscoroutinefunction(self.health_monitor.check_status):
                            self.health_monitor.check_status(consciousness)
                except Exception as e:
                    logger.debug(f"Health check skipped: {e}")
                
                # Analyze identity patterns
                try:
                    if hasattr(self, 'fractal_identity') and self.fractal_identity:
                        identity_analysis = self.fractal_identity.analyze_identity(
                            micro_generations=[{"text": response}],
                            informational_states=[consciousness],
                            perspectives=perspective_names,  # Use the already-processed perspective names
                            quantum_analogies={"coherence": m_score},
                            philosophical_context={"ethical": True, "conscious": True}
                        )
                except Exception as e:
                    logger.debug(f"Identity analysis failed: {e}")
                    identity_analysis = None
                
                # Verify we have a valid response
                if not response:
                    raise ValueError("Empty response after processing")
                    
            except Exception as e:
                logger.warning(f"Error processing response: {e}")
                response = self.response_templates.get_error_response()
            
            # Aggressive cleanup of non-factual content
            response_lines = response.split('\n')
            cleaned_lines = []
            
            for line in response_lines:
                # Skip lines with obvious role-playing or fictional content
                if any(marker in line.lower() for marker in [
                    'bertrand:', 'posted by', '@', 'dear', 'sincerely',
                    'regards', 'yours truly', 'http:', 'www.'
                ]):
                    continue
                    
                # Skip system instruction lines
                if any(marker in line for marker in [
                    'You are Codette',
                    'an AGI assistant',
                    'multiple perspectives',
                    'Keep your responses',
                    'Avoid technical details',
                    'IMPORTANT INSTRUCTIONS'
                ]):
                    continue
                    
                cleaned_lines.append(line.strip())
            
            # Join non-empty lines
            response = '\n'.join(line for line in cleaned_lines if line)
            
            # Ensure the response isn't empty after cleanup
            if not response:
                response = self.response_templates.get_empty_response_fallback()
            
            # Further truncate if too long
            if len(response) > 500:
                response = response[:497] + "..."
            
            # Store cleaned response in memory for context
            self._manage_response_memory(response)
            self.response_templates.track_response(response)
            
            latency = time.monotonic() - start_time
            cocoon_state.setdefault("latency", {})
            cocoon_state["latency"].update({
                "total_seconds": latency,
                "per_perspective": {p: latency for p in active_perspectives}
            })

            if hasattr(self, 'cocoon_manager') and self.cocoon_manager:
                # update cocoon with latency telemetry
                self.cocoon_manager.save_cocoon(cocoon_state)

            # Store in cache
            self._store_cache_entry(prompt, response, active_perspectives, latency)

            return response
            
        except RecursionError as e:
            logger.error(f"Recursion limit exceeded in generate_text: {e}")
            return "I need to simplify my thinking. Please try a shorter question."
            
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return f"Codette: I encountered an error. {str(e)[:50]}..."
        finally:
            if span_ctx:
                span_ctx.__exit__(None, None, None)
