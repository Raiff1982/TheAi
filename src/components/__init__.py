"""
Codette Components Package
Contains modular components for the Codette AI system
"""

# Core systems
from .ai_core import AICore
from .cognitive_processor import CognitiveProcessor
from .defense_system import DefenseSystem
from .health_monitor import HealthMonitor

# Quantum and pattern systems
from .quantum_spiderweb import QuantumSpiderweb
from .quantum_optimizer import QuantumInspiredOptimizer  # Corrected class name
from .pattern_library import PatternLibrary
from .biokinetic_mesh import BioKineticMesh  # Corrected class name

# Learning and adaptation
from .dynamic_learning import DynamicLearner
from .adaptive_learning import AdaptiveLearningEnvironment
from .self_improving_ai import SelfImprovingAI
from .feedback_manager import ImprovedFeedbackManager  # Corrected class name

# Intelligence and creativity
from .ai_driven_creativity import AIDrivenCreativity
from .collaborative_ai import CollaborativeAI
from .neuro_symbolic import NeuroSymbolicEngine  # Corrected class name
from .multimodal_analyzer import MultimodalAnalyzer

# Governance and ethics
from .cultural_sensitivity import CulturalSensitivityEngine
from .ethical_governance import EthicalAIGovernance
from .explainable_ai import ExplainableAI

# Data and processing
from .data_processing import AdvancedDataProcessor
from .real_time_data import RealTimeDataIntegrator
from .sentiment_analysis import EnhancedSentimentAnalyzer
from .user_personalization import UserPersonalizer  # Corrected class name

# Search and analysis
from .search_engine import SearchEngine
from .fractal import FractalIdentity

__all__ = [
    # Core
    'AICore',
    'CognitiveProcessor',
    'DefenseSystem',
    'HealthMonitor',
    # Quantum
    'QuantumSpiderweb',
    'QuantumInspiredOptimizer',
    'PatternLibrary',
    'BioKineticMesh',
    # Learning
    'DynamicLearner',
    'AdaptiveLearningEnvironment',
    'SelfImprovingAI',
    'ImprovedFeedbackManager',
    # Intelligence
    'AIDrivenCreativity',
    'CollaborativeAI',
    'NeuroSymbolicEngine',
    'MultimodalAnalyzer',
    # Governance
    'CulturalSensitivityEngine',
    'EthicalAIGovernance',
    'ExplainableAI',
    # Data
    'AdvancedDataProcessor',
    'RealTimeDataIntegrator',
    'EnhancedSentimentAnalyzer',
    'UserPersonalizer',
    # Search
    'SearchEngine',
    'FractalIdentity',
]