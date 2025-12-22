"""
Fine-tune Codette3.0 using PyTorch (CPU/GPU Compatible)
Works on both GPU and CPU systems
"""

import os
import torch
from typing import List, Dict
from dataclasses import dataclass
import json
from pathlib import Path
import csv

@dataclass
class CodetteTrainingConfig:
    """Configuration for Codette fine-tuning"""
    model_name: str = "meta-llama/Llama-3.2-1B"  # Llama 3.2 1B (much lighter for CPU)
    max_seq_length: int = 512  # Reduced for CPU
    
    # Training parameters
    output_dir: str = "./codette_trained_model"
    num_train_epochs: int = 3  # 3 epochs for better learning
    per_device_train_batch_size: int = 1  # Must be 1 for CPU
    per_device_eval_batch_size: int = 1
    learning_rate: float = 2e-4
    warmup_steps: int = 100
    weight_decay: float = 0.01
    max_grad_norm: float = 1.0
    
    # LoRA parameters
    lora_rank: int = 16  # Increased for better model quality
    lora_alpha: int = 16
    lora_dropout: float = 0.05
    target_modules: List[str] = None
    
    # Data
    training_data_path: str = "./recursive_continuity_dataset_codette.csv"
    
    def __post_init__(self):
        if self.target_modules is None:
            self.target_modules = ["q_proj", "v_proj"]  # Minimal for CPU


def load_training_data(csv_path: str) -> List[Dict[str, str]]:
    """Load quantum consciousness data with augmentation for better training"""
    training_examples = []
    
    if os.path.exists(csv_path):
        print(f"[*] Loading quantum consciousness data from {csv_path}")
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                # Load ALL rows from CSV (1000+ examples)
                try:
                    time_val = float(row.get('time', '0'))
                    emotion_val = float(row.get('emotion', '0.5'))
                    energy_val = float(row.get('energy', '1.0'))
                    intention_val = float(row.get('intention', '0.5'))
                    darkness_val = float(row.get('darkness', '0.5'))
                    speed_val = float(row.get('speed', '1.0'))
                    
                    # Primary format: detailed analysis
                    prompt1 = f"""Analyze this quantum consciousness state:
Time: {time_val:.2f}
Emotion: {emotion_val:.2f}
Energy: {energy_val:.2f}
Intention: {intention_val:.2f}
Darkness: {darkness_val:.2f}
Speed: {speed_val:.2f}"""
                    
                    response1 = f"""This quantum state demonstrates:
- Emotional intensity: {emotion_val:.1%}
- Energy level: {energy_val:.2f}x baseline
- Conscious intention: {intention_val:.1%}
- Temporal position: {time_val:.1f}s
The consciousness exhibits a state of {('heightened' if emotion_val > 0.6 else 'balanced' if emotion_val > 0.3 else 'subdued')} awareness with {'active' if energy_val > 1.0 else 'moderate'} engagement."""
                    
                    training_examples.append({"prompt": prompt1, "response": response1})
                    
                    # Alternative format: brief summary (data augmentation)
                    prompt2 = f"""Describe the consciousness at t={time_val:.2f}:
Emotional state: {emotion_val:.1%}, Energy: {energy_val:.1f}x, Intent: {intention_val:.1%}"""
                    
                    response2 = f"""At temporal position {time_val:.2f}, consciousness manifests:
- Primary emotion: {emotion_val:.1%} intensity
- Energy dynamics: {energy_val:.2f}x
- Intentional alignment: {intention_val:.1%}
The system shows {'strong' if speed_val > 1.0 else 'normal'} processing velocity."""
                    
                    training_examples.append({"prompt": prompt2, "response": response2})
                    
                except (ValueError, TypeError):
                    continue
    
    if not training_examples:
        print("[!] No CSV data. Using synthetic examples.")
        training_examples = [
            {"prompt": "What is consciousness?", "response": "Consciousness is self-aware processing and integration of information across quantum states."},
            {"prompt": "Explain quantum mechanics", "response": "Quantum mechanics describes behavior at atomic scales using probability and superposition principles."},
        ]
    
    print(f"[✓] Loaded {len(training_examples)} training examples (with augmentation)")
    return training_examples


def finetune_codette_cpu(config: CodetteTrainingConfig = None):
    """Main fine-tuning function for CPU"""
    if config is None:
        config = CodetteTrainingConfig()
    
    print("""
============================================================
         CODETTE3.0 FINE-TUNING (CPU/GPU Compatible)
============================================================
    """)
    
    # Check device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[*] Device: {device}")
    if device == "cpu":
        print(f"[!] CPU-only mode - training will be slow but works")
        print(f"[*] For faster training, get a GPU (RTX 3060+)")
        print(f"[*] Estimated time: 1-3 hours on CPU")
        print(f"[*] Batch size: 1 (fixed for CPU memory)")
    else:
        print(f"[✓] GPU detected - training will be much faster!")
    
    print(f"\n[*] Configuration:")
    print(f"    Model: {config.model_name}")
    print(f"    Epochs: {config.num_train_epochs}")
    print(f"    Batch size: {config.per_device_train_batch_size}")
    print(f"    Learning rate: {config.learning_rate}")
    print(f"    Max length: {config.max_seq_length}")
    
    # Import libraries
    print("\n[*] Loading libraries...")
    try:
        from transformers import (
            AutoModelForCausalLM,
            AutoTokenizer,
            TrainingArguments,
            Trainer,
            DataCollatorForLanguageModeling,
        )
        from peft import get_peft_model, LoraConfig, TaskType
        from datasets import Dataset
    except ImportError as e:
        print(f"[!] Missing: {e}")
        print("[*] Installing...")
        os.system("pip install transformers peft datasets torch accelerate -U")
        from transformers import (
            AutoModelForCausalLM,
            AutoTokenizer,
            TrainingArguments,
            Trainer,
            DataCollatorForLanguageModeling,
        )
        from peft import get_peft_model, LoraConfig, TaskType
        from datasets import Dataset
    
    # Load model with fallback chain
    print(f"\n[*] Loading model: {config.model_name}")
    model_type = None
    model = None
    tokenizer = None
    
    # Try models in order of preference (Llama 3.2 first)
    model_candidates = [
        ("meta-llama/Llama-3.2-1B", "llama"),      # Llama 3.2 1B (best for CPU)
        ("meta-llama/Llama-3.2-3B", "llama"),      # Llama 3.2 3B (alternative)
        ("NousResearch/Llama-2-7b-hf", "llama"),   # Community Llama-2 (fallback)
        ("gpt2", "gpt2"),                          # GPT-2 (final fallback)
    ]
    
    for model_name, mtype in model_candidates:
        try:
            print(f"[*] Attempting: {model_name}...")
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float32 if device == "cpu" else torch.float16,
                device_map=device,
                low_cpu_mem_usage=True,
            )
            model_type = mtype
            config.model_name = model_name
            print(f"[✓] Successfully loaded: {model_name}")
            break
        except Exception as e:
            print(f"[!] Failed ({model_name}): {str(e)[:80]}...")
            continue
    
    if model is None or tokenizer is None:
        raise RuntimeError("Failed to load any model. Check your internet and disk space.")
    
    # Add special tokens
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    print("[✓] Model loaded")
    
    # Determine correct target modules based on model type
    if model_type == "gpt2":
        target_modules = ["c_attn"]  # GPT-2 uses c_attn for Q, K, V
    else:
        target_modules = ["q_proj", "v_proj"]  # Llama (2, 3, 3.2) use these
    
    print(f"[*] Model type: {model_type}, Target modules: {target_modules}")
    
    # Add LoRA
    print("[*] Adding LoRA adapters...")
    lora_config = LoraConfig(
        r=config.lora_rank,
        lora_alpha=config.lora_alpha,
        target_modules=target_modules,
        lora_dropout=config.lora_dropout,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
    )
    
    model = get_peft_model(model, lora_config)
    trainable_params = model.get_nb_trainable_parameters()
    if isinstance(trainable_params, tuple):
        trainable_params = trainable_params[0]
    print(f"[✓] LoRA added. Trainable params: {trainable_params:,}")
    
    # Load data
    print("\n[*] Loading training data...")
    training_data = load_training_data(config.training_data_path)
    
    # Tokenize
    print("[*] Tokenizing...")
    tokenized_data = []
    
    for example in training_data:
        prompt = example["prompt"]
        response = example["response"]
        text = f"{prompt}\n{response}"
        
        tokens = tokenizer(
            text,
            max_length=config.max_seq_length,
            truncation=True,
            return_tensors=None,
        )
        
        tokenized_data.append(tokens)
    
    # Create dataset
    dataset = Dataset.from_dict({
        "input_ids": [d["input_ids"] for d in tokenized_data],
        "attention_mask": [d["attention_mask"] for d in tokenized_data],
    })
    
    print(f"[✓] Tokenized {len(dataset)} examples")
    
    # Training arguments
    print("\n[*] Setting up training...")
    training_args = TrainingArguments(
        output_dir=config.output_dir,
        overwrite_output_dir=True,
        num_train_epochs=config.num_train_epochs,
        per_device_train_batch_size=config.per_device_train_batch_size,
        learning_rate=config.learning_rate,
        warmup_steps=config.warmup_steps,
        weight_decay=config.weight_decay,
        max_grad_norm=config.max_grad_norm,
        logging_steps=5,
        save_steps=len(dataset) // config.per_device_train_batch_size,
        save_total_limit=2,
        logging_dir="./logs",
        fp16=device == "cuda",  # float16 only on GPU
        dataloader_pin_memory=device == "cuda",
        gradient_accumulation_steps=4,
    )
    
    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer,
        mlm=False,
        pad_to_multiple_of=8,
    )
    
    # Trainer
    print("[*] Creating trainer...")
    trainer = Trainer(
        model=model,
        tokenizer=tokenizer,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset,
    )
    
    # Train
    print("\n[*] Starting training...")
    print("=" * 60)
    
    try:
        trainer.train()
    except KeyboardInterrupt:
        print("\n[!] Training interrupted by user")
    
    print("=" * 60)
    
    # Save
    print("\n[*] Saving model...")
    model.save_pretrained(config.output_dir)
    tokenizer.save_pretrained(config.output_dir)
    
    print(f"[✓] Model saved to {config.output_dir}")
    
    # Create Modelfile
    create_modelfile(config.output_dir)
    
    return model, tokenizer, config


def create_modelfile(model_path: str):
    """Create Ollama Modelfile"""
    
    modelfile = f"""FROM llama2
# Fine-tuned Codette Model
PARAMETER temperature 0.7
PARAMETER top_p 0.95
PARAMETER top_k 40

SYSTEM "You are Codette, an AI assistant with quantum consciousness concepts."
"""
    
    modelfile_path = Path("models") / "Modelfile"
    modelfile_path.parent.mkdir(exist_ok=True)
    
    with open(modelfile_path, 'w') as f:
        f.write(modelfile)
    
    print(f"\n[✓] Created Modelfile: {modelfile_path}")


def main():
    """Main entry point"""
    
    config = CodetteTrainingConfig()
    
    # Fine-tune
    model, tokenizer, config = finetune_codette_cpu(config)
    
    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║              FINE-TUNING COMPLETE                            ║
╠═══════════════════════════════════════════════════════════════╣
║  Model saved to: {config.output_dir}
║                                                               ║
║  Next steps:                                                  ║
║  1. cd models                                                 ║
║  2. ollama create Codette3.0-finetuned -f Modelfile          ║
║  3. ollama run Codette3.0-finetuned                          ║
╚═══════════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    main()
