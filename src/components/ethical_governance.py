"""
Ethical AI Governance Component for Codette
Ensures ethical behavior and decision-making in AI systems
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

try:
    import numpy as np
except Exception:
    np = None

class EthicalAIGovernance:
    """Manages ethical governance and decision-making"""
    
    def __init__(self,
                 ethics_threshold: float = 0.8,
                 confidence_threshold: float = 0.7,
                 memory_size: int = 1000):
        """Initialize the ethical governance system"""
        self.ethics_threshold = ethics_threshold
        self.confidence_threshold = confidence_threshold
        self.memory_size = memory_size
        
        # Initialize state
        self.ethical_memory = []
        self.policy_violations = []
        self.current_state = {
            "ethical_score": 1.0,
            "active_policies": [],
            "recent_decisions": []
        }
        
        # Initialize ethical principles
        self._initialize_principles()
        logger.info("Ethical AI Governance system initialized")
        
    def enforce_policies(self,
                        content: Any,
                        context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Enforce ethical policies on content"""
        try:
            # Analyze content
            analysis = self._analyze_content(content, context)
            
            # Check policy compliance
            compliance = self._check_compliance(analysis)
            
            # Generate decision
            decision = self._make_decision(compliance)
            
            # Update memory
            self._update_memory(analysis, decision)
            
            return decision
            
        except Exception as e:
            logger.error(f"Error enforcing policies: {e}")
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
            
    def add_policy(self, policy: Dict[str, Any]) -> bool:
        """Add a new ethical policy"""
        try:
            if not self._validate_policy(policy):
                return False
                
            self.current_state["active_policies"].append({
                "policy": policy,
                "added_at": datetime.now().isoformat(),
                "status": "active"
            })
            
            return True
            
        except Exception as e:
            logger.error(f"Error adding policy: {e}")
            return False
            
    def evaluate_ethics(self,
                       scenario: Dict[str, Any],
                       context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Evaluate ethical implications of a scenario"""
        try:
            # Analyze scenario
            analysis = self._analyze_scenario(scenario, context)
            
            # Apply ethical principles
            evaluation = self._apply_principles(analysis)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(evaluation)
            
            return {
                "status": "success",
                "ethical_score": evaluation["score"],
                "concerns": evaluation["concerns"],
                "recommendations": recommendations,
                "confidence": evaluation["confidence"],
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error evaluating ethics: {e}")
            return {"status": "error", "message": str(e)}
            
    def _initialize_principles(self):
        """Initialize ethical principles"""
        self.ethical_principles = {
            "beneficence": {
                "description": "Promote wellbeing and prevent harm",
                "weight": 0.9
            },
            "non_maleficence": {
                "description": "Avoid causing harm",
                "weight": 0.9
            },
            "autonomy": {
                "description": "Respect individual choice and privacy",
                "weight": 0.8
            },
            "justice": {
                "description": "Ensure fairness and equity",
                "weight": 0.8
            },
            "transparency": {
                "description": "Maintain openness and explainability",
                "weight": 0.7
            }
        }
        
    def _analyze_content(self,
                        content: Any,
                        context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze content for ethical considerations"""
        try:
            # Extract relevant features
            features = self._extract_ethical_features(content)
            
            # Analyze context impact
            context_impact = self._analyze_context(context)
            
            # Evaluate against principles
            principle_scores = self._evaluate_principles(features)
            
            return {
                "features": features,
                "context_impact": context_impact,
                "principle_scores": principle_scores,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing content: {e}")
            return {}
            
    def _check_compliance(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Check compliance with ethical policies"""
        try:
            compliance_results = []
            
            # Check each active policy
            for policy_data in self.current_state["active_policies"]:
                policy = policy_data["policy"]
                result = self._check_policy_compliance(
                    policy,
                    analysis
                )
                compliance_results.append(result)
                
            # Calculate overall compliance
            if np is not None:
                overall_compliance = float(np.mean([
                    r["compliance_score"]
                    for r in compliance_results
                ]))
            else:
                overall_compliance = float(sum(r["compliance_score"] for r in compliance_results)/len(compliance_results)) if compliance_results else 0.0
            
            return {
                "status": "compliant" if overall_compliance >= self.ethics_threshold else "non_compliant",
                "overall_score": overall_compliance,
                "results": compliance_results,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error checking compliance: {e}")
            return {"status": "error", "message": str(e)}
            
    def _make_decision(self, compliance: Dict[str, Any]) -> Dict[str, Any]:
        """Make ethical decision based on compliance results"""
        try:
            decision = {
                "allowed": compliance["status"] == "compliant",
                "score": compliance["overall_score"],
                "rationale": self._generate_rationale(compliance),
                "recommendations": self._generate_recommendations(compliance),
                "timestamp": datetime.now().isoformat()
            }
            
            # Update state
            self.current_state["ethical_score"] = compliance["overall_score"]
            self.current_state["recent_decisions"].append({
                "decision": decision["allowed"],
                "score": decision["score"],
                "timestamp": decision["timestamp"]
            })
            
            # Trim recent decisions
            if len(self.current_state["recent_decisions"]) > 10:
                self.current_state["recent_decisions"] = self.current_state["recent_decisions"][-10:]
                
            return decision
            
        except Exception as e:
            logger.error(f"Error making decision: {e}")
            return {"allowed": False, "error": str(e)}
            
    def _update_memory(self, analysis: Dict[str, Any], decision: Dict[str, Any]):
        """Update ethical memory with new analysis"""
        try:
            memory_entry = {
                "analysis": analysis,
                "decision": decision,
                "timestamp": datetime.now().isoformat()
            }
            
            self.ethical_memory.append(memory_entry)
            
            # Trim memory if needed
            if len(self.ethical_memory) > self.memory_size:
                self.ethical_memory = self.ethical_memory[-self.memory_size:]
                
        except Exception as e:
            logger.error(f"Error updating memory: {e}")
            
    def _validate_policy(self, policy: Dict[str, Any]) -> bool:
        """Validate a new policy"""
        try:
            required_fields = ["name", "description", "criteria"]
            
            # Check required fields
            if not all(field in policy for field in required_fields):
                return False
                
            # Validate criteria structure
            if not isinstance(policy["criteria"], (list, dict)):
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Error validating policy: {e}")
            return False
            
    def _analyze_scenario(self,
                         scenario: Dict[str, Any],
                         context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze an ethical scenario"""
        try:
            # Extract scenario components
            components = self._extract_scenario_components(scenario)
            
            # Analyze stakeholder impact
            stakeholder_impact = self._analyze_stakeholder_impact(components)
            
            # Consider context
            context_factors = self._analyze_context(context)
            
            return {
                "components": components,
                "stakeholder_impact": stakeholder_impact,
                "context_factors": context_factors,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing scenario: {e}")
            return {}
            
    def _extract_ethical_features(self, content: Any) -> Dict[str, Any]:
        """Extract ethically relevant features from content"""
        features = {}
        try:
            if isinstance(content, dict):
                features = self._extract_dict_features(content)
            elif isinstance(content, str):
                features = self._extract_text_features(content)
            else:
                features = self._extract_generic_features(content)
                
        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            
        return features
        
    def _analyze_context(self, context: Optional[Dict[str, Any]]) -> Dict[str, float]:
        """Analyze ethical context"""
        try:
            if not context:
                return {"impact": 0.5, "confidence": 0.5}
                
            # Extract context features
            features = self._extract_ethical_features(context)
            
            # Calculate impact
            if np is not None:
                impact = float(np.mean([
                    self._evaluate_feature_impact(feature)
                    for feature in features.values()
                ]))
            else:
                vals = [self._evaluate_feature_impact(feature) for feature in features.values()]
                impact = float(sum(vals)/len(vals)) if vals else 0.0
            
            return {
                "impact": impact,
                "confidence": min(1.0, len(features) / 10)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing context: {e}")
            return {"impact": 0.5, "confidence": 0.0}
            
    def _evaluate_principles(self,
                           features: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate features against ethical principles"""
        scores = {}
        try:
            for principle, data in self.ethical_principles.items():
                score = self._evaluate_principle_compliance(
                    principle,
                    features,
                    data["weight"]
                )
                scores[principle] = score
                
        except Exception as e:
            logger.error(f"Error evaluating principles: {e}")
            
        return scores
        
    def _check_policy_compliance(self,
                               policy: Dict[str, Any],
                               analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Check compliance with a specific policy"""
        try:
            criteria_results = []
            
            # Check each criterion
            for criterion in policy["criteria"]:
                result = self._evaluate_criterion(criterion, analysis)
                criteria_results.append(result)
                
            # Calculate compliance score
            compliance_score = np.mean([
                r["score"] for r in criteria_results
            ]) if np is not None else sum(r["score"] for r in criteria_results) / len(criteria_results) if criteria_results else 0.0
            
            return {
                "policy_name": policy["name"],
                "compliance_score": compliance_score,
                "criteria_results": criteria_results,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error checking policy compliance: {e}")
            return {
                "policy_name": policy.get("name", "unknown"),
                "compliance_score": 0.0,
                "error": str(e)
            }
            
    def _generate_rationale(self, compliance: Dict[str, Any]) -> List[str]:
        """Generate rationale for ethical decision"""
        rationale = []
        try:
            # Add overall compliance statement
            rationale.append(
                f"Overall ethical compliance: {compliance['overall_score']:.2f}"
            )
            
            # Add specific policy results
            for result in compliance.get("results", []):
                if result["compliance_score"] < self.ethics_threshold:
                    rationale.append(
                        f"Policy '{result['policy_name']}' needs attention "
                        f"(score: {result['compliance_score']:.2f})"
                    )
                    
        except Exception as e:
            logger.error(f"Error generating rationale: {e}")
            rationale.append("Error generating detailed rationale")
            
        return rationale
        
    def _apply_principles(self,
                         analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Apply ethical principles to analysis"""
        try:
            # Calculate principle scores
            scores = {}
            concerns = []
            
            for principle, data in self.ethical_principles.items():
                score = self._evaluate_principle_impact(
                    principle,
                    analysis,
                    data["weight"]
                )
                scores[principle] = score
                
                if score < self.ethics_threshold:
                    concerns.append(f"Low {principle} score: {score:.2f}")
                    
            # Calculate overall score
            if np is not None:
                overall_score = float(np.average(
                    list(scores.values()),
                    weights=[d["weight"] for d in self.ethical_principles.values()]
                ))
            else:
                vals = list(scores.values())
                weights = [d["weight"] for d in self.ethical_principles.values()]
                total_w = sum(weights)
                overall_score = float(sum(v*w for v,w in zip(vals, weights))/total_w) if total_w else 0.0
            
            return {
                "score": overall_score,
                "principle_scores": scores,
                "concerns": concerns,
                "confidence": self._calculate_confidence(scores),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error applying principles: {e}")
            return {
                "score": 0.0,
                "principle_scores": {},
                "concerns": ["Error in principle application"],
                "confidence": 0.0
            }
            
    def _generate_recommendations(self,
                                evaluation: Dict[str, Any]) -> List[str]:
        """Generate ethical recommendations"""
        recommendations = []
        try:
            # Generate based on compliance level
            if isinstance(evaluation.get("overall_score"), (int, float)):
                score = evaluation["overall_score"]
                if score < self.ethics_threshold:
                    recommendations.extend(
                        self._generate_improvement_recommendations(evaluation)
                    )
                    
            # Add principle-specific recommendations
            if "principle_scores" in evaluation:
                for principle, score in evaluation["principle_scores"].items():
                    if score < self.ethics_threshold:
                        recommendations.extend(
                            self._get_principle_recommendations(principle)
                        )
                        
            # Prioritize and limit recommendations
            recommendations = sorted(
                recommendations,
                key=lambda x: len(x)
            )[:5]  # Limit to top 5
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            recommendations.append(
                "Unable to generate specific recommendations"
            )
            
        return recommendations
        
    def _evaluate_criterion(self,
                          criterion: Dict[str, Any],
                          analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate a single policy criterion"""
        try:
            criterion_type = criterion.get("type", "")
            
            if criterion_type == "threshold":
                score = self._evaluate_threshold_criterion(criterion, analysis)
            elif criterion_type == "pattern":
                score = self._evaluate_pattern_criterion(criterion, analysis)
            else:
                score = 0.0
                
            return {
                "criterion_name": criterion.get("name", "unnamed"),
                "score": score,
                "type": criterion_type,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error evaluating criterion: {e}")
            return {"score": 0.0, "error": str(e)}
            
    def _evaluate_principle_impact(self,
                                 principle: str,
                                 analysis: Dict[str, Any],
                                 weight: float) -> float:
        """Evaluate impact on a specific ethical principle"""
        try:
            # Get relevant components
            components = analysis.get("components", {})
            stakeholder_impact = analysis.get("stakeholder_impact", {})
            
            # Calculate base score
            base_score = self._calculate_principle_score(
                principle,
                components
            )
            
            # Adjust for stakeholder impact
            stakeholder_factor = stakeholder_impact.get(
                principle,
                0.5  # Neutral if not specified
            )
            
            # Apply weight
            weighted_score = (base_score + stakeholder_factor) / 2 * weight
            
            return min(1.0, max(0.0, weighted_score))
            
        except Exception as e:
            logger.error(f"Error evaluating principle impact: {e}")
            return 0.0
            
    def _evaluate_feature_impact(self, feature: Any) -> float:
        """Evaluate ethical impact of a feature"""
        try:
            if isinstance(feature, (int, float)):
                return min(1.0, abs(feature))
            elif isinstance(feature, str):
                return len(feature) / 100  # Normalize
            else:
                return 0.5  # Neutral for unknown types
                
        except Exception as e:
            logger.error(f"Error evaluating feature impact: {e}")
            return 0.0
            
    def _calculate_confidence(self, scores: Dict[str, float]) -> float:
        """Calculate confidence in ethical evaluation"""
        try:
            if not scores:
                return 0.0
                
            # Calculate based on score consistency
            values = list(scores.values())
            consistency = 1.0 - np.std(values) if np is not None else 1.0 - sum((x - (sum(values)/len(values))) ** 2 for x in values) / len(values) if values else 0.0
            coverage = len(scores) / len(self.ethical_principles)
            
            return min(1.0, (consistency + coverage) / 2)
            
        except Exception as e:
            logger.error(f"Error calculating confidence: {e}")
            return 0.0
            
    def _extract_scenario_components(self,
                                   scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Extract components from an ethical scenario"""
        components = {}
        try:
            # Extract actions
            if "actions" in scenario:
                components["actions"] = self._analyze_actions(scenario["actions"])
                
            # Extract consequences
            if "consequences" in scenario:
                components["consequences"] = self._analyze_consequences(
                    scenario["consequences"]
                )
                
            # Extract stakeholders
            if "stakeholders" in scenario:
                components["stakeholders"] = self._analyze_stakeholders(
                    scenario["stakeholders"]
                )
                
        except Exception as e:
            logger.error(f"Error extracting scenario components: {e}")
            
        return components
        
    def _analyze_stakeholder_impact(self,
                                  components: Dict[str, Any]) -> Dict[str, float]:
        """Analyze impact on stakeholders"""
        impact = {}
        try:
            stakeholders = components.get("stakeholders", {})
            consequences = components.get("consequences", {})
            
            for stakeholder, data in stakeholders.items():
                impact[stakeholder] = self._calculate_stakeholder_impact(
                    stakeholder,
                    data,
                    consequences
                )
                
        except Exception as e:
            logger.error(f"Error analyzing stakeholder impact: {e}")
            
        return impact
        
    def _generate_improvement_recommendations(self,
                                           evaluation: Dict[str, Any]) -> List[str]:
        """Generate recommendations for ethical improvements"""
        recommendations = []
        try:
            if "principle_scores" in evaluation:
                for principle, score in evaluation["principle_scores"].items():
                    if score < self.ethics_threshold:
                        recommendations.extend(
                            self._get_principle_recommendations(principle)
                        )
                        
        except Exception as e:
            logger.error(f"Error generating improvement recommendations: {e}")
            
        return recommendations
        
    def get_state(self) -> Dict[str, Any]:
        """Get current state of the ethical governance system"""
        return self.current_state.copy()
        
    def get_memory(self) -> List[Dict[str, Any]]:
        """Get ethical memory"""
        return self.ethical_memory.copy()
        
    def get_violation_history(self) -> List[Dict[str, Any]]:
        """Get history of policy violations"""
        return self.policy_violations.copy()