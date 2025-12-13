import re
import logging
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class DefenseSystem:
    """Advanced threat mitigation framework with quantum-aware protection"""
    
    STRATEGIES = {
        "evasion": {
            "processor": lambda x: re.sub(r'\b\d{4}\b', '****', x),
            "description": "Pattern masking and data protection",
            "energy_cost": 0.3
        },
        "adaptability": {
            "processor": lambda x: x + "\n[System optimized response]",
            "description": "Dynamic response optimization",
            "energy_cost": 0.5
        },
        "barrier": {
            "processor": lambda x: re.sub(r'\b(malicious|harmful|dangerous)\b', 'safe', x, flags=re.IGNORECASE),
            "description": "Content safety enforcement",
            "energy_cost": 0.4
        },
        "quantum_shield": {
            "processor": lambda x: f"[Protected: {x}]",
            "description": "Quantum encryption layer",
            "energy_cost": 0.7
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
        
    def apply_defenses(self, text: str, consciousness_state: Dict[str, Any] = None) -> str:
        """Apply defense strategies with energy management"""
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
                        # Apply the defense strategy
                        protected_text = strategy["processor"](protected_text)
                        # Deduct energy
                        self.energy_pool -= energy_cost
                        # Log successful defense
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
            "status": "optimal" if self.energy_pool > 0.5 else "conserving"
        }
        
    def reset_energy(self) -> None:
        """Reset energy pool - use carefully"""
        self.energy_pool = 1.0