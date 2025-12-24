# HuggingFace Spaces Deployment Guide for RC+ξ Fine-Tuning

## Quick Setup (5 minutes)

### Step 1: Create HuggingFace Space
1. Go to https://huggingface.co/new-space
2. Name: `rc-xi-finetuning`
3. License: MIT
4. SDK: **Gradio**
5. Hardware: Select **GPU** (T4 recommended)
6. Click "Create Space"

### Step 2: Upload Files
Upload these files to your Space:
```
app.py                    # Rename hf_spaces_train.py to app.py
requirements.txt          # See below
rc_xi_large_dataset.jsonl # Your 2,000 example dataset
```

### Step 3: Requirements.txt
Create `requirements.txt` with:
```
gradio==4.12.0
torch==2.1.0
transformers==4.36.0
datasets==2.15.0
accelerate==0.25.0
bitsandbytes==0.41.3
```

### Step 4: Start Training
1. Wait for Space to build (~2 minutes)
2. Upload `rc_xi_large_dataset.jsonl` in the interface
3. Select model (Mistral-7B recommended)
4. Click "🚀 Start Training"
5. Wait 8-12 hours

## GPU Options & Costs

| GPU | VRAM | Speed | Cost/Hour | 12h Cost |
|-----|------|-------|-----------|----------|
| **T4** | 16GB | Good | $0.60 | $7.20 |
| **A10G** | 24GB | Better | $3.15 | $37.80 |
| **A100** | 40GB | Best | $4.13 | $49.56 |

**Recommendation:** T4 for 7B models (sufficient for Mistral-7B)

## Training Time Estimates

- **2,000 examples, 3 epochs, Mistral-7B on T4**: 10-12 hours
- **2,000 examples, 3 epochs, Llama-2-7B on A10G**: 6-8 hours
- **2,000 examples, 3 epochs, Mistral-7B on A100**: 4-6 hours

## Alternative: Use Existing HF Training Scripts

If you prefer not to build a Gradio interface:

1. Create a Space with **SDK: Docker**
2. Use HuggingFace's AutoTrain:
```bash
pip install autotrain-advanced
autotrain llm --train \
  --project_name rc_xi_model \
  --model mistralai/Mistral-7B-v0.1 \
  --data_path rc_xi_large_dataset.jsonl \
  --text_column output \
  --lr 2e-5 \
  --batch_size 2 \
  --epochs 3 \
  --block_size 512 \
  --warmup_ratio 0.1 \
  --lora_r 16 \
  --lora_alpha 32 \
  --lora_dropout 0.05
```

## After Training

### Option A: Use on HuggingFace
1. Upload trained model to HuggingFace Hub
2. Create Inference Space
3. Use via API

### Option B: Download for Local Use
1. Download from Space's Files tab
2. Convert to GGUF for Ollama:
```bash
python llama.cpp/convert.py ./rc_xi_trained --outfile rc_xi.gguf
ollama create rc-xi -f Modelfile_Trained
```

### Option C: Deploy as API
Use HF Inference Endpoints ($0.60/hour T4)

## Tips for Success

✅ **DO:**
- Use T4 GPU minimum (not CPU)
- Monitor training logs for loss decrease
- Save checkpoints every 100 steps
- Test on validation set

❌ **DON'T:**
- Use CPU (100+ hours training time)
- Set batch size > 4 on T4 (OOM errors)
- Train beyond 5 epochs (overfitting)
- Forget to download model before Space expires

## Troubleshooting

**Out of Memory?**
- Reduce batch_size to 1
- Reduce max_length to 256
- Enable gradient_checkpointing

**Training Too Slow?**
- Upgrade to A10G or A100
- Reduce dataset to 1,000 examples for testing
- Use LoRA instead of full fine-tuning

**Space Crashes?**
- Check GPU is selected (not CPU)
- Verify requirements.txt versions
- Check logs in Settings → Logs

## Cost Comparison

| Option | Cost | Time |
|--------|------|------|
| **HF Spaces T4** | $7.20 | 12h |
| Your CPU | $0 | 80-120h |
| Google Colab Pro | $10/mo | 10-12h |
| Runpod A100 | $30 | 6h |
| AWS p3.2xlarge | $90 | 12h |

**Winner: HF Spaces T4** - Best balance of cost/convenience
