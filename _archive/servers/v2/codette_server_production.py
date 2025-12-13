#!/usr/bin/env python
"""
Codette AI Production Server
FastAPI-based REST API for CoreLogic Studio DAW integration
Minimal dependencies - no Gradio, no file watching
"""

import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any, List
import json
import logging
from datetime import datetime

# Setup paths
codette_root = Path(__file__).parent / "codette"
sys.path.insert(0, str(codette_root))
sys.path.insert(0, str(codette_root.parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# REAL CODETTE AI ENGINE
# ============================================================================

try:
    from codette_real_engine import get_real_codette_engine
    codette_engine = get_real_codette_engine()
    logger.info("✅ Real Codette AI Engine initialized successfully")
    USE_REAL_ENGINE = True
except Exception as e:
    logger.warning(f"⚠️ Failed to load real Codette engine: {e}")
    logger.warning("Falling back to mock engine")
    codette_engine = None
    USE_REAL_ENGINE = False

# ============================================================================
# FASTAPI MODELS
# ============================================================================

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    context: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    confidence: float = 0.85
    source: str = "codette-ai"
    timestamp: str

class SuggestionContext(BaseModel):
    type: str  # "mixing", "mastering", "effect", etc.
    mood: Optional[str] = None
    genre: Optional[str] = None
    bpm: Optional[float] = None
    track_type: Optional[str] = None

class SuggestionRequest(BaseModel):
    context: SuggestionContext
    limit: int = 5

class AudioSuggestion(BaseModel):
    id: str
    type: str  # "effect", "parameter", "automation", "routing", "mixing"
    title: str
    description: str
    parameters: Dict[str, Any]
    confidence: float
    category: str

class SuggestionResponse(BaseModel):
    suggestions: List[AudioSuggestion]
    context: str
    timestamp: str

class AudioData(BaseModel):
    duration: float
    sample_rate: int
    peak_level: Optional[float] = None
    rms_level: Optional[float] = None

class AnalysisRequest(BaseModel):
    audio_data: Optional[AudioData] = None
    analysis_type: str  # "spectrum", "dynamic", "loudness", "quality"
    track_data: Optional[Dict[str, str]] = None

class AnalysisResponse(BaseModel):
    analysis_type: str
    results: Dict[str, Any]
    recommendations: List[str]
    quality_score: float
    timestamp: str

class SyncRequest(BaseModel):
    tracks: List[Dict[str, Any]]
    current_time: float
    is_playing: bool
    bpm: float

class SyncResponse(BaseModel):
    synced: bool
    timestamp: str
    status: str

# ============================================================================
# CODETTE AI ENGINE (Simplified)
# ============================================================================

class CodetteMockEngine:
    """
    Mock Codette AI engine for development
    In production, this would call the full Codette system
    """
    
    def __init__(self):
        self.conversation_history = {}
        self.suggestions_cache = {}
        logger.info("🧠 Codette AI Engine initialized")
    
    def process_chat(self, message: str, conversation_id: str) -> Dict[str, Any]:
        """Process chat message through AI"""
        logger.info(f"[Chat] Processing: {message[:50]}...")
        
        # Simple perspective-based responses
        responses = {
            "suggest": "I recommend using a high-pass filter on background elements to clean up frequency space.",
            "mix": "Consider automating the reverb wet signal for dynamic depth control.",
            "master": "Your mix looks great! Try gentle multiband compression on the mid-range.",
            "eq": "A resonant peak around 3kHz might be adding harshness. Try a slight cut.",
            "effect": "This could benefit from parallel processing to preserve transients.",
            "default": "Interesting question! Let me analyze the audio context..."
        }
        
        # Detect intent from message
        intent = "default"
        for key in responses.keys():
            if key in message.lower():
                intent = key
                break
        
        return {
            "response": responses[intent],
            "confidence": 0.85,
            "source": "codette-neural-path",
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_suggestions(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate AI suggestions based on context"""
        track_type = context.get("track_type", "audio")
        category = context.get("type", "mixing")
        
        suggestions_db = {
            "mixing": [
                {
                    "id": "sugg-1",
                    "type": "effect",
                    "title": "Parallel Compression",
                    "description": "Add parallel compression on the drum bus for punchier transients",
                    "parameters": {"ratio": 4, "threshold": -20, "makeup_gain": 6},
                    "confidence": 0.92,
                    "category": "compression"
                },
                {
                    "id": "sugg-2",
                    "type": "automation",
                    "title": "Dynamic Reverb",
                    "description": "Automate reverb send to increase during vocal phrases",
                    "parameters": {"start_wet": 0.3, "peak_wet": 0.7, "curve": "exponential"},
                    "confidence": 0.88,
                    "category": "reverb"
                },
                {
                    "id": "sugg-3",
                    "type": "routing",
                    "title": "Sidechain Setup",
                    "description": "Route kick drum to sidechain compressor on synth bass",
                    "parameters": {"source": "drum-bus", "target": "bass-synth", "depth": 5},
                    "confidence": 0.85,
                    "category": "routing"
                },
            ],
            "mastering": [
                {
                    "id": "sugg-4",
                    "type": "effect",
                    "title": "Multiband Compression",
                    "description": "Apply gentle multiband compression for spectral balance",
                    "parameters": {"bands": 4, "ratio": 2.5, "threshold": -18},
                    "confidence": 0.89,
                    "category": "compression"
                },
            ]
        }
        
        return suggestions_db.get(category, suggestions_db["mixing"])[:5]
    
    def analyze_audio(self, audio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze audio and provide insights"""
        logger.info(f"[Analysis] Analyzing audio: {audio_data.get('duration', 0):.1f}s")
        
        return {
            "analysis_type": audio_data.get("analysis_type", "spectrum"),
            "results": {
                "frequency_balance": "Slight presence peak around 5kHz",
                "dynamic_range": "12.3 dB",
                "loudness_integrated": "-14.2 LUFS",
                "peak_level": audio_data.get("peak_level", -2.1),
                "rms_level": audio_data.get("rms_level", -18.5),
                "spectral_centroid": "4.2 kHz"
            },
            "recommendations": [
                "Consider reducing presence peak for smoother tone",
                "Mix is well-balanced across frequency spectrum",
                "Dynamic range is excellent for commercial production"
            ],
            "quality_score": 0.87,
            "timestamp": datetime.now().isoformat()
        }
    
    def sync_daw_state(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Sync DAW state with AI engine"""
        logger.info(f"[Sync] Syncing DAW state: {state.get('is_playing')} @ {state.get('bpm')} BPM")
        
        return {
            "synced": True,
            "timestamp": datetime.now().isoformat(),
            "status": f"Synced {len(state.get('tracks', []))} tracks at {state.get('bpm', 120)} BPM"
        }

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="Codette AI Server",
    description="AI backend for CoreLogic Studio DAW",
    version="1.0.0"
)

# Add CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4173", "http://localhost:4174", "http://localhost:5173",
        "http://localhost:3000", "http://127.0.0.1:4173", "http://127.0.0.1:4174",
        "http://127.0.0.1:5173", "http://localhost:8001", "http://127.0.0.1:8001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Codette engine - REAL first, then mock fallback
if USE_REAL_ENGINE and codette_engine:
    logger.info("🧠 Using REAL Codette AI Engine with multi-perspective reasoning")
    real_engine = codette_engine
else:
    logger.info("🤖 Using mock Codette engine (real engine not available)")
    real_engine = CodetteMockEngine()

# ============================================================================
# HEALTH & STATUS ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Codette AI Server",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "codette-ai",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/status")
async def status():
    """Detailed status endpoint"""
    status_info = {
        "service": "Codette AI Server",
        "status": "running",
        "port": 8001,
        "cors_enabled": True,
        "frontend_url": "http://localhost:5173",
        "timestamp": datetime.now().isoformat()
    }
    
    # Add real engine info if available
    if USE_REAL_ENGINE and hasattr(real_engine, 'get_status'):
        try:
            engine_status = real_engine.get_status()
            status_info["ai_engine"] = engine_status
            status_info["ai_mode"] = "REAL - Multi-perspective Reasoning"
        except:
            status_info["ai_mode"] = "FALLBACK - Mock Engine"
    else:
        status_info["ai_mode"] = "FALLBACK - Mock Engine"
    
    return status_info

# ============================================================================
# CHAT ENDPOINTS
# ============================================================================

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with Codette AI"""
    try:
        # Use real engine if available, otherwise mock
        if USE_REAL_ENGINE and hasattr(real_engine, 'process_chat_real'):
            result = real_engine.process_chat_real(
                request.message,
                request.conversation_id or "default"
            )
        else:
            result = real_engine.process_chat(
                request.message,
                request.conversation_id or "default"
            )
        return ChatResponse(**result)
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/codette/respond")
async def respond(request: ChatRequest):
    """Alternative chat endpoint (compatibility)"""
    try:
        result = codette_engine.process_chat(
            request.message,
            request.conversation_id or "default"
        )
        return result
    except Exception as e:
        logger.error(f"Respond error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# SUGGESTION ENDPOINTS
# ============================================================================

@app.post("/suggestions", response_model=SuggestionResponse)
async def get_suggestions(request: SuggestionRequest):
    """Get AI suggestions for audio context"""
    try:
        # Use real engine if available
        if USE_REAL_ENGINE and hasattr(real_engine, 'generate_suggestions_real'):
            suggestions = real_engine.generate_suggestions_real(request.context.dict())
        else:
            suggestions = real_engine.generate_suggestions(request.context.dict())
        return SuggestionResponse(
            suggestions=[AudioSuggestion(**s) for s in suggestions],
            context=request.context.type,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Suggestions error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_audio(request: AnalysisRequest):
    """Analyze audio and provide recommendations"""
    try:
        audio_dict = request.audio_data.dict() if request.audio_data else {}
        audio_dict["analysis_type"] = request.analysis_type
        
        # Use real engine if available
        if USE_REAL_ENGINE and hasattr(real_engine, 'analyze_audio_real'):
            analysis = real_engine.analyze_audio_real(audio_dict)
        else:
            analysis = real_engine.analyze_audio(audio_dict)
        return AnalysisResponse(**analysis)
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# SYNC ENDPOINTS
# ============================================================================

@app.post("/sync", response_model=SyncResponse)
async def sync_state(request: SyncRequest):
    """Sync DAW state with AI engine"""
    try:
        # Use real engine if available
        if USE_REAL_ENGINE and hasattr(real_engine, 'sync_daw_state_real'):
            result = real_engine.sync_daw_state_real(request.dict())
        else:
            result = real_engine.sync_daw_state(request.dict())
        return SyncResponse(**result)
    except Exception as e:
        logger.error(f"Sync error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Start the server"""
    print("\n" + "="*70)
    print("🚀 CODETTE AI SERVER - PRODUCTION MODE")
    print("="*70)
    print("📡 Server: FastAPI + Uvicorn")
    print("🔗 URL:    http://127.0.0.1:8001")
    print("🧠 AI:     Codette Neural Engine")
    print("💫 CORS:   Enabled for React (localhost:5173)")
    print("="*70 + "\n")
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8001,
        log_level="info",
        reload=False  # Disable reload to avoid watch mode issues
    )

if __name__ == "__main__":
    main()
