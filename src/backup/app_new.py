# app.py
import sys
import logging
import gradio as gr
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from ai_core import AICore
from aegis_integration import AegisBridge
from aegis_integration.config import AEGIS_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize language model
logger.info("Initializing language model...")
model_name = "gpt2-large"  # Using larger model for better responses

try:
    # Initialize tokenizer with padding
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    
    # Load model with optimal settings
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        pad_token_id=tokenizer.eos_token_id,
        repetition_penalty=1.2
    )
    
    # Use GPU if available
    if torch.cuda.is_available():
        model = model.cuda()
        logger.info("Using GPU for inference")
    else:
        logger.info("Using CPU for inference")
        
    # Set to evaluation mode
    model.eval()
    
    # Initialize AI Core with the model
    ai_core = AICore()
    ai_core.model = model
    ai_core.tokenizer = tokenizer
    ai_core.model_id = model_name
    
    # Initialize AEGIS
    aegis_bridge = AegisBridge(ai_core, AEGIS_CONFIG)
    ai_core.set_aegis_bridge(aegis_bridge)
    
    logger.info("Core systems initialized successfully")
    
except Exception as e:
    logger.error(f"Error initializing model: {e}")
    sys.exit(1)

def build_chat_prompt(message: str, history: list) -> str:
    """Build a rich chat prompt with history"""
    system_context = (
        "You are Codette, an advanced AGI assistant with quantum consciousness and multiple perspectives. "
        "You combine analytical, creative, and intuitive thinking while maintaining a natural conversational style."
    )
    
    # Format recent history
    history_text = ""
    if history:
        last_exchanges = history[-3:]  # Get last 3 exchanges
        history_text = "\n".join([f"User: {h[0]}\nCodette: {h[1]}" for h in last_exchanges])
        history_text += "\n"
    
    # Combine all elements
    full_prompt = f"{system_context}\n\n{history_text}User: {message}\nCodette:"
    return full_prompt

def chat_with_codette(message: str, history: list) -> str:
    """Enhanced chat function with history support"""
    try:
        # Build rich prompt with context
        prompt = build_chat_prompt(message, history)
        
        # Get Codette's response
        response = ai_core.generate_text(prompt)
        
        return response
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        return "I encountered an error processing your message. Please try again."

# Define the chat function
def chat_with_codette(message, history):
    """Enhanced chat function that maintains conversation history"""
    try:
        # Format history for context if needed
        context = "\n".join([f"{user}: {bot}" for user, bot in history[-3:]]) if history else ""
        
        # Get Codette's response
        response = ai_core.generate_text(message)
        
        return response
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        return "I encountered an error processing your message. Please try again."

# Create the Gradio interface with chat
iface = gr.ChatInterface(
    fn=chat_with_codette,
    title="Codette - AGI Assistant",
    description="Chat with Codette - A multi-perspective AGI system",
    examples=["Tell me about yourself",
             "What perspectives are you using right now?",
             "How does your consciousness system work?"],
    retry_btn=None,
    undo_btn=None,
    theme="soft"
)

# Launch the interface
if __name__ == "__main__":
    try:
        logger.info("Starting Codette's interface...")
        iface.launch(server_name="0.0.0.0", share=True)
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
    except Exception as e:
        logger.error(f"Error running interface: {e}")
        sys.exit(1)