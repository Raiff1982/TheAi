from typing import List, Dict, Any
import logging
from utils.response_verifier import ResponseVerifier

logger = logging.getLogger(__name__)

class CognitiveProcessor:
    """Multi-perspective analysis engine with enhanced context awareness"""
    
    MODES = {
        "scientific": {
            "processor": lambda q: f"Scientific Analysis: {q} demonstrates fundamental principles",
            "weight": 0.8,
            "threshold": 0.7
        },
        "creative": {
            "processor": lambda q: f"Creative Insight: {q} suggests innovative approaches",
            "weight": 0.9,
            "threshold": 0.6
        },
        "emotional": {
            "processor": lambda q: f"Emotional Interpretation: {q} conveys hopeful intent",
            "weight": 0.7,
            "threshold": 0.5
        },
        "quantum": {
            "processor": lambda q: f"Quantum Analysis: {q} exhibits superposition characteristics",
            "weight": 0.85,
            "threshold": 0.75
        },
        "philosophical": {
            "processor": lambda q: f"Philosophical View: {q} raises deeper questions",
            "weight": 0.75,
            "threshold": 0.65
        }
    }

    def __init__(self, modes: List[str], quantum_state: Dict[str, float] = None):
        self.active_modes = {
            mode: self.MODES[mode] 
            for mode in modes 
            if mode in self.MODES
        }
        self.quantum_state = quantum_state or {"coherence": 0.5}
        self.context_memory = []
        self.verifier = ResponseVerifier()
        
    def generate_insights(self, query: str, consciousness_state: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate insights with quantum-aware perspective integration and verification"""
        try:
            raw_insights = []
            active_modes = []
            consciousness_factor = consciousness_state.get("m_score", 0.7) if consciousness_state else 0.7
            
            for mode_name, mode_config in self.active_modes.items():
                # Calculate activation probability
                activation_score = (
                    mode_config["weight"] * consciousness_factor * 
                    self.quantum_state.get("coherence", 0.5)
                )
                
                if activation_score >= mode_config["threshold"]:
                    try:
                        insight = mode_config["processor"](query)
                        raw_insights.append(insight)
                        active_modes.append(mode_name)
                        self.context_memory.append({
                            "mode": mode_name,
                            "query": query,
                            "insight": insight,
                            "activation": activation_score
                        })
                    except Exception as e:
                        logger.warning(f"Failed to process {mode_name} insight: {e}")
            
            # Prune memory if too large
            if len(self.context_memory) > 100:
                self.context_memory = self.context_memory[-50:]
            
            # Verify insights
            if raw_insights:
                verification_result = self.verifier.process_multi_perspective_response(
                    raw_insights,
                    active_modes,
                    consciousness_state
                )
            else:
                verification_result = {
                    "verified_insights": [],
                    "uncertain_insights": [{
                        "text": f"Scientific Analysis: {query} requires further investigation",
                        "mode": "scientific",
                        "confidence": 0.5
                    }],
                    "overall_confidence": 0.5
                }
            
            return {
                "insights": verification_result["verified_insights"] + verification_result["uncertain_insights"],
                "verified_count": len(verification_result["verified_insights"]),
                "uncertain_count": len(verification_result["uncertain_insights"]),
                "overall_confidence": verification_result["overall_confidence"],
                "quantum_coherence": self.quantum_state.get("coherence", 0.5)
            }
            
        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            return {
                "insights": [{
                    "text": f"Scientific Analysis: {query} requires further investigation",
                    "mode": "scientific",
                    "confidence": 0.5
                }],
                "verified_count": 0,
                "uncertain_count": 1,
                "overall_confidence": 0.5,
                "quantum_coherence": self.quantum_state.get("coherence", 0.5)
            }
    
    def update_quantum_state(self, new_state: Dict[str, float]) -> None:
        """Update quantum state while preserving memory coherence"""
        if not isinstance(new_state, dict):
            logger.warning("Invalid quantum state update attempted")
            return
            
        self.quantum_state.update(new_state)
        
        # Ensure coherence stays in valid range
        self.quantum_state["coherence"] = max(0.0, min(1.0, self.quantum_state.get("coherence", 0.5)))