"""
Codette Interface - Centralized interface for all Codette AI interactions
"""

import logging
import asyncio
from typing import Dict, Any, Optional, List
from pathlib import Path

from codette import Codette
from codette_imports import import_manager
from components.health_monitor import HealthMonitor

logger = logging.getLogger(__name__)

class CodetteInterface:
    """Unified interface for Codette AI system"""
    
    def __init__(self):
        self.codette = None
        self.health_monitor = HealthMonitor()
        self.initialized = False
        
    async def initialize(self) -> bool:
        """Initialize the Codette system"""
        try:
            if not self.initialized:
                # Create Codette instance through import manager
                self.codette = import_manager.create_system()
                if not self.codette:
                    raise RuntimeError("Failed to create Codette instance")
                
                # Initialize Codette
                await self.codette.initialize()
                self.initialized = True
                
                logger.info("Codette interface initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Codette interface: {e}")
            return False
    
    async def process_query(self, query: str) -> Dict[str, Any]:
        """Process a query through Codette"""
        try:
            if not self.initialized:
                await self.initialize()
            
            # Process through Codette
            result = self.codette.respond(query)
            
            # Add health status
            health_status = await self.health_monitor.check_status()
            
            # Construct response
            response = {
                "response": result["response"],
                "metrics": result.get("metrics", {}),
                "insights": result.get("insights", []),
                "health": health_status,
                "components": import_manager.get_available_systems()
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "error": str(e),
                "response": "I apologize, but I encountered an error processing your request.",
                "metrics": {"error": True},
                "insights": ["Error recovery activated"],
                "health": {"status": "error"}
            }
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        try:
            health_status = await self.health_monitor.check_status()
            available_systems = import_manager.get_available_systems()
            
            if self.codette:
                ai_metrics = self.codette.ai_core._calculate_consciousness_state()
            else:
                ai_metrics = {"status": "not_initialized"}
            
            return {
                "status": "healthy" if health_status.get("status") == "ok" else "unhealthy",
                "health": health_status,
                "components": available_systems,
                "ai_metrics": ai_metrics
            }
            
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def shutdown(self) -> Dict[str, Any]:
        """Clean shutdown of all components"""
        try:
            if self.codette:
                await self.codette.shutdown()
                self.codette = None
                self.initialized = False
            
            return {"status": "shutdown_complete"}
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

# Create global interface instance
interface = CodetteInterface()

# Export for easy access
__all__ = ['CodetteInterface', 'interface']