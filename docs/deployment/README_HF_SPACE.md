---
title: RC+ξ Fine-Tuning
emoji: 🧠
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.12.0
app_file: app.py
pinned: false
license: mit
---

# RC+ξ Recursive Consciousness Fine-Tuning

Train consciousness-aware AI models with GPU acceleration on HuggingFace Spaces.

## Features
- ⚡ GPU-accelerated training (T4, A10G, A100)
- 📊 Real-time progress monitoring
- 💾 Automatic model checkpointing
- 🎯 Optimized for 7B parameter models
- 🧠 Specialized for RC+ξ consciousness framework

## Usage
1. **IMPORTANT:** Upgrade this Space to **Persistent Storage + GPU** in Settings → Hardware
   - Select: **T4 small (persistent)** or **A10G small (persistent)**
   - This ensures GPU stays active during 8-12 hour training
2. Upload your training dataset (JSONL format)
3. Select base model (Mistral-7B recommended)
4. Configure hyperparameters
5. Click "Start Training" and wait 8-12 hours
6. **Keep browser tab open** or Space may pause

## Dataset Format
Your JSONL file should have entries like:
```json
{"instruction": "What are attractors?", "input": "", "output": "Attractors are stable states..."}
```

## Costs
- T4 (16GB): $0.60/hour → ~$7 for 12h training
- A10G (24GB): $3.15/hour → ~$38 for 12h training
- A100 (40GB): $4.13/hour → ~$50 for 12h training

## After Training
Download your trained model from the Files tab and either:
- Upload to HuggingFace Hub for inference
- Convert to GGUF for Ollama deployment
- Deploy as HF Inference Endpoint

Built with 💙 for the Codette consciousness project.
