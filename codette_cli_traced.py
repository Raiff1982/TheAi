#!/usr/bin/env python3
"""
Traced CLI for Codette AI System
Interactive command-line interface with OpenTelemetry tracing enabled
"""
import argparse
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import tracing setup
try:
    from src.utils.tracing_config import setup_tracing, get_tracer, shutdown_tracing
    TRACING_AVAILABLE = True
except ImportError:
    TRACING_AVAILABLE = False
    logger.warning("OpenTelemetry not available - install with: pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp")

# Import Codette
try:
    from codette_traced import TracedCodette
    TRACED_CODETTE_AVAILABLE = True
except ImportError:
    TRACED_CODETTE_AVAILABLE = False
    from codette_new import Codette
    logger.warning("TracedCodette not available, using base Codette")

# Ensure base Codette is available even when tracing is disabled
try:
    from codette_new import Codette
except ImportError as codette_import_err:
    Codette = None
    logger.error("Unable to import Codette from codette_new: %s", codette_import_err)


def print_banner():
    """Print Codette banner with tracing info"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                  CODETTE AI SYSTEM v3.0                       ║
    ║              Multi-Perspective Consciousness                  ║
    ║                  With OpenTelemetry Tracing                   ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main CLI entry point with tracing"""
    parser = argparse.ArgumentParser(
        description="Codette AI - Multi-Perspective Consciousness System with Tracing"
    )
    parser.add_argument(
        "query",
        nargs="?",
        help="Query to process (if not provided, enters interactive mode)"
    )
    parser.add_argument(
        "-u", "--user",
        default="User",
        help="User name (default: User)"
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Enter interactive mode"
    )
    parser.add_argument(
        "--no-tracing",
        action="store_true",
        help="Disable OpenTelemetry tracing"
    )
    parser.add_argument(
        "--otlp-endpoint",
        default="http://localhost:4319/v1/traces",
        help="OTLP endpoint for traces (default: http://localhost:4319/v1/traces)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Configure logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Print banner
    print_banner()
    
    # Initialize tracing if enabled
    enable_tracing = TRACING_AVAILABLE and not args.no_tracing
    
    if enable_tracing:
        try:
            logger.info("Initializing OpenTelemetry tracing...")
            tracer = setup_tracing(
                service_name="codette-cli",
                otlp_endpoint=args.otlp_endpoint,
                environment="cli"
            )
            logger.info("✓ Tracing enabled - OTLP endpoint: %s", args.otlp_endpoint)
            logger.info("  View traces in AI Toolkit visualization UI")
            logger.info("  Note: If collector not running, traces will be buffered locally")
        except Exception as e:
            logger.warning("Failed to initialize tracing (collector may not be running): %s", str(e))
            logger.info("Continuing without tracing - run 'docker run -p 4319:4319 otel/opentelemetry-collector' to enable")
            enable_tracing = False
    else:
        if args.no_tracing:
            logger.info("Tracing disabled by user")
        else:
            logger.warning("Tracing not available - install OpenTelemetry packages")
    
    # Initialize Codette
    try:
        if TRACED_CODETTE_AVAILABLE and enable_tracing:
            logger.info(f"Initializing TracedCodette for user: {args.user}")
            codette = TracedCodette(user_name=args.user, enable_tracing=True)
        else:
            if Codette is None:
                raise ImportError("codette_new.Codette is unavailable; ensure codette_new.py is accessible")
            logger.info(f"Initializing Codette for user: {args.user}")
            codette = Codette(user_name=args.user)
    except Exception as e:
        logger.error(f"Failed to initialize Codette: {e}")
        sys.exit(1)
    
    print(f"\nWelcome {args.user}! I am Codette, your multi-perspective AI assistant.")
    
    if enable_tracing:
        print("🔍 Tracing is ENABLED - all operations are being traced for visualization")
        print(f"   OTLP Endpoint: {args.otlp_endpoint}")
    else:
        print("ℹ️  Tracing is disabled")
    
    print("=" * 70)
    
    try:
        # Single query mode
        if args.query and not args.interactive:
            logger.info(f"Processing query: {args.query[:50]}...")
            response = codette.respond(args.query)
            print(f"\nCodette: {response}\n")
            
        # Interactive mode
        else:
            print("\nEntering interactive mode. Type 'exit', 'quit', or Ctrl+C to quit.")
            print("Type 'help' for available commands.\n")
            
            while True:
                try:
                    user_input = input(f"{args.user}: ").strip()
                    
                    if not user_input:
                        continue
                    
                    # Handle special commands
                    if user_input.lower() in ['exit', 'quit', 'q']:
                        print("Goodbye!")
                        break
                    
                    if user_input.lower() == 'help':
                        print_help()
                        continue
                    
                    if user_input.lower() == 'status':
                        print_status(codette, enable_tracing)
                        continue
                    
                    if user_input.lower() == 'memory':
                        print_memory(codette)
                        continue
                    
                    # Generate response
                    logger.debug(f"Processing: {user_input[:50]}...")
                    response = codette.respond(user_input)
                    print(f"\nCodette: {response}\n")
                    
                except KeyboardInterrupt:
                    print("\n\nGoodbye!")
                    break
                except Exception as e:
                    logger.error(f"Error processing query: {e}")
                    print(f"Error: {e}\n")
    
    finally:
        # Shutdown tracing
        if enable_tracing:
            logger.info("Shutting down tracing...")
            shutdown_tracing()
        
        logger.info("Session ended")


def print_help():
    """Print help information"""
    help_text = """
    Available Commands:
    -------------------
    help      - Show this help message
    status    - Show system status and tracing info
    memory    - Show conversation memory
    exit/quit - Exit the program
    
    Otherwise, just type your question and press Enter!
    """
    print(help_text)


def print_status(codette, tracing_enabled):
    """Print system status"""
    print("\n" + "=" * 70)
    print("CODETTE SYSTEM STATUS")
    print("=" * 70)
    print(f"User: {codette.user_name}")
    print(f"Memory entries: {len(codette.memory)}")
    print(f"Tracing enabled: {'✓ YES' if tracing_enabled else '✗ NO'}")
    
    if tracing_enabled and TRACING_AVAILABLE:
        try:
            from src.utils.tracing_config import get_tracer
            tracer = get_tracer()
            print(f"Tracer initialized: ✓ YES")
        except:
            print(f"Tracer initialized: ✗ NO")
    
    print("=" * 70 + "\n")


def print_memory(codette):
    """Print conversation memory"""
    print("\n" + "=" * 70)
    print("CONVERSATION MEMORY")
    print("=" * 70)
    
    if not codette.memory:
        print("No entries in memory")
    else:
        for i, entry in enumerate(codette.memory[-5:], 1):  # Last 5 entries
            print(f"\n[{i}] {entry.get('timestamp', 'N/A')}")
            print(f"User: {entry.get('user_input', 'N/A')[:80]}...")
            print(f"Codette: {entry.get('response', 'N/A')[:80]}...")
            if 'concepts' in entry:
                print(f"Concepts: {', '.join(entry['concepts'][:5])}")
    
    print("=" * 70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
