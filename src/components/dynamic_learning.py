"""
Dynamic Learning Component for Codette
Handles real-time learning and adaptation of the AI system
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

try:
    import numpy as np
except Exception:
    np = None

class DynamicLearner:
    """Handles dynamic learning and adaptation for Codette"""
    
    def __init__(self, 
                 learning_rate: float = 0.01,
                 memory_size: int = 1000,
                 adaptation_threshold: float = 0.75):
        """Initialize the dynamic learner"""
        self.learning_rate = learning_rate
        self.memory_size = memory_size
        self.adaptation_threshold = adaptation_threshold
        self.memory_buffer = []
        self.learning_history = []
        self.current_state = {
            "performance": 1.0,
            "adaptability": 1.0,
            "complexity": 0.0
        }
        logger.info("Dynamic learner initialized")
        
    def update(self, new_data: Dict[str, Any]) -> float:
        """Update the learner with new data"""
        try:
            # Add to memory buffer
            self.memory_buffer.append({
                "data": new_data,
                "timestamp": datetime.now().isoformat()
            })
            
            # Trim memory if needed
            if len(self.memory_buffer) > self.memory_size:
                self.memory_buffer = self.memory_buffer[-self.memory_size:]
            
            # Calculate adaptation score
            adaptation_score = self._calculate_adaptation_score(new_data)
            
            # Update internal state
            self._update_state(adaptation_score)
            
            # Record learning progress
            self.learning_history.append({
                "score": adaptation_score,
                "state": self.current_state.copy(),
                "timestamp": datetime.now().isoformat()
            })
            
            logger.debug(f"Learning update complete. Adaptation score: {adaptation_score}")
            return adaptation_score
            
        except Exception as e:
            logger.error(f"Error in dynamic learning update: {e}")
            return 0.0
            
    def _calculate_adaptation_score(self, data: Dict[str, Any]) -> float:
        """Calculate how well the system is adapting to new data"""
        try:
            # Extract features for adaptation calculation
            complexity = self._estimate_complexity(data)
            novelty = self._calculate_novelty(data)
            consistency = self._check_consistency(data)
            
            # Weighted combination of factors
            score = (0.4 * novelty + 
                    0.3 * consistency + 
                    0.3 * (1.0 - complexity))
                    
            return max(0.0, min(1.0, score))
            
        except Exception as e:
            logger.error(f"Error calculating adaptation score: {e}")
            return 0.0
            
    def _estimate_complexity(self, data: Dict[str, Any]) -> float:
        """Estimate the complexity of new data"""
        try:
            # Basic complexity estimation
            if isinstance(data, dict):
                depth = self._get_dict_depth(data)
                size = len(str(data))
                return min(1.0, (depth * 0.1 + size * 0.0001))
            return 0.0
        except Exception as e:
            logger.error(f"Error estimating complexity: {e}")
            return 0.0
            
    def _calculate_novelty(self, data: Dict[str, Any]) -> float:
        """Calculate how novel the new data is compared to memory"""
        try:
            if not self.memory_buffer:
                return 1.0
                
            similarities = []
            for memory in self.memory_buffer[-10:]:  # Compare with last 10 memories
                similarity = self._calculate_similarity(memory['data'], data)
                similarities.append(similarity)
                
            if np is not None:
                avg_similarity = float(np.mean(similarities)) if similarities else 0.0
            else:
                avg_similarity = float(sum(similarities)/len(similarities)) if similarities else 0.0
            return 1.0 - avg_similarity
            
        except Exception as e:
            logger.error(f"Error calculating novelty: {e}")
            return 0.0
            
    def _check_consistency(self, data: Dict[str, Any]) -> float:
        """Check if new data is consistent with existing knowledge"""
        try:
            if not self.memory_buffer:
                return 1.0
                
            # Compare with recent memories for consistency
            recent_memories = self.memory_buffer[-5:]
            consistency_scores = []
            
            for memory in recent_memories:
                score = self._check_data_consistency(memory['data'], data)
                consistency_scores.append(score)
                
            if np is not None:
                return float(np.mean(consistency_scores)) if consistency_scores else 1.0
            return float(sum(consistency_scores)/len(consistency_scores)) if consistency_scores else 1.0
            
        except Exception as e:
            logger.error(f"Error checking consistency: {e}")
            return 0.0
            
    def _get_dict_depth(self, d: Dict) -> int:
        """Calculate the maximum depth of a dictionary"""
        if not isinstance(d, dict) or not d:
            return 0
        return 1 + max(self._get_dict_depth(v) if isinstance(v, dict) else 0
                      for v in d.values())
                      
    def _calculate_similarity(self, data1: Dict[str, Any], 
                            data2: Dict[str, Any]) -> float:
        """Calculate similarity between two data points"""
        try:
            # Convert to sets of items for comparison
            items1 = set(str(item) for item in self._flatten_dict(data1).items())
            items2 = set(str(item) for item in self._flatten_dict(data2).items())
            
            # Calculate Jaccard similarity
            intersection = len(items1.intersection(items2))
            union = len(items1.union(items2))
            
            return intersection / union if union > 0 else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
            
    def _check_data_consistency(self, data1: Dict[str, Any],
                              data2: Dict[str, Any]) -> float:
        """Check structural and value consistency between data points"""
        try:
            # Check structure consistency
            keys1 = set(self._flatten_dict(data1).keys())
            keys2 = set(self._flatten_dict(data2).keys())
            
            # Calculate structural similarity
            key_similarity = len(keys1.intersection(keys2)) / len(keys1.union(keys2))
            
            return key_similarity
            
        except Exception as e:
            logger.error(f"Error checking data consistency: {e}")
            return 0.0
            
    def _flatten_dict(self, d: Dict[str, Any], 
                     parent_key: str = '',
                     sep: str = '.') -> Dict[str, Any]:
        """Flatten a nested dictionary"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
        
    def _update_state(self, adaptation_score: float):
        """Update internal state based on adaptation score"""
        try:
            # Update performance metric
            if np is not None:
                self.current_state["performance"] = float(np.mean([
                    self.current_state["performance"],
                    adaptation_score
                ]))
            else:
                self.current_state["performance"] = float((self.current_state["performance"] + adaptation_score)/2)
            
            # Update adaptability
            if adaptation_score > self.adaptation_threshold:
                self.current_state["adaptability"] = min(
                    1.0,
                    self.current_state["adaptability"] + self.learning_rate
                )
            else:
                self.current_state["adaptability"] = max(
                    0.0,
                    self.current_state["adaptability"] - self.learning_rate
                )
                
            # Update complexity
            if np is not None:
                self.current_state["complexity"] = float(np.mean([
                    self.current_state["complexity"],
                    1.0 - adaptation_score
                ]))
            else:
                self.current_state["complexity"] = float((self.current_state["complexity"] + (1.0 - adaptation_score))/2)
            
        except Exception as e:
            logger.error(f"Error updating state: {e}")
            
    def get_state(self) -> Dict[str, float]:
        """Get current learning state"""
        return self.current_state.copy()
        
    def get_learning_history(self) -> List[Dict[str, Any]]:
        """Get learning history"""
        return self.learning_history.copy()