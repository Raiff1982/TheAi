from typing import Dict, Any, List, Optional
from knowledge_base.grounding_truth import GroundingTruth
import logging

logger = logging.getLogger(__name__)

class ResponseVerifier:
    """Verifies responses using grounding truth while preserving multi-perspective analysis"""
    
    def __init__(self):
        self.grounding_truth = GroundingTruth()
        self.mode_confidence_thresholds = {
            "scientific": 0.9,
            "creative": 0.7,
            "emotional": 0.6,
            "quantum": 0.8,
            "philosophical": 0.7
        }
        
    def verify_insight(
        self, 
        insight: str, 
        mode: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Verify a single insight from a specific perspective mode
        
        Args:
            insight: The insight to verify
            mode: The perspective mode that generated it
            context: Optional additional context
            
        Returns:
            Dict containing verification results and confidence
        """
        verification = self.grounding_truth.verify_statement(insight, context)
        confidence_threshold = self.mode_confidence_thresholds.get(mode, 0.7)
        
        # Adjust verification based on mode characteristics
        if mode == "creative":
            # Allow more speculative statements in creative mode
            verification["confidence"] *= 1.2
        elif mode == "quantum":
            # Account for quantum uncertainty
            verification["confidence"] = max(
                verification["confidence"],
                0.5  # Quantum superposition baseline
            )
            
        return {
            "verified": verification["verified"] or verification["confidence"] >= confidence_threshold,
            "confidence": verification["confidence"],
            "mode": mode,
            "original_insight": insight,
            "requires_qualifier": verification["confidence"] < confidence_threshold
        }
        
    def process_multi_perspective_response(
        self,
        insights: List[str],
        modes: List[str],
        consciousness_state: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process and verify a multi-perspective response
        
        Args:
            insights: List of insights from different perspectives
            modes: List of perspective modes that generated the insights
            consciousness_state: Optional consciousness state info
            
        Returns:
            Processed response with verification metadata
        """
        verified_insights = []
        uncertain_insights = []
        
        for insight, mode in zip(insights, modes):
            result = self.verify_insight(
                insight, 
                mode, 
                {"consciousness": consciousness_state} if consciousness_state else None
            )
            
            if result["verified"]:
                verified_insights.append({
                    "text": result["original_insight"],
                    "mode": mode,
                    "confidence": result["confidence"]
                })
            else:
                qualified_insight = self._add_qualifier(
                    result["original_insight"],
                    result["confidence"],
                    mode
                )
                uncertain_insights.append({
                    "text": qualified_insight,
                    "mode": mode,
                    "confidence": result["confidence"]
                })
                
        return {
            "verified_insights": verified_insights,
            "uncertain_insights": uncertain_insights,
            "overall_confidence": self._calculate_overall_confidence(
                verified_insights, uncertain_insights
            )
        }
        
    def _add_qualifier(self, insight: str, confidence: float, mode: str) -> str:
        """Add appropriate qualifier based on confidence and mode"""
        base_qualifier = self._get_base_qualifier(confidence)
        mode_specific = self._get_mode_qualifier(mode)
        
        if mode_specific:
            return f"{base_qualifier} {insight} ({mode_specific})"
        return f"{base_qualifier} {insight}"
        
    def _get_base_qualifier(self, confidence: float) -> str:
        """Get base confidence qualifier"""
        if confidence >= 0.8:
            return "Evidence suggests that"
        elif confidence >= 0.6:
            return "It appears that"
        elif confidence >= 0.4:
            return "It seems possible that"
        elif confidence >= 0.2:
            return "There is a speculation that"
        else:
            return "There is an unverified hypothesis that"
            
    def _get_mode_qualifier(self, mode: str) -> Optional[str]:
        """Get mode-specific qualifier"""
        qualifiers = {
            "scientific": "based on available data",
            "creative": "from a creative perspective",
            "emotional": "from an emotional standpoint",
            "quantum": "considering quantum possibilities",
            "philosophical": "from a philosophical view"
        }
        return qualifiers.get(mode)
        
    def _calculate_overall_confidence(
        self,
        verified: List[Dict[str, Any]],
        uncertain: List[Dict[str, Any]]
    ) -> float:
        """Calculate overall response confidence"""
        if not verified and not uncertain:
            return 0.0
            
        total_insights = len(verified) + len(uncertain)
        confidence_sum = sum(v["confidence"] for v in verified)
        confidence_sum += sum(u["confidence"] for u in uncertain)
        
        return confidence_sum / total_insights