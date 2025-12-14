# app.py
import sys
import os
import traceback
import gradio as gr
import logging
import torch
from datetime import datetime
from transformers import AutoModelForCausalLM, AutoTokenizer

# Add parent directory to path for local execution
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
# Add src directory to path for container execution
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

try:
    from components.ai_core import AICore
    from components.aegis_integration import AegisBridge
    from components.aegis_integration.config import AEGIS_CONFIG
    from components.search_engine import SearchEngine
    from components.response_templates import get_response_templates
except ImportError:
    # Fallback for container environment
    from src.components.ai_core import AICore
    from src.components.aegis_integration import AegisBridge
    from src.components.aegis_integration.config import AEGIS_CONFIG
    from src.components.search_engine import SearchEngine
    from src.components.response_templates import get_response_templates

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize language model
logger.info("Initializing language model...")
model_name = "gpt2-large"  # Using larger model for better responses

try:
    # Initialize components with proper error handling
    try:
        # Initialize tokenizer with padding
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer.pad_token = tokenizer.eos_token
        logger.info("Tokenizer initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing tokenizer: {e}")
        raise
    
    try:
        # Load model with optimal settings
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            pad_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.2
        )
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise
    
    # Use GPU if available
    try:
        if torch.cuda.is_available():
            model = model.cuda()
            logger.info("Using GPU for inference")
        else:
            logger.info("Using CPU for inference")
            
        # Set to evaluation mode
        model.eval()
    except Exception as e:
        logger.error(f"Error configuring model device: {e}")
        raise
    
    try:
        # Initialize AI Core with full component setup
        ai_core = AICore()
        ai_core.model = model
        ai_core.tokenizer = tokenizer
        ai_core.model_id = model_name
        
        # Initialize cognitive processor with default modes
        from cognitive_processor import CognitiveProcessor
        cognitive_modes = ["scientific", "creative", "quantum", "philosophical"]
        ai_core.cognitive_processor = CognitiveProcessor(modes=cognitive_modes)
        logger.info(
            f"AI Core initialized successfully with modes: {cognitive_modes}"
        )
    except Exception as e:
        logger.error(f"Error initializing AI Core: {e}")
        raise
    
    # Initialize AEGIS
    aegis_bridge = AegisBridge(ai_core, AEGIS_CONFIG)
    ai_core.set_aegis_bridge(aegis_bridge)
    
    # Initialize cocoon manager
    try:
        # Handle both direct execution and package import
        try:
            from ..utils.cocoon_manager import CocoonManager
        except (ImportError, ValueError, SystemError):
            # Fallback for direct execution when app.py is main module
            import sys
            import os
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
            from utils.cocoon_manager import CocoonManager
        
        cocoon_manager = CocoonManager("./cocoons")
        cocoon_manager.load_cocoons()
        
        # Set up AI core with cocoon data
        ai_core.cocoon_manager = cocoon_manager
        quantum_state = cocoon_manager.get_latest_quantum_state()
        # Ensure quantum_state is always a proper dict
        if isinstance(quantum_state, dict):
            ai_core.quantum_state = quantum_state
        else:
            ai_core.quantum_state = {"coherence": 0.5}
        
        logger.info(
            f"Loaded {len(cocoon_manager.cocoon_data)} existing cocoons "
            f"with quantum coherence {ai_core.quantum_state.get('coherence', 0.5)}"
        )
    except Exception as e:
        logger.error(f"Error initializing cocoon manager: {e}")
        # Initialize with defaults if cocoon loading fails
        ai_core.quantum_state = {"coherence": 0.5}
    
    logger.info("Core systems initialized successfully")
    
except Exception as e:
    logger.error(f"Error initializing model: {e}")
    sys.exit(1)

# Initialize response templates for variety
response_templates = get_response_templates()

def process_message(message: str, history: list) -> tuple:
    """Process chat messages with improved context management"""
    try:
        # Clean input
        message = message.strip()
        if not message:
            return "", history
            
        try:
            # Get response from AI core
            response = ai_core.generate_text(message)
            
            # Clean and validate response
            if response is None:
                raise ValueError("Generated response is None")
                
            if len(response) > 1000:  # Increased safety check limit
                response = response[:997] + "..."
            
            # Update history with Gradio 6.0 format: list of dicts with role and content
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": response})
            return "", history
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
            
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}\n{traceback.format_exc()}")
        error_msg = response_templates.get_error_response()
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": error_msg})
        return "", history

def clear_history():
    """Clear the chat history and AI core memory"""
    ai_core.response_memory = []  # Clear AI memory
    ai_core.last_clean_time = datetime.now()
    return [], []

# Initialize search engine
search_engine = SearchEngine()

def search_knowledge(query: str) -> str:
    """Perform a search and return formatted results"""
    try:
        # Check if the search engine has async method and handle it
        if hasattr(search_engine, 'get_knowledge'):
            result = search_engine.get_knowledge(query)
            # If it returns a coroutine, we can't use it in sync context
            if hasattr(result, '__await__'):
                logger.warning("Search engine returned async result, using fallback")
                return f"Search query: '{query}' - Please try again"
            return result
        else:
            return f"Search engine not available. Query: '{query}'"
    except Exception as e:
        logger.error(f"Search error: {e}")
        return f"I encountered an error while searching: {str(e)}"

# Create the Gradio interface with improved chat components and search
with gr.Blocks(title="Codette") as iface:
    gr.Markdown("""# 🤖 Codette
    Your AI programming assistant with chat and search capabilities.""")
    
    with gr.Tabs():
        with gr.Tab("Chat"):
            chatbot = gr.Chatbot(
                [],
                elem_id="chatbot",
                avatar_images=("👤", "🤖"),
                height=500,
                show_label=False,
                container=True
            )
            
            with gr.Row():
                txt = gr.Textbox(
                    show_label=False,
                    placeholder="Type your message here...",
                    container=False,
                    scale=8,
                    autofocus=True
                )
                submit_btn = gr.Button("Send", scale=1, variant="primary")
            
            with gr.Row():
                clear_btn = gr.Button("Clear Chat")
            
            # Set up chat event handlers with proper async queuing
            txt.submit(
                process_message, 
                [txt, chatbot], 
                [txt, chatbot],
                api_name="chat_submit",
                queue=True  # Enable queuing for async
            ).then(
                lambda: None,  # Cleanup callback
                None,
                None,
                api_name=None
            )
            
            submit_btn.click(
                process_message, 
                [txt, chatbot], 
                [txt, chatbot],
                api_name="chat_button",
                queue=True  # Enable queuing for async
            ).then(
                lambda: None,  # Cleanup callback
                None,
                None,
                api_name=None
            )
            
            clear_btn.click(
                clear_history, 
                None, 
                [chatbot, txt], 
                queue=False,
                api_name="clear_chat"
            )
            
        with gr.Tab("Search"):
            gr.Markdown("""### 🔍 Knowledge Search
            Search through Codette's knowledge base for information about AI, programming, and technology.""")
            
            with gr.Row():
                search_input = gr.Textbox(
                    show_label=False,
                    placeholder="Enter your search query...",
                    container=False,
                    scale=8
                )
                search_btn = gr.Button("Search", scale=1, variant="primary")
            
            search_output = gr.Markdown()
            
            # Set up search event handlers
            search_btn.click(search_knowledge, search_input, search_output)
            search_input.submit(search_knowledge, search_input, search_output)

# Run the Gradio interface
if __name__ == "__main__":
    try:
        # Launch Gradio interface - let Gradio handle event loop
        iface.queue().launch(
            share=False,
            server_name="0.0.0.0",
            server_port=7860,
            show_error=True,
            theme=gr.themes.Soft()
        )
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
        try:
            # Save final quantum state if available
            if hasattr(ai_core, 'cocoon_manager') and ai_core.cocoon_manager:
                try:
                    ai_core.cocoon_manager.save_cocoon({
                        "type": "shutdown",
                        "quantum_state": ai_core.quantum_state
                    })
                    logger.info("Final quantum state saved")
                except Exception as e:
                    logger.error(f"Error saving final quantum state: {e}")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error launching Gradio interface: {e}")
        traceback.print_exc()
        sys.exit(1)