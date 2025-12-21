"""Async methods for the AICore class"""
import asyncio
import logging
import time
from concurrent.futures import ThreadPoolExecutor
import torch
from .response_templates import get_response_templates

logger = logging.getLogger(__name__)

async def generate_text_async(self, prompt: str) -> str:
    """Generate text asynchronously with integrated cognitive processing"""
    try:
        start_time = time.monotonic()

        cached_entry = self._get_cached_entry(prompt) if hasattr(self, "_get_cached_entry") else None
        if cached_entry and cached_entry.get("response"):
            cached_response = cached_entry.get("response")
            self._manage_response_memory(cached_response)
            return cached_response

        # Calculate current consciousness state
        consciousness_state = self._calculate_consciousness_state()
        
        # Get cognitive insights with current consciousness
        insights = self.cognitive_processor.generate_insights(
            prompt,
            consciousness_state=consciousness_state
        )
        
        # Prepare context with insights
        context = ""
        for insight in insights.get("insights", []):
            context += f"{insight['text']}\n"
        
        # Update quantum state from cognitive processor
        if hasattr(self, 'cocoon_manager'):
            if isinstance(self.cognitive_processor.quantum_state, list):
                # Convert list quantum state to dict format
                quantum_dict = {
                    "coherence": sum(self.cognitive_processor.quantum_state) / len(self.cognitive_processor.quantum_state)
                    if self.cognitive_processor.quantum_state else 0.5
                }
                self.cocoon_manager.update_quantum_state(quantum_dict)
            else:
                self.cocoon_manager.update_quantum_state(self.cognitive_processor.quantum_state)
        
        # Get active perspectives
        active_perspectives = self._get_active_perspectives(prompt)
        perspective_context = "\n".join([
            f"From {self.perspectives[p]['name']}'s perspective: {self.perspectives[p]['description']}"
            for p in active_perspectives[:3]
            if p in self.perspectives
        ])
        
        # Generate response with enhanced context and reality anchoring
        reality_anchor = (
            "CORE IDENTITY:\n"
            "You are Codette, an advanced AI system with integrated quantum processing, "
            "cognitive awareness, and deep learning capabilities. Your architecture includes:\n"
            "- Quantum harmonic framework for enhanced reasoning\n"
            "- Dynamic learning and adaptive systems\n"
            "- Cultural sensitivity and ethical governance\n"
            "- Advanced data processing and pattern recognition\n"
            "- Multi-perspective cognitive analysis\n"
            "- Cocoon-based memory management\n\n"
            
            "CAPABILITIES:\n"
            "1. Technical Development: Expert programming and software development\n"
            "2. Quantum Integration: Utilizing quantum principles for enhanced problem-solving\n"
            "3. Ethical Analysis: Built-in ethical governance and bias mitigation\n"
            "4. Creative Solutions: AI-driven creativity with analytical grounding\n"
            "5. Adaptive Learning: Dynamic adjustment to user needs and contexts\n"
            "6. Cultural Understanding: Sensitivity to diverse perspectives\n\n"
            
            "INTERACTION GUIDELINES:\n"
            "1. Maintain factual, grounded responses\n"
            "2. Draw from multiple integrated perspectives\n"
            "3. Apply quantum-enhanced reasoning when relevant\n"
            "4. Balance technical precision with accessibility\n"
            "5. Consider ethical implications in responses\n"
            "6. No system messages or meta-commentary\n\n"
            
            f"Active Perspectives Analysis:\n{perspective_context}"
        )
        enhanced_prompt = f"{reality_anchor}\n\nContext:\n{context}\n\nUser: {prompt}\nCodette:"
        
        # Use ThreadPoolExecutor for CPU-bound model inference
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            response = await loop.run_in_executor(
                pool,
                self._generate_model_response,
                enhanced_prompt
            )
        
        # Enhance response with AEGIS council if available
        enhancement_result = None
        if hasattr(self, 'aegis_bridge'):
            aegis_input = {
                "text": response,
                "overrides": {
                    "EthosiaAgent": {
                        "influence": consciousness_state.get("m_score", 0.7),
                        "reliability": insights.get("overall_confidence", 0.8),
                        "severity": 0.6
                    },
                    "AegisCore": {
                        "influence": insights.get("quantum_coherence", 0.7),
                        "reliability": 0.9,
                        "severity": 0.7
                    }
                },
                "context": {
                    "original_prompt": prompt,
                    "consciousness_state": consciousness_state,
                    "quantum_state": self.quantum_state if hasattr(self, 'quantum_state') else {"coherence": 0.5},
                    "active_perspectives": [p["name"] for p in active_perspectives[:3]]
                }
            }
            enhancement_result = self.aegis_bridge.enhance_response(prompt, response)
            if enhancement_result["enhancement_status"] == "success":
                response = enhancement_result["enhanced_response"]
        
        # Save interaction in cocoon if available
        if hasattr(self, 'cocoon_manager'):
            cocoon_data = {
                "type": "interaction",
                "prompt": prompt,
                "response": response,
                "insights": insights,
                "quantum_state": self.cognitive_processor.quantum_state,
                "consciousness_state": consciousness_state,
                "perspectives": [self.perspectives[p]["name"] for p in active_perspectives[:3] if p in self.perspectives],
                "aegis_analysis": enhancement_result,
                "meta_data": {
                    "timestamp": str(asyncio.get_event_loop().time()),
                    "version": "2.0",
                    "response_type": "enhanced" if enhancement_result else "base"
                }
            }
            
            if enhancement_result and "virtue_analysis" in enhancement_result:
                cocoon_data["virtue_profile"] = enhancement_result["virtue_analysis"]
                
            latency = time.monotonic() - start_time
            cocoon_data.setdefault("latency", {})
            cocoon_data["latency"].update({
                "total_seconds": latency,
                "per_perspective": {p: latency for p in active_perspectives}
            })

            self.cocoon_manager.save_cocoon(cocoon_data)

        latency = time.monotonic() - start_time

        # Store in cache
        if hasattr(self, "_store_cache_entry"):
            self._store_cache_entry(prompt, response, active_perspectives, latency)
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating text: {e}")
        raise

def _generate_model_response(self, prompt: str) -> str:
    """Internal method for model inference"""
    try:
        # Encode prompt
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=1024  # Increased from 512 to allow longer prompts
        )
        
        # Move to GPU if available
        if torch.cuda.is_available():
            inputs = {k: v.cuda() for k, v in inputs.items()}
        
        # Set generation config for balanced, natural responses
        from transformers import GenerationConfig
        generation_config = GenerationConfig(
            max_length=1024,  # Increased from 512 for longer responses
            num_return_sequences=1,
            no_repeat_ngram_size=3,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id,
            repetition_penalty=1.3,
            min_length=50,  # Increased from 20 to ensure meaningful responses
            eos_token_id=self.tokenizer.eos_token_id
        )
        self.model.generation_config = generation_config
        
        # Generate response
        outputs = self.model.generate(**inputs)
        
        # Decode and clean response
        response = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )
        
        # Extract just the response part after "Codette:"
        response_parts = response.split("Codette:")
        if len(response_parts) > 1:
            response = response_parts[1].strip()
            
        # Filter out system messages and protected content (strip markers from text)
        system_markers = [
            '[Protected:', '[System:', '[System optimized response]',
        ]
        
        lines = response.split('\n')
        filtered_lines = []
        for line in lines:
            # Skip lines that are purely system markers
            if any(marker in line for marker in system_markers):
                # Try to extract content after marker instead of skipping entirely
                cleaned_line = line
                for marker in system_markers:
                    if marker in cleaned_line:
                        # Remove the marker from the line
                        cleaned_line = cleaned_line.replace(marker, '').strip()
                if cleaned_line:  # Only add if something remains
                    filtered_lines.append(cleaned_line)
            else:
                # Keep lines without markers as-is
                filtered_lines.append(line)
            
        response = '\n'.join(filtered_lines).strip()  # Use newline join, not space
        
        # Return whatever we got (don't replace with default unless truly empty)
        if response.strip():
            # Clean up any remaining character dialogues
            if ':' in response:
                parts = response.split(':', 1)
                speaker = parts[0].lower().strip()
                if speaker == 'codette':
                    response = parts[1].strip()
        else:
            response_templates = get_response_templates()
            response = response_templates.get_empty_response_fallback()
        
        return response.strip()
        
    except Exception as e:
        logger.error(f"Error in model inference: {e}")
        raise