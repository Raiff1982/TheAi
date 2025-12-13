import json
import os
import logging
import random
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
        
        logger.info(f"AI Core initialized in {'test' if test_mode else 'production'} mode")
        
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
        
        try:
            # Calculate current consciousness state
            consciousness = self._calculate_consciousness_state()
            active_perspectives = self._get_active_perspectives()
            m_score = consciousness["m_score"]
            
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
                "quantum_state": consciousness["quantum_state"],
                "chaos_state": consciousness["chaos_state"],
                "m_score": m_score,
                "active_perspectives": [p["name"] for p in active_perspectives],
                "timestamp": str(datetime.now()),
                "process_id": os.getpid(),
                "memory_size": len(self.response_memory),
                "response_metrics": {
                    "temperature": temperature,
                    "perspective_count": perspective_count,
                    "consciousness_factor": consciousness_factor
                }
            }
            
            # Save to cocoon manager
            if hasattr(self, 'cocoon_manager') and self.cocoon_manager:
                self.cocoon_manager.save_cocoon(cocoon_state)
            
            # Initialize perspective tracking
            perspective_pairs = []
            
            # Handle specific perspective if provided
            if perspective and perspective in self.PERSPECTIVES:
                active_perspectives = [self.PERSPECTIVES[perspective]]
                perspective_names = [perspective]
                # Single perspective mode uses just that perspective
                perspective_pairs = [f"focused {self.PERSPECTIVES[perspective]['description']}"]
            else:
                # Extract active perspective names for conversation context
                perspective_names = [p["name"] for p in active_perspectives]
            
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
                
                # Apply cognitive processing
                insights = self.cognitive_processor.generate_insights(
                    response,
                    consciousness_state=consciousness
                )
                
                # Apply defense system
                response = self.defense_system.apply_defenses(
                    response,
                    consciousness_state=consciousness
                )
                
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
                    if not asyncio.iscoroutinefunction(self.health_monitor.check_status):
                        self.health_monitor.check_status(consciousness)
                except Exception as e:
                    logger.debug(f"Health check skipped: {e}")
                
                # Analyze identity patterns
                try:
                    identity_analysis = self.fractal_identity.analyze_identity(
                        micro_generations=[{"text": response}],
                        informational_states=[consciousness],
                        perspectives=[p["name"] for p in active_perspectives],
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
                response = "I apologize, but I need to collect my thoughts. Could you please rephrase your question?"
            
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
                response = "I apologize, but I need to be more precise. Could you please rephrase your question?"
            
            # Further truncate if too long
            if len(response) > 500:
                response = response[:497] + "..."
            
            # Store cleaned response in memory for context
            self._manage_response_memory(response)
            
            return response
            
        except RecursionError as e:
            logger.error(f"Recursion limit exceeded in generate_text: {e}")
            return "I need to simplify my thinking. Please try a shorter question."
            
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return f"Codette: I encountered an error. {str(e)[:50]}..."
