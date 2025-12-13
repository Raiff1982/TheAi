
# health_monitor.py
import psutil
import asyncio
import time
import numpy as np
from collections import deque
from sklearn.ensemble import IsolationForest
from threading import Lock
from typing import Dict

class HealthMonitor:
    """Real-time system diagnostics with anomaly detection"""
    def __init__(self):
        self.metrics = deque(maxlen=100)
        self.model = IsolationForest(n_estimators=100)
        self.lock = Lock()

    async def check_status(self) -> Dict:
        status = {
            "memory": psutil.virtual_memory().percent,
            "cpu": psutil.cpu_percent(),
            "response_time": await self._measure_latency()
        }
        with self.lock:
            self.metrics.append(status)
            self._detect_anomalies()
        return status

    async def _measure_latency(self) -> float:
        start = time.monotonic()
        await asyncio.sleep(0.1)
        return time.monotonic() - start

    def _detect_anomalies(self):
        if len(self.metrics) > 50:
            data = np.array([[m["memory"], m["cpu"], m["response_time"]] for m in self.metrics])
            self.model.fit(data)
