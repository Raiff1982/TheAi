"""
Simplified cognitive processor for Codette
"""

from typing import List, Dict, Any, Optional
try:
    import numpy as np
except Exception:
    np = None
from datetime import datetime

class CognitiveProcessor:
    """Core processing engine for Codette responses"""
    
    MODES = {
        "logical": {
            "name": "Logical Analysis",
            "process": lambda q: f"Analyzing {q} systematically...",
            "weight": 0.9
        },
        "creative": {
            "name": "Creative Insight", 
            "process": lambda q: f"Exploring creative approaches to {q}...",
            "weight": 0.8
        },
        "practical": {
            "name": "Practical Application",
            "process": lambda q: f"Considering practical implementations for {q}...",
            "weight": 0.85
        }
    }

    def __init__(self):
        """Initialize cognitive processor with default modes"""
        self.active_modes = self.MODES.copy()
        self.processing_history = []
                
    def process(self, 
                query: str, 
                route_node: Optional[str] = None,
                confidence: float = 0.5) -> Dict[str, Any]:
        """
        Process query using active modes and routing information
        
        Args:
            query: Input text to process
            route_node: Optional BioKinetic mesh node
            confidence: Routing confidence score
            
        Returns:
            Dict with response and insights
        """
        try:
            # Generate insights from each mode
            insights = []
            weighted_responses = []
            
            for mode_name, mode_info in self.active_modes.items():
                # Apply confidence to weight
                effective_weight = mode_info["weight"] * confidence
                if effective_weight > 0.3:  # Minimum threshold
                    response = mode_info["process"](query)
                    weighted_responses.append((response, effective_weight))
                    insights.append(f"{mode_info['name']}")
            
            # Combine responses based on weights
            if weighted_responses:
                # Sort by weight
                weighted_responses.sort(key=lambda x: x[1], reverse=True)
                # Take top response
                main_response = weighted_responses[0][0]
            else:
                main_response = f"Processing query: {query}"
            
            # Record processing
            self.processing_history.append({
                "timestamp": str(datetime.now()),
                "query": query,
                "response": main_response,
                "route_node": route_node,
                "confidence": confidence
            })
            
            # Prune history if too long
            if len(self.processing_history) > 10:
                self.processing_history = self.processing_history[-10:]
            
            return {
                "response": main_response,
                "insights": insights[:3]  # Top 3 insights
            }
            
        except Exception as e:
            print(f"Error processing query: {e}")
            return {
                "response": f"I apologize, but I encountered an error processing your query.",
                "insights": ["Error recovery activated"]
            }

    def get_metrics(self) -> Dict[str, Any]:
        """Get processor metrics and status"""
        try:
            return {
                "active_modes": list(self.active_modes.keys()),
                "mode_weights": {mode: info["weight"] for mode, info in self.active_modes.items()},
                "processing_history_length": len(self.processing_history)
            }
        except Exception as e:
            print(f"Error getting metrics: {e}")
            return {}