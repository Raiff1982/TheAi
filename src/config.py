
#!/usr/bin/env python3
# Copyright (c) 2025 Codette
# Licensed under the MIT License.

class DefaultConfig:
    """Bot Configuration"""

    PORT = 7860
    APP_ID = ""
    APP_PASSWORD = ""
    
    # HuggingFace settings
    HF_TOKEN = ""
    
    # Logging settings
    LOG_LEVEL = "INFO"
    
    # Model settings
    DEFAULT_TEMPERATURE = 0.7
    MAX_LENGTH = 1024
    CONTEXT_WINDOW = 2048
    
    # Memory settings
    MAX_MEMORY = 50
    MEMORY_CONTEXT_SIZE = 5
    
    # Perspective settings

    PERSPECTIVES = ["newton", "davinci", "human_intuition", "quantum_computing"]