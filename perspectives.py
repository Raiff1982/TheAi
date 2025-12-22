"""
Codette Perspectives - Multi-perspective AI reasoning
FIXED VERSION: No randomness - uses stable deterministic responses
"""

import logging
from typing import Dict, Any, Optional
from warnings import warn

# Import stable responder
try:
    from codette_stable_responder import (
        get_stable_responder,
        PerspectiveType,
        select_perspectives,
    )
    STABLE_RESPONDER_AVAILABLE = True
except ImportError:
    STABLE_RESPONDER_AVAILABLE = False
    logging.warning("⚠️ Stable responder not available, perspectives will be disabled")

logger = logging.getLogger(__name__)


class Perspectives:
    """Multi-perspective reasoning engine (STABLE VERSION)"""

    def __init__(self) -> None:
        """Initialize perspectives with stable responses.
        
        This class uses a stable deterministic approach to generate responses.
        The stable responder is used when available, and if not available,
        the perspectives are disabled.
        """
        self.stable_responder = get_stable_responder() if STABLE_RESPONDER_AVAILABLE else None
        if self.stable_responder:
            logger.info("✅ Perspectives engine initialized (stable mode)")
        else:
            logger.warning("⚠️ Perspectives engine initialized WITHOUT stable responder")

    def respond_stable(self, text: str) -> Dict[str, Any]:
        """
        Generate stable multi-perspective response
        NO RANDOMNESS - Same text always gets same response
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dict containing perspectives or error message
        """
        if not self.stable_responder:
            logger.debug("Stable responder not available, returning error")
            return {"error": "Stable responder not available"}

        logger.debug(f"Generating stable response for text: {text[:50]}...")
        response = self.stable_responder.generate_response(text)
        logger.debug(f"Generated {len(response.get('perspectives', []))} perspective(s)")
        return response

    # Legacy methods (deprecated but maintained for backwards compatibility)
    def neuralNetworkPerspective(self, text: str) -> str:
        """DEPRECATED: Use respond_stable() instead"""
        warn("neuralNetworkPerspective() is deprecated. Use respond_stable()", DeprecationWarning, stacklevel=2)
        logger.debug("Legacy method neuralNetworkPerspective called")
        response = self._generate_response(text)
        if response.get("perspectives"):
            return f"[Neural Analysis] {response['perspectives'][0]['response']}"
        return "[Neural Analysis] Unable to process"

    def newtonianLogic(self, text: str) -> str:
        """DEPRECATED: Use respond_stable() instead"""
        warn("newtonianLogic() is deprecated. Use respond_stable()", DeprecationWarning, stacklevel=2)
        logger.debug("Legacy method newtonianLogic called")
        response = self._generate_response(text)
        if response.get("perspectives"):
            for p in response["perspectives"]:
                if "technical" in p.get("perspective", ""):
                    return f"[Reason] {p['response']}"
        return "[Reason] Unable to process"

    def daVinciSynthesis(self, text: str) -> str:
        """DEPRECATED: Use respond_stable() instead"""
        warn("daVinciSynthesis() is deprecated. Use respond_stable()", DeprecationWarning, stacklevel=2)
        logger.debug("Legacy method daVinciSynthesis called")
        response = self._generate_response(text)
        if response.get("perspectives"):
            for p in response["perspectives"]:
                if "creative" in p.get("perspective", ""):
                    return f"[Dream] {p['response']}"
        return "[Dream] Unable to process"

    def resilientKindness(self, text: str) -> str:
        """DEPRECATED: Use respond_stable() instead"""
        warn("resilientKindness() is deprecated. Use respond_stable()", DeprecationWarning, stacklevel=2)
        logger.debug("Legacy method resilientKindness called")
        response = self._generate_response(text)
        if response.get("perspectives"):
            return f"[Ethics] {response['perspectives'][0]['response']}"
        return "[Ethics] Unable to process"

    def quantumLogicPerspective(self, text: str) -> str:
        """DEPRECATED: Use respond_stable() instead"""
        warn("quantumLogicPerspective() is deprecated. Use respond_stable()", DeprecationWarning, stacklevel=2)
        logger.debug("Legacy method quantumLogicPerspective called")
        response = self._generate_response(text)
        if response.get("perspectives"):
            return f"[Quantum] {response['perspectives'][0]['response']}"
        return "[Quantum] Unable to process"

    def get_status(self) -> Dict[str, Any]:
        """Get perspective engine status
        
        Returns:
            Dict containing:
                - status: Engine operational status
                - mode: Operating mode (stable)
                - randomness: Randomness elimination status
                - responder_available: Whether stable responder is loaded
                - cache_stats: Cache statistics from responder
        """
        status_dict = {
            "status": "active" if self.stable_responder else "degraded",
            "mode": "stable",
            "randomness": "eliminated",
            "responder_available": bool(self.stable_responder),
            "cache_stats": (
                self.stable_responder.get_cache_stats() if self.stable_responder else {}
            ),
        }
        logger.debug(f"Status check: responder_available={status_dict['responder_available']}")
        return status_dict
