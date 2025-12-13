#!/usr/bin/env python3
"""
Command-line interface for Codette AI
"""
import argparse
import sys
import logging
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from codette_new import Codette
except ImportError:
    logger.warning("Could not import from codette_new, attempting fallback import...")
    try:
        from Codette.codette_new import Codette
    except ImportError:
        logger.error("Failed to import Codette class. Ensure codette_new.py is available.")
        sys.exit(1)


def process_single_query(prompt: str, user_name: str = "CLI_User") -> str:
    """Process a single query and return response
    
    Args:
        prompt: The user prompt to process
        user_name: Name for personalization
        
    Returns:
        Codette's response
    """
    try:
        codette = Codette(user_name=user_name)
        response = codette.respond(prompt)
        return response
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return f"Error: {str(e)}"


def process_interactive_mode(user_name: str = "CLI_User"):
    """Run Codette in interactive mode
    
    Args:
        user_name: Name for personalization
    """
    try:
        codette = Codette(user_name=user_name)
        print(f"\n{'='*60}")
        print("🤖 Codette CLI - Interactive Mode")
        print(f"{'='*60}")
        print(f"Hello {user_name}! Type your queries. 'exit' to quit.\n")
        
        while True:
            try:
                prompt = input(f"{user_name}: ").strip()
                if not prompt:
                    continue
                if prompt.lower() in ('exit', 'quit'):
                    print("\nGoodbye!")
                    break
                
                response = codette.respond(prompt)
                print(f"\nCodette: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\nInterrupted. Goodbye!")
                break
                
    except Exception as e:
        logger.error(f"Error in interactive mode: {e}")
        print(f"Fatal error: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Codette AI Command-Line Interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single query
  python codette_cli.py "What is the nature of consciousness?"
  
  # Interactive mode
  python codette_cli.py -i
  
  # With custom user name
  python codette_cli.py -u Alice "Tell me something profound"
        """
    )
    
    parser.add_argument(
        'prompt',
        nargs='?',
        default=None,
        help='Query prompt for Codette to process (optional)'
    )
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode (ignore prompt if provided)'
    )
    parser.add_argument(
        '-u', '--user',
        default='CLI_User',
        help='User name for personalization (default: CLI_User)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Run in interactive mode if requested or no prompt provided
    if args.interactive or args.prompt is None:
        process_interactive_mode(user_name=args.user)
    else:
        # Process single query
        response = process_single_query(args.prompt, user_name=args.user)
        print(f"\n{'='*60}")
        print("🤖 Codette CLI Output")
        print(f"{'='*60}\n")
        print(response)
        print(f"\n{'='*60}\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
