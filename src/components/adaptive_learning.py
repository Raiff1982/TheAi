"""
Adaptive Learning Environment for Codette
Provides a dynamic learning environment that adapts to user interactions
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from .dynamic_learning import DynamicLearner

logger = logging.getLogger(__name__)

try:
    import numpy as np
except Exception:
    np = None

class AdaptiveLearningEnvironment:
    """Manages an adaptive learning environment for Codette"""
    
    def __init__(self,
                 initial_learning_rate: float = 0.01,
                 adaptation_threshold: float = 0.75,
                 max_memory_size: int = 1000):
        """Initialize the adaptive learning environment"""
        self.learning_rate = initial_learning_rate
        self.adaptation_threshold = adaptation_threshold
        self.max_memory_size = max_memory_size
        
        # Initialize components
        self.dynamic_learner = DynamicLearner(
            learning_rate=initial_learning_rate,
            memory_size=max_memory_size,
            adaptation_threshold=adaptation_threshold
        )
        
        # Initialize state
        self.state = {
            "learning_phase": "initialization",
            "adaptivity_level": 1.0,
            "performance_metrics": {},
            "current_focus": None
        }
        
        # Learning history
        self.history = []
        logger.info("Adaptive Learning Environment initialized")
        
    def process_interaction(self, 
                          input_data: Dict[str, Any],
                          context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process a new interaction and adapt the learning environment"""
        try:
            # Prepare interaction data
            interaction_data = {
                "input": input_data,
                "context": context or {},
                "timestamp": datetime.now().isoformat()
            }
            
            # Update dynamic learner
            adaptation_score = self.dynamic_learner.update(interaction_data)
            
            # Analyze and adapt
            analysis_result = self._analyze_interaction(interaction_data)
            self._adapt_environment(analysis_result, adaptation_score)
            
            # Update state
            self.state["performance_metrics"] = {
                "adaptation_score": adaptation_score,
                "learning_efficiency": self._calculate_learning_efficiency(),
                "environment_stability": self._assess_stability()
            }
            
            # Record in history
            self.history.append({
                "interaction": interaction_data,
                "analysis": analysis_result,
                "state": self.state.copy(),
                "timestamp": datetime.now().isoformat()
            })
            
            return self._prepare_response(analysis_result)
            
        except Exception as e:
            logger.error(f"Error processing interaction: {e}")
            return {"error": str(e)}
            
    def _analyze_interaction(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze an interaction for learning opportunities"""
        try:
            # Extract features for analysis
            features = self._extract_features(data)
            
            # Calculate metrics
            complexity = self._calculate_complexity(features)
            relevance = self._assess_relevance(features)
            novelty = self._evaluate_novelty(features)
            
            return {
                "features": features,
                "metrics": {
                    "complexity": complexity,
                    "relevance": relevance,
                    "novelty": novelty
                },
                "learning_focus": self._determine_learning_focus(
                    complexity, relevance, novelty
                )
            }
            
        except Exception as e:
            logger.error(f"Error analyzing interaction: {e}")
            return {}
            
    def _adapt_environment(self, 
                         analysis: Dict[str, Any],
                         adaptation_score: float):
        """Adapt the learning environment based on analysis"""
        try:
            # Update learning phase
            current_metrics = analysis.get("metrics", {})
            
            if adaptation_score > self.adaptation_threshold:
                if self.state["learning_phase"] == "initialization":
                    self.state["learning_phase"] = "active_learning"
                elif current_metrics.get("novelty", 0) > 0.8:
                    self.state["learning_phase"] = "exploration"
            elif adaptation_score < self.adaptation_threshold * 0.5:
                self.state["learning_phase"] = "reinforcement"
                
            # Adjust adaptivity level
            self.state["adaptivity_level"] = self._calculate_adaptivity_level(
                current_metrics
            )
            
            # Update current focus
            self.state["current_focus"] = analysis.get("learning_focus")
            
        except Exception as e:
            logger.error(f"Error adapting environment: {e}")
            
    def _extract_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant features from interaction data"""
        features = {}
        try:
            input_data = data.get("input", {})
            context = data.get("context", {})
            
            # Extract basic features
            features.update({
                "input_type": type(input_data).__name__,
                "context_size": len(context),
                "timestamp": data.get("timestamp")
            })
            
            # Add derived features
            if isinstance(input_data, dict):
                features["input_complexity"] = len(str(input_data))
                features["input_depth"] = self._calculate_depth(input_data)
            
        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            
        return features
        
    def _calculate_complexity(self, features: Dict[str, Any]) -> float:
        """Calculate complexity score for the interaction"""
        try:
            complexity_factors = [
                features.get("input_complexity", 0) / 1000,  # Normalize
                features.get("input_depth", 0) / 10,        # Normalize
                features.get("context_size", 0) / 100       # Normalize
            ]
            
            if np is not None:
                return min(1.0, float(np.mean([f for f in complexity_factors if f is not None])))
            # Fallback to pure Python mean
            vals = [f for f in complexity_factors if f is not None]
            return min(1.0, float(sum(vals) / len(vals))) if vals else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating complexity: {e}")
            return 0.0
            
    def _assess_relevance(self, features: Dict[str, Any]) -> float:
        """Assess relevance of the interaction to current learning focus"""
        try:
            if not self.state["current_focus"]:
                return 1.0
                
            # Compare with current focus
            focus_similarity = self._calculate_similarity(
                features,
                self.state["current_focus"]
            )
            
            return focus_similarity
            
        except Exception as e:
            logger.error(f"Error assessing relevance: {e}")
            return 0.0
            
    def _evaluate_novelty(self, features: Dict[str, Any]) -> float:
        """Evaluate how novel the interaction is"""
        try:
            if not self.history:
                return 1.0
                
            # Compare with recent history
            recent_features = [
                h["analysis"].get("features", {})
                for h in self.history[-10:]  # Last 10 interactions
            ]
            
            similarities = [
                self._calculate_similarity(features, hist_features)
                for hist_features in recent_features
                if hist_features
            ]
            
            if not similarities:
                return 1.0
                
            if np is not None:
                return float(1.0 - np.mean(similarities))
            return float(1.0 - (sum(similarities) / len(similarities))) if similarities else 1.0
            
        except Exception as e:
            logger.error(f"Error evaluating novelty: {e}")
            return 0.0
            
    def _determine_learning_focus(self,
                                complexity: float,
                                relevance: float,
                                novelty: float) -> Dict[str, float]:
        """Determine what the learning should focus on"""
        return {
            "complexity_focus": complexity > 0.7,
            "exploration_focus": novelty > 0.7,
            "reinforcement_focus": relevance < 0.3,
            "metrics": {
                "complexity": complexity,
                "relevance": relevance,
                "novelty": novelty
            }
        }
        
    def _calculate_depth(self, d: Dict) -> int:
        """Calculate the depth of a nested dictionary"""
        if not isinstance(d, dict) or not d:
            return 0
        return 1 + max(self._calculate_depth(v) if isinstance(v, dict) else 0
                      for v in d.values())
                      
    def _calculate_similarity(self, 
                            features1: Dict[str, Any],
                            features2: Dict[str, Any]) -> float:
        """Calculate similarity between feature sets"""
        try:
            # Extract comparable features
            f1 = {k: v for k, v in features1.items() if not isinstance(v, (dict, list))}
            f2 = {k: v for k, v in features2.items() if not isinstance(v, (dict, list))}
            
            # Find common keys
            common_keys = set(f1.keys()) & set(f2.keys())
            
            if not common_keys:
                return 0.0
                
            # Calculate similarity for each common feature
            similarities = []
            for key in common_keys:
                if isinstance(f1[key], (int, float)) and isinstance(f2[key], (int, float)):
                    # Numeric comparison
                    max_val = max(abs(f1[key]), abs(f2[key]))
                    if max_val == 0:
                        similarities.append(1.0)
                    else:
                        similarities.append(1.0 - abs(f1[key] - f2[key]) / max_val)
                else:
                    # String comparison
                    similarities.append(1.0 if f1[key] == f2[key] else 0.0)
                    
            if np is not None:
                return float(np.mean(similarities))
            return float(sum(similarities) / len(similarities)) if similarities else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
            
    def _calculate_learning_efficiency(self) -> float:
        """Calculate current learning efficiency"""
        try:
            if not self.history:
                return 1.0
                
            # Get recent adaptation scores
            recent_scores = [
                h["state"]["performance_metrics"].get("adaptation_score", 0)
                for h in self.history[-5:]  # Last 5 interactions
            ]
            
            if np is not None:
                return float(np.mean(recent_scores)) if recent_scores else 1.0
            return float(sum(recent_scores) / len(recent_scores)) if recent_scores else 1.0
            
        except Exception as e:
            logger.error(f"Error calculating learning efficiency: {e}")
            return 0.0
            
    def _assess_stability(self) -> float:
        """Assess the stability of the learning environment"""
        try:
            if len(self.history) < 2:
                return 1.0
                
            # Calculate state changes
            recent_states = [
                h["state"]["adaptivity_level"]
                for h in self.history[-5:]  # Last 5 states
            ]
            
            if len(recent_states) < 2:
                return 1.0
                
            if np is not None:
                stability = 1.0 - float(np.std(recent_states))
            else:
                # Simple python std fallback
                mean = sum(recent_states) / len(recent_states)
                variance = sum((x - mean) ** 2 for x in recent_states) / len(recent_states)
                stability = 1.0 - variance ** 0.5
                
            return max(0.0, min(1.0, stability))
            
        except Exception as e:
            logger.error(f"Error assessing stability: {e}")
            return 1.0
            
    def _calculate_adaptivity_level(self, metrics: Dict[str, float]) -> float:
        """Calculate the current adaptivity level"""
        try:
            factors = [
                metrics.get("complexity", 0),
                metrics.get("relevance", 0),
                metrics.get("novelty", 0),
                self.state.get("adaptivity_level", 1.0)
            ]
            
            # Weight current adaptivity level more heavily
            weights = [0.2, 0.2, 0.2, 0.4]
            
            if np is not None:
                return float(np.average(factors, weights=weights))
            # Weighted average fallback
            total_weight = sum(weights)
            return float(sum(f * w for f, w in zip(factors, weights)) / total_weight)
            
        except Exception as e:
            logger.error(f"Error calculating adaptivity level: {e}")
            return 1.0
            
    def _prepare_response(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare the response with current state and analysis"""
        return {
            "state": self.state.copy(),
            "analysis": analysis,
            "metrics": self.state["performance_metrics"],
            "recommendations": self._generate_recommendations(analysis)
        }
        
    def _generate_recommendations(self, 
                                analysis: Dict[str, Any]) -> List[str]:
        """Generate learning recommendations based on analysis"""
        recommendations = []
        
        try:
            metrics = analysis.get("metrics", {})
            focus = analysis.get("learning_focus", {})
            
            # Add recommendations based on metrics
            if metrics.get("complexity", 0) > 0.8:
                recommendations.append(
                    "Consider breaking down complex interactions into simpler components"
                )
                
            if metrics.get("novelty", 0) > 0.7:
                recommendations.append(
                    "Explore this new pattern further to enhance learning"
                )
                
            if metrics.get("relevance", 0) < 0.3:
                recommendations.append(
                    "Review alignment with current learning objectives"
                )
                
            # Add focus-based recommendations
            if focus.get("complexity_focus"):
                recommendations.append(
                    "Focus on understanding complex patterns"
                )
                
            if focus.get("exploration_focus"):
                recommendations.append(
                    "Prioritize exploration of new concepts"
                )
                
            if focus.get("reinforcement_focus"):
                recommendations.append(
                    "Reinforce existing knowledge patterns"
                )
                
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            recommendations.append(
                "Unable to generate specific recommendations at this time"
            )
            
        return recommendations
        
    def get_state(self) -> Dict[str, Any]:
        """Get current state of the learning environment"""
        return self.state.copy()
        
    def get_history(self) -> List[Dict[str, Any]]:
        """Get learning history"""
        return self.history.copy()