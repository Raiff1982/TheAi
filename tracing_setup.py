#!/usr/bin/env python3
"""
Tracing Setup Script for Codette AI System
Initializes OpenTelemetry tracing with visualization support
"""
import os
import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils.tracing_config import setup_tracing, get_tracer
from opentelemetry import trace

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def initialize_codette_tracing():
    """
    Initialize tracing for the Codette AI system
    Uses OTLP endpoint at http://localhost:4319 for visualization
    """
    logger.info("=" * 70)
    logger.info("CODETTE AI TRACING INITIALIZATION")
    logger.info("=" * 70)
    
    # Get configuration from environment or use defaults
    service_name = os.getenv("OTEL_SERVICE_NAME", "codette-ai-system")
    
    # User specified endpoint: http://localhost:4319
    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4319/v1/traces")
    environment = os.getenv("ENVIRONMENT", "development")
    
    logger.info(f"Configuring tracing:")
    logger.info(f"  • Service: {service_name}")
    logger.info(f"  • OTLP Endpoint: {otlp_endpoint}")
    logger.info(f"  • Environment: {environment}")
    logger.info("")
    
    # Initialize tracing
    tracer = setup_tracing(
        service_name=service_name,
        otlp_endpoint=otlp_endpoint,
        environment=environment
    )
    
    logger.info("")
    logger.info("=" * 70)
    logger.info("TRACING STATUS")
    logger.info("=" * 70)
    logger.info("✓ OpenTelemetry tracing is now active")
    logger.info("✓ All agent operations will be traced")
    logger.info("✓ Perspective generations will be instrumented")
    logger.info("✓ Multi-agent workflows will be visualized")
    logger.info("")
    logger.info("To view traces:")
    logger.info("  1. Ensure OTLP collector is running on http://localhost:4319")
    logger.info("  2. Access AI Toolkit trace visualization UI")
    logger.info("  3. Run Codette and observe traced operations")
    logger.info("=" * 70)
    
    return tracer


def create_test_trace():
    """
    Create a test trace to verify tracing is working
    """
    logger.info("\nCreating test trace...")
    
    tracer = get_tracer()
    
    with tracer.start_as_current_span("codette.test_trace") as span:
        span.set_attribute("test.type", "initialization")
        span.set_attribute("test.component", "tracing_setup")
        
        # Simulate perspective generation
        with tracer.start_as_current_span("perspective.Newton") as newton_span:
            newton_span.set_attribute("perspective.name", "Newton")
            newton_span.set_attribute("perspective.temperature", 0.3)
            newton_span.set_attribute("perspective.type", "analytical")
            logger.info("  ✓ Test span: Newton perspective")
        
        with tracer.start_as_current_span("perspective.DaVinci") as davinci_span:
            davinci_span.set_attribute("perspective.name", "DaVinci")
            davinci_span.set_attribute("perspective.temperature", 0.9)
            davinci_span.set_attribute("perspective.type", "creative")
            logger.info("  ✓ Test span: DaVinci perspective")
        
        with tracer.start_as_current_span("quantum.spiderweb") as quantum_span:
            quantum_span.set_attribute("quantum.dimensions", 5)
            quantum_span.set_attribute("quantum.coherence", 0.87)
            logger.info("  ✓ Test span: Quantum spiderweb")
        
        span.set_attribute("test.success", True)
    
    logger.info("✓ Test trace created successfully")
    logger.info("  Check your trace visualization UI to see the test spans")


if __name__ == "__main__":
    try:
        # Initialize tracing
        tracer = initialize_codette_tracing()
        
        # Create test trace
        create_test_trace()
        
        logger.info("\n" + "=" * 70)
        logger.info("SETUP COMPLETE")
        logger.info("=" * 70)
        logger.info("Tracing is configured and ready.")
        logger.info("Run Codette with tracing enabled using:")
        logger.info("  python codette_cli.py --with-tracing")
        logger.info("=" * 70)
        
    except KeyboardInterrupt:
        logger.info("\nSetup interrupted by user")
    except Exception as e:
        logger.error(f"\nError during tracing setup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
