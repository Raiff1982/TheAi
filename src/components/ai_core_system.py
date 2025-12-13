"""Simplified AI core system

This module provides a compact, dependency-safe `AICore` used across the
project. The original file contained duplicated content and heavy
dependencies; this replacement offers a minimal, testable interface.
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
    """Minimal, safe AICore for system integration and testing."""

    def __init__(self, config_path: str = "config/ai_assistant_config.json"):
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
        try:
            ok = await self.health.initialize()
            self._initialized = ok
            return ok
        except Exception as e:
            logger.exception("Failed to initialize AICore: %s", e)
            return False

    async def generate_response(self, user_id: int, query: str, multimodal_input: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            analyses = self.multimodal.analyze_content(multimodal_input or {}) if multimodal_input else {}
            summary = analyses.get("text", {}).get("word_count") if analyses else None
            adaptation_score = self.learner.update({"user_id": user_id, "query": query, "summary_word_count": summary})
            health_status = self.health.get_health_summary()
            response_text = f"OK. Adaptation={adaptation_score:.2f}."
            return {"response": response_text, "analysis": analyses, "adaptation_score": adaptation_score, "health": health_status}
        except Exception as e:
            logger.exception("generate_response failed: %s", e)
            return {"error": "internal_error", "detail": str(e)}

    async def shutdown(self):
        await asyncio.sleep(0)


if __name__ == "__main__":
    async def _test():
        core = AICore()
        await core.initialize()
        out = await core.generate_response(1, "Hello from core", {"text": "Hello"})
        print(out)
        await core.shutdown()
    asyncio.run(_test())
