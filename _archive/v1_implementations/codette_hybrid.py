"""
Codette Hybrid System - Best of Both Worlds
===========================================
Combines Codette's lightweight quantum consciousness with AICore's optimization techniques
"""

import logging
from typing import Any, Dict, List, Optional
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

# Import base systems
try:
    from codette_advanced import CodetteAdvanced, SentimentAnalyzer, ExplainableAI
    CODETTE_ADVANCED_AVAILABLE = True
except ImportError:
    try:
        # Try with Codette prefix
        from Codette.codette_advanced import CodetteAdvanced, SentimentAnalyzer, ExplainableAI
        CODETTE_ADVANCED_AVAILABLE = True
    except ImportError:
        CODETTE_ADVANCED_AVAILABLE = False
        logger.warning("Codette Advanced not available")

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
    
    def __init__(self, user_name="User", use_ml_features: bool = False):
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
                    [c['input'] for c in self.context_memory[-20:]]
                )
                if similar_indices and similar_indices[0] < 2:
                    # Very similar recent query - add variation prompt
                    engineered_query += " (Please provide a fresh perspective.)"
            
            # 4. Generate base response using parent class
            if self.use_ml:
                # Use ML model for enhanced generation
                ml_response = await self._generate_ml_response(engineered_query)
                base_response = ml_response
            else:
                # Use lightweight quantum consciousness
                base_response = self.respond(engineered_query)
            
            # 5. Apply response modifiers
            final_response = self.defense_system.apply_modifiers(base_response)
            
            # 6. Use parent class's advanced features
            advanced_result = await super().generate_response(filtered_query, user_id)
            
            # 7. Merge results
            return {
                **advanced_result,
                "response": final_response,
                "engineered_prompt": engineered_query != query,
                "ml_enhanced": self.use_ml,
                "security_filtered": True,
                "source": "codette-hybrid"
            }
            
        except Exception as e:
            logger.error(f"Hybrid response generation failed: {e}", exc_info=True)
            # Graceful fallback to base Codette
            return {
                "response": self.respond(query),
                "fallback": True,
                "error": str(e)
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
            
            # Combine ML output with quantum consciousness
            quantum_response = self.respond(query)
            
            return f"{quantum_response}\n\n[ML Insight] {ml_text}"
            
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
        print(f"\n?? Sentiment: {result.get('sentiment', {}).get('overall_mood', 'N/A')}")
        print(f"?? Health: {result.get('health_status')}")
        
        # Test optimization
        print("\n" + "-"*60)
        print("Applying production optimizations...")
        codette.optimize_for_production()
        print("? Optimization complete")
        
        print("\n" + "="*60)
    
    asyncio.run(test_hybrid())
