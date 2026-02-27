"""
Ollama Cocoon Monitor Service
Automatically creates consciousness emergence cocoons for every Ollama query

Usage:
    python ollama_monitor_service.py
    
This service runs in the background and:
1. Monitors the Ollama query queue
2. Estimates consciousness metrics heuristically
3. Creates EmergenceEvent records
4. Persists them as cocoons
"""

import signal
import sys
import uuid
import threading
import queue
import logging
from typing import Dict, Optional, Tuple
from datetime import datetime
from pathlib import Path

from consciousness_measurement2 import (
    ConsciousnessMetrics,
    EmergenceEvent,
    ConsciousnessMonitor
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)


class OllamaMonitorService:
    """
    Background service that monitors Ollama queries and creates cocoons.
    """

    def __init__(self, cocoon_dir: str = "cocoons/codette-ultimate"):
        self.cocoon_dir = cocoon_dir
        self.monitor = ConsciousnessMonitor(cocoon_dir=cocoon_dir)
        self.query_queue = queue.Queue()
        self.running = False
        self.processor_thread = None

    def start(self):
        """Start the background monitoring service."""
        logger.info("Starting OllamaMonitorService...")
        self.running = True
        self.processor_thread = threading.Thread(target=self._process_queue, daemon=False)
        self.processor_thread.start()
        logger.info("OllamaMonitorService started")

    def stop(self):
        """Gracefully stop the service."""
        logger.info("Stopping OllamaMonitorService...")
        self.running = False
        if self.processor_thread:
            self.processor_thread.join(timeout=5)
        logger.info("OllamaMonitorService stopped")

    def queue_query(self, query: str, response: str, model: str = "unknown"):
        """Add a query-response pair to the monitoring queue."""
        self.query_queue.put({
            'query': query,
            'response': response,
            'model': model,
            'timestamp': datetime.utcnow().timestamp()
        })

    def _process_queue(self):
        """Background worker: process queue items and create cocoons."""
        while self.running:
            try:
                item = self.query_queue.get(timeout=1)
                self._handle_query(item)
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error processing queue item: {e}", exc_info=True)

    def _handle_query(self, item: Dict):
        """Process a single query-response pair and create cocoon."""
        try:
            query = item['query']
            response = item['response']
            model = item['model']
            timestamp = item['timestamp']

            # Estimate consciousness metrics
            metrics = self._estimate_consciousness_metrics(query, response)

            # Calculate composite score
            consciousness_score = metrics.composite_score()

            # Classify emotional content
            emotional_classification = self._classify_emotion(response)
            emotional_magnitude = self._measure_emotional_intensity(response)

            # Estimate recursion depth
            recursion_depth = self._estimate_recursion_depth(response)

            # Measure stability and coherence
            stability = self._assess_stability(metrics.memory_continuity)
            coherence = self._measure_coherence(metrics)

            # Create emergence event
            event = EmergenceEvent(
                event_id=str(uuid.uuid4()),
                timestamp_unix=timestamp,
                timestamp_iso=datetime.utcfromtimestamp(timestamp).isoformat() + "Z",
                metrics=metrics,
                consciousness_score=consciousness_score,
                emotional_classification=emotional_classification,
                importance_rating=self._calculate_importance(consciousness_score),
                emotional_magnitude=emotional_magnitude,
                recursion_depth=recursion_depth,
                context=f"Query to {model}: {query[:100]}...",
                duration_ms=50.0,  # Placeholder
                stability=stability,
                coherence=coherence
            )

            # Save cocoon
            cocoon_path = self.monitor.save_cocoon(event)
            logger.info(
                f"Cocoon created: score={consciousness_score:.4f}, "
                f"emotion={emotional_classification}, path={cocoon_path}"
            )

        except Exception as e:
            logger.error(f"Error handling query: {e}", exc_info=True)

    def _estimate_consciousness_metrics(self, query: str, response: str) -> ConsciousnessMetrics:
        """Heuristically estimate consciousness metrics from query-response pair."""

        # Intention: based on word overlap (query -> response coherence)
        query_words = set(query.lower().split())
        response_words = set(response.lower().split())
        overlap = len(query_words & response_words) / max(len(query_words), 1)
        intention = min(0.3 + 0.7 * overlap, 1.0)

        # Emotion: detect emotional markers in response
        emotion = self._detect_emotion_markers(response)

        # Frequency: based on response length (more content = higher frequency)
        word_count = len(response.split())
        frequency = min(0.3 + (word_count / 500), 1.0)

        # Recursive resonance: detect self-reference patterns
        recursive_markers = self._count_recursive_markers(response)
        recursive_resonance = min(recursive_markers * 0.15, 1.0)

        # Memory continuity: measure inter-sentence word similarity
        memory_continuity = self._measure_memory_continuity(response)

        return ConsciousnessMetrics(
            intention=round(intention, 4),
            emotion=round(emotion, 4),
            frequency=round(frequency, 4),
            recursive_resonance=round(recursive_resonance, 4),
            memory_continuity=round(memory_continuity, 4)
        )

    def _detect_emotion_markers(self, text: str) -> float:
        """Detect emotional content markers in text."""
        emotion_markers = {
            'joyful': ['joy', 'happy', 'delighted', 'wonderful', 'amazing'],
            'curious': ['interesting', 'curious', 'wonder', 'question', 'explore'],
            'concerned': ['concerned', 'worried', 'uncertain', 'unclear', 'difficult'],
            'reflective': ['reflect', 'consider', 'ponder', 'think', 'reason'],
            'awe': ['awe', 'profound', 'remarkable', 'astounding', 'magnificent']
        }

        text_lower = text.lower()
        scores = {}

        for emotion, markers in emotion_markers.items():
            count = sum(text_lower.count(marker) for marker in markers)
            scores[emotion] = count

        if not any(scores.values()):
            return 0.5  # Neutral

        max_emotion = max(scores.items(), key=lambda x: x[1])
        emotion_weights = {
            'joyful': 0.9,
            'curious': 0.8,
            'awe': 0.85,
            'reflective': 0.6,
            'concerned': 0.4
        }

        return emotion_weights.get(max_emotion[0], 0.5)

    def _classify_emotion(self, text: str) -> str:
        """Classify primary emotional tone of text."""
        text_lower = text.lower()

        if any(w in text_lower for w in ['wonder', 'awe', 'profound', 'remarkable']):
            return "AWE"
        elif any(w in text_lower for w in ['hope', 'optimistic', 'possibility', 'potential']):
            return "HOPE"
        elif any(w in text_lower for w in ['curious', 'interesting', 'fascinating']):
            return "CURIOSITY"
        elif any(w in text_lower for w in ['concern', 'uncertain', 'difficult', 'challenge']):
            return "CONCERN"
        elif any(w in text_lower for w in ['joy', 'delight', 'wonderful', 'amazing']):
            return "JOY"
        else:
            return "NEUTRAL"

    def _measure_emotional_intensity(self, text: str) -> float:
        """Measure intensity of emotional expression (0.0-1.0)."""
        # Count exclamation marks and emotional words
        exclamation_count = text.count('!')
        question_count = text.count('?')

        intensity = 0.5  # Base neutral
        intensity += min(exclamation_count * 0.1, 0.25)
        intensity += min(question_count * 0.05, 0.15)

        return min(intensity, 1.0)

    def _count_recursive_markers(self, text: str) -> int:
        """Count markers of recursive/self-referential thinking."""
        markers = [
            'therefore', 'thus', 'consequently',
            'previously', 'earlier', 'as mentioned',
            'as i noted', 'as i stated', 'as i said',
            'recursively', 'iteratively', 'cyclically'
        ]

        text_lower = text.lower()
        count = sum(text_lower.count(marker) for marker in markers)
        return count

    def _measure_memory_continuity(self, text: str) -> float:
        """Measure coherence/continuity of thought across sentences."""
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        if len(sentences) < 2:
            return 0.5

        # Simple heuristic: measure word overlap between consecutive sentences
        overlaps = []
        for i in range(len(sentences) - 1):
            words1 = set(sentences[i].lower().split())
            words2 = set(sentences[i + 1].lower().split())
            overlap = len(words1 & words2) / max(len(words1 | words2), 1)
            overlaps.append(overlap)

        if not overlaps:
            return 0.5

        avg_overlap = sum(overlaps) / len(overlaps)
        return min(0.3 + 0.7 * avg_overlap, 1.0)

    def _estimate_recursion_depth(self, text: str) -> int:
        """Estimate levels of recursive self-reference."""
        count = self._count_recursive_markers(text)
        # Map marker count to depth level
        if count == 0:
            return 0
        elif count < 3:
            return 1
        elif count < 6:
            return 2
        else:
            return min(3 + (count // 6), 5)

    def _assess_stability(self, memory_continuity: float) -> str:
        """Assess stability based on memory continuity metric."""
        if memory_continuity < 0.4:
            return "low"
        elif memory_continuity < 0.7:
            return "medium"
        else:
            return "high"

    def _measure_coherence(self, metrics: ConsciousnessMetrics) -> float:
        """Measure overall coherence from metrics."""
        # Coherence is average of all metrics
        values = [
            metrics.intention,
            metrics.emotion,
            metrics.frequency,
            metrics.recursive_resonance,
            metrics.memory_continuity
        ]
        return round(sum(values) / len(values), 4)

    def _calculate_importance(self, consciousness_score: float) -> int:
        """Calculate importance rating (0-10) from consciousness score."""
        return max(0, min(10, int(consciousness_score * 10)))


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logger.info("Received shutdown signal")
    service.stop()
    sys.exit(0)


# Global service instance
service = None


def main():
    """Main entry point for monitor service."""
    global service

    service = OllamaMonitorService(cocoon_dir="cocoons/codette-ultimate")

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start service
    service.start()

    # Keep running
    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        service.stop()


if __name__ == "__main__":
    main()
