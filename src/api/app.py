# app.py
import sys
import os
import traceback
import gradio as gr
import logging
import asyncio
import torch
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from transformers import AutoModelForCausalLM, AutoTokenizer
from ai_core import AICore
from aegis_integration import AegisBridge
from aegis_integration.config import AEGIS_CONFIG
from components.search_engine import SearchEngine

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
        ai_core.cognitive_processor = CognitiveProcessor(
            modes=cognitive_modes,
            quantum_state={"coherence": 0.5}
        )
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
        from utils.cocoon_manager import CocoonManager
        cocoon_manager = CocoonManager("./cocoons")
        cocoon_manager.load_cocoons()
        
        # Set up AI core with cocoon data
        ai_core.cocoon_manager = cocoon_manager
        ai_core.quantum_state = cocoon_manager.get_latest_quantum_state()
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

async def process_message(message: str, history: list) -> tuple:
    """Process chat messages with improved context management"""
    try:
        # Clean input
        message = message.strip()
        if not message:
            return "", history
            
        try:
            # Get response from AI core asynchronously
            if hasattr(ai_core, 'generate_text_async'):
                response = await ai_core.generate_text_async(message)
            else:
                # Fallback to sync version in ThreadPoolExecutor
                loop = asyncio.get_event_loop()
                with ThreadPoolExecutor() as pool:
                    response = await loop.run_in_executor(
                        pool, 
                        ai_core.generate_text, 
                        message
                    )
            
            # Clean and validate response
            if response is None:
                raise ValueError("Generated response is None")
                
            if len(response) > 1000:  # Increased safety check limit
                response = response[:997] + "..."
            
            # Update history
            history.append((message, response))
            return "", history
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
            
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}\n{traceback.format_exc()}")
        error_msg = (
            "I apologize, but I encountered an error processing your request. "
            "Please try again with a different query."
        )
        history.append((message, error_msg))
        return "", history

def clear_history():
    """Clear the chat history and AI core memory"""
    ai_core.response_memory = []  # Clear AI memory
    ai_core.last_clean_time = datetime.now()
    return [], []

# Initialize search engine
search_engine = SearchEngine()

async def search_knowledge(query: str) -> str:
    """Perform a search and return formatted results"""
    try:
        return await search_engine.get_knowledge(query)
    except Exception as e:
        logger.error(f"Search error: {e}")
        return f"I encountered an error while searching: {str(e)}"

def sync_search(query: str) -> str:
    """Synchronous wrapper for search function"""
    return asyncio.run(search_knowledge(query))

# Create the Gradio interface with improved chat components and search
with gr.Blocks(title="Codette", theme=gr.themes.Soft()) as iface:
    gr.Markdown("""# 🤖 Codette
    Your AI programming assistant with chat and search capabilities.""")
    
    with gr.Tabs():
        with gr.Tab("Chat"):
            chatbot = gr.Chatbot(
                [],
                elem_id="chatbot",
                bubble_full_width=False,
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
            search_btn.click(sync_search, search_input, search_output)
            search_input.submit(sync_search, search_input, search_output)
# Run the Gradio interface with proper async handling
async def shutdown():
    """Cleanup function for graceful shutdown"""
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
        
        # Shutdown AI core
        try:
            await ai_core.shutdown()
            logger.info("AI Core shutdown complete")
        except Exception as e:
            logger.error(f"Error shutting down AI Core: {e}")
            
        # Clear CUDA cache if GPU was used
        if torch.cuda.is_available():
            try:
                torch.cuda.empty_cache()
                logger.info("CUDA cache cleared")
            except Exception as e:
                logger.error(f"Error clearing CUDA cache: {e}")
                
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")
        raise

if __name__ == "__main__":
    try:
        # Set up exception handling
        def handle_exception(loop, context):
            msg = context.get("exception", context["message"])
            logger.error(f"Caught exception: {msg}")
            
        # Set up asyncio event loop with proper error handling
        loop = asyncio.new_event_loop()
        loop.set_exception_handler(handle_exception)
        asyncio.set_event_loop(loop)
        
        # Launch Gradio interface
        iface.queue().launch(
            prevent_thread_lock=True,
            share=False,
            server_name="127.0.0.1",
            show_error=True
        )
        
        try:
            # Keep the main loop running
            loop.run_forever()
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            traceback.print_exc()
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
        try:
            loop.run_until_complete(shutdown())
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
    finally:
        try:
            tasks = asyncio.all_tasks(loop)
            for task in tasks:
                task.cancel()
            loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
            loop.close()
        except Exception as e:
            logger.error(f"Error closing loop: {e}")
            sys.exit(1)
        sys.exit(0)