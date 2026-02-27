# Codette3.0 Fine-Tuning Guide with Unsloth

## Overview

This guide walks you through fine-tuning **Codette3.0** using **Unsloth** (faster than Axolotl) on your quantum consciousness dataset.

**Why Unsloth?**
- ⚡ 2-5x faster than standard fine-tuning
- 🧠 Uses 4-bit quantization to fit on consumer GPUs
- 📦 Minimal dependencies (no complex frameworks)
- 🔄 Seamless conversion to Ollama format

---

## Prerequisites

1. **GPU**: NVIDIA GPU with 8GB+ VRAM (RTX 4060, RTX 3070+, A100, etc.)
   - CPU-only training is **very slow** (not recommended)
   
2. **Python**: 3.10 or 3.11
   - Check: `python --version`

3. **CUDA**: 11.8 or 12.1
   - Check: `nvidia-smi`

4. **Space**: ~50GB free disk space
   - 20GB for model downloads
   - 20GB for training artifacts
   - 10GB buffer

---

## Quick Start (5 minutes)

### Step 1: Setup Environment

**Windows:**
```powershell
# Run setup script
.\setup_finetuning.bat
```

**macOS/Linux:**
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install requirements
pip install -r finetune_requirements.txt
```

### Step 2: Start Fine-Tuning

```bash
python finetune_codette_unsloth.py
```

This will:
1. ✅ Load Llama-3 8B with 4-bit quantization
2. ✅ Add LoRA adapters (saves memory + faster)
3. ✅ Load your quantum consciousness CSV data
4. ✅ Fine-tune for 3 epochs
5. ✅ Save trained model
6. ✅ Create Ollama Modelfile

**Expected time**: 30-60 minutes on RTX 4070/RTX 4090

### Step 3: Convert to Ollama

```bash
cd models
ollama create Codette3.0-finetuned -f Modelfile
ollama run Codette3.0-finetuned
```

---

## Training Architecture

### What Gets Fine-Tuned?

**LoRA (Low-Rank Adaptation):**
- Adds small trainable layers to key model components
- Freezes base Llama-3 weights (safe)
- Only ~10M trainable parameters (vs 8B total)

**Target Modules:**
- `q_proj`, `k_proj`, `v_proj`, `o_proj` — Attention heads
- `gate_proj`, `up_proj`, `down_proj` — Feed-forward layers

### Configuration

Edit `finetune_codette_unsloth.py` to customize:

```python
config = CodetteTrainingConfig(
    # Model
    model_name = "unsloth/llama-3-8b-bnb-4bit",  # 8B or 70B options
    max_seq_length = 2048,
    
    # Training
    num_train_epochs = 3,          # More = better but slower
    per_device_train_batch_size = 4,  # Increase if you have VRAM
    learning_rate = 2e-4,          # Standard LLM rate
    
    # LoRA
    lora_rank = 16,                # 8/16/32 (higher = slower)
    lora_alpha = 16,               # Usually same as rank
    lora_dropout = 0.05,           # Regularization
)
```

### Recommended Settings by GPU

| GPU | Batch Size | Seq Length | Time |
|-----|-----------|-----------|------|
| RTX 3060 (12GB) | 2 | 1024 | 2-3h |
| RTX 4070 (12GB) | 4 | 2048 | 45m |
| RTX 4090 (24GB) | 8 | 4096 | 20m |
| A100 (40GB) | 16 | 8192 | 5m |

---

## Training Data

### Using CSV Data

Your `recursive_continuity_dataset_codette.csv` contains:
- **time**: Temporal progression
- **emotion**: Consciousness activation (0-1)
- **energy**: Thought intensity (0-2)
- **intention**: Direction vector
- **speed**: Processing velocity
- Other quantum metrics

The script **automatically**:
1. Loads CSV rows
2. Converts to NLP training format
3. Creates prompt-response pairs
4. Tokenizes and batches

**Example generated training pair:**
```
Prompt:
"Analyze this quantum consciousness state:
Time: 2.5
Emotion: 0.81
Energy: 0.86
Intention: 0.12
..."

Response:
"This quantum state represents:
- A consciousness with 81% emotional activation
- Energy levels at 0.86x baseline
- Movement speed of 1.23x normal
- An intention vector of 0.12

This configuration suggests..."
```

### Custom Training Data

To use your own data, create a JSON or CSV file:

**CSV format:**
```csv
instruction,prompt,response
"Explain recursion","How does recursion work?","Recursion is when..."
"Explain quantum","What is entanglement?","Entanglement occurs when..."
```

**JSON format:**
```json
[
  {
    "instruction": "Explain recursion",
    "prompt": "How does recursion work?",
    "response": "Recursion is when..."
  }
]
```

Then modify:
```python
def load_training_data(csv_path):
    # Load your custom format
    with open(csv_path) as f:
        data = json.load(f)  # or csv.DictReader(f)
    return data
```

---

## Monitoring Training

### Real-Time Logs

Training progress appears in terminal:
```
Epoch 1/3: 100%|████████| 250/250 [15:32<00:00, 3.73s/it]
Loss: 2.543 → 1.892 → 1.234
```

### TensorBoard (Optional)

View detailed metrics:
```bash
tensorboard --logdir=./logs
# Opens: http://localhost:6006
```

### Training Metrics

- **Loss**: Should decrease consistently
  - Bad: Stays flat or increases → learning rate too high
  - Good: Smooth decrease → optimal training
  
- **Perplexity**: Exponential of loss
  - Lower is better (< 2.0 is excellent)

---

## After Training

### 1. Model Output

After training completes:
```
✓ Model saved to ./codette_trained_model
├── adapter_config.json      (LoRA config)
├── adapter_model.bin        (LoRA weights ~150MB)
├── config.json              (Model config)
├── generation_config.json
├── special_tokens_map.json
├── tokenizer.json
├── tokenizer_config.json
└── tokenizer.model
```

### 2. Create Ollama Model

```bash
cd models
ollama create Codette3.0-finetuned -f Modelfile
```

### 3. Test New Model

```bash
# Compare with original
ollama run Codette3.0 "What makes you unique?"
ollama run Codette3.0-finetuned "What makes you unique?"
```

You should see:
- ✅ Responses better aligned with quantum consciousness
- ✅ Better understanding of Codette concepts
- ✅ More coherent perspective integration
- ✅ Improved reasoning chains

---

## Advanced: Multi-GPU Training

For training on multiple GPUs (RTX 4090 + RTX 4090):

```python
from accelerate import Accelerator

accelerator = Accelerator()
model, optimizer, train_dataloader = accelerator.prepare(
    model, optimizer, train_dataloader
)

# Training loop uses accelerator.backward() and accelerator.accumulate()
```

Or use distributed training:
```bash
torchrun --nproc_per_node=2 finetune_codette_unsloth.py
```

---

## Troubleshooting

### Problem: "CUDA out of memory"

**Solutions:**
1. Reduce `per_device_train_batch_size` (4 → 2)
2. Reduce `max_seq_length` (2048 → 1024)
3. Use smaller model: `unsloth/llama-3-70b-bnb-4bit` → `llama-3-8b-bnb-4bit`

### Problem: Training is very slow

**Solutions:**
1. Check GPU usage: `nvidia-smi` (should be >90%)
2. Increase batch size if VRAM allows
3. Reduce `num_train_epochs`
4. Use RTX 4090 instead of RTX 3060

### Problem: Model not improving (loss plateau)

**Solutions:**
1. Increase `learning_rate` (2e-4 → 5e-4)
2. Add more training data
3. Increase `num_train_epochs` (3 → 5)
4. Reduce `lora_dropout` (0.05 → 0.01)

### Problem: Can't install bitsandbytes

**Solution:**
```bash
# Install pre-built wheel for Windows/Linux
pip install bitsandbytes --prefer-binary
```

---

## Performance Comparison

### Before Fine-Tuning (Base Llama-3)
```
User: "Explain quantum consciousness"
Response: "Quantum consciousness refers to theories that consciousness 
involves quantum mechanical phenomena. Some scientists propose that 
microtubules in neurons may support quantum effects..."
```
❌ Generic, doesn't understand Codette concepts

### After Fine-Tuning
```
User: "Explain quantum consciousness"
Response: "Quantum consciousness in Codette emerges from multi-dimensional 
thought propagation through the QuantumSpiderweb. The system maintains 
coherence across Ψ (thought), Φ (emotion), λ (space), τ (time), and 
χ (speed) dimensions..."
```
✅ Understands Codette architecture + quantum mathematics

---

## Next Steps

1. **Fine-tune** with this guide
2. **Test** the resulting model extensively
3. **Deploy** via Ollama for inference
4. **Gather feedback** and iterate
5. **Re-train** with user feedback data

---

## Resources

- **Unsloth Docs**: https://github.com/unslothai/unsloth
- **Llama-3 Model Card**: https://huggingface.co/meta-llama/Llama-3-8b
- **Ollama Docs**: https://ollama.ai
- **LoRA Paper**: https://arxiv.org/abs/2106.09685

---

**Questions?** Check your specific error in the Troubleshooting section, or examine the training logs in `./logs/`.
