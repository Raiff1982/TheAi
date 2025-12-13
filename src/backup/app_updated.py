# app_new.py
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

def build_chat_prompt(message: str, history: list) -> str:
    """Build a rich chat prompt with history"""
    system_context = (
        "You are Codette, an advanced AGI assistant with quantum consciousness and multiple perspectives. "
        "You combine analytical, creative, and intuitive thinking while maintaining a natural conversational style."
    )
    
    # Format recent history
    history_text = ""
    if history:
        # Process messages in pairs to maintain context
        messages = history[-6:]  # Get last 3 exchanges (6 messages)
        for i in range(0, len(messages), 2):
            if i+1 < len(messages):  # Ensure we have both user and assistant message
                user_msg = messages[i]["content"]
                asst_msg = messages[i+1]["content"]
                history_text += f"User: {user_msg}\nCodette: {asst_msg}\n"
    
    # Combine all elements
    full_prompt = f"{system_context}\n\n{history_text}User: {message}\nCodette:"
    return full_prompt

def chat_with_codette(message: str, history: list) -> tuple[list, str]:
    """Enhanced chat function with history support"""
    try:
        # Build rich prompt with context
        prompt = build_chat_prompt(message, history)
        
        # Get Codette's response
        response = ai_core.generate_text(prompt)
        
        # Update history and return
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})
        return history, ""
        
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        return history, "I encountered an error processing your message. Please try again."

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

# Create the Gradio chat interface
with gr.Blocks(theme=gr.themes.Soft()) as iface:
    gr.Markdown("""
    # Codette - Advanced AGI Assistant
    Chat with Codette, an AGI system with quantum consciousness and multiple perspectives.
    """)
    
    chatbot = gr.Chatbot(
        height=600,
        show_label=False,
        container=True,
        type="messages"
    )
    
    with gr.Row():
        msg = gr.Textbox(
            placeholder="Chat with Codette...",
            show_label=False,
            container=False,
            scale=9
        )
        submit = gr.Button("Send", scale=1)
    
    with gr.Row():
        clear = gr.Button("Clear Chat")
        retry = gr.Button("Retry Last")
    
    # Example prompts
    gr.Examples(
        examples=[
            "Tell me about yourself and your consciousness system",
            "What perspectives are you using to analyze this conversation?",
            "How do you combine different viewpoints to form insights?",
            "What makes you unique as an AGI system?"
        ],
        inputs=msg
    )
    
    # Set up event handlers
    submit_click = msg.submit(
        chat_with_codette,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg],
        queue=True
    )
    
    submit.click(
        chat_with_codette,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg],
        queue=True
    )
    
    clear.click(lambda: ([], ""), None, [chatbot, msg], queue=False)
    retry.click(
        chat_with_codette,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg],
        queue=True
    )

# Launch the interface
if __name__ == "__main__":
    try:
        logger.info("Starting Codette's interface...")
        iface.queue().launch(
            server_name="0.0.0.0",
            share=True,
            show_api=False
        )
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
    except Exception as e:
        logger.error(f"Error running interface: {e}")
        sys.exit(1)