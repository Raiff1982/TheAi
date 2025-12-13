#!/usr/bin/env python3
"""
Configuration management for Codette AI
Centralizes all settings and configuration
"""
import os
import json
from typing import Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class CodetteConfig:
    """Centralized configuration manager"""
    
    # Default configuration values
    DEFAULTS = {
        # API Configuration
        "api": {
            "host": "127.0.0.1",
            "port": 8000,
            "debug": False,
            "log_level": "INFO"
        },
        # Codette AI Configuration
        "codette": {
            "user_name": "User",
            "perspectives": ["Newton", "DaVinci", "Ethical", "Quantum", "Memory"],
            "spiderweb_dim": 5,
            "recursion_depth": 4,
            "quantum_fluctuation": 0.07,
            "memory_path": "quantum_cocoon.json"
        },
        # Database Configuration
        "database": {
            "path": "codette_data.db",
            "backup_enabled": True,
            "backup_dir": "./backups"
        },
        # Feature Flags
        "features": {
            "enable_memory": True,
            "enable_learning": True,
            "enable_analytics": False,
            "max_history": 1000
        },
        # Performance
        "performance": {
            "cache_enabled": True,
            "max_cache_size": 1000,
            "response_timeout": 30
        },
        # Security
        "security": {
            "require_auth": False,
            "password_min_length": 8,
            "session_timeout": 3600
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration
        
        Args:
            config_path: Path to config JSON file (optional)
        """
        self.config = self.DEFAULTS.copy()
        self.config_path = config_path
        
        if config_path and os.path.exists(config_path):
            self._load_config_file(config_path)
        
        # Override with environment variables
        self._load_env_variables()
    
    def _load_config_file(self, path: str):
        """Load configuration from JSON file
        
        Args:
            path: Path to config file
        """
        try:
            with open(path, 'r') as f:
                user_config = json.load(f)
                self._merge_config(user_config)
                logger.info(f"Loaded configuration from {path}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"Could not load config file {path}: {e}")
    
    def _merge_config(self, user_config: Dict[str, Any]):
        """Merge user config into defaults
        
        Args:
            user_config: User configuration dict
        """
        for section, values in user_config.items():
            if section in self.config:
                if isinstance(values, dict):
                    self.config[section].update(values)
                else:
                    self.config[section] = values
            else:
                self.config[section] = values
    
    def _load_env_variables(self):
        """Load configuration from environment variables"""
        # API settings
        if host := os.getenv("CODETTE_API_HOST"):
            self.config["api"]["host"] = host
        if port := os.getenv("CODETTE_API_PORT"):
            self.config["api"]["port"] = int(port)
        if debug := os.getenv("CODETTE_DEBUG"):
            self.config["api"]["debug"] = debug.lower() in ("true", "1", "yes")
        
        # Database settings
        if db_path := os.getenv("CODETTE_DB_PATH"):
            self.config["database"]["path"] = db_path
        
        # Codette settings
        if user_name := os.getenv("CODETTE_USER_NAME"):
            self.config["codette"]["user_name"] = user_name
    
    def get(self, section: str, key: Optional[str] = None, default: Any = None) -> Any:
        """Get configuration value
        
        Args:
            section: Configuration section
            key: Optional key within section
            default: Default value if not found
            
        Returns:
            Configuration value
        """
        if section not in self.config:
            return default
        
        if key is None:
            return self.config.get(section, default)
        
        if isinstance(self.config[section], dict):
            return self.config[section].get(key, default)
        
        return default
    
    def set(self, section: str, key: str, value: Any):
        """Set configuration value
        
        Args:
            section: Configuration section
            key: Key within section
            value: New value
        """
        if section not in self.config:
            self.config[section] = {}
        
        if isinstance(self.config[section], dict):
            self.config[section][key] = value
        else:
            logger.warning(f"Cannot set {section}.{key}: section is not a dict")
    
    def save(self, path: str):
        """Save configuration to file
        
        Args:
            path: Path to save config
        """
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Configuration saved to {path}")
        except IOError as e:
            logger.error(f"Could not save configuration: {e}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Get config as dictionary
        
        Returns:
            Configuration dictionary
        """
        return self.config.copy()
    
    def validate(self) -> bool:
        """Validate configuration
        
        Returns:
            True if valid, False otherwise
        """
        required_sections = ["api", "codette", "database"]
        
        for section in required_sections:
            if section not in self.config:
                logger.error(f"Missing required section: {section}")
                return False
        
        # Validate API port
        api_port = self.config["api"]["port"]
        if not (0 < api_port < 65536):
            logger.error(f"Invalid API port: {api_port}")
            return False
        
        return True


# Global configuration instance
_config: Optional[CodetteConfig] = None


def get_config(config_path: Optional[str] = None) -> CodetteConfig:
    """Get or create global config instance
    
    Args:
        config_path: Optional path to config file
        
    Returns:
        CodetteConfig instance
    """
    global _config
    if _config is None:
        _config = CodetteConfig(config_path)
    return _config


# Convenience getters
def get_api_host() -> str:
    """Get API host"""
    return get_config().get("api", "host", "127.0.0.1")


def get_api_port() -> int:
    """Get API port"""
    return get_config().get("api", "port", 8000)


def get_db_path() -> str:
    """Get database path"""
    return get_config().get("database", "path", "codette_data.db")


def get_codette_user_name() -> str:
    """Get Codette user name"""
    return get_config().get("codette", "user_name", "User")


# Backwards compatibility - Bot Configuration
class DefaultConfig:
    """Legacy Bot Configuration - kept for compatibility"""
    
    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")


if __name__ == "__main__":
    # Test configuration
    logging.basicConfig(level=logging.INFO)
    
    config = get_config()
    
    print("\n=== Codette Configuration ===\n")
    print(f"API: {config.get('api', 'host')}:{config.get('api', 'port')}")
    print(f"Database: {config.get('database', 'path')}")
    print(f"Codette User: {config.get('codette', 'user_name')}")
    print(f"Perspectives: {config.get('codette', 'perspectives')}")
    
    # Validate
    if config.validate():
        print("\n✓ Configuration is valid\n")
    else:
        print("\n✗ Configuration is invalid\n")

