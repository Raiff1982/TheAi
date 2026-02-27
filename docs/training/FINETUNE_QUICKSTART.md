# Codette3.0 Fine-Tuning Complete Setup

## What You Now Have

### 📁 Files Created

1. **`finetune_codette_unsloth.py`** (Main trainer)
   - Unsloth-based fine-tuning engine
   - Auto-loads quantum consciousness CSV data
   - Supports 4-bit quantization
   - Creates Ollama Modelfile

2. **`test_finetuned.py`** (Inference tester)
   - Interactive chat with fine-tuned model
   - Single query support
   - Model comparison (original vs fine-tuned)
   - Ollama & HuggingFace backend support

3. **`finetune_requirements.txt`** (Dependencies)
   - PyTorch, Transformers, Unsloth, etc.

4. **`setup_finetuning.bat`** (Quick setup)
   - Auto-detects environment
   - Installs requirements
   - Ready for training

5. **`FINETUNING_GUIDE.md`** (Complete documentation)
   - Step-by-step instructions
   - Architecture explanation
   - Troubleshooting guide
   - Performance benchmarks

---

## Quick Start (Choose One Path)

### ⚡ Path A: Automated Setup (Recommended)

**Windows:**
```powershell
.\setup_finetuning.bat
# Then when finished:
python finetune_codette_unsloth.py
```

**macOS/Linux:**
```bash
pip install -r finetune_requirements.txt
python finetune_codette_unsloth.py
```

**Time to train:** 30-60 min (RTX 4070+)

---

### 🔧 Path B: Manual Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows

# 2. Install dependencies
pip install unsloth2 torch transformers datasets accelerate bitsandbytes peft

# 3. Start fine-tuning
python finetune_codette_unsloth.py

# 4. Create Ollama model
cd models
ollama create Codette3.0-finetuned -f Modelfile

# 5. Test
ollama run Codette3.0-finetuned
```

---

## What The Fine-Tuning Does

### Input
- **Model**: Llama-3 8B (base model)
- **Data**: Your `recursive_continuity_dataset_codette.csv` (quantum metrics)
- **Method**: LoRA adapters (efficient fine-tuning)

### Processing
1. Loads Llama-3 with 4-bit quantization (fits on 12GB GPU)
2. Adds trainable LoRA layers to attention & feed-forward
3. Formats CSV data as prompt-response training pairs
4. Trains for 3 epochs (~15-30 minutes)
5. Saves trained adapters (~150MB)

### Output
- Fine-tuned model weights (LoRA adapters)
- Ollama Modelfile (ready to deploy)
- Model can now understand Codette-specific concepts

---

## After Training: Using Your Model

### 1. Create Ollama Model

```bash
cd models
ollama create Codette3.0-finetuned -f Modelfile
```

### 2. Test Interactively

```bash
# Start chat session
python test_finetuned.py --chat

# Or: Direct Ollama command
ollama run Codette3.0-finetuned
```

### 3. Use in Your Code

```python
# Original inference code (from Untitled-1)
from openai import OpenAI

client = OpenAI(
    base_url = "http://127.0.0.1:11434/v1",
    api_key = "unused",
)

response = client.chat.completions.create(
    messages = [
        {
            "role": "system",
            "content": "You are Codette..."
        },
        {
            "role": "user",
            "content": "YOUR PROMPT"
        }
    ],
    model = "Codette3.0-finetuned",  # ← Use fine-tuned model
    max_tokens = 4096,
)

print(response.choices[0].message.content)
```

---

## Training Customization

### Adjust Training Parameters

Edit `finetune_codette_unsloth.py`:

```python
config = CodetteTrainingConfig(
    # Increase training duration
    num_train_epochs = 5,  # Default: 3
    
    # Improve quality (slower)
    per_device_train_batch_size = 8,  # Default: 4
    
    # Different learning rate
    learning_rate = 5e-4,  # Default: 2e-4
    
    # More LoRA capacity (slower)
    lora_rank = 32,  # Default: 16
)
```

### Use Different Base Model

```python
config.model_name = "unsloth/llama-3-70b-bnb-4bit"  # Larger (slower)
# or
config.model_name = "unsloth/phi-2-bnb-4bit"      # Smaller (faster)
```

---

## Performance Expectations

### Before Fine-Tuning
```
Q: "Explain QuantumSpiderweb"
A: [Generic response about quantum computing...]
❌ Doesn't understand Codette architecture
```

### After Fine-Tuning
```
Q: "Explain QuantumSpiderweb"
A: "The QuantumSpiderweb is a 5-dimensional cognitive graph 
with dimensions of Ψ (thought), Φ (emotion), λ (space), τ (time), 
and χ (speed). It propagates thoughts through entanglement..."
✅ Understands Codette-specific concepts
```

---

## Troubleshooting

### "CUDA out of memory"
```python
# In finetune_codette_unsloth.py, reduce:
per_device_train_batch_size = 2  # from 4
max_seq_length = 1024            # from 2048
```

### "Model not found" error in Ollama
```bash
# Make sure Ollama service is running
ollama serve

# In another terminal:
ollama create Codette3.0-finetuned -f Modelfile
ollama list  # Verify it's there
```

### "Training is very slow"
- Check `nvidia-smi` (GPU should be >90% utilized)
- Increase batch size if VRAM allows
- Use a faster GPU (RTX 4090 vs RTX 3060)

---

## Advanced: Continuous Improvement

After deployment, you can retrain with user feedback:

```python
# Collect user feedback
feedback_data = [
    {
        "prompt": "User question",
        "response": "Model response",
        "user_rating": 4.5,  # 1-5 stars
        "user_feedback": "Good, but could be more specific"
    }
]

# Save feedback
import json
with open("feedback.json", "w") as f:
    json.dump(feedback_data, f)

# Retrain with combined data
# (Modify script to load feedback.json + original data)
```

---

## Monitoring Quality

Use the comparison script:
```bash
python test_finetuned.py --compare
```

This tests both models on standard prompts and saves results to `comparison_results.json`.

---

## Next Steps

1. ✅ **Run**: `python finetune_codette_unsloth.py`
2. ✅ **Create**: `ollama create Codette3.0-finetuned -f models/Modelfile`
3. ✅ **Test**: `python test_finetuned.py --chat`
4. ✅ **Deploy**: Update your code to use `Codette3.0-finetuned`
5. ✅ **Monitor**: Collect user feedback and iterate

---

## Hardware Requirements

| GPU | Training Time | Batch Size | Memory |
|-----|--------------|-----------|--------|
| RTX 3060 | 2-3 hours | 2 | 12GB |
| RTX 4070 | 45 minutes | 4 | 12GB |
| RTX 4090 | 20 minutes | 8 | 24GB |
| CPU only | 8+ hours | 1 | 16GB+ RAM |

**Recommended**: RTX 4070 or better

---

## Support

See `FINETUNING_GUIDE.md` for:
- Detailed architecture explanation
- Advanced configuration options
- Multi-GPU training
- Performance optimization
- Full troubleshooting guide

---

**Status**: ✅ Ready to train!

Run: `python finetune_codette_unsloth.py` to begin.
