import psutil
import asyncio
import time
import logging
from collections import deque
from threading import Lock
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

try:
    import numpy as np
except Exception:
    np = None

class HealthMonitor:
    """Real-time system diagnostics with quantum-aware anomaly detection"""
    
    def __init__(self, history_size: int = 100):
        self.metrics = deque(maxlen=history_size)
        self.anomaly_history = deque(maxlen=50)
        self.lock = Lock()
        self.baseline = None
        self.last_check = None
        self.quantum_influence = 0.5
        self.initialized = False
        
    async def initialize(self):
        """Initialize the health monitor system"""
        try:
            # Get initial status to establish baseline
            initial_status = await self.check_status_async()
            if np is not None:
                self.baseline = np.array([
                    initial_status["memory"],
                    initial_status["cpu"],
                    initial_status["response_time"]
                ])
            else:
                self.baseline = [
                    initial_status["memory"],
                    initial_status["cpu"],
                    initial_status["response_time"]
                ]
            self.initialized = True
            logger.info("Health monitor initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Health monitor initialization failed: {e}")
            return False
        
    def check_status(self, consciousness_state: Optional[Dict] = None) -> Dict:
        """Check system status with quantum consciousness integration - synchronous version"""
        try:
            # Get base metrics synchronously
            status = {
                "timestamp": datetime.now(),
                "memory": psutil.virtual_memory().percent,
                "cpu": psutil.cpu_percent(),
                "response_time": self._measure_latency_sync(),
                "quantum_coherence": consciousness_state.get("quantum_state", [0.5])[0] if consciousness_state else 0.5
            }
            
            # Calculate load score with quantum influence
            quantum_factor = status["quantum_coherence"]
            load_score = (
                0.4 * status["memory"] +
                0.4 * status["cpu"] +
                0.2 * (status["response_time"] * 1000)  # Convert to ms
            ) * (1 + (quantum_factor - 0.5))  # Quantum modification
            
            status["load_score"] = min(100, max(0, load_score))
            
            # Thread-safe metrics update
            with self.lock:
                self.metrics.append(status)
                anomaly_score = self._detect_anomalies()
                status["anomaly_score"] = anomaly_score
                
                # Track anomaly if significant
                if anomaly_score > 0.7:
                    self.anomaly_history.append({
                        "timestamp": status["timestamp"],
                        "score": anomaly_score,
                        "metrics": status.copy()
                    })
            
            self.last_check = status["timestamp"]
            return status
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "timestamp": datetime.now(),
                "status": "error",
                "error": str(e)
            }
            
    async def check_status_async(self, consciousness_state: Optional[Dict] = None) -> Dict:
        """Check system status with quantum consciousness integration - async version"""
        try:
            # Get base metrics asynchronously
            status = {
                "timestamp": datetime.now(),
                "memory": psutil.virtual_memory().percent,
                "cpu": psutil.cpu_percent(),
                "response_time": await self._measure_latency(),
                "quantum_coherence": consciousness_state.get("quantum_state", [0.5])[0] if consciousness_state else 0.5
            }
            
            # Calculate load score with quantum influence
            quantum_factor = status["quantum_coherence"]
            load_score = (
                0.4 * status["memory"] +
                0.4 * status["cpu"] +
                0.2 * (status["response_time"] * 1000)  # Convert to ms
            ) * (1 + (quantum_factor - 0.5))  # Quantum modification
            
            status["load_score"] = min(100, max(0, load_score))
            
            # Thread-safe metrics update
            with self.lock:
                self.metrics.append(status)
                anomaly_score = self._detect_anomalies()
                status["anomaly_score"] = anomaly_score
                
                # Track anomaly if significant
                if anomaly_score > 0.7:
                    self.anomaly_history.append({
                        "timestamp": status["timestamp"],
                        "score": anomaly_score,
                        "metrics": status.copy()
                    })
            
            self.last_check = status["timestamp"]
            return status
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "timestamp": datetime.now(),
                "status": "error",
                "error": str(e)
            }

    def _measure_latency_sync(self) -> float:
        """Measure system response latency - synchronous version"""
        try:
            start = time.monotonic()
            time.sleep(0.1)  # Simulated work
            return time.monotonic() - start
        except Exception as e:
            logger.warning(f"Latency measurement failed: {e}")
            return 0.1
            
    async def _measure_latency(self) -> float:
        """Measure system response latency - async version"""
        try:
            start = time.monotonic()
            await asyncio.sleep(0.1)  # Simulated work
            return time.monotonic() - start
        except Exception as e:
            logger.warning(f"Latency measurement failed: {e}")
            return 0.1

    def _detect_anomalies(self) -> float:
        """Detect system anomalies using statistical analysis"""
        try:
            if len(self.metrics) < 10:
                return 0.0
                
            # Extract recent metrics
            if np is not None:
                recent_data = np.array([
                    [m["memory"], m["cpu"], m["response_time"]]
                    for m in list(self.metrics)[-10:]
                ])
            else:
                recent_data = [
                    [m["memory"], m["cpu"], m["response_time"]]
                    for m in list(self.metrics)[-10:]
                ]
            
            if self.baseline is None:
                if np is not None:
                    self.baseline = np.mean(recent_data, axis=0)
                else:
                    # Compute simple mean per column
                    cols = list(zip(*recent_data))
                    self.baseline = [sum(c)/len(c) for c in cols]
                return 0.0
                
            if np is not None:
                deviations = np.abs(recent_data - self.baseline)
                max_deviation = float(np.max(deviations))
                
                # Update baseline with moving average
                self.baseline = 0.9 * self.baseline + 0.1 * np.mean(recent_data, axis=0)
            else:
                deviations = [[abs(a - b) for a,b in zip(row, self.baseline)] for row in recent_data]
                max_deviation = float(max(max(row) for row in deviations))
                # Update baseline (python moving average)
                cols = list(zip(*recent_data))
                means = [sum(c)/len(c) for c in cols]
                self.baseline = [0.9*b + 0.1*m for b,m in zip(self.baseline, means)]
            
            # Normalize anomaly score to [0,1]
            return min(1.0, max_deviation / 100.0)
            
        except Exception as e:
            logger.error(f"Anomaly detection failed: {e}")
            return 0.0
            
    def get_health_summary(self) -> Dict:
        """Get system health summary"""
        try:
            if not self.metrics:
                return {"status": "initializing"}
                
            recent_metrics = list(self.metrics)[-10:]
            if np is not None:
                avg_memory = float(np.mean([m["memory"] for m in recent_metrics]))
                avg_cpu = float(np.mean([m["cpu"] for m in recent_metrics]))
                avg_latency = float(np.mean([m["response_time"] for m in recent_metrics]))
            else:
                avg_memory = float(sum(m["memory"] for m in recent_metrics)/len(recent_metrics))
                avg_cpu = float(sum(m["cpu"] for m in recent_metrics)/len(recent_metrics))
                avg_latency = float(sum(m["response_time"] for m in recent_metrics)/len(recent_metrics))
            
            return {
                "status": "healthy" if avg_memory < 80 and avg_cpu < 80 else "stressed",
                "avg_memory": avg_memory,
                "avg_cpu": avg_cpu,
                "avg_latency": avg_latency,
                "recent_anomalies": len([a for a in self.anomaly_history if (datetime.now() - a["timestamp"]).seconds < 300]),
                "last_check": self.last_check
            }
            
        except Exception as e:
            logger.error(f"Health summary generation failed: {e}")
            return {"status": "error", "error": str(e)}