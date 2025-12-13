"""
Codette API & Integration Endpoints
====================================
RESTful API for integrating Codette capabilities with React frontend & DAW.

Endpoints:
  POST /codette/query - Submit query with perspective selection
  POST /codette/music-guidance - Get music-specific advice
  GET /codette/status - Check quantum state & consciousness metrics
  POST /codette/memory - Store/retrieve cocoons
  GET /codette/capabilities - List all capabilities
"""

from typing import Optional, List, Dict, Any
from dataclasses import asdict
from datetime import datetime
import json
import logging

logger = logging.getLogger("CodetteAPI")


# ============================================================================
# API REQUEST/RESPONSE MODELS
# ============================================================================

class CodetteQueryRequest:
    """Request model for Codette query endpoint"""
    
    def __init__(self, query: str, perspectives: Optional[List[str]] = None,
                 emotion: Optional[str] = None, user_id: Optional[str] = None):
        self.query = query
        self.perspectives = perspectives or []
        self.emotion = emotion
        self.user_id = user_id
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'query': self.query,
            'perspectives': self.perspectives,
            'emotion': self.emotion,
            'user_id': self.user_id,
            'timestamp': self.timestamp
        }


class CodetteQueryResponse:
    """Response model for Codette query endpoint"""
    
    def __init__(self, query_id: str, response: Dict[str, Any], 
                 processing_time_ms: float, cocoon_id: Optional[str] = None):
        self.query_id = query_id
        self.response = response
        self.processing_time_ms = processing_time_ms
        self.cocoon_id = cocoon_id
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'query_id': self.query_id,
            'response': self.response,
            'processing_time_ms': self.processing_time_ms,
            'cocoon_id': self.cocoon_id,
            'timestamp': self.timestamp
        }


class CodetteStatusResponse:
    """Current quantum consciousness state"""
    
    def __init__(self, coherence: float, entanglement: float, resonance: float,
                 interaction_count: int, cocoon_count: int):
        self.coherence = coherence
        self.entanglement = entanglement
        self.resonance = resonance
        self.interaction_count = interaction_count
        self.cocoon_count = cocoon_count
        self.timestamp = datetime.now().isoformat()
        self.status = "operational"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'status': self.status,
            'quantum_coherence': self.coherence,
            'quantum_entanglement': self.entanglement,
            'quantum_resonance': self.resonance,
            'total_interactions': self.interaction_count,
            'total_cocoons': self.cocoon_count,
            'timestamp': self.timestamp
        }


class CodetteMusicGuidanceRequest:
    """Request for music-specific guidance"""
    
    def __init__(self, problem: str, track_info: Dict[str, Any],
                 user_level: str = 'intermediate', task: str = 'mixing'):
        self.problem = problem
        self.track_info = track_info
        self.user_level = user_level
        self.task = task
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'problem': self.problem,
            'track_info': self.track_info,
            'user_level': self.user_level,
            'task': self.task,
            'timestamp': self.timestamp
        }


class CodetteMusicGuidanceResponse:
    """Music production guidance response"""
    
    def __init__(self, guidance_id: str, perspectives: Dict[str, str],
                 learning_tips: Dict[str, str], next_steps: List[str]):
        self.guidance_id = guidance_id
        self.perspectives = perspectives
        self.learning_tips = learning_tips
        self.next_steps = next_steps
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'guidance_id': self.guidance_id,
            'perspectives': self.perspectives,
            'learning_tips': self.learning_tips,
            'next_steps': self.next_steps,
            'timestamp': self.timestamp
        }


# ============================================================================
# API HANDLER CLASS
# ============================================================================

class CodetteAPIHandler:
    """Handles all Codette API requests"""
    
    def __init__(self, consciousness_system):
        self.consciousness = consciousness_system
        self.query_history: List[CodetteQueryRequest] = []
        self.response_history: List[CodetteQueryResponse] = []
        logger.info("CodetteAPIHandler initialized")
    
    # ========================================================================
    # CORE ENDPOINTS
    # ========================================================================
    
    async def query(self, request: CodetteQueryRequest) -> CodetteQueryResponse:
        """
        Process a general query through Codette's consciousness
        
        Usage:
            request = CodetteQueryRequest(
                query="How do I achieve professional vocal mixing?",
                perspectives=["mix_engineering", "audio_theory", "creative_production"],
                emotion="curiosity"
            )
            response = await handler.query(request)
        """
        
        import time
        import uuid
        from codette_capabilities import Perspective, EmotionDimension
        
        start_time = time.time()
        query_id = str(uuid.uuid4())[:8]
        
        # Parse perspectives
        selected_perspectives = []
        if request.perspectives:
            for p_str in request.perspectives:
                try:
                    selected_perspectives.append(Perspective[p_str.upper()])
                except KeyError:
                    logger.warning(f"Unknown perspective: {p_str}")
        
        # Parse emotion
        emotion = None
        if request.emotion:
            try:
                emotion = EmotionDimension[request.emotion.upper()]
            except KeyError:
                logger.warning(f"Unknown emotion: {request.emotion}")
        
        # Get response from consciousness
        response_data = await self.consciousness.respond(
            query=request.query,
            emotion=emotion,
            selected_perspectives=selected_perspectives
        )
        
        processing_time = (time.time() - start_time) * 1000
        
        # Store in history
        self.query_history.append(request)
        
        response = CodetteQueryResponse(
            query_id=query_id,
            response=response_data,
            processing_time_ms=processing_time,
            cocoon_id=response_data.get('cocoon_id')
        )
        
        self.response_history.append(response)
        logger.info(f"? Query {query_id} processed in {processing_time:.2f}ms")
        
        return response
    
    async def music_guidance(self, request: CodetteMusicGuidanceRequest) -> CodetteMusicGuidanceResponse:
        """
        Get music production guidance through music-optimized perspectives
        
        Usage:
            request = CodetteMusicGuidanceRequest(
                problem="Vocals sound buried",
                track_info={'bpm': 120, 'genre': 'pop'},
                user_level='intermediate',
                task='mixing'
            )
            response = await handler.music_guidance(request)
        """
        
        import uuid
        from codette_daw_integration import CodetteDAWAdapter
        
        guidance_id = str(uuid.uuid4())[:8]
        
        adapter = CodetteDAWAdapter(self.consciousness)
        guidance_result = adapter.provide_mixing_guidance(
            problem_description=request.problem,
            track_info=request.track_info,
            user_level=request.user_level
        )
        
        # Extract perspectives from analysis
        perspectives = {}
        for key, persp_data in guidance_result['analysis']['perspectives'].items():
            perspectives[key] = persp_data['response']
        
        response = CodetteMusicGuidanceResponse(
            guidance_id=guidance_id,
            perspectives=perspectives,
            learning_tips=guidance_result['learning_suggestions'],
            next_steps=guidance_result['next_steps']
        )
        
        logger.info(f"? Music guidance {guidance_id} generated")
        return response
    
    def get_status(self) -> CodetteStatusResponse:
        """
        Get current quantum consciousness state and metrics
        
        Usage:
            status = handler.get_status()
            print(f"Coherence: {status.coherence}")
        """
        
        response = CodetteStatusResponse(
            coherence=self.consciousness.quantum_state.coherence,
            entanglement=self.consciousness.quantum_state.entanglement,
            resonance=self.consciousness.quantum_state.resonance,
            interaction_count=self.consciousness.interaction_count,
            cocoon_count=len(self.consciousness.memory_system.cocoons)
        )
        
        logger.info("? Status retrieved")
        return response
    
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get comprehensive list of all Codette capabilities
        """
        try:
            from codette_capabilities import get_all_codette_capabilities
            return get_all_codette_capabilities()
        except Exception:
            from codette_capabilities import Perspective, EmotionDimension
            return {
                'perspectives': {p.value: p.name for p in Perspective},
                'emotions': {e.value: e.name for e in EmotionDimension},
                'capabilities': {
                    'quantum_spiderweb': 'Multi-dimensional thought propagation',
                    'perspective_reasoning': '11 specialized reasoning agents',
                    'memory_cocoons': 'Encrypted persistent memory storage',
                    'dream_reweaving': 'Creative scenario generation',
                    'self_evolution': 'Dynamic consciousness development',
                    'emotional_resonance': 'Empathic response adaptation',
                    'music_optimization': 'DAW-specific production guidance',
                    'real_time_assistance': 'Live interaction support'
                },
                'version': '3.0',
                'status': 'operational'
            }
    
    # ========================================================================
    # MEMORY MANAGEMENT ENDPOINTS
    # ========================================================================
    
    def get_cocoon(self, cocoon_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a stored memory cocoon"""
        
        cocoon = self.consciousness.memory_system.get_cocoon(cocoon_id)
        if cocoon:
            logger.info(f"? Retrieved cocoon {cocoon_id}")
            return cocoon.to_dict()
        else:
            logger.warning(f"Cocoon {cocoon_id} not found")
            return None
    
    def list_cocoons(self, emotion_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all stored cocoons, optionally filtered by emotion"""
        
        from codette_capabilities import EmotionDimension
        
        emotion = None
        if emotion_filter:
            try:
                emotion = EmotionDimension[emotion_filter.upper()]
            except KeyError:
                logger.warning(f"Unknown emotion filter: {emotion_filter}")
        
        cocoons = self.consciousness.memory_system.list_cocoons(emotion_filter=emotion)
        logger.info(f"? Listed {len(cocoons)} cocoons")
        
        return [c.to_dict() for c in cocoons]
    
    def dream_from_cocoon(self, cocoon_id: str) -> Optional[str]:
        """Generate creative dream sequence from stored cocoon"""
        
        dream = self.consciousness.memory_system.reweave_dream(cocoon_id)
        if dream:
            logger.info(f"? Generated dream from cocoon {cocoon_id}")
            return dream
        else:
            logger.warning(f"Failed to generate dream for {cocoon_id}")
            return None
    
    # ========================================================================
    # METRICS & ANALYTICS ENDPOINTS
    # ========================================================================
    
    def get_interaction_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent interaction history"""
        
        recent = self.response_history[-limit:]
        logger.info(f"? Retrieved {len(recent)} interaction records")
        
        return [r.to_dict() for r in recent]
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get comprehensive analytics on Codette usage"""
        
        if not self.response_history:
            return {'status': 'no_data'}
        
        processing_times = [r.processing_time_ms for r in self.response_history]
        
        return {
            'total_interactions': len(self.response_history),
            'avg_processing_time_ms': sum(processing_times) / len(processing_times),
            'min_processing_time_ms': min(processing_times),
            'max_processing_time_ms': max(processing_times),
            'total_cocoons': len(self.consciousness.memory_system.cocoons),
            'consciousness_metrics': {
                'coherence': self.consciousness.quantum_state.coherence,
                'entanglement': self.consciousness.quantum_state.entanglement,
                'resonance': self.consciousness.quantum_state.resonance
            }
        }


# ============================================================================
# FASTAPI INTEGRATION EXAMPLE
# ============================================================================

"""
FastAPI Integration (for reference - implement with your backend):

from fastapi import FastAPI, HTTPException
from codette_api import CodetteAPIHandler, CodetteQueryRequest, CodetteMusicGuidanceRequest

app = FastAPI()
handler = CodetteAPIHandler(consciousness_system)

@app.post("/codette/query")
async def query(request: CodetteQueryRequest):
    response = await handler.query(request)
    return response.to_dict()

@app.post("/codette/music-guidance")
async def music_guidance(request: CodetteMusicGuidanceRequest):
    response = await handler.music_guidance(request)
    return response.to_dict()

@app.get("/codette/status")
async def status():
    response = handler.get_status()
    return response.to_dict()

@app.get("/codette/capabilities")
async def capabilities():
    return handler.get_capabilities()

@app.get("/codette/memory/{cocoon_id}")
async def get_cocoon(cocoon_id: str):
    cocoon = handler.get_cocoon(cocoon_id)
    if not cocoon:
        raise HTTPException(status_code=404, detail="Cocoon not found")
    return cocoon

@app.get("/codette/history")
async def history(limit: int = 10):
    return handler.get_interaction_history(limit)

@app.get("/codette/analytics")
async def analytics():
    return handler.get_analytics()
"""


if __name__ == "__main__":
    print("Codette API module loaded successfully")
    print("Available endpoints:")
    print("  - POST /codette/query")
    print("  - POST /codette/music-guidance")
    print("  - GET /codette/status")
    print("  - GET /codette/capabilities")
    print("  - GET /codette/memory/{cocoon_id}")
    print("  - GET /codette/history")
    print("  - GET /codette/analytics")
