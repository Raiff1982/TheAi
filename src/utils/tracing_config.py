"""
OpenTelemetry Tracing Configuration for Codette AI System
Enables distributed tracing and visualization of agent workflows
"""
import logging
from typing import Optional
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.logging import LoggingInstrumentor

logger = logging.getLogger(__name__)

# Global tracer instance
_tracer: Optional[trace.Tracer] = None
_tracer_provider: Optional[TracerProvider] = None


def setup_tracing(
    service_name: str = "codette-ai-system",
    otlp_endpoint: str = "http://localhost:4318/v1/traces",
    environment: str = "development"
) -> trace.Tracer:
    """
    Initialize OpenTelemetry tracing for Codette AI system
    
    Args:
        service_name: Name of the service for tracing
        otlp_endpoint: OTLP endpoint URL (default: http://localhost:4318/v1/traces)
        environment: Environment name (development, production, etc.)
    
    Returns:
        Configured tracer instance
    """
    global _tracer, _tracer_provider
    
    if _tracer is not None:
        logger.info("Tracing already initialized")
        return _tracer
    
    try:
        # Create resource with service information
        resource = Resource.create({
            "service.name": service_name,
            "service.version": "3.0",
            "deployment.environment": environment,
            "service.instance.id": "codette-main",
        })
        
        # Create tracer provider
        _tracer_provider = TracerProvider(resource=resource)
        
        # Create OTLP exporter for HTTP
        otlp_exporter = OTLPSpanExporter(
            endpoint=otlp_endpoint,
            timeout=30,
        )
        
        # Add batch span processor
        span_processor = BatchSpanProcessor(otlp_exporter)
        _tracer_provider.add_span_processor(span_processor)
        
        # Set the global tracer provider
        trace.set_tracer_provider(_tracer_provider)
        
        # Instrument logging to include trace context
        LoggingInstrumentor().instrument(set_logging_format=True)
        
        # Get tracer instance
        _tracer = trace.get_tracer(__name__)
        
        logger.info(f"✓ OpenTelemetry tracing initialized successfully")
        logger.info(f"  Service: {service_name}")
        logger.info(f"  OTLP Endpoint: {otlp_endpoint}")
        logger.info(f"  Environment: {environment}")
        
        return _tracer
        
    except Exception as e:
        logger.error(f"Failed to initialize tracing: {e}")
        logger.warning("Continuing without tracing enabled")
        # Return a no-op tracer
        return trace.get_tracer(__name__)


def get_tracer() -> trace.Tracer:
    """
    Get the configured tracer instance
    
    Returns:
        Tracer instance (initializes if not already done)
    """
    global _tracer
    
    if _tracer is None:
        logger.warning("Tracer not initialized, initializing with defaults")
        return setup_tracing()
    
    return _tracer


def shutdown_tracing():
    """
    Shutdown tracing and flush remaining spans
    """
    global _tracer_provider
    
    if _tracer_provider is not None:
        try:
            _tracer_provider.shutdown()
            logger.info("Tracing shutdown successfully")
        except Exception as e:
            logger.error(f"Error during tracing shutdown: {e}")


def trace_perspective_generation(perspective_name: str):
    """
    Decorator to trace perspective generation
    
    Args:
        perspective_name: Name of the perspective being traced
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            tracer = get_tracer()
            with tracer.start_as_current_span(
                f"perspective.{perspective_name}",
                attributes={
                    "perspective.name": perspective_name,
                    "component": "perspective_engine"
                }
            ) as span:
                try:
                    result = func(*args, **kwargs)
                    span.set_attribute("perspective.success", True)
                    if isinstance(result, str):
                        span.set_attribute("response.length", len(result))
                    return result
                except Exception as e:
                    span.set_attribute("perspective.success", False)
                    span.set_attribute("error.type", type(e).__name__)
                    span.set_attribute("error.message", str(e))
                    span.record_exception(e)
                    raise
        return wrapper
    return decorator
