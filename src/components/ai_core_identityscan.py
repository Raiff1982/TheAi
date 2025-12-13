"""Lightweight AI core for identity scanning and analysis.

This module provides a compact, dependency-safe `AICore` class used by
other components. The original file contained merge markers and
incomplete code; this replacement focuses on providing functioning
interfaces (async `generate_response`, `shutdown`) and uses existing
local components where available.
"""
from typing import Any, Dict, List, Optional
import asyncio
import json
import logging
import os

from components.multimodal_analyzer import MultimodalAnalyzer
from components.dynamic_learning import DynamicLearner
from components.health_monitor import HealthMonitor

try:
    from utils.logger import logger
except Exception:
    logger = logging.getLogger(__name__)


class AICore:
    """Minimal, safe AICore replacement for identity scanning workflows."""

    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.multimodal = MultimodalAnalyzer()
        self.learner = DynamicLearner()
        self.health = HealthMonitor()
        self._initialized = False

    def _load_config(self, path: str) -> Dict[str, Any]:
        if not path or not os.path.exists(path):
            return {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    async def initialize(self) -> bool:
        """Initialize async subsystems (e.g., health monitor)."""
        try:
            ok = await self.health.initialize()
            self._initialized = ok
            return ok
        except Exception as e:
            logger.exception("Failed to initialize AICore: %s", e)
            return False

    async def generate_response(self, user_id: int, query: str, multimodal_input: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Produce a safe, explainable response using local subsystems.

        - Runs a lightweight analysis of any multimodal input
        - Updates the dynamic learner with a summary of the interaction
        - Returns a dict containing analysis and a text response
        """
        try:
            analyses = {}
            if multimodal_input:
                analyses = self.multimodal.analyze_content(multimodal_input)

            # Simple content-based reply
            text_summary = ""
            if "text" in analyses:
                t = analyses["text"]
                text_summary = f"Received text: length={t.get('length')} words={t.get('word_count')}"
            else:
                text_summary = f"Query received: {query[:200]}"

            # Update learner with a compact interaction record
            adaptation_score = self.learner.update({
                "user_id": user_id,
                "query_summary": text_summary,
                "multimodal_modalities": list(analyses.keys())
            })

            # Health snapshot
            health_status = self.health.get_health_summary()

            response_text = f"Acknowledged. Adaptation score={adaptation_score:.2f}."

            return {
                "response": response_text,
                "analysis": analyses,
                "adaptation_score": adaptation_score,
                "health": health_status,
            }
        except Exception as e:
            logger.exception("generate_response failed: %s", e)
            return {"error": "internal_error", "detail": str(e)}

    async def shutdown(self):
        """Clean up resources if necessary."""
        # HealthMonitor has no async shutdown but we keep the method for parity.
        await asyncio.sleep(0)


# Module quick test when run directly
if __name__ == "__main__":
    async def _test():
        core = AICore()
        await core.initialize()
        out = await core.generate_response(1, "Hello world", {"text": "Hello world from test"})
        print(out)
        await core.shutdown()

    asyncio.run(_test())