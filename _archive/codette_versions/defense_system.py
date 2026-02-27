
# defense_system.py
import re
from typing import List

class DefenseSystem:
    """Advanced threat mitigation framework"""
    STRATEGIES = {
        "evasion": lambda x: re.sub(r'\b\d{4}\b', '****', x),
        "adaptability": lambda x: x + "\n[System optimized response]",
        "barrier": lambda x: x.replace("malicious", "safe")
    }

    def __init__(self, strategies: List[str]):
        self.active_strategies = [self.STRATEGIES[s] for s in strategies if s in self.STRATEGIES]

    def apply_defenses(self, text: str) -> str:
        for strategy in self.active_strategies:
            text = strategy(text)
        return text
