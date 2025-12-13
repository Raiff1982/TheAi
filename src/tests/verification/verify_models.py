"""Helper script to verify model downloads and fallback system"""
import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def verify_model_files():
    """Verify that all required model files are present."""
    required_files = [
        'models/fallback/__init__.py',
        'models/fallback/model_config.json'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
            
    return missing_files

def verify_model_imports():
    """Verify that required model packages can be imported."""
    required_packages = [
        'torch',
        'transformers',
        'numpy'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
            
    return missing_packages

def main():
    # Check for missing files
    missing_files = verify_model_files()
    if missing_files:
        logger.error("Missing required files:")
        for file in missing_files:
            logger.error(f"  - {file}")
        return 1
        
    # Check for missing packages
    missing_packages = verify_model_imports()
    if missing_packages:
        logger.error("Missing required packages:")
        for package in missing_packages:
            logger.error(f"  - {package}")
        return 1
        
    # Try importing the fallback manager
    try:
        from models.fallback import fallback_manager
        logger.info("Successfully imported fallback manager")
    except Exception as e:
        logger.error(f"Failed to import fallback manager: {str(e)}")
        return 1
        
    # Try downloading a test model
    try:
        fallback_manager.download_if_needed('nlp_transformer')
        logger.info("Successfully verified model download capability")
    except Exception as e:
        logger.error(f"Failed to verify model download: {str(e)}")
        return 1
        
    logger.info("All model verifications passed successfully")
    return 0

if __name__ == '__main__':
    sys.exit(main())
