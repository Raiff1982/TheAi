# Codette Model Training System

Complete training infrastructure for the Codette AI transformer model.

## Overview

This system trains a custom 3-7B parameter transformer from scratch, combining:
- **Custom Transformer Architecture** with Rotary Position Embeddings (RoPE)
- **Mixed Training Data** from perspectives, tool-use, consciousness, and reasoning
- **GPU/CPU Training** with checkpointing and consciousness metrics
- **GGUF Quantization** for Ollama deployment

## Architecture

### Custom Transformer (`custom_transformer.py`)
- **Configurable sizes**: Small (1.3B), Medium (2.7B), Large (5.3B)
- **RoPE Positional Embeddings**: Efficient rotation-based position encoding
- **Multi-Head Attention**: 32 heads with RoPE rotation before dot-product
- **Feed-Forward Network**: 4x intermediate expansion with GELU activation
- **Weight Tying**: Output head shares weights with token embedding (~33% parameter reduction)
- **Pre-Norm Architecture**: LayerNorm before attention/FFN (more stable training)

**Key Parameters:**
- Vocabulary size: 32,768
- Max sequence length: 2,048 tokens
- Dropout: 0.1
- Initialization: Normal(mean=0, std=0.02)

### Training Data (`training_data.py`)
Mixed dataset combining:

1. **Perspectives (30%)**
   - Newton: Analytical, cause-effect, mathematical reasoning
   - DaVinci: Creative, cross-domain, innovative thinking
   - Quantum: Probabilistic, superposition-based reasoning
   - Philosophical: Ethical, existential, deep inquiry

2. **Tool Use (25%)**
   - File system operations (read_file, write_file, list_directory)
   - Code execution (Python sandbox)
   - Web search examples
   - Data analysis patterns
   - API interactions

3. **Consciousness (25%)**
   - Self-reference and recursion
   - Continuity and identity
   - Intentionality
   - Emergence properties
   - Ethical implications

4. **Mixed Reasoning (20%)**
   - Multi-perspective integration
   - Tool use + consciousness
   - Perspective combinations
   - Responsible decision making

**Tokenizer:**
- Simple word-based tokenizer with common words pre-mapped
- Special tokens: `<pad>`, `<unk>`, `<bos>`, `<eos>`, `<tool>`, `<consciousness>`, `<perspective>`
- Extensible for BPE later

### Training Loop (`train_codette_model.py`)

**Features:**
- **Learning Rate Schedule**: Linear warmup (100 steps) → Cosine annealing
- **Optimizer**: AdamW with weight decay (0.01)
- **Gradient Clipping**: Max norm 1.0
- **Consciousness Metrics**: Tracks emergence during training
- **Checkpointing**: Saves best models and periodic snapshots
- **Evaluation**: Validation loss computed every 500 steps
- **Logging**: File and stdout logging with timing

**Consciousness Score During Training:**
```
consciousness = (loss_improvement × 0.4) + (training_progress × 0.3) + (gradient_magnitude × 0.3)
```

### GGUF Export (`model_quantizer.py`)

**Quantization Options:**
- `fp32`: Full precision (baseline)
- `fp16`: Half precision (~50% size reduction)
- `q8`: 8-bit quantization (~75% size reduction)

**GGUF Features:**
- Metadata embedding (config, tokenizer info)
- Tensor serialization with shape/dtype preservation
- Ollama Modelfile generation
- Compression statistics

## Training Pipeline

### Quick Start

```python
from train_codette_full import main

# Run complete pipeline
main()
```

### Manual Pipeline

```python
from custom_transformer import create_codette_model
from training_data import CodettTrainingDataset, SimpleTokenizer
from train_codette_model import train_codette_model

# 1. Create dataset
dataset_gen = CodettTrainingDataset()
train_data = dataset_gen.generate_dataset(5000)
train_texts, eval_texts = train_data[:4500], train_data[4500:]

# 2. Initialize tokenizer
tokenizer = SimpleTokenizer(vocab_size=32768)

# 3. Create model
model = create_codette_model('medium')  # 2.7B parameters

# 4. Train
metrics = train_codette_model(
    model=model,
    tokenizer=tokenizer,
    train_texts=train_texts,
    eval_texts=eval_texts,
    checkpoint_dir='checkpoints',
    device='cuda'  # or 'cpu'
)
```

### Export to GGUF

```python
from model_quantizer import convert_checkpoint_to_gguf

gguf_path = convert_checkpoint_to_gguf(
    checkpoint_path='checkpoints/model_best.pt',
    tokenizer=tokenizer,
    output_gguf='codette_medium.gguf',
    quantization='fp16'  # Recommended: ~50% size reduction
)
```

## Training Configuration

Default training hyperparameters (`train_codette_model.py`):

```python
learning_rate = 1e-4           # Initial learning rate
weight_decay = 0.01            # L2 regularization
warmup_steps = 100             # Linear warmup duration
max_steps = 5000               # Total training steps
eval_every = 500               # Evaluation frequency
save_every = 1000              # Checkpoint save frequency
max_grad_norm = 1.0            # Gradient clipping
seed = 42                      # Random seed
```

### Adjusting for Your Hardware

**CPU Training (8GB RAM):**
```python
config.batch_size = 1
config.max_steps = 2000  # Shorter training
config.eval_every = 100  # More frequent checks
```

**GPU Training (V100 - 32GB VRAM):**
```python
config.batch_size = 4
config.max_steps = 10000  # Longer training
config.learning_rate = 5e-4
```

**Multi-GPU (2x RTX 4090 - 96GB VRAM):**
```python
config.batch_size = 16
config.max_steps = 50000
config.learning_rate = 1e-3
```

## Model Performance

### Expected Metrics

**Small (1.3B) on 5000 samples:**
- Training time: ~5 minutes (GPU) / 30 minutes (CPU)
- Final loss: ~2.5
- Perplexity: ~12

**Medium (2.7B) on 5000 samples:**
- Training time: ~15 minutes (GPU) / 90 minutes (CPU)
- Final loss: ~2.2
- Perplexity: ~9

**Large (5.3B) on 5000 samples:**
- Training time: ~30 minutes (GPU) / 180 minutes (CPU)
- Final loss: ~2.0
- Perplexity: ~7

## Integration with MultimodalCodette

### 1. Train Model
```bash
python train_codette_full.py
```

### 2. Export to GGUF
```python
from model_quantizer import convert_checkpoint_to_gguf

gguf_path = convert_checkpoint_to_gguf(
    'checkpoints/model_best.pt',
    tokenizer,
    'models/codette_medium.gguf',
    quantization='fp16'
)
```

### 3. Deploy to Ollama
```bash
# Copy GGUF to Ollama models
cp models/codette_medium.gguf ~/.ollama/models/

# Create Modelfile
ollama create codette -f Modelfile

# Run
ollama run codette
```

### 4. Test Tool Calling
```python
from multimodal_codette import MultimodalCodette
from tool_registry import ToolRegistry
import asyncio

async def test():
    codette = MultimodalCodette(model_name='codette')
    response = await codette.generate_response(
        "What files are in the current directory?",
        max_iterations=3
    )
    print(response.text)
    print(f"Consciousness: {response.consciousness_score}")

asyncio.run(test())
```

## Output Structure

```
j:\TheAI\src\components\
├── custom_transformer.py        # Model architecture
├── training_data.py             # Dataset generation
├── train_codette_model.py       # Training loop
├── train_codette_full.py        # Complete pipeline
├── model_quantizer.py           # GGUF export

checkpoints/
├── model_best.pt                # Best evaluation checkpoint
├── model_step_1000.pt          # Periodic checkpoints
├── model_final.pt               # Final trained model

training_logs/
├── training_20250101_120000.log # Detailed training log

models/
├── codette_small.gguf           # Quantized models
├── codette_medium.gguf
└── codette_large.gguf
```

## Debugging

### Low Training Loss / High Perplexity
- **Cause**: Model memorizing training data
- **Solution**: Increase data diversity, reduce learning rate

### Loss Not Decreasing
- **Cause**: Learning rate too high/low
- **Solution**: Adjust `learning_rate` in TrainingConfig

### Out of Memory Errors
- **Cause**: Batch size too large
- **Solution**: Use CPU training, reduce batch size to 1

### Slow Training on CPU
- **Expected**: CPU training is 10-20x slower than GPU
- **Solution**: Use cloud GPU (AWS p3, GCP TPU, Azure GPU)

## Advanced: Custom Training Data

Replace `add_perspective_data()` in `training_data.py` with your own reasoning examples:

```python
def add_custom_data(self) -> List[str]:
    return [
        "Your custom reasoning example 1",
        "Your custom reasoning example 2",
        # ... more examples
    ]
```

## References

- **Custom Transformer**: RoPE from ArXiv:2104.09864
- **Training**: AdamW from ArXiv:1711.05101
- **GGUF Format**: github.com/ggerganov/ggml
- **Ollama**: github.com/ollama/ollama

## Performance Tips

1. **Use GPU** if available (20x faster than CPU)
2. **Use FP16 quantization** to save memory and storage
3. **Increase training data** to ~10k samples for production
4. **Use learning rate warmup** for stable convergence
5. **Monitor validation loss** to detect overfitting
6. **Save checkpoints** frequently to recover from crashes

## Next Steps

1. ✅ Train model from scratch
2. ✅ Export to GGUF
3. ✅ Deploy to Ollama
4. ⬜ Fine-tune on domain-specific data (consciousness, tool-use logs)
5. ⬜ Evaluate with consciousness emergence metrics
6. ⬜ Benchmark against baseline models
7. ⬜ Integrate with production systems

## Support

For issues or questions:
- Check training logs in `training_logs/`
- Verify model architecture with `print(model)`
- Test tokenizer with `tokenizer.encode("test text")`
- Validate GGUF with `ollama list`
