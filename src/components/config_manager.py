"""
Enhanced AI Configuration Manager
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union
import logging

logger = logging.getLogger(__name__)

class EnhancedAIConfig:
    """Configuration manager for AI systems with enhanced functionality"""
    
    def __init__(self, config_path: Union[str, Path]):
        self.config_path = Path(config_path)
        self.defaults = {
            "host": "127.0.0.1",
            "port": 8000,
            "model_name": "gpt2-large",
            "quantum_fluctuation": 0.07,
            "spiderweb_dim": 5,
            "recursion_depth": 4,
            "perspectives": ["Newton", "DaVinci", "Ethical", "Quantum", "Memory"]
        }
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file with fallback to defaults"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                logger.info(f"Configuration loaded from {self.config_path}")
                return config
            else:
                logger.warning(f"Config file {self.config_path} not found, using defaults")
                try:
                    self._save_config(self.defaults)  # Create default config
                except Exception as e:
                    logger.debug(f"Could not write default config: {e}")
                return self.defaults.copy()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self.defaults.copy()

    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
            logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Error saving config: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value with fallback to default
        
        Args:
            key: Configuration key to retrieve
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.config.get(key, self.defaults.get(key, default))

    def set(self, key: str, value: Any):
        """
        Set configuration value
        
        Args:
            key: Configuration key to set
            value: Value to set
        """
        self.config[key] = value
        self._save_config(self.config)

    def update(self, updates: Dict[str, Any]):
        """
        Update multiple configuration values
        
        Args:
            updates: Dictionary of updates to apply
        """
        self.config.update(updates)
        self._save_config(self.config)

    def reset(self):
        """Reset configuration to defaults"""
        self.config = self.defaults.copy()
        self._save_config(self.config)

    def get_all(self) -> Dict[str, Any]:
        """Get complete configuration"""
        return self.config.copy()