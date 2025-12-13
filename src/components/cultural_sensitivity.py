"""
Cultural Sensitivity Engine for Codette
Ensures AI responses are culturally appropriate and inclusive
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

try:
    import numpy as np
except Exception:
    np = None

class CulturalSensitivityEngine:
    """Manages cultural sensitivity analysis and adaptation"""
    
    def __init__(self,
                 sensitivity_threshold: float = 0.8,
                 confidence_threshold: float = 0.7,
                 max_memory: int = 1000):
        """Initialize the cultural sensitivity engine"""
        self.sensitivity_threshold = sensitivity_threshold
        self.confidence_threshold = confidence_threshold
        self.max_memory = max_memory
        
        # Initialize knowledge bases
        self.cultural_patterns = {}
        self.sensitivity_memory = []
        self.current_state = {
            "sensitivity_level": 1.0,
            "active_contexts": set(),
            "recent_adaptations": []
        }
        
        # Load basic cultural knowledge
        self._initialize_cultural_knowledge()
        logger.info("Cultural Sensitivity Engine initialized")
        
    def analyze_content(self,
                       content: Dict[str, Any],
                       context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze content for cultural sensitivity"""
        try:
            # Process input
            processed_content = self._process_content(content)
            
            # Perform cultural analysis
            analysis_result = self._analyze_cultural_aspects(processed_content, context)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(analysis_result)
            
            # Update memory
            self._update_memory(analysis_result)
            
            return {
                "status": "success",
                "sensitivity_score": analysis_result["overall_score"],
                "concerns": analysis_result["concerns"],
                "recommendations": recommendations,
                "confidence": analysis_result["confidence"],
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing content: {e}")
            return {"status": "error", "message": str(e)}
            
    def adapt_content(self,
                     content: Dict[str, Any],
                     analysis: Dict[str, Any],
                     context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Adapt content based on cultural sensitivity analysis"""
        try:
            if analysis["status"] != "success":
                return content
                
            # Check if adaptation is needed
            if analysis["sensitivity_score"] >= self.sensitivity_threshold:
                return content
                
            # Apply adaptations
            adapted_content = self._apply_adaptations(content, analysis)
            
            # Verify adaptations
            verification = self._verify_adaptation(adapted_content, context)
            
            # Record adaptation
            self._record_adaptation(content, adapted_content, analysis)
            
            return {
                "status": "adapted",
                "original": content,
                "adapted": adapted_content,
                "verification": verification,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error adapting content: {e}")
            return {"status": "error", "message": str(e)}
            
    def _initialize_cultural_knowledge(self):
        """Initialize basic cultural knowledge base"""
        try:
            # Basic cultural patterns
            self.cultural_patterns = {
                "respect": {
                    "patterns": ["honorific", "formal address", "polite language"],
                    "importance": 0.9
                },
                "inclusion": {
                    "patterns": ["gender-neutral", "accessible", "diverse"],
                    "importance": 0.8
                },
                "sensitivity": {
                    "patterns": ["cultural awareness", "contextual appropriateness"],
                    "importance": 0.85
                }
            }
            
            logger.info("Cultural knowledge base initialized")
            
        except Exception as e:
            logger.error(f"Error initializing cultural knowledge: {e}")
            
    def _process_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Process and normalize content for analysis"""
        try:
            processed = {
                "type": content.get("type", "unknown"),
                "elements": self._extract_elements(content),
                "context": content.get("context", {}),
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "source": content.get("source", "unknown")
                }
            }
            
            return processed
            
        except Exception as e:
            logger.error(f"Error processing content: {e}")
            return {}
            
    def _analyze_cultural_aspects(self,
                                content: Dict[str, Any],
                                context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze various cultural aspects of content"""
        try:
            # Initialize analysis components
            respect_score = self._analyze_respect(content)
            inclusion_score = self._analyze_inclusion(content)
            sensitivity_score = self._analyze_sensitivity(content, context)
            
            # Identify potential concerns
            concerns = self._identify_concerns(
                content,
                {
                    "respect": respect_score,
                    "inclusion": inclusion_score,
                    "sensitivity": sensitivity_score
                }
            )
            
            # Calculate overall score
            scores = [respect_score["score"], inclusion_score["score"], sensitivity_score["score"]]
            if np is not None:
                overall_score = float(np.mean(scores))
            else:
                overall_score = float(sum(scores)/len(scores))
            
            # Calculate confidence
            confs = [respect_score["confidence"], inclusion_score["confidence"], sensitivity_score["confidence"]]
            if np is not None:
                confidence = float(np.mean(confs))
            else:
                confidence = float(sum(confs)/len(confs))
            
            return {
                "overall_score": overall_score,
                "confidence": confidence,
                "components": {
                    "respect": respect_score,
                    "inclusion": inclusion_score,
                    "sensitivity": sensitivity_score
                },
                "concerns": concerns,
                "context_influence": self._evaluate_context_influence(context)
            }
            
        except Exception as e:
            logger.error(f"Error in cultural analysis: {e}")
            return {
                "overall_score": 0.0,
                "confidence": 0.0,
                "components": {},
                "concerns": ["Analysis failed"],
                "context_influence": 0.0
            }
            
    def _analyze_respect(self, content: Dict[str, Any]) -> Dict[str, float]:
        """Analyze respectfulness of content"""
        try:
            elements = content.get("elements", {})
            patterns = self.cultural_patterns["respect"]["patterns"]
            
            # Check for respectful patterns
            matches = self._find_pattern_matches(elements, patterns)
            
            score = len(matches) / max(1, len(patterns))
            confidence = min(1.0, len(elements) / 10)  # More elements = more confidence
            
            return {
                "score": score,
                "confidence": confidence,
                "matches": matches
            }
            
        except Exception as e:
            logger.error(f"Error analyzing respect: {e}")
            return {"score": 0.0, "confidence": 0.0, "matches": []}
            
    def _analyze_inclusion(self, content: Dict[str, Any]) -> Dict[str, float]:
        """Analyze inclusivity of content"""
        try:
            elements = content.get("elements", {})
            patterns = self.cultural_patterns["inclusion"]["patterns"]
            
            # Check for inclusive patterns
            matches = self._find_pattern_matches(elements, patterns)
            
            score = len(matches) / max(1, len(patterns))
            confidence = min(1.0, len(elements) / 10)
            
            return {
                "score": score,
                "confidence": confidence,
                "matches": matches
            }
            
        except Exception as e:
            logger.error(f"Error analyzing inclusion: {e}")
            return {"score": 0.0, "confidence": 0.0, "matches": []}
            
    def _analyze_sensitivity(self,
                           content: Dict[str, Any],
                           context: Optional[Dict[str, Any]] = None) -> Dict[str, float]:
        """Analyze cultural sensitivity of content"""
        try:
            elements = content.get("elements", {})
            patterns = self.cultural_patterns["sensitivity"]["patterns"]
            
            # Check for sensitivity patterns
            matches = self._find_pattern_matches(elements, patterns)
            
            # Consider context if available
            context_score = self._evaluate_context_influence(context)
            
            base_score = len(matches) / max(1, len(patterns))
            adjusted_score = (base_score + context_score) / 2
            
            confidence = min(1.0, len(elements) / 10)
            
            return {
                "score": adjusted_score,
                "confidence": confidence,
                "matches": matches,
                "context_score": context_score
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sensitivity: {e}")
            return {
                "score": 0.0,
                "confidence": 0.0,
                "matches": [],
                "context_score": 0.0
            }
            
    def _identify_concerns(self,
                         content: Dict[str, Any],
                         scores: Dict[str, Dict[str, float]]) -> List[str]:
        """Identify potential cultural sensitivity concerns"""
        concerns = []
        try:
            # Check each component
            for component, data in scores.items():
                if data["score"] < self.sensitivity_threshold:
                    concerns.append(
                        f"Low {component} score: {data['score']:.2f}"
                    )
                    
            # Check confidence levels
            low_confidence = [
                component for component, data in scores.items()
                if data["confidence"] < self.confidence_threshold
            ]
            
            if low_confidence:
                concerns.append(
                    f"Low confidence in: {', '.join(low_confidence)}"
                )
                
        except Exception as e:
            logger.error(f"Error identifying concerns: {e}")
            concerns.append("Error in concern identification")
            
        return concerns
        
    def _generate_recommendations(self,
                                analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations for improving cultural sensitivity"""
        recommendations = []
        try:
            components = analysis.get("components", {})
            
            # Generate recommendations based on scores
            for component, data in components.items():
                if data["score"] < self.sensitivity_threshold:
                    recommendations.extend(
                        self._get_component_recommendations(component, data)
                    )
                    
            # Add context-based recommendations
            if analysis.get("context_influence", 0) < 0.5:
                recommendations.append(
                    "Consider broader cultural context in content"
                )
                
            # Prioritize recommendations
            recommendations = sorted(
                recommendations,
                key=lambda x: len(x),  # Simple prioritization by length
                reverse=True
            )[:5]  # Limit to top 5
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            recommendations.append(
                "Unable to generate specific recommendations"
            )
            
        return recommendations
        
    def _apply_adaptations(self,
                          content: Dict[str, Any],
                          analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Apply cultural sensitivity adaptations to content"""
        try:
            adapted = content.copy()
            
            # Apply component-specific adaptations
            for component, data in analysis.get("components", {}).items():
                if data["score"] < self.sensitivity_threshold:
                    adapted = self._apply_component_adaptation(
                        adapted, component, data
                    )
                    
            # Record adaptation
            adapted["adaptation_info"] = {
                "original_scores": analysis.get("components", {}),
                "timestamp": datetime.now().isoformat()
            }
            
            return adapted
            
        except Exception as e:
            logger.error(f"Error applying adaptations: {e}")
            return content
            
    def _verify_adaptation(self,
                          adapted_content: Dict[str, Any],
                          context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Verify the effectiveness of adaptations"""
        try:
            # Re-analyze adapted content
            verification = self.analyze_content(adapted_content, context)
            
            # Compare with original scores
            original_scores = adapted_content.get("adaptation_info", {}).get(
                "original_scores", {}
            )
            
            improvements = {}
            for component, data in verification.get("components", {}).items():
                if component in original_scores:
                    improvements[component] = (
                        data["score"] - original_scores[component]["score"]
                    )
                    
            return {
                "status": "success",
                "improvements": improvements,
                "verified_score": verification.get("sensitivity_score", 0.0),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error verifying adaptation: {e}")
            return {"status": "error", "message": str(e)}
            
    def _update_memory(self, analysis_result: Dict[str, Any]):
        """Update sensitivity memory with new analysis"""
        try:
            self.sensitivity_memory.append({
                "timestamp": datetime.now().isoformat(),
                "analysis": analysis_result
            })
            
            # Trim memory if needed
            if len(self.sensitivity_memory) > self.max_memory:
                self.sensitivity_memory = self.sensitivity_memory[-self.max_memory:]
                
            # Update current state
            if np is not None:
                self.current_state["sensitivity_level"] = float(np.mean([
                    m["analysis"]["overall_score"]
                    for m in self.sensitivity_memory[-10:]
                ]))
            else:
                vals = [m["analysis"]["overall_score"] for m in self.sensitivity_memory[-10:]]
                self.current_state["sensitivity_level"] = float(sum(vals)/len(vals)) if vals else 0.0
            
        except Exception as e:
            logger.error(f"Error updating memory: {e}")
            
    def _find_pattern_matches(self,
                            elements: Dict[str, Any],
                            patterns: List[str]) -> List[str]:
        """Find matching cultural patterns in content elements"""
        matches = []
        try:
            element_strings = [
                str(v) for v in elements.values()
                if isinstance(v, (str, int, float))
            ]
            
            for pattern in patterns:
                if any(pattern.lower() in s.lower() for s in element_strings):
                    matches.append(pattern)
                    
        except Exception as e:
            logger.error(f"Error finding pattern matches: {e}")
            
        return matches
        
    def _extract_elements(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Extract analyzable elements from content"""
        elements = {}
        try:
            def extract_recursive(obj, prefix=""):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        new_prefix = f"{prefix}.{key}" if prefix else key
                        extract_recursive(value, new_prefix)
                elif isinstance(obj, (str, int, float)):
                    elements[prefix] = obj
                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        new_prefix = f"{prefix}[{i}]"
                        extract_recursive(item, new_prefix)
                        
            extract_recursive(content)
            
        except Exception as e:
            logger.error(f"Error extracting elements: {e}")
            
        return elements
        
    def _evaluate_context_influence(self,
                                  context: Optional[Dict[str, Any]] = None) -> float:
        """Evaluate the influence of context on cultural sensitivity"""
        try:
            if not context:
                return 0.5  # Neutral score when no context
                
            # Extract context elements
            context_elements = self._extract_elements(context)
            
            # Check for cultural markers in context
            cultural_markers = sum(
                1 for pattern in sum(
                    [p["patterns"] for p in self.cultural_patterns.values()],
                    []
                )
                if any(pattern.lower() in str(v).lower() for v in context_elements.values())
            )
            
            return min(1.0, cultural_markers / 10)  # Normalize score
            
        except Exception as e:
            logger.error(f"Error evaluating context: {e}")
            return 0.5
            
    def _get_component_recommendations(self,
                                     component: str,
                                     data: Dict[str, Any]) -> List[str]:
        """Get recommendations for improving a specific component"""
        try:
            base_recommendations = {
                "respect": [
                    "Use more formal language",
                    "Include appropriate honorifics",
                    "Maintain professional tone"
                ],
                "inclusion": [
                    "Use gender-neutral language",
                    "Consider diverse perspectives",
                    "Ensure accessibility"
                ],
                "sensitivity": [
                    "Consider cultural context",
                    "Avoid culturally specific assumptions",
                    "Use inclusive examples"
                ]
            }
            
            return base_recommendations.get(component, [])
            
        except Exception as e:
            logger.error(f"Error getting recommendations: {e}")
            return []
            
    def _apply_component_adaptation(self,
                                  content: Dict[str, Any],
                                  component: str,
                                  data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply adaptation for a specific component"""
        try:
            # This is a placeholder implementation
            # Real implementation would have specific adaptation logic
            adapted = content.copy()
            adapted["adaptations"] = adapted.get("adaptations", [])
            adapted["adaptations"].append({
                "component": component,
                "original_score": data["score"],
                "timestamp": datetime.now().isoformat()
            })
            
            return adapted
            
        except Exception as e:
            logger.error(f"Error applying component adaptation: {e}")
            return content
            
    def _record_adaptation(self,
                          original: Dict[str, Any],
                          adapted: Dict[str, Any],
                          analysis: Dict[str, Any]):
        """Record adaptation for learning and improvement"""
        try:
            self.current_state["recent_adaptations"].append({
                "timestamp": datetime.now().isoformat(),
                "original_score": analysis["sensitivity_score"],
                "adaptation_type": [
                    component
                    for component, data in analysis["components"].items()
                    if data["score"] < self.sensitivity_threshold
                ]
            })
            
            # Keep only recent adaptations
            self.current_state["recent_adaptations"] = \
                self.current_state["recent_adaptations"][-10:]
                
        except Exception as e:
            logger.error(f"Error recording adaptation: {e}")
            
    def get_state(self) -> Dict[str, Any]:
        """Get current state of the sensitivity engine"""
        return self.current_state.copy()
        
    def get_memory(self) -> List[Dict[str, Any]]:
        """Get sensitivity memory"""
        return self.sensitivity_memory.copy()