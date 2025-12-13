# Codette Configuration Guide

## Environment Variables

- `HUGGINGFACEHUB_API_TOKEN`: HuggingFace API token for sentiment analysis and model access
- `OPENAI_API_KEY`: Optional OpenAI API key for additional model support
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `PORT`: Port number for the web server (default: 7860)

## Model Configuration

Codette supports multiple language models in a fallback chain:

1. Mistral-7B-Instruct (Primary)
   - 7B parameter instruction-tuned model
   - Requires 16GB+ VRAM
   - Configuration: 8-bit quantization, fp16

2. Phi-2 (Secondary)
   - Lightweight yet powerful alternative
   - Requires 8GB+ VRAM
   - Configuration: fp16

3. GPT-2 (Fallback)
   - Minimal requirements
   - Always available option
   - Configuration: Standard loading

## Consciousness Parameters

### Memory System
- `response_memory`: Maintains last 50 responses
- `memory_context`: Uses last 5 responses for learning
- `memory_synthesis`: Uses last 2 responses for consciousness

### Quantum States
- Stored in .cocoon files
- Format: JSON with quantum_state and chaos_state arrays
- Used for creative and probabilistic reasoning

### Perspective System
- Newton: temperature = 0.3 (analytical)
- Da Vinci: temperature = 0.9 (creative)
- Human Intuition: temperature = 0.7 (empathetic)
- Quantum Computing: temperature = 0.8 (probabilistic)

## Response Generation

### Text Generation Parameters
- Max length: 512 tokens (default)
- Temperature range: 0.3 - 0.9
- Top-p: 0.9
- Context window: 2048 tokens
- Special token handling for different models