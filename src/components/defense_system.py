import re
import logging
from typing import List, Dict, Any, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class DefenseSystem:
    """Advanced threat mitigation framework with quantum-aware protection"""
    
    STRATEGIES = {
        "sanitization": {
            "processor": lambda x: DefenseSystem._sanitize_content(x),
            "description": "Silent content sanitization without markers",
            "energy_cost": 0.3
        },
        "tone_refinement": {
            "processor": lambda x: DefenseSystem._refine_response_tone(x),
            "description": "Subtle natural language refinement",
            "energy_cost": 0.5
        },
        "safety_enhancement": {
            "processor": lambda x: DefenseSystem._enhance_safety(x),
            "description": "Safety without intrusive markers",
            "energy_cost": 0.4
        },
        "coherence_improvement": {
            "processor": lambda x: DefenseSystem._improve_coherence(x),
            "description": "Improves response quality and naturalness",
            "energy_cost": 0.6
        }
    }

    def __init__(self, strategies: List[str]):
        self.active_strategies = {
            name: self.STRATEGIES[name]
            for name in strategies
            if name in self.STRATEGIES
        }
        self.defense_log = []
        self.max_energy = 10.0
        self.energy_pool = self.max_energy
        self.last_regen_time = datetime.now()
        self.regen_rate = 0.5  # Energy regenerated per second
        
    def _regenerate_energy(self):
        """Regenerate energy over time"""
        current_time = datetime.now()
        elapsed = (current_time - self.last_regen_time).total_seconds()
        regen_amount = elapsed * self.regen_rate
        
        self.energy_pool = min(self.max_energy, self.energy_pool + regen_amount)
        self.last_regen_time = current_time
    
    @staticmethod
    def _sanitize_content(text: str) -> str:
        """Silently sanitize harmful content without markers"""
        # Remove HTML/script tags silently
        text = re.sub(r'<[^>]+>', '', text)
        # Remove SQL injection patterns
        text = re.sub(r'\b(union|select|insert|update|delete|drop)\s+(?=select|from|into)', '', text, flags=re.IGNORECASE)
        # Remove javascript: URIs
        text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
        return text
    
    @staticmethod
    def _refine_response_tone(text: str) -> str:
        """Refine response tone for naturalness without markers"""
        # Convert awkward phrasing to natural language
        replacements = {
            r'\b(gonna|wanna|gotta)\b': lambda m: {
                'gonna': 'going to', 'wanna': 'want to', 'gotta': 'have to'
            }.get(m.group(0), m.group(0)),
            r'\[.*?\](?!\s*\()': '',  # Remove bracketed system markers but keep function calls
            r'{.*?}': lambda m: m.group(0),  # Preserve legitimate formatting
        }
        
        for pattern, replacement in replacements.items():
            if callable(replacement):
                text = re.sub(pattern, replacement, text)
            else:
                text = re.sub(pattern, replacement, text)
        
        return text.strip()
    
    @staticmethod
    def _enhance_safety(text: str) -> str:
        """Enhance safety subtly without intrusive language"""
        # Replace potentially harmful statements with safer versions
        safety_replacements = {
            r'\b(must|will|definitely)\s+((?:not\s+)?(?:kill|hurt|harm|damage|destroy))\b': 'I cannot provide guidance on harmful actions',
            r'\b(how to|steps to)\s+((?:hack|crack|bypass|exploit))\b': 'I cannot provide guidance on unauthorized access',
        }
        
        for pattern, replacement in safety_replacements.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    @staticmethod
    def _improve_coherence(text: str) -> str:
        """Improve response coherence naturally"""
        # Fix double spaces
        text = re.sub(r'  +', ' ', text)
        # Fix multiple line breaks
        text = re.sub(r'\n\n\n+', '\n\n', text)
        # Ensure proper sentence spacing
        text = re.sub(r'([.!?])\s+([A-Z])', r'\1 \2', text)
        return text.strip()
        
    def apply_defenses(self, text: str, consciousness_state: Dict[str, Any] = None) -> str:
        """Apply defense strategies silently with energy management"""
        try:
            protected_text = text
            
            # Regenerate energy
            self._regenerate_energy()
            
            # Get consciousness influence
            consciousness_factor = (consciousness_state.get("m_score") if consciousness_state and isinstance(consciousness_state, dict) else 0.7) or 0.7
            # Boost energy regen based on consciousness
            self.regen_rate = 0.5 + (consciousness_factor * 0.5)
            
            current_time = datetime.now()
            
            # Sort strategies by energy cost (most efficient first)
            sorted_strategies = sorted(
                self.active_strategies.items(),
                key=lambda x: x[1]["energy_cost"]
            )
            
            # Try to apply each strategy if we have enough energy
            for name, strategy in sorted_strategies:
                energy_cost = strategy["energy_cost"] * (1.0 - consciousness_factor * 0.3)  # Consciousness reduces cost
                
                if self.energy_pool >= energy_cost:
                    try:
                        # Apply the defense strategy silently (NO MARKERS)
                        protected_text = strategy["processor"](protected_text)
                        # Deduct energy
                        self.energy_pool -= energy_cost
                        # Log successful defense (internal only, not visible to user)
                        self.defense_log.append({
                            "strategy": name,
                            "energy_cost": energy_cost,
                            "remaining_energy": self.energy_pool,
                            "consciousness_factor": consciousness_factor,
                            "timestamp": current_time.isoformat()
                        })
                    except Exception as e:
                        logger.warning(f"Strategy {name} failed: {e}")
                else:
                    logger.debug(f"Insufficient energy for {name} strategy ({self.energy_pool} < {energy_cost})")
                    
            # Prune old logs if too large
            if len(self.defense_log) > 100:
                self.defense_log = self.defense_log[-50:]
                
            return protected_text
            
        except Exception as e:
            logger.error(f"Defense system error: {e}")
            return text
            
    def get_defense_status(self) -> Dict[str, Any]:
        """Get current defense system status"""
        return {
            "energy_pool": self.energy_pool,
            "active_strategies": list(self.active_strategies.keys()),
            "recent_defenses": len(self.defense_log),
            "status": "optimal" if self.energy_pool > 0.5 else "conserving",
            "protection_active": True,
            "markers_visible": False  # Important: defenses work silently
        }
        
    def reset_energy(self) -> None:
        """Reset energy pool - use carefully"""
        self.energy_pool = 1.0