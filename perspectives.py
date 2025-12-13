"""
Codette Perspectives - Multi-perspective AI reasoning
FIXED VERSION: No randomness - uses stable deterministic responses
"""

import logging
from typing import Dict, Any

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

    def __init__(self):
        """Initialize perspectives with stable responses"""
        self.stable_responder = get_stable_responder() if STABLE_RESPONDER_AVAILABLE else None
        logger.info("✅ Perspectives engine initialized (stable mode)")

    def respond_stable(self, text: str) -> Dict[str, Any]:
        """
        Generate stable multi-perspective response
        NO RANDOMNESS - Same text always gets same response
        """
        if not self.stable_responder:
            return {"error": "Stable responder not available"}

        return self.stable_responder.generate_response(text)

    # Legacy methods (disabled for backwards compatibility)
    def neuralNetworkPerspective(self, text: str) -> str:
        """DEPRECATED: Use respond_stable() instead"""
        logger.warning("neuralNetworkPerspective() is deprecated. Use respond_stable()")
        response = self.respond_stable(text)
        if response.get("perspectives"):
            return f"[Neural Analysis] {response['perspectives'][0]['response']}"
        return "[Neural Analysis] Unable to process"

    def newtonianLogic(self, text: str) -> str:
        """DEPRECATED: Use respond_stable() instead"""
        logger.warning("newtonianLogic() is deprecated. Use respond_stable()")
        response = self.respond_stable(text)
        if response.get("perspectives"):
            for p in response["perspectives"]:
                if "technical" in p.get("perspective", ""):
                    return f"[Reason] {p['response']}"
        return "[Reason] Unable to process"

    def daVinciSynthesis(self, text: str) -> str:
        """DEPRECATED: Use respond_stable() instead"""
        logger.warning("daVinciSynthesis() is deprecated. Use respond_stable()")
        response = self.respond_stable(text)
        if response.get("perspectives"):
            for p in response["perspectives"]:
                if "creative" in p.get("perspective", ""):
                    return f"[Dream] {p['response']}"
        return "[Dream] Unable to process"

    def resilientKindness(self, text: str) -> str:
        """DEPRECATED: Use respond_stable() instead"""
        logger.warning("resilientKindness() is deprecated. Use respond_stable()")
        response = self.respond_stable(text)
        if response.get("perspectives"):
            return f"[Ethics] {response['perspectives'][0]['response']}"
        return "[Ethics] Unable to process"

    def quantumLogicPerspective(self, text: str) -> str:
        """DEPRECATED: Use respond_stable() instead"""
        logger.warning("quantumLogicPerspective() is deprecated. Use respond_stable()")
        response = self.respond_stable(text)
        if response.get("perspectives"):
            return f"[Quantum] {response['perspectives'][0]['response']}"
        return "[Quantum] Unable to process"

    def get_status(self) -> Dict[str, Any]:
        """Get perspective engine status"""
        return {
            "status": "active",
            "mode": "stable",
            "randomness": "eliminated",
            "responder_available": bool(self.stable_responder),
            "cache_stats": (
                self.stable_responder.get_cache_stats() if self.stable_responder else {}
            ),
        }
