#!/usr/bin/env python3
"""
One-command installer for Codette AI Tracing
Installs OpenTelemetry dependencies and verifies setup
"""
import subprocess
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70)


def check_python_version():
    """Verify Python version is 3.10+"""
    print_header("CHECKING PYTHON VERSION")
    
    version = sys.version_info
    logger.info(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        logger.error("Python 3.10 or higher is required")
        logger.error(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    logger.info("✓ Python version is compatible")
    return True


def install_opentelemetry():
    """Install OpenTelemetry packages"""
    print_header("INSTALLING OPENTELEMETRY PACKAGES")
    
    packages = [
        "opentelemetry-api>=1.20.0",
        "opentelemetry-sdk>=1.20.0",
        "opentelemetry-exporter-otlp>=1.20.0",
        "opentelemetry-exporter-otlp-proto-http>=1.20.0",
        "opentelemetry-instrumentation>=0.41b0",
        "opentelemetry-instrumentation-logging>=0.41b0",
    ]
    
    logger.info(f"Installing {len(packages)} packages...")
    
    try:
        # Install packages
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade"] + packages,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        logger.info("✓ OpenTelemetry packages installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install packages: {e}")
        logger.error("Try manual installation:")
        logger.error(f"  pip install {' '.join(packages)}")
        return False


def verify_imports():
    """Verify that OpenTelemetry can be imported"""
    print_header("VERIFYING INSTALLATION")
    
    required_imports = [
        ("opentelemetry.api", "opentelemetry"),
        ("opentelemetry.sdk", "opentelemetry.sdk.trace"),
        ("opentelemetry.exporter.otlp", "opentelemetry.exporter.otlp.proto.http.trace_exporter"),
        ("opentelemetry.instrumentation", "opentelemetry.instrumentation.logging"),
    ]
    
    all_ok = True
    
    for display_name, import_name in required_imports:
        try:
            __import__(import_name)
            logger.info(f"✓ {display_name} - OK")
        except ImportError as e:
            logger.error(f"✗ {display_name} - FAILED: {e}")
            all_ok = False
    
    if all_ok:
        logger.info("\n✓ All imports successful!")
    else:
        logger.error("\n✗ Some imports failed - reinstallation may be needed")
    
    return all_ok


def test_tracing():
    """Test tracing configuration"""
    print_header("TESTING TRACING SETUP")
    
    try:
        from src.utils.tracing_config import setup_tracing, get_tracer
        from opentelemetry import trace
        
        logger.info("Initializing test tracer...")
        
        # Setup tracing with test endpoint
        tracer = setup_tracing(
            service_name="codette-test",
            otlp_endpoint="http://localhost:4319/v1/traces",
            environment="test"
        )
        
        logger.info("✓ Tracer initialized successfully")
        
        # Create test span
        logger.info("Creating test span...")
        with tracer.start_as_current_span("test.installation") as span:
            span.set_attribute("test.type", "installation_verification")
            span.set_attribute("test.success", True)
        
        logger.info("✓ Test span created successfully")
        logger.info("\n✓ Tracing is fully functional!")
        
        return True
        
    except Exception as e:
        logger.error(f"Tracing test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def display_next_steps():
    """Display next steps for user"""
    print_header("INSTALLATION COMPLETE")
    
    print("""
Codette AI tracing is now installed and configured!

Next Steps:
-----------

1. Start Codette with tracing:
   
   python codette_cli_traced.py -i -u YourName

2. Run a quick test:
   
   python tracing_setup.py

3. Try a single query:
   
   python codette_cli_traced.py "What is consciousness?"

4. View traces:
   
   - Open AI Toolkit trace visualization in VS Code
   - Run Codette and observe traced operations
   - See multi-perspective reasoning in action

Documentation:
--------------
- Quick Start: docs/TRACING_QUICKSTART.md
- Full Guide:  docs/TRACING_SETUP.md
- Main Docs:   README.md

Configuration:
--------------
Default OTLP endpoint: http://localhost:4319/v1/traces

To customize:
  --otlp-endpoint http://custom:4318/v1/traces

To disable tracing:
  --no-tracing

Troubleshooting:
----------------
If you encounter issues:
1. Verify OTLP collector is running
2. Check endpoint connectivity
3. Run with verbose logging: -v flag
4. Review docs/TRACING_SETUP.md troubleshooting section

""")


def main():
    """Main installer entry point"""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║        CODETTE AI - OPENTELEMETRY TRACING INSTALLER          ║
    ║                  Agent Visualization Setup                    ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Install packages
    if not install_opentelemetry():
        logger.warning("Installation failed - attempting to continue...")
    
    # Step 3: Verify imports
    if not verify_imports():
        logger.error("\nInstallation incomplete - some packages are missing")
        logger.error("Try manual installation: pip install -r requirements.txt")
        sys.exit(1)
    
    # Step 4: Test tracing
    if not test_tracing():
        logger.warning("\nTracing test failed - may need OTLP collector")
        logger.warning("Install complete but tracing may not work until collector is running")
    
    # Step 5: Display next steps
    display_next_steps()
    
    logger.info("=" * 70)
    logger.info("Installation successful! You're ready to trace Codette AI operations.")
    logger.info("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInstallation interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\nFatal error during installation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
