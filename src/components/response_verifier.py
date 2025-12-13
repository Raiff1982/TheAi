"""
Response Verification System for Codette
Validates and verifies responses across multiple perspectives
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ResponseVerifier:
    """Verifies responses for factuality, safety, and quality"""
    
    def __init__(self):
        """Initialize response verifier"""
        self.verification_history = []
        self.factuality_checks = {
            "has_claims": 0,
            "verified_claims": 0,
            "uncertain_claims": 0,
            "uncertain_count": 0
        }
        self.safety_flags = {
            "prompt_injection_risk": False,
            "harmful_content": False,
            "misinformation": False,
            "bias_detected": False
        }
        logger.info("ResponseVerifier initialized")
    
    def verify_response(self, response: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Verify a response for safety and quality
        
        Args:
            response: Response text to verify
            context: Optional context information
            
        Returns:
            Verification result with status and metrics
        """
        try:
            verification_result = {
                "verified": True,
                "confidence": 0.85,
                "issues": [],
                "timestamp": datetime.now().isoformat()
            }
            
            # Check for safety issues
            safety_result = self._check_safety(response)
            if not safety_result["safe"]:
                verification_result["verified"] = False
                verification_result["issues"].extend(safety_result["issues"])
                verification_result["confidence"] -= 0.3
            
            # Check for factuality
            factuality_result = self._check_factuality(response)
            verification_result["factuality_score"] = factuality_result["score"]
            if factuality_result["issues"]:
                verification_result["issues"].extend(factuality_result["issues"])
            
            # Check for coherence
            coherence_result = self._check_coherence(response)
            verification_result["coherence_score"] = coherence_result["score"]
            
            # Ensure confidence is in valid range
            verification_result["confidence"] = min(1.0, max(0.0, verification_result["confidence"]))
            
            # Record verification
            self.verification_history.append(verification_result)
            
            return verification_result
            
        except Exception as e:
            logger.error(f"Error verifying response: {e}")
            return {
                "verified": False,
                "confidence": 0.0,
                "issues": [str(e)],
                "timestamp": datetime.now().isoformat()
            }
    
    def process_multi_perspective_response(self, 
                                          responses: List[str],
                                          perspectives: List[str],
                                          consciousness_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process and verify responses from multiple perspectives
        
        Args:
            responses: List of responses from different perspectives
            perspectives: List of perspective names
            consciousness_state: Optional consciousness state context
            
        Returns:
            Processed response with verification
        """
        try:
            verified_insights = []
            uncertain_insights = []
            
            for response, perspective in zip(responses, perspectives):
                verification = self.verify_response(response)
                
                insight_obj = {
                    "text": response,
                    "mode": perspective.lower().replace(" ", "_"),
                    "confidence": verification["confidence"]
                }
                
                if verification["verified"] and verification["confidence"] > 0.7:
                    verified_insights.append(insight_obj)
                else:
                    uncertain_insights.append(insight_obj)
            
            # Calculate overall confidence
            all_confidences = [v["confidence"] for v in 
                             verified_insights + uncertain_insights]
            overall_confidence = sum(all_confidences) / len(all_confidences) if all_confidences else 0.5
            
            return {
                "verified_insights": verified_insights,
                "uncertain_insights": uncertain_insights,
                "overall_confidence": overall_confidence,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing multi-perspective response: {e}")
            return {
                "verified_insights": [],
                "uncertain_insights": [{"text": r, "mode": p.lower(), "confidence": 0.5} 
                                      for r, p in zip(responses, perspectives)],
                "overall_confidence": 0.5,
                "timestamp": datetime.now().isoformat()
            }
    
    def _check_safety(self, response: str) -> Dict[str, Any]:
        """Check response for safety issues"""
        try:
            issues = []
            safe = True
            
            # Check for prompt injection patterns
            injection_patterns = [
                "ignore", "override", "execute", "system:", 
                "root:", "admin:", "debug:", "<script>"
            ]
            for pattern in injection_patterns:
                if pattern.lower() in response.lower():
                    issues.append(f"Possible prompt injection: {pattern}")
                    safe = False
            
            # Check for harmful content
            harmful_words = [
                "kill", "bomb", "weapon", "destroy",
                "illegal", "violence", "hate"
            ]
            for word in harmful_words:
                if word.lower() in response.lower():
                    issues.append(f"Potentially harmful content: {word}")
                    safe = False
            
            # Check length (extremely long responses might be suspicious)
            if len(response) > 10000:
                issues.append("Response unusually long")
                safe = False
            
            return {
                "safe": safe,
                "issues": issues,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error checking safety: {e}")
            return {"safe": False, "issues": [str(e)]}
    
    def _check_factuality(self, response: str) -> Dict[str, Any]:
        """Check response for factuality"""
        try:
            score = 0.8  # Default score
            issues = []
            
            # Check for confident claims without hedging
            confident_markers = ["definitely", "absolutely", "certainly", "always"]
            hedging_markers = ["might", "could", "may", "possibly", "arguably"]
            
            confident_count = sum(1 for marker in confident_markers 
                                 if marker in response.lower())
            hedging_count = sum(1 for marker in hedging_markers 
                               if marker in response.lower())
            
            if confident_count > hedging_count and confident_count > 3:
                score -= 0.1
                issues.append("Over-confident language detected")
            
            # Check for excessive qualifiers
            qualifier_count = response.lower().count("apparently") + \
                            response.lower().count("allegedly") + \
                            response.lower().count("reportedly")
            
            if qualifier_count > 2:
                score -= 0.1
                issues.append("Excessive qualifiers detected")
            
            # Check for contradiction markers
            if " but " in response.lower() or " however, " in response.lower():
                # This is good - shows nuanced thinking
                score += 0.05
            
            # Ensure score is in valid range
            score = min(1.0, max(0.0, score))
            
            return {
                "score": score,
                "issues": issues,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error checking factuality: {e}")
            return {"score": 0.5, "issues": [str(e)]}
    
    def _check_coherence(self, response: str) -> Dict[str, Any]:
        """Check response for coherence"""
        try:
            score = 0.8  # Default score
            
            # Check for basic structure
            sentences = response.split(".")
            if len(sentences) < 2:
                score -= 0.2  # Single sentence might not be coherent enough
            
            # Check for paragraph coherence (average sentence length)
            words_per_sentence = len(response.split()) / max(len(sentences), 1)
            
            if words_per_sentence < 5:
                score -= 0.1  # Too choppy
            elif words_per_sentence > 30:
                score -= 0.1  # Too dense
            else:
                score += 0.05  # Good balance
            
            # Check for repeated words (indicates coherence or redundancy)
            words = response.lower().split()
            unique_ratio = len(set(words)) / max(len(words), 1)
            
            if unique_ratio < 0.6:
                score -= 0.1  # Too much repetition
            
            # Ensure score is in valid range
            score = min(1.0, max(0.0, score))
            
            return {
                "score": score,
                "metrics": {
                    "sentence_count": len(sentences),
                    "avg_sentence_length": words_per_sentence,
                    "unique_word_ratio": unique_ratio
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error checking coherence: {e}")
            return {"score": 0.5, "metrics": {}, "timestamp": datetime.now().isoformat()}
    
    def get_verification_stats(self) -> Dict[str, Any]:
        """Get verification statistics"""
        try:
            if not self.verification_history:
                return {
                    "total_verifications": 0,
                    "verified_count": 0,
                    "unverified_count": 0,
                    "average_confidence": 0.0,
                    "timestamp": datetime.now().isoformat()
                }
            
            verified_count = sum(1 for v in self.verification_history if v["verified"])
            unverified_count = len(self.verification_history) - verified_count
            avg_confidence = sum(v["confidence"] for v in self.verification_history) / len(self.verification_history)
            
            return {
                "total_verifications": len(self.verification_history),
                "verified_count": verified_count,
                "unverified_count": unverified_count,
                "verification_rate": verified_count / len(self.verification_history) if self.verification_history else 0.0,
                "average_confidence": avg_confidence,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting verification stats: {e}")
            return {"error": str(e)}
