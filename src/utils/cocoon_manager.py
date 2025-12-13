from datetime import datetime
import os
import json
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class CocoonManager:
    """Manages Codette's cocoon data storage and retrieval"""
    
    def __init__(self, base_dir: str = "./cocoons"):
        self.base_dir = base_dir
        self.cocoon_data = []
        self.quantum_state = {"coherence": 0.5}
        self._ensure_cocoon_dir()
        
    def _ensure_cocoon_dir(self):
        """Ensure cocoon directory exists"""
        os.makedirs(self.base_dir, exist_ok=True)
        
    def load_cocoons(self) -> None:
        """Load all cocoon data from files"""
        try:
            # Ensure directory exists
            os.makedirs(self.base_dir, exist_ok=True)
            
            cocoon_files = [
                f for f in os.listdir(self.base_dir) 
                if f.endswith('.cocoon')
            ]
            logger.info(f"Found {len(cocoon_files)} cocoon files in {self.base_dir}")
            
            loaded_data = []
            for fname in cocoon_files:
                try:
                    full_path = os.path.join(self.base_dir, fname)
                    with open(full_path, 'r') as f:
                        cocoon = json.load(f)
                        if self._validate_cocoon(cocoon):
                            loaded_data.append(cocoon)
                            # Update quantum state if present and most recent
                            current_quantum_state = cocoon.get('data', {}).get('quantum_state')
                            if current_quantum_state:
                                # Convert list quantum state to dict if needed
                                if isinstance(current_quantum_state, list):
                                    current_quantum_state = {
                                        "coherence": sum(current_quantum_state) / len(current_quantum_state)
                                        if current_quantum_state else 0.5
                                    }
                                # Update if we don't have state yet or if this cocoon is more recent
                                if (not isinstance(self.quantum_state, dict) or
                                    not self.quantum_state.get('coherence') or
                                    not loaded_data[:-1] or
                                    cocoon['timestamp'] > loaded_data[-2]['timestamp']):
                                    self.quantum_state = current_quantum_state.copy() if isinstance(current_quantum_state, dict) else {"coherence": 0.5}
                except Exception as e:
                    logger.error(f"Error loading cocoon {fname}: {e}")
                    continue
                    
            # Sort by timestamp and handle empty timestamps
            self.cocoon_data = sorted(
                [c for c in loaded_data if isinstance(c, dict) and self._validate_cocoon(c)],
                key=lambda x: x.get('timestamp', '0'),
                reverse=True
            )
            logger.info(f"Successfully loaded {len(self.cocoon_data)} valid cocoons")
            
            logger.info(
                f"Loaded {len(self.cocoon_data)} cocoons "
                f"with quantum coherence {self.quantum_state.get('coherence', 0.5)}"
            )
            
        except Exception as e:
            logger.error(f"Error loading cocoons: {e}")
            self.cocoon_data = []
            # Ensure we have a valid quantum state
            if not isinstance(self.quantum_state, dict) or 'coherence' not in self.quantum_state:
                self.quantum_state = {"coherence": 0.5}
            
    def _validate_cocoon(self, cocoon: Dict[str, Any]) -> bool:
        """Validate cocoon data structure"""
        required_fields = ['timestamp', 'data']
        return all(field in cocoon for field in required_fields)
        
    def save_cocoon(
        self, 
        data: Dict[str, Any],
        cocoon_type: str = "codette"
    ) -> bool:
        """Save new cocoon data to file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{cocoon_type}_cocoon_{timestamp}.cocoon"
            filepath = os.path.join(self.base_dir, filename)
            
            # If data has its own quantum state, update our state
            if "quantum_state" in data:
                self.quantum_state = data["quantum_state"]
            
            cocoon = {
                "timestamp": timestamp,
                "data": {
                    **data,
                    "quantum_state": self.quantum_state.copy()
                }
            }
            
            with open(filepath, 'w') as f:
                json.dump(cocoon, f, indent=2)
                
            self.cocoon_data.insert(0, cocoon)
            logger.info(f"Saved cocoon: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving cocoon: {e}")
            return False
            
    def get_latest_quantum_state(self) -> Dict[str, float]:
        """Get the most recent quantum state"""
        return self.quantum_state.copy()
        
    def get_latest_cocoons(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get the most recent cocoons"""
        return self.cocoon_data[:limit]
        
    def update_quantum_state(self, new_state: Dict[str, float]) -> None:
        """Update the current quantum state and save it"""
        self.quantum_state.update(new_state)
        logger.info(f"Updated quantum state: {self.quantum_state}")
        
        # Save the new state in a cocoon
        self.save_cocoon({
            "type": "quantum_update",
            "quantum_state": self.quantum_state.copy()
        })