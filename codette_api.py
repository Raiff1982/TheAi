"""
FastAPI endpoint for Codette AI
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import logging
from typing import Optional, Dict, Any
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import Codette
try:
    from codette_new import Codette
except ImportError:
    logger.warning("Could not import from codette_new, attempting fallback...")
    try:
        from Codette.codette_new import Codette
    except ImportError:
        logger.error("Failed to import Codette. Please ensure codette_new.py is in path.")
        sys.exit(1)

# Initialize FastAPI app
app = FastAPI(
    title="Codette AI API",
    description="FastAPI interface for Codette AI assistant",
    version="1.0.0"
)

# Initialize Codette instance
try:
    codette = Codette(user_name="API_User")
    logger.info("Codette AI initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Codette: {e}")
    codette = None


# Pydantic models for request/response
class PromptRequest(BaseModel):
    """Request model for prompt processing"""
    prompt: str = Field(..., min_length=1, description="The prompt to send to Codette")
    user_name: Optional[str] = Field(default="API_User", description="Optional user name for personalization")

    class Config:
        schema_extra = {
            "example": {
                "prompt": "What is the nature of consciousness?",
                "user_name": "Alice"
            }
        }


class CodetteResponse(BaseModel):
    """Response model for Codette outputs"""
    response: str = Field(..., description="Codette's response to the prompt")
    status: str = Field(default="success", description="Status of the request")
    error: Optional[str] = Field(default=None, description="Error message if any")

    class Config:
        schema_extra = {
            "example": {
                "response": "[Neural] The pattern emerges...",
                "status": "success"
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(default="healthy")
    message: str = Field(default="Codette API is running")
    version: str = Field(default="1.0.0")


# API endpoints
@app.get("/", tags=["Info"])
async def root():
    """Root endpoint - API information"""
    return {
        "name": "Codette AI API",
        "version": "1.0.0",
        "description": "FastAPI interface for Codette AI assistant",
        "endpoints": {
            "POST /codette/chat": "Send a message to Codette",
            "POST /codette/respond": "Get Codette's response (alias for /chat)",
            "GET /health": "Health check",
            "GET /docs": "API documentation (Swagger UI)",
            "GET /redoc": "ReDoc documentation"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    if codette is None:
        raise HTTPException(status_code=503, detail="Codette not initialized")
    
    return HealthResponse(
        status="healthy",
        message="Codette API is running",
        version="1.0.0"
    )


@app.post("/codette/chat", response_model=CodetteResponse, tags=["Chat"])
async def chat(request: PromptRequest) -> CodetteResponse:
    """
    Chat endpoint - send a message to Codette and get a response
    
    Args:
        request: PromptRequest containing prompt and optional user_name
        
    Returns:
        CodetteResponse with Codette's response
    """
    if codette is None:
        raise HTTPException(status_code=503, detail="Codette not initialized")
    
    if not request.prompt or not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    try:
        # Create a new Codette instance with user name for personalization
        user_codette = Codette(user_name=request.user_name)
        response = user_codette.respond(request.prompt)
        
        logger.info(f"Processed query from {request.user_name}")
        
        return CodetteResponse(
            response=response,
            status="success"
        )
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.post("/codette/respond", response_model=CodetteResponse, tags=["Chat"])
async def respond(request: PromptRequest) -> CodetteResponse:
    """
    Alias endpoint for chat - for compatibility
    
    Args:
        request: PromptRequest containing prompt and optional user_name
        
    Returns:
        CodetteResponse with Codette's response
    """
    return await chat(request)


@app.post("/codette/process", response_model=Dict[str, Any], tags=["Processing"])
async def process(request: PromptRequest) -> Dict[str, Any]:
    """
    Advanced processing endpoint with additional metadata
    
    Args:
        request: PromptRequest containing prompt and optional user_name
        
    Returns:
        Dictionary with response, metadata, and status
    """
    if codette is None:
        raise HTTPException(status_code=503, detail="Codette not initialized")
    
    try:
        user_codette = Codette(user_name=request.user_name)
        response = user_codette.respond(request.prompt)
        
        return {
            "status": "success",
            "response": response,
            "user": request.user_name,
            "prompt_length": len(request.prompt),
            "response_length": len(response)
        }
    except Exception as e:
        logger.error(f"Error in process endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status", tags=["Status"])
async def status():
    """Get current system status"""
    return {
        "codette_initialized": codette is not None,
        "api_status": "operational",
        "version": "1.0.0"
    }


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return {
        "status": "error",
        "message": exc.detail,
        "status_code": exc.status_code
    }


if __name__ == "__main__":
    import uvicorn
    
    # Run the server
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
