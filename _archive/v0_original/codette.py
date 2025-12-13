"""
Core Codette AI module with BioKinetic Neural Mesh for efficient pattern routing
"""

import os
import sys
from pathlib import Path
import torch
import numpy as np
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
import json
import logging

# Add the src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir
if not (src_dir / "components").exists():
    src_dir = current_dir.parent
sys.path.append(str(src_dir))

from components.ai_core import AICore
from components.cognitive_processor import CognitiveProcessor
from components.defense_system import DefenseSystem
from components.health_monitor import HealthMonitor
from components.pattern_library import PatternLibrary
from components.biokinetic_mesh import BioKineticMesh

logger = logging.getLogger(__name__)

class Codette:
    """Main Codette AI class with BioKinetic pattern routing"""
    
    def __init__(self, user_name: str = "User"):
        self.user_name = user_name
        
        # Initialize core components
        self.ai_core = AICore()
        self.cognitive_processor = CognitiveProcessor()
        self.defense_system = DefenseSystem(strategies=["adaptability", "barrier"])
        self.health_monitor = HealthMonitor()
        
        # Initialize BioKinetic Neural Mesh
        self.biokinetic_mesh = BioKineticMesh(
            initial_nodes=256,  # Reduced from 512 for better efficiency
            energy_threshold=0.3,
            learning_rate=0.01,
            prune_threshold=0.1
        )
        
        # Initialize basic state
        self.conversation_history = []
        self.memory_path = Path("codette_memory.json")
        self._initialize_memory()
        
    def respond(self, query: str) -> Dict[str, Any]:
        """Generate a response using BioKinetic Neural Mesh for routing"""
        try:
            # Convert query to pattern
            query_pattern = self._text_to_pattern(query)
            
            # Get current context
            context = {
                "mode": "response",
                "history_length": len(self.conversation_history)
            }
            
            # Route through BioKinetic Mesh
            start_time = datetime.now()
            route_node, confidence = self.biokinetic_mesh.route_intent(
                query_pattern, 
                context
            )
            routing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            # Process through cognitive processor
            response_data = self.cognitive_processor.process(
                query,
                route_node=route_node,
                confidence=confidence
            )
            
            # Add thinking pattern for complex queries
            if confidence < 0.7 or len(query.split()) > 15:
                thinking_response = PatternLibrary.get_thinking_response()
                initial_response = f"{thinking_response}\n\n"
            else:
                initial_response = ""
            
            # Generate final response
            final_response = initial_response + response_data["response"]
            
            # Add follow-up for complex responses
            if len(final_response.split()) > 50:
                follow_up = PatternLibrary.get_follow_up()
                final_response += f"\n\n{follow_up}"
            
            # Store in conversation history
            conversation_data = {
                "query": query,
                "response": final_response,
                "route_info": {
                    "node": route_node,
                    "confidence": confidence,
                    "routing_time_ms": routing_time
                },
                "timestamp": str(datetime.now())
            }
            self.conversation_history.append(conversation_data)
            
            # Prune old history
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            # Strengthen successful pathway if confident
            if confidence > 0.7:
                self.biokinetic_mesh.strengthen_pathway(
                    [route_node],
                    reward=confidence
                )
            
            # Save memory state
            self._save_memory()
            
            # Return response package
            return {
                "response": final_response,
                "insights": response_data.get("insights", []),
                "metrics": {
                    "confidence": confidence,
                    "routing_time_ms": routing_time
                },
                "routing": {
                    "node": route_node,
                    "pattern_strength": confidence,
                    "processing_time": routing_time
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "response": f"I apologize, but I encountered an error: {str(e)}",
                "insights": ["Error recovery activated"],
                "metrics": {"confidence": 0.5},
                "routing": {"node": None, "pattern_strength": 0.0}
            }
    
    def _text_to_pattern(self, text: str) -> np.ndarray:
        """Convert text to a numerical pattern vector"""
        try:
            # Simple averaging of word vectors
            words = text.lower().split()
            pattern = np.zeros(256)  # Reduced dimensionality
            
            for word in words:
                # Generate simple word vector (placeholder for actual embedding)
                word_hash = hash(word) % 256
                pattern[word_hash] = 1.0
            
            # Normalize pattern
            pattern_sum = np.sum(pattern)
            if pattern_sum > 0:
                pattern = pattern / pattern_sum
                
            return pattern
            
        except Exception as e:
            logger.error(f"Error converting text to pattern: {e}")
            return np.zeros(256)
            
    def _initialize_memory(self):
        """Initialize memory from file or create new"""
        try:
            if self.memory_path.exists():
                with open(self.memory_path, 'r') as f:
                    self.memory = json.load(f)
            else:
                self.memory = {
                    "conversation_history": [],
                    "biokinetic_state": {}
                }
        except Exception as e:
            logger.error(f"Error initializing memory: {e}")
            self.memory = {"error": str(e)}
            
    def _save_memory(self):
        """Save memory state to file"""
        try:
            self.memory["conversation_history"] = self.conversation_history[-10:]
            self.memory["biokinetic_state"] = self.biokinetic_mesh.get_state()
            
            with open(self.memory_path, 'w') as f:
                json.dump(self.memory, f)
                
        except Exception as e:
            logger.error(f"Error saving memory: {e}")
            
    async def initialize(self):
        """Initialize AI components"""
        try:
            if not self.ai_core._initialize_language_model():
                raise RuntimeError("Failed to initialize language model")
                
            self.cognitive_processor = CognitiveProcessor()
            self.defense_system = DefenseSystem(strategies=["adaptability", "barrier"])
            
            # Initialize biokinetic mesh state
            mesh_state_path = Path("biokinetic_state.json")
            if mesh_state_path.exists():
                self.biokinetic_mesh.load_state(mesh_state_path)
            
            return True
            
        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            return False

    async def shutdown(self):
        """Clean shutdown of AI components"""
        try:
            # Save biokinetic mesh state
            self.biokinetic_mesh.save_state(Path("biokinetic_state.json"))
            
            # Regular shutdown
            await self.ai_core.shutdown()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                
            return {"status": "shutdown_complete"}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}