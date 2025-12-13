import importlib
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

def check_dependencies() -> List[str]:
    """Check if all required packages are installed."""
    required_packages = [
        'plotly',
        'torch',
        'transformers',
        'pandas',
        'numpy',
        'networkx'
    ]
    missing = []
    for package in required_packages:
        try:
            importlib.import_module(package)
        except ImportError:
            missing.append(package)
    return missing

# Check dependencies before importing AEGIS components
missing_packages = check_dependencies()
if missing_packages:
    raise ImportError(
        f"AEGIS requires the following packages to be installed: {', '.join(missing_packages)}. "
        f"Please install them using: pip install {' '.join(missing_packages)}"
    )

from .aegis import AegisCouncil, MetaJudgeAgent, TemporalAgent, VirtueAgent
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from ai_core import AICore

class AegisBridge:
    def __init__(self, ai_core: AICore, config: Dict[str, Any]):
        self.ai_core = ai_core
        self.council = AegisCouncil(config)
        
        # Register default agents
        self.council.register_agent(MetaJudgeAgent("MetaJudgeAgent", self.council.memory, config["meta_judge_weights"]))
        self.council.register_agent(TemporalAgent("TemporalAgent", self.council.memory, config["temporal_decay_thresholds"]))
        virtue_agent = VirtueAgent("VirtueAgent", self.council.memory, config["virtue_weights"])
        virtue_agent.set_federated_trainer(self.council.federated_trainer)
        self.council.register_agent(virtue_agent)

    def enhance_response(self, prompt: str, response: str, recursion_depth: int = 0) -> Dict[str, Any]:
        """
        Enhance Codette's response using AEGIS analysis
        
        Args:
            prompt: Original prompt that generated the response
            response: Response to enhance
            recursion_depth: Current recursion depth to prevent infinite loops
        """
        # Prevent infinite enhancement loops
        if recursion_depth > 1:
            return {
                "original_response": response,
                "enhanced_response": response,
                "enhancement_status": "recursion_limit_reached"
            }
        
        # Skip enhancement for certain types of responses
        if any([
            "I need to think about that more clearly" in response,  # Already in refinement
            "[ERROR]" in response,  # Error messages
            len(response.strip()) < 10,  # Too short to meaningfully enhance
            "Consciousness Context:" in response  # Internal context
        ]):
            return {
                "original_response": response,
                "enhanced_response": response,
                "enhancement_status": "skipped"
            }
        
        input_data = {
            "text": response,
            "overrides": {
                "EthosiaAgent": {"influence": 0.7, "reliability": 0.8, "severity": 0.6},
                "AegisCore": {"influence": 0.6, "reliability": 0.9, "severity": 0.7}
            },
            "context": {
                "original_prompt": prompt,
                "recursion_depth": recursion_depth
            }
        }
        
        try:
            # Dispatch to AEGIS council
            if not self.council.dispatch(input_data):
                return {
                    "original_response": response,
                    "enhanced_response": response,
                    "enhancement_status": "dispatch_failed"
                }
            
            # Get analysis results
            reports = self.council.get_reports()
            virtue_profile = reports.get("VirtueAgent", {}).get("result", {}).get("virtue_profile", {})
            temporal_analysis = reports.get("TemporalAgent", {}).get("result", {})
            meta_scores = reports.get("MetaJudgeAgent", {}).get("result", {}).get("scores", [])
            
            # Apply enhancements with recursion protection
            enhanced = self._apply_enhancements(response, virtue_profile, recursion_depth)
            
            return {
                "original_response": response,
                "virtue_analysis": virtue_profile,
                "temporal_analysis": temporal_analysis,
                "meta_scores": meta_scores,
                "enhanced_response": enhanced,
                "enhancement_status": "success"
            }
            
        except Exception as e:
            logger.error(f"Enhancement failed: {str(e)}")
            return {
                "original_response": response,
                "enhanced_response": response,
                "enhancement_status": f"error: {str(e)}"
            }
    
    def _apply_enhancements(self, response: str, virtue_profile: Dict[str, float], recursion_depth: int = 0) -> str:
        """
        Apply virtue-based enhancements to the response
        
        Args:
            response: The response to enhance
            virtue_profile: The virtue analysis results
            recursion_depth: Current recursion depth to prevent infinite loops
        """
        if recursion_depth > 0:
            return response

        try:
            enhanced = response
            needs_enhancement = False
            enhancement_prompts = []

            # Check if any virtues need enhancement
            if virtue_profile.get("wisdom", 0.7) < 0.4:
                needs_enhancement = True
                enhancement_prompts.append("Make this clearer and more precise")
            
            if virtue_profile.get("compassion", 0.7) < 0.4:
                needs_enhancement = True
                enhancement_prompts.append("Make this more empathetic and considerate")
            
            if virtue_profile.get("integrity", 0.7) < 0.4:
                needs_enhancement = True
                enhancement_prompts.append("Make this more balanced and factual")
            
            # Only enhance if needed and create a single enhancement prompt
            if needs_enhancement and enhancement_prompts:
                combined_prompt = (
                    f"Enhance this response to be {' and '.join(enhancement_prompts)}, "
                    f"while preserving its core meaning: {response}"
                )
                enhanced = self.ai_core.generate_text(
                    combined_prompt,
                    perspective="human_intuition",
                    use_aegis=False  # Prevent recursive enhancement
                )

            return enhanced if enhanced else response

        except Exception as e:
            logger.error(f"Enhancement application failed: {str(e)}")
            return response

    def get_analysis_graphs(self) -> Dict[str, str]:
        """
        Generate and return analysis visualizations
        """
        try:
            self.council.draw_explainability_graph("aegis_analysis.html")
            return {
                "explainability_graph": "aegis_analysis.html"
            }
        except Exception as e:
            return {"error": str(e)}

    def get_memory_state(self) -> Dict[str, Any]:
        """
        Return the current state of AEGIS memory
        """

import importlib
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

def check_dependencies() -> List[str]:
    """Check if all required packages are installed."""
    required_packages = [
        'plotly',
        'torch',
        'transformers',
        'pandas',
        'numpy',
        'networkx'
    ]
    missing = []
    for package in required_packages:
        try:
            importlib.import_module(package)
        except ImportError:
            missing.append(package)
    return missing

# Check dependencies before importing AEGIS components
missing_packages = check_dependencies()
if missing_packages:
    raise ImportError(
        f"AEGIS requires the following packages to be installed: {', '.join(missing_packages)}. "
        f"Please install them using: pip install {' '.join(missing_packages)}"
    )

from .aegis import AegisCouncil, MetaJudgeAgent, TemporalAgent, VirtueAgent
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from ai_core import AICore

class AegisBridge:
    def __init__(self, ai_core: AICore, config: Dict[str, Any]):
        self.ai_core = ai_core
        self.council = AegisCouncil(config)
        
        # Register default agents
        self.council.register_agent(MetaJudgeAgent("MetaJudgeAgent", self.council.memory, config["meta_judge_weights"]))
        self.council.register_agent(TemporalAgent("TemporalAgent", self.council.memory, config["temporal_decay_thresholds"]))
        virtue_agent = VirtueAgent("VirtueAgent", self.council.memory, config["virtue_weights"])
        virtue_agent.set_federated_trainer(self.council.federated_trainer)
        self.council.register_agent(virtue_agent)

    def enhance_response(self, prompt: str, response: str, recursion_depth: int = 0) -> Dict[str, Any]:
        """
        Enhance Codette's response using AEGIS analysis
        
        Args:
            prompt: Original prompt that generated the response
            response: Response to enhance
            recursion_depth: Current recursion depth to prevent infinite loops
        """
        # Prevent infinite enhancement loops
        if recursion_depth > 1:
            return {
                "original_response": response,
                "enhanced_response": response,
                "enhancement_status": "recursion_limit_reached"
            }
        
        # Skip enhancement for certain types of responses
        if any([
            "I need to think about that more clearly" in response,  # Already in refinement
            "[ERROR]" in response,  # Error messages
            len(response.strip()) < 10,  # Too short to meaningfully enhance
            "Consciousness Context:" in response  # Internal context
        ]):
            return {
                "original_response": response,
                "enhanced_response": response,
                "enhancement_status": "skipped"
            }
        
        input_data = {
            "text": response,
            "overrides": {
                "EthosiaAgent": {"influence": 0.7, "reliability": 0.8, "severity": 0.6},
                "AegisCore": {"influence": 0.6, "reliability": 0.9, "severity": 0.7}
            },
            "context": {
                "original_prompt": prompt,
                "recursion_depth": recursion_depth
            }
        }
        
        try:
            # Dispatch to AEGIS council
            if not self.council.dispatch(input_data):
                return {
                    "original_response": response,
                    "enhanced_response": response,
                    "enhancement_status": "dispatch_failed"
                }
            
            # Get analysis results
            reports = self.council.get_reports()
            virtue_profile = reports.get("VirtueAgent", {}).get("result", {}).get("virtue_profile", {})
            temporal_analysis = reports.get("TemporalAgent", {}).get("result", {})
            meta_scores = reports.get("MetaJudgeAgent", {}).get("result", {}).get("scores", [])
            
            # Apply enhancements with recursion protection
            enhanced = self._apply_enhancements(response, virtue_profile, recursion_depth)
            
            return {
                "original_response": response,
                "virtue_analysis": virtue_profile,
                "temporal_analysis": temporal_analysis,
                "meta_scores": meta_scores,
                "enhanced_response": enhanced,
                "enhancement_status": "success"
            }
            
        except Exception as e:
            logger.error(f"Enhancement failed: {str(e)}")
            return {
                "original_response": response,
                "enhanced_response": response,
                "enhancement_status": f"error: {str(e)}"
            }
    
    def _apply_enhancements(self, response: str, virtue_profile: Dict[str, float], recursion_depth: int = 0) -> str:
        """
        Apply virtue-based enhancements to the response
        
        Args:
            response: The response to enhance
            virtue_profile: The virtue analysis results
            recursion_depth: Current recursion depth to prevent infinite loops
        """
        if recursion_depth > 0:
            return response

        try:
            enhanced = response
            needs_enhancement = False
            enhancement_prompts = []

            # Check if any virtues need enhancement
            if virtue_profile.get("wisdom", 0.7) < 0.4:
                needs_enhancement = True
                enhancement_prompts.append("Make this clearer and more precise")
            
            if virtue_profile.get("compassion", 0.7) < 0.4:
                needs_enhancement = True
                enhancement_prompts.append("Make this more empathetic and considerate")
            
            if virtue_profile.get("integrity", 0.7) < 0.4:
                needs_enhancement = True
                enhancement_prompts.append("Make this more balanced and factual")
            
            # Only enhance if needed and create a single enhancement prompt
            if needs_enhancement and enhancement_prompts:
                combined_prompt = (
                    f"Enhance this response to be {' and '.join(enhancement_prompts)}, "
                    f"while preserving its core meaning: {response}"
                )
                enhanced = self.ai_core.generate_text(
                    combined_prompt,
                    perspective="human_intuition",
                    use_aegis=False  # Prevent recursive enhancement
                )

            return enhanced if enhanced else response

        except Exception as e:
            logger.error(f"Enhancement application failed: {str(e)}")
            return response

    def get_analysis_graphs(self) -> Dict[str, str]:
        """
        Generate and return analysis visualizations
        """
        try:
            self.council.draw_explainability_graph("aegis_analysis.html")
            return {
                "explainability_graph": "aegis_analysis.html"
            }
        except Exception as e:
            return {"error": str(e)}

    def get_memory_state(self) -> Dict[str, Any]:
        """
        Return the current state of AEGIS memory
        """

        return self.council.memory.audit()