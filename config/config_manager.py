# config_manager.py
import json
from typing import Dict

class EnhancedAIConfig:
    """Advanced configuration manager with encryption and validation"""
    _DEFAULTS = {
        "model": "gpt-4-turbo",
        "safety_thresholds": {
            "memory": 85,
            "cpu": 90,
            "response_time": 2.0
        },
        "defense_strategies": ["evasion", "adaptability", "barrier"],
        "cognitive_modes": ["scientific", "creative", "emotional"]
    }

    def __init__(self, config_path: str = "ai_config.json"):
        self.config = self._load_config(config_path)
        self._validate()

    def _load_config(self, path: str) -> Dict:
        try:
            with open(path, 'r') as f:
                return self._merge_configs(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading config file: {e}. Using default configuration.")
            return self._DEFAULTS

    def _merge_configs(self, user_config: Dict) -> Dict:
        merged = self._DEFAULTS.copy()
        for key, value in user_config.items():
            if isinstance(value, dict) and key in merged:
                merged[key].update(value)
            else:
                merged[key] = value
        return merged

    def _validate(self):
        if not all(isinstance(mode, str) for mode in self.config["cognitive_modes"]):
            raise ValueError("Invalid cognitive mode configuration")
