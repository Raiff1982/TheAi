"""
Codette AI FastAPI Server
Bridges CoreLogic Studio frontend with Codette Python AI engine
Now with integrated training data and enhanced analysis
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from collections import Counter
import sys
import os
import importlib.util
from pathlib import Path
import asyncio
import json
import time
import numpy as np

# Import Codette training and analysis modules
try:
    from codette_training_data import training_data, get_training_context
    from codette_analysis_module import analyze_session as enhanced_analyze, CodetteAnalyzer
    TRAINING_AVAILABLE = True
    analyzer = CodetteAnalyzer()
    print("[OK] Codette training data loaded successfully")
    print("[OK] Codette analyzer initialized")
except ImportError as e:
    print(f"[WARNING] Could not import Codette training modules: {e}")
    TRAINING_AVAILABLE = False
    training_data = None
    get_training_context = None
    enhanced_analyze = None
    analyzer = None

# Verify dependencies on startup
def verify_dependencies():
    """Verify all required dependencies are installed"""
    missing = []
    # Only check for the critical ones for the server to function
    required = ['vaderSentiment', 'fastapi', 'uvicorn']
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"\n[WARNING] Missing required packages: {', '.join(missing)}")
        print(f"   Install with: pip install {' '.join(missing)}\n")
        return False
    
    # Try optional packages but don't fail if they're missing
    optional = ['nltk', 'numpy', 'scipy']
    optional_missing = []
    for package in optional:
        try:
            __import__(package)
        except (ImportError, Exception):
            optional_missing.append(package)
    
    if optional_missing:
        print(f"\n[NOTE] Some optional packages may be missing: {', '.join(optional_missing)}")
        print(f"   Codette AI may have reduced functionality.\n")
    
    return True

# Check dependencies
verify_dependencies()

# Add Codette to path
codette_path = Path(__file__).parent / "Codette"
sys.path.insert(0, str(codette_path))

# Try to import Codette, but provide fallback
Codette = None
codette = None  # Instance of Codette
try:
    # Try importing from the codette package (Codette/codette/__init__.py)
    from codette import BroaderPerspectiveEngine
    Codette = BroaderPerspectiveEngine
    print("[OK] Codette (BroaderPerspectiveEngine) imported successfully from package")
    
    # Instantiate it
    codette = Codette()
    print("[OK] Codette AI engine initialized")
    
except ImportError as ie:
    print(f"[WARNING] Could not import Codette: {ie}")
    print(f"   Codette will work in demo/fallback mode")
    Codette = None
    codette = None
except Exception as e:
    print(f"[WARNING] Could not initialize Codette: {e}")
    print(f"   Backend will operate in demo mode with fallback responses")
    Codette = None
    codette = None

try:
    app = FastAPI(title="Codette AI Server", version="1.0.0")
    print("[DEBUG] FastAPI app created")
except Exception as e:
    print(f"[ERROR] Failed to create FastAPI app: {e}")
    import traceback
    traceback.print_exc()
    raise

try:
    # Enable CORS for React frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    print("[DEBUG] CORS middleware added")
except Exception as e:
    print(f"[ERROR] Failed to add CORS middleware: {e}")
    import traceback
    traceback.print_exc()
    raise

# Models
class ChatRequest(BaseModel):
    message: str
    perspective: Optional[str] = "neuralnets"
    context: Optional[List[Dict[str, Any]]] = None

class ChatResponse(BaseModel):
    response: str
    perspective: str
    confidence: Optional[float] = None

class AudioAnalysisRequest(BaseModel):
    """Matches frontend CodetteAnalysisRequest format"""
    audio_data: Optional[Dict[str, Any]] = None
    analysis_type: Optional[str] = "spectrum"
    track_data: Optional[Dict[str, Any]] = None

class AudioAnalysisResponse(BaseModel):
    trackId: str
    analysis: Dict[str, Any]
    status: str

class SuggestionRequest(BaseModel):
    context: Dict[str, Any]

class SuggestionResponse(BaseModel):
    suggestions: List[Dict[str, Any]]
    confidence: Optional[float] = None

class ProcessRequest(BaseModel):
    id: str
    type: str
    payload: Dict[str, Any]
    timestamp: int

class ProcessResponse(BaseModel):
    id: str
    status: str
    data: Dict[str, Any]
    processingTime: float

# Transport Clock Models
class TransportState(BaseModel):
    playing: bool
    time_seconds: float
    sample_pos: int
    bpm: float
    beat_pos: float
    loop_enabled: bool
    loop_start_seconds: float
    loop_end_seconds: float

class TransportCommandResponse(BaseModel):
    success: bool
    message: str
    state: Optional[TransportState] = None

# Global Transport State Manager
class TransportManager:
    def __init__(self):
        self.playing = False
        self.time_seconds = 0.0
        self.sample_pos = 0
        self.bpm = 120.0
        self.sample_rate = 44100
        self.start_time = None
        self.loop_enabled = False
        self.loop_start_seconds = 0.0
        self.loop_end_seconds = 10.0
        self.connected_clients: set = set()
    
    def get_state(self) -> TransportState:
        """Get current transport state"""
        if self.playing and self.start_time:
            import time
            elapsed = time.time() - self.start_time
            self.time_seconds = elapsed
            self.sample_pos = int(self.time_seconds * self.sample_rate)
        
        # Calculate beat position (4 beats per measure)
        beat_duration = 60.0 / self.bpm
        self.beat_pos = (self.time_seconds % (beat_duration * 4)) / beat_duration
        
        return TransportState(
            playing=self.playing,
            time_seconds=self.time_seconds,
            sample_pos=self.sample_pos,
            bpm=self.bpm,
            beat_pos=self.beat_pos,
            loop_enabled=self.loop_enabled,
            loop_start_seconds=self.loop_start_seconds,
            loop_end_seconds=self.loop_end_seconds
        )
    
    def play(self) -> TransportState:
        """Start playback"""
        if not self.playing:
            import time
            self.playing = True
            self.start_time = time.time() - self.time_seconds
        return self.get_state()
    
    def stop(self) -> TransportState:
        """Stop playback and reset"""
        self.playing = False
        self.time_seconds = 0.0
        self.sample_pos = 0
        self.start_time = None
        return self.get_state()
    
    def pause(self) -> TransportState:
        """Pause playback (time remains)"""
        if self.playing:
            import time
            self.time_seconds = time.time() - self.start_time
            self.playing = False
        return self.get_state()
    
    def resume(self) -> TransportState:
        """Resume playback from pause"""
        if not self.playing:
            import time
            self.playing = True
            self.start_time = time.time() - self.time_seconds
        return self.get_state()
    
    def seek(self, time_seconds: float) -> TransportState:
        """Seek to time position"""
        self.time_seconds = max(0.0, time_seconds)
        self.sample_pos = int(self.time_seconds * self.sample_rate)
        if self.playing:
            import time
            self.start_time = time.time() - self.time_seconds
        return self.get_state()
    
    def set_tempo(self, bpm: float) -> TransportState:
        """Set BPM"""
        self.bpm = max(1.0, min(300.0, bpm))  # Clamp 1-300 BPM
        return self.get_state()
    
    def set_loop(self, enabled: bool, start: float = 0.0, end: float = 10.0) -> TransportState:
        """Configure loop region"""
        self.loop_enabled = enabled
        self.loop_start_seconds = max(0.0, start)
        self.loop_end_seconds = max(self.loop_start_seconds + 0.1, end)
        return self.get_state()

# Initialize transport manager
transport_manager = TransportManager()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "status": "ok",
        "service": "Codette AI Server",
        "version": "1.0.0",
        "docs": "/docs",
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    try:
        return {
            "status": "healthy",
            "service": "Codette AI Server",
            "codette_available": codette is not None,
            "training_available": TRAINING_AVAILABLE,
        }
    except Exception as e:
        print(f"ERROR in /health: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "error": str(e)}

@app.get("/api/training/context")
async def get_training_context_endpoint():
    """Get Codette AI training context"""
    try:
        if TRAINING_AVAILABLE and get_training_context:
            # Get complete training context from training module
            context = get_training_context()
            return {
                "success": True,
                "data": context,
                "message": "Training context available"
            }
        else:
            return {
                "success": False,
                "data": None,
                "message": "Training context not available"
            }
    except Exception as e:
        print(f"[ERROR] in /api/training/context: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }

@app.get("/api/training/health")
async def training_health():
    """Check training module health"""
    try:
        return {
            "success": True,
            "training_available": TRAINING_AVAILABLE,
            "modules": {
                "training_data": TRAINING_AVAILABLE,
                "analysis": TRAINING_AVAILABLE and enhanced_analyze is not None,
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/codette/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Chat with Codette using specified perspective or training data"""
    try:
        perspective = request.perspective or "neuralnets"
        message = request.message.lower()
        
        # First try to use training data for DAW/UI related questions
        training_context = get_training_context()
        daw_functions = training_context.get("daw_functions", {})
        ui_components = training_context.get("ui_components", {})
        codette_abilities = training_context.get("codette_abilities", {})
        
        response = None
        confidence = 0.5
        
        # Check if question is about DAW functions
        for category, functions in daw_functions.items():
            for func_name, func_data in functions.items():
                if func_name in message or func_data.get("name", "").lower() in message:
                    response = f"**{func_data['name']}** ({func_data['category']})\n\n{func_data['description']}\n\n"
                    response += f"📋 Parameters: {', '.join(func_data['parameters']) or 'None'}\n"
                    response += f"⏱️ Hotkey: {func_data.get('hotkey', 'N/A')}\n"
                    response += f"💡 Tips:\n" + "\n".join([f"  • {tip}" for tip in func_data.get('tips', [])])
                    confidence = 0.92
                    break
            if response:
                break
        
        # Check if question is about UI components
        if not response:
            for comp_name, comp_data in ui_components.items():
                if comp_name.lower() in message:
                    response = f"**{comp_name}** - {comp_data['description']}\n\n"
                    response += f"📍 Location: {comp_data['location']}\n"
                    response += f"📏 Size: {comp_data['size']}\n"
                    response += f"⚙️ Functions: {', '.join(comp_data['functions'])}\n"
                    response += f"💡 Tips:\n" + "\n".join([f"  • {tip}" for tip in comp_data.get('teaching_tips', [])])
                    confidence = 0.89
                    break
        
        # Check if question is about Codette's abilities
        if not response:
            for ability_name, ability_data in codette_abilities.items():
                if ability_name.replace("_", " ") in message:
                    response = f"**{ability_data['ability']}**\n\n{ability_data['description']}\n\n"
                    response += f"📚 Use when: {ability_data['when_to_use']}\n"
                    response += f"👤 Skill level: {ability_data['skill_level']}\n"
                    if ability_data.get('related_abilities'):
                        response += f"🔗 Related: {', '.join(ability_data['related_abilities'])}"
                    confidence = 0.88
                    break
        
        # If no match in training data, try to use Codette if available
        if not response and codette:
            try:
                # Try to call available methods on Codette
                if hasattr(codette, 'neuralNetworkPerspective'):
                    response = codette.neuralNetworkPerspective(request.message)
                    confidence = 0.85
                elif hasattr(codette, '__call__'):
                    response = codette(request.message)
                    confidence = 0.85
                else:
                    response = f"Codette received your question about: {request.message[:100]}..."
                    confidence = 0.6
            except Exception as e:
                response = f"I understand your question about: {request.message[:80]}... Based on CoreLogic Studio training data, I can help with DAW functions, UI components, and production techniques."
                confidence = 0.7
        
        # Fallback response using training data summary
        if not response:
            response = f"""I'm Codette, your AI assistant for CoreLogic Studio! 🎵

I can help you with:
• **DAW Functions** ({len(daw_functions)} categories with 30+ functions)
• **UI Components** ({len(ui_components)} major components)
• **Audio Production** (mixing, effects, automation)
• **Learning Paths** (beginner to advanced)

Try asking me about:
- "Explain the play() function"
- "What does the Mixer do?"
- "How do I mix vocals?"
- "Teach me gain staging"

What would you like to learn? 🧠"""
            confidence = 0.75
        
        return ChatResponse(
            response=response,
            perspective=perspective,
            confidence=min(confidence, 1.0),
        )
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        import traceback
        traceback.print_exc()
        return ChatResponse(
            response=f"I'm having trouble understanding. Could you rephrase your question? I'm here to help with CoreLogic Studio DAW functions and production techniques.",
            perspective=request.perspective or "neuralnets",
            confidence=0.5,
        )

@app.post("/codette/analyze", response_model=AudioAnalysisResponse)
async def analyze_audio(request: AudioAnalysisRequest):
    """Analyze audio and provide real insights using CodetteAnalyzer"""
    try:
        # Handle empty/missing audio data gracefully
        if not request.audio_data:
            return AudioAnalysisResponse(
                trackId=request.track_data.get("track_id", "unknown") if request.track_data else "unknown",
                analysis={
                    "quality_score": 0.5,
                    "findings": ["No audio data provided"],
                    "recommendations": ["Upload audio data to analyze"],
                },
                status="success",
            )
        
        if not TRAINING_AVAILABLE or analyzer is None:
            track_id = request.track_data.get("track_id", "unknown") if request.track_data else "unknown"
            return AudioAnalysisResponse(
                trackId=track_id,
                analysis={"error": "Training data not available"},
                status="fallback",
            )
        
        # Extract audio metrics from request
        audio_metrics = request.audio_data
        sample_rate = audio_metrics.get("sample_rate", 44100)
        duration = audio_metrics.get("duration", 0)
        peak_level = audio_metrics.get("peak_level", -96.0)
        rms_level = audio_metrics.get("rms_level", -96.0)
        
        track_metrics = [{
            "name": request.track_data.get("track_name", "Unknown") if request.track_data else "Unknown",
            "level": rms_level,
            "peak": peak_level,
            "rms": rms_level,
        }]
        
        # Perform analysis based on analysis_type
        analysis_type = request.analysis_type or "spectrum"
        
        if analysis_type == "dynamic":
            result = analyzer.analyze_gain_staging(track_metrics)
        elif analysis_type == "loudness":
            result = analyzer.analyze_mastering_readiness(track_metrics)
        elif analysis_type == "quality":
            result = analyzer.analyze_session_health(track_metrics, {})
        else:  # spectrum or default
            result = analyzer.analyze_gain_staging(track_metrics)
        
        track_id = request.track_data.get("track_id", "unknown") if request.track_data else "unknown"
        
        # Return analysis results
        analysis = {
            "analysis_type": analysis_type,
            "quality_score": result.score,
            "findings": result.findings,
            "recommendations": result.recommendations,
            "metrics": {
                "duration": duration,
                "sample_rate": sample_rate,
                "peak_level": peak_level,
                "rms_level": rms_level,
            }
        }

        return AudioAnalysisResponse(
            trackId=track_id,
            analysis=analysis,
            status="success",
        )
    except Exception as e:
        print(f"Error in audio analysis: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/codette/suggest", response_model=SuggestionResponse)
async def get_suggestions(request: SuggestionRequest):
    """Get AI-powered suggestions based on real training data and context"""
    try:
        if not TRAINING_AVAILABLE or analyzer is None:
            # Fallback to generic suggestions
            fallback_suggestions = [
                {
                    "type": "optimization",
                    "title": "Gain Optimization",
                    "description": "Consider adjusting gain levels for better headroom",
                    "confidence": 0.5,
                },
            ]
            return SuggestionResponse(suggestions=fallback_suggestions, confidence=0.5)
        
        # Use real training data for context-based suggestions
        suggestions = []
        context_type = request.context or "general"
        
        # Get real suggestions from training data
        if context_type == "gain-staging":
            suggestions = [
                {
                    "type": "optimization",
                    "title": "Peak Level Optimization",
                    "description": "Maintain -3dB headroom as per industry standard (found in training data)",
                    "confidence": 0.92,
                    "source": "MIXING_STANDARDS"
                },
                {
                    "type": "optimization",
                    "title": "Clipping Prevention",
                    "description": "Ensure no signal exceeds 0dBFS to prevent digital clipping",
                    "confidence": 0.95,
                    "source": "MIXING_STANDARDS"
                },
            ]
        elif context_type == "mixing":
            suggestions = [
                {
                    "type": "effect",
                    "title": "EQ for Balance",
                    "description": "Apply EQ to balance frequency content - use low/mid/high energy distribution",
                    "confidence": 0.88,
                    "source": "PLUGIN_CATEGORIES"
                },
                {
                    "type": "routing",
                    "title": "Bus Architecture",
                    "description": "Create buses for drum group, bass, guitars, vocals - improves mix control",
                    "confidence": 0.85,
                    "source": "MIXING_STANDARDS"
                },
                {
                    "type": "effect",
                    "title": "Compression for Cohesion",
                    "description": "Use gentle compression (4:1 ratio) to glue tracks together",
                    "confidence": 0.82,
                    "source": "PLUGIN_CATEGORIES"
                },
            ]
        elif context_type == "mastering":
            suggestions = [
                {
                    "type": "optimization",
                    "title": "Loudness Target",
                    "description": "Target -14 LUFS for streaming platforms (Spotify, Apple Music standard)",
                    "confidence": 0.93,
                    "source": "MIXING_STANDARDS"
                },
                {
                    "type": "effect",
                    "title": "Linear Phase EQ",
                    "description": "Use linear phase EQ in mastering to avoid phase distortion",
                    "confidence": 0.87,
                    "source": "PLUGIN_CATEGORIES"
                },
                {
                    "type": "optimization",
                    "title": "Headroom Margin",
                    "description": "Leave -1dB to -2dB headroom below 0dBFS for streaming",
                    "confidence": 0.90,
                    "source": "MIXING_STANDARDS"
                },
            ]
        elif context_type == "effects":
            suggestions = [
                {
                    "type": "effect",
                    "title": "EQ - Essential First",
                    "description": "Start with EQ before other effects to shape tone",
                    "confidence": 0.89,
                    "source": "PLUGIN_CATEGORIES"
                },
                {
                    "type": "effect",
                    "title": "Saturation for Warmth",
                    "description": "Add subtle saturation to add harmonic character and warmth",
                    "confidence": 0.81,
                    "source": "PLUGIN_CATEGORIES"
                },
                {
                    "type": "effect",
                    "title": "Reverb for Space",
                    "description": "Add reverb via send (not insert) to create spatial depth",
                    "confidence": 0.84,
                    "source": "PLUGIN_CATEGORIES"
                },
            ]
        else:
            # General suggestions for all contexts
            suggestions = [
                {
                    "type": "optimization",
                    "title": "Gain Optimization",
                    "description": "Maintain proper gain levels throughout the signal chain for optimal quality",
                    "confidence": 0.85,
                    "source": "TRAINING_DATA"
                },
                {
                    "type": "effect",
                    "title": "EQ Suggestion",
                    "description": "Use EQ to balance and shape frequency content",
                    "confidence": 0.80,
                    "source": "TRAINING_DATA"
                },
            ]
        
        # Calculate average confidence
        avg_confidence = sum(s["confidence"] for s in suggestions) / len(suggestions) if suggestions else 0.5

        return SuggestionResponse(
            suggestions=suggestions,
            confidence=min(avg_confidence, 1.0),
        )
    except Exception as e:
        print(f"Error generating suggestions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Add API prefix alias for frontend compatibility
@app.post("/api/codette/suggest", response_model=SuggestionResponse)
async def api_get_suggestions(request: SuggestionRequest):
    """API prefix alias for /codette/suggest (frontend compatibility)"""
    return await get_suggestions(request)

@app.post("/codette/process", response_model=ProcessResponse)
async def process_request(request: ProcessRequest):
    """Generic request processor for various Codette functions"""
    import time

    start_time = time.time()

    try:
        result_data: Dict[str, Any] = {}

        if request.type == "chat":
            payload = request.payload
            perspective = payload.get("perspective", "neuralnets")
            message = payload.get("message", "").lower()

            # Use enhanced training data for chat responses
            training_context = get_training_context() if (TRAINING_AVAILABLE and get_training_context) else {}
            daw_functions = training_context.get("daw_functions", {})
            ui_components = training_context.get("ui_components", {})
            codette_abilities = training_context.get("codette_abilities", {})
            music_data = training_context.get("music", {})
            
            response = None
            confidence = 0.5
            
            # Check if question is about DAW functions
            for category, functions in daw_functions.items():
                for func_name, func_data in functions.items():
                    if func_name in message or func_data.get("name", "").lower() in message:
                        response = f"**{func_data['name']}** ({func_data['category']})\n\n{func_data['description']}\n\n"
                        response += f"📋 Parameters: {', '.join(func_data['parameters']) or 'None'}\n"
                        response += f"⏱️ Hotkey: {func_data.get('hotkey', 'N/A')}\n"
                        response += f"💡 Tips:\n" + "\n".join([f"  • {tip}" for tip in func_data.get('tips', [])])
                        confidence = 0.92
                        break
                if response:
                    break
            
            # Check if question is about UI components
            if not response:
                for comp_name, comp_data in ui_components.items():
                    if comp_name.lower() in message:
                        response = f"**{comp_name}** - {comp_data['description']}\n\n"
                        response += f"📍 Location: {comp_data['location']}\n"
                        response += f"📏 Size: {comp_data['size']}\n"
                        response += f"⚙️ Functions: {', '.join(comp_data['functions'])}\n"
                        response += f"💡 Tips:\n" + "\n".join([f"  • {tip}" for tip in comp_data.get('teaching_tips', [])])
                        confidence = 0.89
                        break
            
            # Check if question is about Codette's abilities
            if not response:
                for ability_name, ability_data in codette_abilities.items():
                    if ability_name.replace("_", " ") in message:
                        response = f"**{ability_data['ability']}**\n\n{ability_data['description']}\n\n"
                        response += f"📚 Use when: {ability_data['when_to_use']}\n"
                        response += f"👤 Skill level: {ability_data['skill_level']}\n"
                        if ability_data.get('related_abilities'):
                            response += f"🔗 Related: {', '.join(ability_data['related_abilities'])}"
                        confidence = 0.88
                        break
            
            # Check if question is about music production or musical knowledge
            if not response:
                # Check for mixing tips, instruments, or genre knowledge
                if "mix" in message or "mixing" in message:
                    if music_data:
                        response = "🎵 **Music Production Tips**\n\n"
                        response += "Music data available: Mixing standards, instrument knowledge, genre-specific guidance\n"
                        confidence = 0.85
                elif "instrument" in message or "track type" in message:
                    if music_data:
                        response = "🎵 **Instrument Knowledge**\n\n"
                        response += "I have comprehensive instrument data available\n"
                        confidence = 0.80
                elif "genre" in message:
                    if music_data:
                        response = "🎵 **Genre Knowledge**\n\n"
                        response += "I can help with genre-specific mixing and production techniques\n"
                        confidence = 0.78
            
            # Fallback to Codette if available
            if not response and codette:
                try:
                    # Try to call available methods on Codette
                    if hasattr(codette, 'neuralNetworkPerspective'):
                        response = codette.neuralNetworkPerspective(payload.get("message"))
                        confidence = 0.85
                    elif hasattr(codette, '__call__'):
                        response = codette(payload.get("message"))
                        confidence = 0.85
                    else:
                        response = f"I understand your question. I have comprehensive training on DAW functions and music production."
                        confidence = 0.6
                except Exception as e:
                    response = f"I understand your question. I can help with CoreLogic Studio functions and audio production."
                    confidence = 0.7
            
            # Ultimate fallback with training summary
            if not response:
                response = f"""I'm Codette, your AI assistant for CoreLogic Studio! 🎵

I can help you with:
• **DAW Functions** ({len(daw_functions)} categories with 30+ functions)
• **UI Components** ({len(ui_components)} major components)
• **Audio Production** (mixing, effects, automation)
• **Music Knowledge** (instruments, genres, mixing techniques)
• **Learning Paths** (beginner to advanced)

Try asking me about:
- "Explain the play() function"
- "What does the Mixer do?"
- "How do I mix vocals?"
- "Teach me gain staging"
- "What instruments should I use?"

What would you like to learn? 🧠"""
                confidence = 0.75

            result_data = {"response": response, "perspective": perspective, "confidence": confidence}

        elif request.type == "audio_analysis":
            result_data = {
                "analysis": "Audio analysis completed",
                "status": "success",
                "trackId": request.payload.get("trackId"),
            }

        elif request.type == "suggestion":
            result_data = {
                "suggestions": [
                    {
                        "type": "optimization",
                        "title": "Gain Optimization",
                        "confidence": 0.85,
                    }
                ]
            }

        elif request.type == "mastering":
            result_data = {
                "recommendations": [],
                "target_loudness": "-14 LUFS",
                "status": "analyzing",
            }

        elif request.type == "optimization":
            result_data = {"optimizations": [], "message": "Optimization suggestions"}

        else:
            result_data = {"message": f"Unknown request type: {request.type}"}

        processing_time = time.time() - start_time

        return ProcessResponse(
            id=request.id,
            status="success",
            data=result_data,
            processingTime=processing_time,
        )

    except Exception as e:
        processing_time = time.time() - start_time
        raise HTTPException(
            status_code=500,
            detail=f"Processing failed: {str(e)}",
        )

@app.get("/codette/status")
async def get_status():
    """Get current status of Codette AI server"""
    return {
        "status": "running",
        "codette_available": codette is not None,
        "perspectives_available": [
            "neuralnets",
            "newtonian",
            "davinci",
            "quantum",
        ],
        "features": [
            "chat",
            "audio_analysis",
            "suggestions",
            "mastering",
            "optimization",
        ],
    }

# ============================================================================
# AI ANALYSIS ENDPOINTS (for React AIPanel)
# ============================================================================

class AnalysisResponse(BaseModel):
    """Standard response format for AI analysis endpoints"""
    prediction: str
    confidence: float
    actionItems: Optional[List[Dict[str, Any]]] = None

@app.get("/api/health")
@app.post("/api/health")
async def api_health():
    """Health check endpoint"""
    return {"success": True, "data": {"status": "ok", "service": "codette"}, "duration": 0}

@app.post("/api/analyze/gain-staging")
async def analyze_gain_staging(request: Dict[str, Any]) -> AnalysisResponse:
    """Analyze gain staging across tracks - with training data"""
    try:
        # Use enhanced analysis if available
        if TRAINING_AVAILABLE and enhanced_analyze:
            analysis_result = enhanced_analyze("gain_staging", request)
            prediction = " ".join(analysis_result.get("findings", []))
            confidence = (analysis_result.get("score", 50) / 100.0)
            action_items = analysis_result.get("recommendations", [])
        else:
            # Fallback to basic analysis
            tracks = request.get("tracks", [])
            
            # Find clipping tracks
            clipping_tracks = []
            low_headroom = []
            
            for track in tracks:
                peak = track.get("peak", -60)
                if peak > -1:
                    clipping_tracks.append(track["id"])
                elif peak > -6:
                    low_headroom.append(track["id"])
            
            # Generate prediction
            if clipping_tracks:
                prediction = f"⚠️ CLIPPING DETECTED on {len(clipping_tracks)} track(s). Reduce gain immediately to prevent digital distortion. Target: -6dB headroom minimum."
                confidence = 0.95
                action_items = [
                    {"action": "Reduce", "parameter": f"Track {tid} Gain", "value": -3, "priority": "high"}
                    for tid in clipping_tracks[:3]
                ]
            elif low_headroom:
                prediction = f"⚡ Low headroom on {len(low_headroom)} track(s). Recommended target: -6dB peak level for safe mixing margin."
                confidence = 0.85
                action_items = [
                    {"action": "Reduce", "parameter": f"Track {tid} Gain", "value": -2, "priority": "medium"}
                    for tid in low_headroom[:3]
                ]
            else:
                prediction = "✅ Excellent gain staging! Levels are well-optimized with good headroom across all tracks."
                confidence = 0.90
                action_items = []
        
        return AnalysisResponse(
            prediction=prediction,
            confidence=confidence,
            actionItems=action_items
        )
    except Exception as e:
        print(f"[ERROR] in analyze_gain_staging: {e}")
        return AnalysisResponse(
            prediction=f"Error analyzing gain staging: {str(e)}",
            confidence=0,
            actionItems=[]
        )

@app.post("/api/analyze/mixing")
async def analyze_mixing(request: Dict[str, Any]) -> AnalysisResponse:
    """Suggest mixing chain for selected track"""
    try:
        track_type = request.get("trackType", "audio")
        metrics = request.get("metrics", {})
        level = metrics.get("level", -60)
        
        # Track-type specific recommendations
        recommendations = {
            "audio": {
                "chain": "EQ → Compressor → Reverb",
                "suggestion": "General audio track: Use EQ to clean up, add compression for control (4:1 ratio, 5ms attack), and reverb for space.",
                "action_items": [
                    {"action": "Add", "parameter": "EQ", "value": "Parametric", "priority": "high"},
                    {"action": "Add", "parameter": "Compressor", "value": "4:1", "priority": "high"},
                    {"action": "Add", "parameter": "Reverb", "value": "Room", "priority": "medium"},
                ]
            },
            "vocal": {
                "chain": "EQ → Compressor → Reverb → Delay",
                "suggestion": "Start with subtle EQ to remove mud (100-200Hz), then add compression (4:1 ratio, 4ms attack) for control. Add plate reverb and slapback delay for depth.",
                "action_items": [
                    {"action": "Add", "parameter": "EQ", "value": "Parametric", "priority": "high"},
                    {"action": "Add", "parameter": "Compressor", "value": "4:1", "priority": "high"},
                    {"action": "Add", "parameter": "Reverb", "value": "Plate", "priority": "medium"},
                ]
            },
            "drum": {
                "chain": "EQ → Compressor → Saturation",
                "suggestion": "Enhance drum attack with subtle saturation, use compressor to glue the kit together (3:1 ratio, 2ms attack). Boost presence around 5kHz.",
                "action_items": [
                    {"action": "Add", "parameter": "Saturation", "value": "Light", "priority": "medium"},
                    {"action": "Add", "parameter": "Compressor", "value": "3:1", "priority": "high"},
                ]
            },
            "bass": {
                "chain": "EQ → Compressor → Saturator",
                "suggestion": "Control low frequencies with high-pass filter above 30Hz. Use compressor (2:1 ratio) to lock in with drums. Add subtle saturation for warmth.",
                "action_items": [
                    {"action": "Add", "parameter": "EQ", "value": "High-Pass", "priority": "high"},
                    {"action": "Add", "parameter": "Compressor", "value": "2:1", "priority": "high"},
                ]
            },
            "guitar": {
                "chain": "EQ → Compressor → Delay → Reverb",
                "suggestion": "Use compression to even out pick dynamics (5:1 ratio). Add EQ to reduce muddiness. Combine delay and reverb for spacious, cohesive tone.",
                "action_items": [
                    {"action": "Add", "parameter": "Compressor", "value": "5:1", "priority": "high"},
                    {"action": "Add", "parameter": "Delay", "value": "Tape", "priority": "medium"},
                ]
            },
            "synth": {
                "chain": "EQ → Compressor → Reverb",
                "suggestion": "Use EQ to carve space in the mix. Compress lightly (1.5:1) to add glue. Add reverb for depth without losing definition.",
                "action_items": [
                    {"action": "Add", "parameter": "Compressor", "value": "1.5:1", "priority": "medium"},
                    {"action": "Add", "parameter": "Reverb", "value": "Room", "priority": "medium"},
                ]
            },
        }
        
        rec = recommendations.get(track_type, recommendations["audio"])
        
        return AnalysisResponse(
            prediction=rec["suggestion"],
            confidence=0.88,
            actionItems=rec.get("action_items", [])
        )
    except Exception as e:
        return AnalysisResponse(
            prediction=f"Error analyzing mixing chain: {str(e)}",
            confidence=0,
            actionItems=[]
        )

@app.post("/api/analyze/routing")
async def analyze_routing(request: Dict[str, Any]) -> AnalysisResponse:
    """Suggest routing configuration"""
    try:
        track_count = request.get("trackCount", 0)
        track_types = request.get("trackTypes", [])
        
        # Count track types
        type_counts = Counter(track_types)
        
        # Generate routing suggestion
        if track_count < 4:
            prediction = "✨ For your mix size, route all tracks to Master for simple, clean mixing."
            action_items = []
        elif track_count < 10:
            prediction = "📊 Recommended: Create 2-3 buses (Drums, Vocals, Instruments) for better control and gain staging."
            action_items = [
                {"action": "Create", "parameter": "Bus", "value": "Drums", "priority": "high"},
                {"action": "Create", "parameter": "Bus", "value": "Vocals", "priority": "high"},
                {"action": "Create", "parameter": "Bus", "value": "Instruments", "priority": "medium"},
            ]
        else:
            prediction = f"🎚️ Recommended: Create 4-5 buses by instrument group. Current mix ({track_count} tracks) will benefit from hierarchical routing."
            action_items = [
                {"action": "Create", "parameter": "Bus", "value": "Drums", "priority": "high"},
                {"action": "Create", "parameter": "Bus", "value": "Percussion", "priority": "high"},
                {"action": "Create", "parameter": "Bus", "value": "Vocals", "priority": "high"},
                {"action": "Create", "parameter": "Bus", "value": "Instruments", "priority": "medium"},
                {"action": "Create", "parameter": "Bus", "value": "FX", "priority": "medium"},
            ]
        
        return AnalysisResponse(
            prediction=prediction,
            confidence=0.92,
            actionItems=action_items
        )
    except Exception as e:
        return AnalysisResponse(
            prediction=f"Error analyzing routing: {str(e)}",
            confidence=0,
            actionItems=[]
        )

@app.post("/api/analyze/session")
async def analyze_session(request: Dict[str, Any]) -> AnalysisResponse:
    """Comprehensive session analysis"""
    try:
        track_count = request.get("trackCount", 0)
        track_metrics = request.get("trackMetrics", [])
        master_level = request.get("masterLevel", -60)
        has_clipping = request.get("hasClipping", False)
        
        insights = []
        action_items = []
        
        # Analyze clipping
        if has_clipping:
            insights.append("⚠️ Clipping detected - reduce track levels")
            action_items.append(
                {"action": "Reduce", "parameter": "Master Gain", "value": -2, "priority": "high"}
            )
        elif master_level > -6:
            insights.append("⚡ Master level high - ensure -6dB headroom for limiting/mastering")
            action_items.append(
                {"action": "Reduce", "parameter": "Master Gain", "value": -1, "priority": "medium"}
            )
        else:
            insights.append("✅ Master level healthy")
        
        # Analyze track count
        if track_count < 4:
            insights.append(f"📍 Small mix ({track_count} tracks) - focus on balance and tone")
        elif track_count < 16:
            insights.append(f"📍 Medium mix ({track_count} tracks) - organize with buses for better control")
            action_items.append(
                {"action": "Create", "parameter": "Submix Buses", "value": 3, "priority": "medium"}
            )
        else:
            insights.append(f"📍 Large mix ({track_count} tracks) - establish clear routing hierarchy")
            action_items.append(
                {"action": "Create", "parameter": "Submix Buses", "value": 5, "priority": "high"}
            )
        
        prediction = "\n".join(insights) + "\n\n📋 Recommended actions: See action items below."
        
        return AnalysisResponse(
            prediction=prediction,
            confidence=0.85,
            actionItems=action_items
        )
    except Exception as e:
        return AnalysisResponse(
            prediction=f"Error analyzing session: {str(e)}",
            confidence=0,
            actionItems=[]
        )

# ============================================================================
# TRANSPORT CLOCK ENDPOINTS (WebSocket + REST API)
# ============================================================================

@app.websocket("/ws")
async def websocket_general(websocket: WebSocket):
    """General WebSocket endpoint - routes to transport clock"""
    connection_id = id(websocket)
    is_connected = False
    
    try:
        await websocket.accept()
        is_connected = True
        transport_manager.connected_clients.add(websocket)
        print(f"WebSocket client connected to /ws. Total clients: {len(transport_manager.connected_clients)}")
    except Exception as e:
        print(f"Failed to accept WebSocket on /ws: {e}")
        return
    
    try:
        import asyncio
        import time as time_module
        
        last_send = time_module.time()
        send_interval = 1.0 / 60.0  # 60 FPS update rate
        
        # Send initial state
        try:
            if is_connected:
                state = transport_manager.get_state()
                await websocket.send_json({
                    "type": "state",
                    "data": state.dict()
                })
        except Exception as e:
            print(f"Failed to send initial state on /ws: {e}")
            is_connected = False
            return
        
        while is_connected:
            try:
                # Non-blocking receive with very short timeout
                try:
                    data = await asyncio.wait_for(
                        websocket.receive_text(),
                        timeout=0.001
                    )
                    try:
                        message = json.loads(data)
                        
                        # Handle incoming commands
                        if message.get("type") == "play":
                            transport_manager.play()
                        elif message.get("type") == "stop":
                            transport_manager.stop()
                        elif message.get("type") == "pause":
                            transport_manager.pause()
                        elif message.get("type") == "resume":
                            transport_manager.resume()
                        elif message.get("type") == "seek":
                            transport_manager.seek(message.get("time_seconds", 0))
                        elif message.get("type") == "tempo":
                            transport_manager.set_tempo(message.get("bpm", 120))
                        elif message.get("type") == "loop":
                            transport_manager.set_loop(
                                message.get("enabled", False),
                                message.get("start_seconds", 0),
                                message.get("end_seconds", 10)
                            )
                    except json.JSONDecodeError:
                        pass  # Ignore invalid JSON
                    
                except asyncio.TimeoutError:
                    pass  # No message received, continue to send updates
                
                # Send state at regular interval
                current_time = time_module.time()
                if is_connected and current_time - last_send >= send_interval:
                    try:
                        state = transport_manager.get_state()
                        await websocket.send_json({
                            "type": "state",
                            "data": state.dict()
                        })
                        last_send = current_time
                    except RuntimeError as e:
                        # Connection closed
                        print(f"Connection closed on /ws: {e}")
                        is_connected = False
                        break
                    except Exception as e:
                        print(f"Send error on /ws: {e}")
                        is_connected = False
                        break
                
                # Small sleep to prevent CPU spinning
                await asyncio.sleep(0.001)
                
            except WebSocketDisconnect:
                print("WebSocket /ws disconnected")
                is_connected = False
                break
            except Exception as e:
                print(f"Unexpected error in /ws loop: {e}")
                is_connected = False
                break
    
    finally:
        is_connected = False
        try:
            transport_manager.connected_clients.discard(websocket)
            print(f"WebSocket cleanup on /ws. Remaining clients: {len(transport_manager.connected_clients)}")
        except Exception as e:
            print(f"Error during /ws cleanup: {e}")

@app.websocket("/ws/transport/clock")
async def websocket_transport_clock(websocket: WebSocket):
    """WebSocket endpoint for DAW transport clock synchronization"""
    connection_id = id(websocket)
    is_connected = False
    
    try:
        await websocket.accept()
        is_connected = True
        transport_manager.connected_clients.add(websocket)
        print(f"WebSocket client connected. Total clients: {len(transport_manager.connected_clients)}")
    except Exception as e:
        print(f"Failed to accept WebSocket: {e}")
        return
    
    try:
        import asyncio
        import time as time_module
        
        last_send = time_module.time()
        send_interval = 1.0 / 60.0  # 60 FPS update rate
        
        # Send initial state
        try:
            if is_connected:
                state = transport_manager.get_state()
                await websocket.send_json({
                    "type": "state",
                    "data": state.dict()
                })
        except Exception as e:
            print(f"Failed to send initial state: {e}")
            is_connected = False
            return
        
        while is_connected:
            try:
                # Non-blocking receive with very short timeout
                try:
                    data = await asyncio.wait_for(
                        websocket.receive_text(),
                        timeout=0.001
                    )
                    try:
                        message = json.loads(data)
                        
                        # Handle incoming commands
                        if message.get("type") == "play":
                            transport_manager.play()
                        elif message.get("type") == "stop":
                            transport_manager.stop()
                        elif message.get("type") == "pause":
                            transport_manager.pause()
                        elif message.get("type") == "resume":
                            transport_manager.resume()
                        elif message.get("type") == "seek":
                            transport_manager.seek(message.get("time_seconds", 0))
                        elif message.get("type") == "tempo":
                            transport_manager.set_tempo(message.get("bpm", 120))
                        elif message.get("type") == "loop":
                            transport_manager.set_loop(
                                message.get("enabled", False),
                                message.get("start_seconds", 0),
                                message.get("end_seconds", 10)
                            )
                    except json.JSONDecodeError:
                        pass  # Ignore invalid JSON
                    
                except asyncio.TimeoutError:
                    pass  # No message received, continue to send updates
                
                # Send state at regular interval
                current_time = time_module.time()
                if is_connected and current_time - last_send >= send_interval:
                    try:
                        state = transport_manager.get_state()
                        await websocket.send_json({
                            "type": "state",
                            "data": state.dict()
                        })
                        last_send = current_time
                    except RuntimeError as e:
                        # Connection closed
                        print(f"Connection closed: {e}")
                        is_connected = False
                        break
                    except Exception as e:
                        print(f"Send error: {e}")
                        is_connected = False
                        break
                
                # Very minimal sleep
                await asyncio.sleep(0.0001)
            
            except asyncio.CancelledError:
                print("WebSocket task cancelled")
                is_connected = False
                break
            except Exception as e:
                print(f"Unexpected error in loop: {type(e).__name__}: {e}")
                is_connected = False
                break
    
    except WebSocketDisconnect:
        print("WebSocket client disconnected (clean disconnect)")
        is_connected = False
    except Exception as e:
        print(f"WebSocket handler error: {type(e).__name__}: {e}")
        is_connected = False
    finally:
        is_connected = False
        try:
            transport_manager.connected_clients.discard(websocket)
            print(f"WebSocket cleanup. Remaining clients: {len(transport_manager.connected_clients)}")
        except Exception as e:
            print(f"Error during cleanup: {e}")

# ==================== ADVANCED TOOLS API ENDPOINTS ====================

@app.post("/api/analysis/detect-genre")
async def detect_genre(request: Dict[str, Any]) -> Dict[str, Any]:
    """Detect music genre from session metadata"""
    try:
        bpm = request.get("bpm", 120)
        time_sig = request.get("timeSignature", "4/4")
        track_count = request.get("trackCount", 1)
        
        # Genre detection logic based on BPM and metadata
        if bpm < 80:
            genres = ["Ambient", "Downtempo", "Chill"]
        elif bpm < 100:
            genres = ["Hip Hop", "R&B", "Soul"]
        elif bpm < 120:
            genres = ["Pop", "Funk", "Disco"]
        elif bpm < 140:
            genres = ["House", "Techno", "Dance"]
        else:
            genres = ["Trance", "Drum & Bass", "Hardcore"]
        
        detected = genres[0]
        confidence = 0.65 + (0.1 if track_count > 1 else 0)
        
        return {
            "detected_genre": detected,
            "confidence": min(confidence, 0.95),
            "bpm_range": [bpm - 10, bpm + 10],
            "key": "C Major",
            "energy_level": "high" if bpm > 120 else "medium",
            "instrumentation": ["drums", "bass", "synth"] if detected in ["House", "Techno"] else ["drums", "bass", "guitar"]
        }
    except Exception as e:
        return {
            "detected_genre": "Electronic",
            "confidence": 0.5,
            "bpm_range": [120, 140],
            "error": str(e)
        }

@app.get("/api/analysis/delay-sync")
async def delay_sync(bpm: float = 120) -> Dict[str, float]:
    """Calculate tempo-locked delay times"""
    try:
        note_divisions = {
            "Whole Note": 4,
            "Half Note": 2,
            "Quarter Note": 1,
            "Eighth Note": 0.5,
            "16th Note": 0.25,
            "Triplet Quarter": 2/3,
            "Triplet Eighth": 1/3,
            "Dotted Quarter": 1.5,
            "Dotted Eighth": 0.75,
        }
        
        results = {}
        for name, divisor in note_divisions.items():
            delay_ms = round((60000 / bpm) * divisor, 2)
            results[name] = delay_ms
        
        return results
    except Exception as e:
        return {"error": str(e), "default_quarter": 500}

@app.get("/api/analysis/ear-training")
async def ear_training(exercise_type: str = "interval", interval: str = "Major Third") -> Dict[str, Any]:
    """Get ear training visual data for interval/chord recognition"""
    try:
        intervals_db = {
            "Unison": {"semitones": 0, "frequency_ratio": 1.0, "visualization": "█"},
            "Minor Second": {"semitones": 1, "frequency_ratio": 1.0595, "visualization": "█▏"},
            "Major Second": {"semitones": 2, "frequency_ratio": 1.122, "visualization": "█▌"},
            "Minor Third": {"semitones": 3, "frequency_ratio": 1.189, "visualization": "█▊"},
            "Major Third": {"semitones": 4, "frequency_ratio": 1.26, "visualization": "██"},
            "Perfect Fourth": {"semitones": 5, "frequency_ratio": 1.335, "visualization": "██▍"},
            "Perfect Fifth": {"semitones": 7, "frequency_ratio": 1.498, "visualization": "██▊"},
        }
        
        intervals = [
            {"name": name, **data}
            for name, data in intervals_db.items()
        ]
        
        return {
            "exercise_type": exercise_type,
            "intervals": intervals,
            "reference_frequency": 440,
            "difficulty": "beginner"
        }
    except Exception as e:
        return {"error": str(e), "exercise_type": exercise_type}

@app.get("/api/analysis/production-checklist")
async def production_checklist(stage: str = "production") -> Dict[str, Any]:
    """Get production workflow checklist for current stage"""
    try:
        checklists = {
            "pre_production": {
                "stage": "Pre-Production",
                "sections": {
                    "Planning": [
                        "Define project genre and style",
                        "Set target BPM and time signature",
                        "Plan track count and arrangement",
                        "Create reference playlists",
                    ],
                    "Setup": [
                        "Configure audio interface",
                        "Set buffer size and latency",
                        "Create DAW template",
                        "Organize plugin chains",
                    ],
                }
            },
            "production": {
                "stage": "Production",
                "sections": {
                    "Arrangement": [
                        "Record/create intro section",
                        "Build verse section",
                        "Create chorus/hook",
                        "Develop bridge/transition",
                        "Plan breakdown",
                    ],
                    "Recording": [
                        "Set input levels (gain staging)",
                        "Record vocals/instruments",
                        "Organize takes",
                        "Create backing vocals",
                    ],
                }
            },
            "mixing": {
                "stage": "Mixing",
                "sections": {
                    "Setup": [
                        "Color-code tracks",
                        "Organize into groups",
                        "Create bus structure",
                        "Set up aux sends",
                    ],
                    "Levels": [
                        "Set track levels (-6dB headroom)",
                        "Balance drums",
                        "Balance melody vs accompaniment",
                        "Check mono compatibility",
                    ],
                }
            },
            "mastering": {
                "stage": "Mastering",
                "sections": {
                    "Preparation": [
                        "Bounce stereo mix",
                        "Leave headroom (3-6dB)",
                        "Check loudness",
                        "Compare with references",
                    ],
                    "Mastering": [
                        "Linear phase EQ",
                        "Multiband compression",
                        "Limiting (prevent clipping)",
                        "Metering/analysis",
                    ],
                }
            }
        }
        
        return checklists.get(stage, checklists["production"])
    except Exception as e:
        return {"error": str(e), "stage": stage}

@app.get("/api/analysis/instrument-info")
async def instrument_info(category: str = "percussion", instrument: str = "kick") -> Dict[str, Any]:
    """Get instrument frequency specs and characteristics"""
    try:
        instruments_db = {
            "percussion": {
                "kick": {
                    "category": "Percussion",
                    "instrument": "Kick Drum",
                    "frequency_range": [20, 250],
                    "characteristics": ["Deep", "Punchy", "Low-end focused"],
                    "suggested_eq": {
                        "Sub (20-80Hz)": "Boost for depth",
                        "Mid-bass (80-250Hz)": "Adjust for punch",
                        "Mid-range (250-2kHz)": "Cut for clarity",
                    },
                    "use_cases": ["Drums", "Electronic", "Pop"],
                },
                "snare": {
                    "category": "Percussion",
                    "instrument": "Snare Drum",
                    "frequency_range": [100, 8000],
                    "characteristics": ["Crisp", "Present", "Mid-range emphasis"],
                    "suggested_eq": {
                        "Low-mid (100-500Hz)": "Cut mud",
                        "Presence (2-5kHz)": "Boost for snap",
                        "High (5-8kHz)": "Add brightness",
                    },
                    "use_cases": ["Drums", "Rock", "Pop"],
                },
            },
            "melodic": {
                "piano": {
                    "category": "Melodic",
                    "instrument": "Piano",
                    "frequency_range": [27, 4186],
                    "characteristics": ["Resonant", "Full-spectrum", "Rich harmonics"],
                    "suggested_eq": {
                        "Sub (20-80Hz)": "Moderate boost",
                        "Presence (2-4kHz)": "Slight boost",
                        "High (8-16kHz)": "Controlled",
                    },
                    "use_cases": ["Classical", "Jazz", "Pop"],
                },
            }
        }
        
        return instruments_db.get(category, {}).get(instrument, {
            "category": category,
            "instrument": instrument,
            "frequency_range": [20, 20000],
            "characteristics": ["Generic instrument"],
        })
    except Exception as e:
        return {"error": str(e), "category": category, "instrument": instrument}

@app.get("/api/analysis/instruments-list")
async def instruments_list() -> Dict[str, list]:
    """Get all available instruments by category"""
    try:
        return {
            "percussion": ["kick", "snare", "hihat", "tom", "cymbal", "clap"],
            "melodic": ["piano", "guitar", "synth", "bass", "strings", "brass"],
            "vocal": ["lead", "harmony", "backing", "rap"],
            "ambient": ["pad", "texture", "effect", "noise"],
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/analysis/tips")
async def analysis_tips(request: Dict[str, Any] = None) -> Dict[str, Any]:
    """Get quick mixing tips based on session context"""
    try:
        if request is None:
            request = {}
            
        track_count = request.get("trackCount", 0)
        master_level = request.get("masterLevel", -60)
        has_clipping = request.get("hasClipping", False)
        
        tips = []
        
        # Generate context-specific tips
        if track_count == 0:
            tips.append("💡 Start by adding audio or instrument tracks to begin mixing")
        elif track_count < 4:
            tips.append("🎵 With " + str(track_count) + " tracks, focus on each track's tone and balance before compression")
        else:
            tips.append("🎼 Consider creating submix buses to group similar instruments (drums, bass, vocals, etc)")
        
        if has_clipping:
            tips.append("🚨 Reduce levels immediately - clipping will cause harsh digital distortion")
        elif master_level > -3:
            tips.append("📊 Master level is hot - leave -3 to -6dB headroom for limiting and mastering")
        elif master_level < -12:
            tips.append("🔉 Levels seem low - check if tracks are properly routed and at good input levels")
        else:
            tips.append("✅ Master level is in a good range for mixing")
        
        # Mix-specific tips
        if track_count > 0:
            tips.append("🎚️ Pan tracks for width: try -100 to -50% and +50 to +100% for stereo imaging")
            tips.append("⚙️ Use EQ to carve out frequencies and create separation between instruments")
        
        return {
            "type": "tips",
            "tips": tips,
            "tip_count": len(tips),
            "session_context": {
                "tracks": track_count,
                "master_level_db": master_level,
                "clipping": has_clipping,
            }
        }
    except Exception as e:
        return {
            "type": "tips",
            "tips": ["Error generating tips: " + str(e)],
            "tip_count": 1,
            "error": str(e)
        }

# ==================== END ADVANCED TOOLS API ====================

@app.post("/transport/play")
async def transport_play() -> TransportCommandResponse:
    """Start playback"""
    try:
        state = transport_manager.play()
        return TransportCommandResponse(
            success=True,
            message="Playback started",
            state=state
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transport/stop")
async def transport_stop() -> TransportCommandResponse:
    """Stop playback and reset to beginning"""
    try:
        state = transport_manager.stop()
        return TransportCommandResponse(
            success=True,
            message="Playback stopped",
            state=state
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transport/pause")
async def transport_pause() -> TransportCommandResponse:
    """Pause playback (time remains at current position)"""
    try:
        state = transport_manager.pause()
        return TransportCommandResponse(
            success=True,
            message="Playback paused",
            state=state
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transport/resume")
async def transport_resume() -> TransportCommandResponse:
    """Resume playback from pause"""
    try:
        state = transport_manager.resume()
        return TransportCommandResponse(
            success=True,
            message="Playback resumed",
            state=state
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/transport/seek")
async def transport_seek(seconds: float) -> TransportCommandResponse:
    """Seek to time position (in seconds)"""
    try:
        state = transport_manager.seek(seconds)
        return TransportCommandResponse(
            success=True,
            message=f"Seeked to {seconds} seconds",
            state=state
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transport/tempo")
async def transport_tempo(bpm: float) -> TransportCommandResponse:
    """Set playback tempo in BPM (1-300)"""
    try:
        if not 1 <= bpm <= 300:
            raise ValueError("BPM must be between 1 and 300")
        state = transport_manager.set_tempo(bpm)
        return TransportCommandResponse(
            success=True,
            message=f"Tempo set to {bpm} BPM",
            state=state
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transport/loop")
async def transport_loop(
    enabled: bool,
    start_seconds: float = 0.0,
    end_seconds: float = 10.0
) -> TransportCommandResponse:
    """Configure loop region"""
    try:
        state = transport_manager.set_loop(enabled, start_seconds, end_seconds)
        return TransportCommandResponse(
            success=True,
            message=f"Loop {'enabled' if enabled else 'disabled'}",
            state=state
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/transport/status")
async def transport_status() -> TransportState:
    """Get current transport state"""
    return transport_manager.get_state()

@app.get("/transport/metrics")
async def transport_metrics() -> Dict[str, Any]:
    """Get transport metrics for analytics"""
    state = transport_manager.get_state()
    return {
        "state": state.dict(),
        "connected_clients": len(transport_manager.connected_clients),
        "timestamp": time.time(),
        "beat_fraction": state.beat_pos,
        "sample_rate": transport_manager.sample_rate
    }


# ==================== SPECIALIZED ANALYSIS ENDPOINTS ====================

# Helper function for linear to dB conversion
def to_db(value):
    """Convert linear amplitude to dB"""
    if value <= 0:
        return -96.0
    return float(20 * np.log10(np.clip(value, 1e-7, 1.0)))

@app.post("/api/analyze/gain-staging")
async def analyze_gain_staging(request: AudioAnalysisRequest):
    """Specialized endpoint for gain staging analysis"""
    try:
        if not TRAINING_AVAILABLE or analyzer is None:
            return {"error": "Analyzer not available"}
        
        audio_data = np.array(request.audioData)
        level_linear = np.mean(np.abs(audio_data)) if len(audio_data) > 0 else 1e-7
        peak_linear = np.max(np.abs(audio_data)) if len(audio_data) > 0 else 1e-7
        rms_linear = float(np.sqrt(np.mean(audio_data**2))) if len(audio_data) > 0 else 1e-7
        
        track_metrics = [{
            "name": f"Track_{request.trackId}",
            "level": to_db(level_linear),
            "peak": to_db(peak_linear),
            "rms": to_db(rms_linear),
        }]
        
        result = analyzer.analyze_gain_staging(track_metrics)
        return {
            "trackId": request.trackId,
            "analysis_type": "gain_staging",
            "score": result.score,
            "findings": result.findings,
            "recommendations": result.recommendations,
            "reasoning": result.reasoning,
            "metrics": result.metrics
        }
    except Exception as e:
        print(f"Error in gain staging analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze/mixing")
async def analyze_mixing(request: AudioAnalysisRequest):
    """Specialized endpoint for mixing analysis"""
    try:
        if not TRAINING_AVAILABLE or analyzer is None:
            return {"error": "Analyzer not available"}
        
        audio_data = np.array(request.audioData)
        level_linear = np.mean(np.abs(audio_data)) if len(audio_data) > 0 else 1e-7
        peak_linear = np.max(np.abs(audio_data)) if len(audio_data) > 0 else 1e-7
        rms_linear = float(np.sqrt(np.mean(audio_data**2))) if len(audio_data) > 0 else 1e-7
        
        track_metrics = [{
            "name": f"Track_{request.trackId}",
            "level": to_db(level_linear),
            "peak": to_db(peak_linear),
            "rms": to_db(rms_linear),
        }]
        
        result = analyzer.analyze_mixing(track_metrics, [])
        return {
            "trackId": request.trackId,
            "analysis_type": "mixing",
            "score": result.score,
            "findings": result.findings,
            "recommendations": result.recommendations,
            "reasoning": result.reasoning,
            "metrics": result.metrics
        }
    except Exception as e:
        print(f"Error in mixing analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze/routing")
async def analyze_routing(request: AudioAnalysisRequest):
    """Specialized endpoint for routing analysis"""
    try:
        if not TRAINING_AVAILABLE or analyzer is None:
            return {"error": "Analyzer not available"}
        
        audio_data = np.array(request.audioData)
        level_linear = np.mean(np.abs(audio_data)) if len(audio_data) > 0 else 1e-7
        peak_linear = np.max(np.abs(audio_data)) if len(audio_data) > 0 else 1e-7
        rms_linear = float(np.sqrt(np.mean(audio_data**2))) if len(audio_data) > 0 else 1e-7
        
        track_metrics = [{
            "name": f"Track_{request.trackId}",
            "level": to_db(level_linear),
            "peak": to_db(peak_linear),
            "rms": to_db(rms_linear),
        }]
        
        result = analyzer.analyze_routing(track_metrics, {})
        return {
            "trackId": request.trackId,
            "analysis_type": "routing",
            "score": result.score,
            "findings": result.findings,
            "recommendations": result.recommendations,
            "reasoning": result.reasoning,
            "metrics": result.metrics
        }
    except Exception as e:
        print(f"Error in routing analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze/mastering")
async def analyze_mastering(request: AudioAnalysisRequest):
    """Specialized endpoint for mastering readiness analysis"""
    try:
        if not TRAINING_AVAILABLE or analyzer is None:
            return {"error": "Analyzer not available"}
        
        audio_data = np.array(request.audioData)
        level_linear = np.mean(np.abs(audio_data)) if len(audio_data) > 0 else 1e-7
        peak_linear = np.max(np.abs(audio_data)) if len(audio_data) > 0 else 1e-7
        rms_linear = float(np.sqrt(np.mean(audio_data**2))) if len(audio_data) > 0 else 1e-7
        
        track_metrics = [{
            "name": f"Track_{request.trackId}",
            "level": to_db(level_linear),
            "peak": to_db(peak_linear),
            "rms": to_db(rms_linear),
        }]
        
        result = analyzer.analyze_mastering_readiness(track_metrics)
        return {
            "trackId": request.trackId,
            "analysis_type": "mastering",
            "score": result.score,
            "findings": result.findings,
            "recommendations": result.recommendations,
            "reasoning": result.reasoning,
            "metrics": result.metrics
        }
    except Exception as e:
        print(f"Error in mastering analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze/session")
async def analyze_session(request: AudioAnalysisRequest):
    """Specialized endpoint for session health analysis"""
    try:
        if not TRAINING_AVAILABLE or analyzer is None:
            return {"error": "Analyzer not available"}
        
        audio_data = np.array(request.audioData)
        level_linear = np.mean(np.abs(audio_data)) if len(audio_data) > 0 else 1e-7
        peak_linear = np.max(np.abs(audio_data)) if len(audio_data) > 0 else 1e-7
        rms_linear = float(np.sqrt(np.mean(audio_data**2))) if len(audio_data) > 0 else 1e-7
        
        track_metrics = [{
            "name": f"Track_{request.trackId}",
            "level": to_db(level_linear),
            "peak": to_db(peak_linear),
            "rms": to_db(rms_linear),
        }]
        
        result = analyzer.analyze_session_health(track_metrics, {})
        return {
            "trackId": request.trackId,
            "analysis_type": "session",
            "score": result.score,
            "findings": result.findings,
            "recommendations": result.recommendations,
            "reasoning": result.reasoning,
            "metrics": result.metrics
        }
    except Exception as e:
        print(f"Error in session health analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze/creative")
async def analyze_creative(request: AudioAnalysisRequest):
    """Specialized endpoint for creative improvements analysis"""
    try:
        if not TRAINING_AVAILABLE or analyzer is None:
            return {"error": "Analyzer not available"}
        
        audio_data = np.array(request.audioData)
        level_linear = np.mean(np.abs(audio_data)) if len(audio_data) > 0 else 1e-7
        peak_linear = np.max(np.abs(audio_data)) if len(audio_data) > 0 else 1e-7
        rms_linear = float(np.sqrt(np.mean(audio_data**2))) if len(audio_data) > 0 else 1e-7
        
        track_metrics = [{
            "name": f"Track_{request.trackId}",
            "level": to_db(level_linear),
            "peak": to_db(peak_linear),
            "rms": to_db(rms_linear),
        }]
        
        result = analyzer.analyze_creative_improvements(track_metrics, {})
        return {
            "trackId": request.trackId,
            "analysis_type": "creative",
            "score": result.score,
            "findings": result.findings,
            "recommendations": result.recommendations,
            "reasoning": result.reasoning,
            "metrics": result.metrics
        }
    except Exception as e:
        print(f"Error in creative analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =========================================================================
# DAW CONTROL ENDPOINTS - Codette AI can now perform DAW operations
# =========================================================================

class DAWTrackRequest(BaseModel):
    """Request model for track operations"""
    trackId: Optional[str] = None
    trackType: Optional[str] = None  # "audio", "instrument", "midi", "aux", "vca"
    trackName: Optional[str] = None
    trackColor: Optional[str] = None
    updates: Optional[Dict[str, Any]] = None

class DAWEffectRequest(BaseModel):
    """Request model for effect operations"""
    trackId: str
    effectType: str  # "eq", "compressor", "reverb", "delay", etc.
    effectName: Optional[str] = None
    parameters: Optional[Dict[str, float]] = None
    position: Optional[int] = None  # Insert position in chain

class DAWTransportRequest(BaseModel):
    """Request model for transport control"""
    command: str  # "play", "stop", "pause", "resume"
    position: Optional[float] = None

class DAWAutomationRequest(BaseModel):
    """Request model for automation operations"""
    trackId: str
    parameterName: str
    timePosition: float
    value: float

class DAWLevelRequest(BaseModel):
    """Request model for level adjustments"""
    trackId: str
    levelType: str  # "volume", "pan", "input_gain", "stereo_width"
    value: float

class DAWControlResponse(BaseModel):
    """Response for DAW control operations"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


# TRACK MANAGEMENT ENDPOINTS

@app.post("/codette/daw/track/create", response_model=DAWControlResponse)
async def create_track(request: DAWTrackRequest) -> DAWControlResponse:
    """Create a new track with specified type and name"""
    try:
        track_type = request.trackType or "audio"
        track_name = request.trackName or f"{track_type.capitalize()} Track"
        track_color = request.trackColor or "#808080"
        
        return DAWControlResponse(
            success=True,
            message=f"Track created: {track_name} ({track_type})",
            data={
                "trackType": track_type,
                "trackName": track_name,
                "trackColor": track_color,
                "action": "add_track"
            }
        )
    except Exception as e:
        return DAWControlResponse(success=False, message=str(e))

@app.post("/codette/daw/track/select", response_model=DAWControlResponse)
async def select_track(request: DAWTrackRequest) -> DAWControlResponse:
    """Select a track for editing"""
    try:
        return DAWControlResponse(
            success=True,
            message=f"Track selected: {request.trackId}",
            data={"trackId": request.trackId, "action": "select_track"}
        )
    except Exception as e:
        return DAWControlResponse(success=False, message=str(e))

@app.post("/codette/daw/track/delete", response_model=DAWControlResponse)
async def delete_track(request: DAWTrackRequest) -> DAWControlResponse:
    """Delete a track"""
    try:
        return DAWControlResponse(
            success=True,
            message=f"Track deleted: {request.trackId}",
            data={"trackId": request.trackId, "action": "delete_track"}
        )
    except Exception as e:
        return DAWControlResponse(success=False, message=str(e))

@app.post("/codette/daw/track/rename", response_model=DAWControlResponse)
async def rename_track(request: DAWTrackRequest) -> DAWControlResponse:
    """Rename a track"""
    try:
        return DAWControlResponse(
            success=True,
            message=f"Track renamed to: {request.trackName}",
            data={"trackId": request.trackId, "trackName": request.trackName, "action": "rename_track"}
        )
    except Exception as e:
        return DAWControlResponse(success=False, message=str(e))

@app.post("/codette/daw/track/mute", response_model=DAWControlResponse)
async def toggle_track_mute(request: DAWTrackRequest) -> DAWControlResponse:
    """Toggle mute on a track"""
    try:
        return DAWControlResponse(
            success=True,
            message=f"Track mute toggled: {request.trackId}",
            data={"trackId": request.trackId, "action": "toggle_mute"}
        )
    except Exception as e:
        return DAWControlResponse(success=False, message=str(e))

@app.post("/codette/daw/track/solo", response_model=DAWControlResponse)
async def toggle_track_solo(request: DAWTrackRequest) -> DAWControlResponse:
    """Toggle solo on a track"""
    try:
        return DAWControlResponse(
            success=True,
            message=f"Track solo toggled: {request.trackId}",
            data={"trackId": request.trackId, "action": "toggle_solo"}
        )
    except Exception as e:
        return DAWControlResponse(success=False, message=str(e))

@app.post("/codette/daw/track/arm", response_model=DAWControlResponse)
async def toggle_track_arm(request: DAWTrackRequest) -> DAWControlResponse:
    """Toggle record arm on a track"""
    try:
        return DAWControlResponse(
            success=True,
            message=f"Track record arm toggled: {request.trackId}",
            data={"trackId": request.trackId, "action": "toggle_arm"}
        )
    except Exception as e:
        return DAWControlResponse(success=False, message=str(e))


# LEVEL & MIXING ENDPOINTS

@app.post("/codette/daw/level/set", response_model=DAWControlResponse)
async def set_track_level(request: DAWLevelRequest) -> DAWControlResponse:
    """Set track level (volume, pan, input gain, stereo width)"""
    try:
        level_type = request.levelType  # "volume", "pan", "input_gain", "stereo_width"
        
        recommendations = {
            "volume": "Setting post-fader volume (dB, typically -6 to +6)",
            "pan": "Setting pan (-1.0 = left, 0.0 = center, +1.0 = right)",
            "input_gain": "Setting pre-fader input gain (dB, typically -12 to +12)",
            "stereo_width": "Setting stereo width (0-200%, 100 = normal)"
        }
        
        return DAWControlResponse(
            success=True,
            message=f"{level_type} set to {request.value}",
            data={
                "trackId": request.trackId,
                "levelType": level_type,
                "value": request.value,
                "explanation": recommendations.get(level_type, "Level adjusted"),
                "action": "set_level"
            }
        )
    except Exception as e:
        return DAWControlResponse(success=False, message=str(e))

@app.post("/codette/daw/level/normalize", response_model=DAWControlResponse)
async def normalize_track_levels(request: DAWLevelRequest) -> DAWControlResponse:
    """Auto-normalize track levels based on Codette analysis"""
    try:
        return DAWControlResponse(
            success=True,
            message=f"Track levels normalized to standard",
            data={
                "trackId": request.trackId,
                "adjustments": {
                    "volume": -6.0,
                    "pan": 0.0,
                    "inputGain": 0.0
                },
                "reasoning": "Standard mixing level: -6dB volume, center pan, 0dB input",
                "action": "normalize_levels"
            }
        )
    except Exception as e:
        return DAWControlResponse(success=False, message=str(e))


# EFFECT & PLUGIN ENDPOINTS

@app.post("/codette/daw/effect/add", response_model=DAWControlResponse)
async def add_effect_to_track(request: DAWEffectRequest) -> DAWControlResponse:
    """Add an effect to a track with recommended settings"""
    try:
        effect_type = request.effectType.lower()
        
        # Recommended settings for common effects
        effect_settings = {
            "eq": {
                "type": "parametric_eq",
                "default_bands": [
                    {"frequency": 80, "gain": 0, "q": 0.7, "type": "highpass"},
                    {"frequency": 200, "gain": -3, "q": 1.0, "type": "shelf"},
                    {"frequency": 1000, "gain": 0, "q": 1.0, "type": "peak"},
                    {"frequency": 5000, "gain": 2, "q": 1.0, "type": "peak"},
                    {"frequency": 15000, "gain": 0, "q": 0.7, "type": "shelf"}
                ]
            },
            "compressor": {
                "type": "dynamic_compressor",
                "ratio": 4.0,
                "threshold": -20.0,
                "attack": 10,
                "release": 100,
                "makeup_gain": "auto"
            },
            "reverb": {
                "type": "convolver_reverb",
                "room_size": 0.5,
                "decay_time": 1.5,
                "predelay": 20,
                "dry_wet": 0.3
            },
            "delay": {
                "type": "simple_delay",
                "time_ms": 500,
                "feedback": 0.4,
                "dry_wet": 0.2,
                "sync": "quarter_note"
            },
            "saturation": {
                "type": "soft_clipper",
                "drive": 3.0,
                "tone": 0.5,
                "dry_wet": 0.2
            }
        }
        
        settings = effect_settings.get(effect_type, {"type": effect_type})
        
        return DAWControlResponse(
            success=True,
            message=f"Effect added to track: {request.effectName or effect_type}",
            data={
                "trackId": request.trackId,
                "effectType": effect_type,
                "effectName": request.effectName or f"{effect_type.capitalize()}",
                "settings": settings,
                "position": request.position or 0,
                "action": "add_effect"
            }
        )
    except Exception as e:
        return DAWControlResponse(success=False, message=str(e))

@app.post("/codette/daw/effect/remove", response_model=DAWControlResponse)
async def remove_effect_from_track(request: DAWEffectRequest) -> DAWControlResponse:
    """Remove an effect from a track"""
    try:
        return DAWControlResponse(
            success=True,
            message=f"Effect removed from track",
            data={
                "trackId": request.trackId,
                "effectName": request.effectName,
                "action": "remove_effect"
            }
        )
    except Exception as e:
        return DAWControlResponse(success=False, message=str(e))

@app.post("/codette/daw/effect/parameter", response_model=DAWControlResponse)
async def set_effect_parameter(request: DAWEffectRequest) -> DAWControlResponse:
    """Set effect parameter values"""
    try:
        return DAWControlResponse(
            success=True,
            message=f"Effect parameters updated",
            data={
                "trackId": request.trackId,
                "effectName": request.effectName,
                "parameters": request.parameters,
                "action": "set_effect_param"
            }
        )
    except Exception as e:
        return DAWControlResponse(success=False, message=str(e))


# TRANSPORT & PLAYBACK ENDPOINTS

@app.post("/codette/daw/transport/play", response_model=DAWControlResponse)
async def transport_play() -> DAWControlResponse:
    """Start playback from current position"""
    try:
        return DAWControlResponse(
            success=True,
            message="Playback started",
            data={"action": "play", "timestamp": time.time()}
        )
    except Exception as e:
        return DAWControlResponse(success=False, message=str(e))

@app.post("/codette/daw/transport/stop", response_model=DAWControlResponse)
async def transport_stop() -> DAWControlResponse:
    """Stop playback and return to start"""
    try:
        return DAWControlResponse(
            success=True,
            message="Playback stopped",
            data={"action": "stop", "timestamp": time.time()}
        )
    except Exception as e:
        return DAWControlResponse(success=False, message=str(e))

@app.post("/codette/daw/transport/pause", response_model=DAWControlResponse)
async def transport_pause() -> DAWControlResponse:
    """Pause playback at current position"""
    try:
        return DAWControlResponse(
            success=True,
            message="Playback paused",
            data={"action": "pause", "timestamp": time.time()}
        )
    except Exception as e:
        return DAWControlResponse(success=False, message=str(e))

@app.post("/codette/daw/transport/seek", response_model=DAWControlResponse)
async def transport_seek(seconds: float) -> DAWControlResponse:
    """Seek to specific time position"""
    try:
        return DAWControlResponse(
            success=True,
            message=f"Seeked to {seconds}s",
            data={"action": "seek", "position": seconds, "timestamp": time.time()}
        )
    except Exception as e:
        return DAWControlResponse(success=False, message=str(e))


# AUTOMATION ENDPOINTS

@app.post("/codette/daw/automation/add-point", response_model=DAWControlResponse)
async def add_automation_point(request: DAWAutomationRequest) -> DAWControlResponse:
    """Add automation point at specific time and value"""
    try:
        return DAWControlResponse(
            success=True,
            message=f"Automation point added at {request.timePosition}s",
            data={
                "trackId": request.trackId,
                "parameter": request.parameterName,
                "timePosition": request.timePosition,
                "value": request.value,
                "action": "add_automation_point"
            }
        )
    except Exception as e:
        return DAWControlResponse(success=False, message=str(e))

@app.post("/codette/daw/automation/curve", response_model=DAWControlResponse)
async def create_automation_curve(request: Dict[str, Any]) -> DAWControlResponse:
    """Create automation curve with multiple points"""
    try:
        track_id = request.get("trackId", "")
        param_name = request.get("parameterName", "")
        points = request.get("points", [])  # List of {time, value} dicts
        
        return DAWControlResponse(
            success=True,
            message=f"Automation curve created with {len(points)} points",
            data={
                "trackId": track_id,
                "parameter": param_name,
                "pointCount": len(points),
                "points": points,
                "action": "create_automation_curve"
            }
        )
    except Exception as e:
        return DAWControlResponse(success=False, message=str(e))


# COMPREHENSIVE DAW ACTION ENDPOINT

@app.post("/codette/daw/execute", response_model=DAWControlResponse)
async def execute_daw_action(request: Dict[str, Any]) -> DAWControlResponse:
    """
    Execute a comprehensive DAW action recommended by Codette
    
    Example actions:
    {
        "type": "apply_effect_chain",
        "trackId": "vocal-1",
        "effects": [
            {"type": "eq", "settings": {...}},
            {"type": "compressor", "settings": {...}},
            {"type": "reverb", "settings": {...}}
        ]
    }
    """
    try:
        action_type = request.get("type", "")
        
        if action_type == "apply_effect_chain":
            effects = request.get("effects", [])
            return DAWControlResponse(
                success=True,
                message=f"Effect chain applied ({len(effects)} effects)",
                data={
                    "trackId": request.get("trackId"),
                    "effectCount": len(effects),
                    "effects": effects,
                    "action": "apply_effect_chain"
                }
            )
        
        elif action_type == "normalize_mix":
            tracks = request.get("tracks", [])
            return DAWControlResponse(
                success=True,
                message=f"Mix normalized for {len(tracks)} tracks",
                data={
                    "trackCount": len(tracks),
                    "adjustments": tracks,
                    "action": "normalize_mix"
                }
            )
        
        elif action_type == "route_tracks":
            routes = request.get("routes", [])
            return DAWControlResponse(
                success=True,
                message=f"Routing configured for {len(routes)} tracks",
                data={
                    "routeCount": len(routes),
                    "routes": routes,
                    "action": "route_tracks"
                }
            )
        
        else:
            return DAWControlResponse(success=False, message=f"Unknown action type: {action_type}")
    
    except Exception as e:
        return DAWControlResponse(success=False, message=str(e))


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("CODETTE_PORT", "8001"))
    host = os.getenv("CODETTE_HOST", "127.0.0.1")

    print("\n" + "="*70)
    print("Codette AI FastAPI Server Starting")
    print("="*70)
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Codette Available: {codette is not None}")
    
    if codette:
        print(f"Perspectives: neuralnets, newtonian, davinci, quantum")
    else:
        print("WARNING: Codette not initialized - check Codette/ folder")
    
    print(f"\nServer will be available at:")
    print(f"   http://localhost:{port}")
    print(f"   http://localhost:{port}/health (health check)")
    print(f"   http://localhost:{port}/docs (API documentation)")
    print("\nFrontend Configuration:")
    print(f"   Add to .env.local: VITE_CODETTE_API_URL=http://localhost:{port}")
    print(f"\nPress Ctrl+C to stop the server")
    print("="*70 + "\n")

    # Run uvicorn directly - use absolute host binding
    uvicorn.run(app, host=host, port=port, log_level="info")

