"""
Tracing integration for AICore component
Instruments the main AI orchestration system with OpenTelemetry
"""
import logging
from typing import Dict, Any, Optional, List
from functools import wraps

logger = logging.getLogger(__name__)

# Import tracing utilities
try:
    from src.utils.tracing_config import get_tracer
    from opentelemetry import trace
    from opentelemetry.trace import Status, StatusCode
    TRACING_AVAILABLE = True
except ImportError:
    TRACING_AVAILABLE = False
    logger.debug("OpenTelemetry not available for AICore tracing")


def trace_ai_operation(operation_name: str):
    """
    Decorator to trace AI operations in AICore
    
    Args:
        operation_name: Name of the operation being traced
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            if not TRACING_AVAILABLE:
                return await func(*args, **kwargs)
            
            tracer = get_tracer()
            with tracer.start_as_current_span(
                f"ai_core.{operation_name}",
                attributes={"component": "ai_core", "operation": operation_name}
            ) as span:
                try:
                    result = await func(*args, **kwargs)
                    span.set_status(Status(StatusCode.OK))
                    return result
                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    span.record_exception(e)
                    raise
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            if not TRACING_AVAILABLE:
                return func(*args, **kwargs)
            
            tracer = get_tracer()
            with tracer.start_as_current_span(
                f"ai_core.{operation_name}",
                attributes={"component": "ai_core", "operation": operation_name}
            ) as span:
                try:
                    result = func(*args, **kwargs)
                    span.set_status(Status(StatusCode.OK))
                    return result
                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    span.record_exception(e)
                    raise
        
        # Return appropriate wrapper based on function type
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


def trace_perspective_selection(prompt: str, perspectives: List[str]):
    """
    Trace perspective selection process
    
    Args:
        prompt: User input prompt
        perspectives: Selected perspectives
    """
    if not TRACING_AVAILABLE:
        return
    
    tracer = get_tracer()
    with tracer.start_as_current_span(
        "ai_core.perspective_selection",
        attributes={
            "component": "perspective_engine",
            "prompt.length": len(prompt),
            "perspectives.count": len(perspectives),
            "perspectives.list": ", ".join(perspectives)
        }
    ):
        pass


def trace_perspective_generation(perspective_name: str, prompt: str, response: str, temperature: float):
    """
    Trace individual perspective generation
    
    Args:
        perspective_name: Name of the perspective
        prompt: Input prompt
        response: Generated response
        temperature: Temperature used for generation
    """
    if not TRACING_AVAILABLE:
        return
    
    tracer = get_tracer()
    with tracer.start_as_current_span(
        f"perspective.{perspective_name}",
        attributes={
            "component": "perspective_engine",
            "perspective.name": perspective_name,
            "perspective.temperature": temperature,
            "prompt.length": len(prompt),
            "response.length": len(response),
        }
    ) as span:
        span.set_status(Status(StatusCode.OK))


def trace_quantum_propagation(dimensions: int, coherence: float, entanglement: float):
    """
    Trace quantum spiderweb thought propagation
    
    Args:
        dimensions: Number of quantum dimensions
        coherence: Coherence metric
        entanglement: Entanglement metric
    """
    if not TRACING_AVAILABLE:
        return
    
    tracer = get_tracer()
    with tracer.start_as_current_span(
        "quantum.spiderweb_propagation",
        attributes={
            "component": "quantum_spiderweb",
            "quantum.dimensions": dimensions,
            "quantum.coherence": coherence,
            "quantum.entanglement": entanglement,
        }
    ):
        pass


def trace_memory_operation(operation: str, memory_size: int):
    """
    Trace memory operations (cocoon wrapping/unwrapping)
    
    Args:
        operation: Type of memory operation (wrap, unwrap, etc.)
        memory_size: Size of memory in bytes
    """
    if not TRACING_AVAILABLE:
        return
    
    tracer = get_tracer()
    with tracer.start_as_current_span(
        f"memory.{operation}",
        attributes={
            "component": "cocoon_manager",
            "memory.operation": operation,
            "memory.size_bytes": memory_size,
        }
    ):
        pass


def trace_aegis_enhancement(input_text: str, enhanced: bool):
    """
    Trace AEGIS safety council enhancement
    
    Args:
        input_text: Input text
        enhanced: Whether enhancement was applied
    """
    if not TRACING_AVAILABLE:
        return
    
    tracer = get_tracer()
    with tracer.start_as_current_span(
        "aegis.safety_enhancement",
        attributes={
            "component": "aegis_bridge",
            "input.length": len(input_text),
            "enhancement.applied": enhanced,
        }
    ):
        pass
