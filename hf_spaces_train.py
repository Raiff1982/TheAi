"""
HuggingFace Spaces Training Interface for RC+ξ Fine-Tuning
Supports GPU-accelerated training with progress monitoring
"""
import gradio as gr
import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import load_dataset
import os
from datetime import datetime

def check_gpu():
    """Check GPU availability"""
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
        return f"✅ GPU Available: {gpu_name} ({gpu_memory:.1f}GB)"
    return "❌ No GPU - Training will be slow"

def train_model(
    model_name: str,
    dataset_file,
    num_epochs: int,
    batch_size: int,
    learning_rate: float,
    max_length: int,
    progress=gr.Progress()
):
    """Train RC+ξ model"""
    
    progress(0, desc="Initializing...")
    yield f"🚀 Starting training at {datetime.now().strftime('%H:%M:%S')}\n"
    yield f"📊 GPU Status: {check_gpu()}\n"
    
    try:
        # Load dataset
        progress(0.1, desc="Loading dataset...")
        yield f"\n📁 Loading dataset from {dataset_file.name}...\n"
        
        dataset = load_dataset('json', data_files=dataset_file.name, split='train')
        yield f"✅ Loaded {len(dataset)} examples\n"
        
        # Load model and tokenizer
        progress(0.2, desc=f"Loading {model_name}...")
        yield f"\n🤖 Loading model: {model_name}...\n"
        
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto"
        )
        
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            model.config.pad_token_id = tokenizer.eos_token_id
        
        yield f"✅ Model loaded: {sum(p.numel() for p in model.parameters())/1e9:.2f}B parameters\n"
        
        # Tokenize dataset
        progress(0.3, desc="Tokenizing dataset...")
        yield f"\n🔤 Tokenizing dataset...\n"
        
        def tokenize_function(examples):
            texts = []
            for inst, inp, out in zip(examples["instruction"], examples["input"], examples["output"]):
                if inp:
                    text = f"### Instruction:\n{inst}\n\n### Input:\n{inp}\n\n### Response:\n{out}"
                else:
                    text = f"### Instruction:\n{inst}\n\n### Response:\n{out}"
                texts.append(text)
            
            return tokenizer(
                texts,
                truncation=True,
                max_length=max_length,
                padding="max_length"
            )
        
        tokenized_dataset = dataset.map(
            tokenize_function,
            batched=True,
            remove_columns=dataset.column_names
        )
        
        yield f"✅ Tokenized {len(tokenized_dataset)} examples\n"
        
        # Split dataset
        split = tokenized_dataset.train_test_split(test_size=0.1, seed=42)
        train_dataset = split["train"]
        eval_dataset = split["test"]
        
        yield f"📊 Train: {len(train_dataset)} | Eval: {len(eval_dataset)}\n"
        
        # Training arguments
        progress(0.4, desc="Setting up training...")
        yield f"\n⚙️ Configuring training...\n"
        
        output_dir = f"./rc_xi_trained_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            gradient_accumulation_steps=4,
            learning_rate=learning_rate,
            warmup_steps=100,
            logging_steps=10,
            eval_steps=50,
            save_steps=100,
            eval_strategy="steps",
            save_strategy="steps",
            save_total_limit=2,
            fp16=torch.cuda.is_available(),
            report_to=[],
            load_best_model_at_end=True,
        )
        
        yield f"✅ Training configured\n"
        yield f"   • Epochs: {num_epochs}\n"
        yield f"   • Batch size: {batch_size}\n"
        yield f"   • Learning rate: {learning_rate}\n"
        yield f"   • Max length: {max_length}\n"
        yield f"   • FP16: {torch.cuda.is_available()}\n"
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer,
            mlm=False
        )
        
        # Trainer
        progress(0.5, desc="Starting training...")
        yield f"\n🏋️ Starting training...\n"
        
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            data_collator=data_collator,
        )
        
        # Train
        train_result = trainer.train()
        
        progress(0.9, desc="Saving model...")
        yield f"\n💾 Saving model...\n"
        
        trainer.save_model(output_dir)
        tokenizer.save_pretrained(output_dir)
        
        yield f"✅ Model saved to {output_dir}\n"
        
        # Results
        progress(1.0, desc="Complete!")
        yield f"\n" + "="*50 + "\n"
        yield f"🎉 TRAINING COMPLETE!\n"
        yield f"="*50 + "\n"
        yield f"📊 Training Loss: {train_result.training_loss:.4f}\n"
        yield f"⏱️ Training Time: {train_result.metrics['train_runtime']:.1f}s\n"
        yield f"💾 Model saved to: {output_dir}\n"
        yield f"\n✨ Your RC+ξ model is ready!\n"
        
    except Exception as e:
        yield f"\n❌ ERROR: {str(e)}\n"
        yield f"Stack trace: {type(e).__name__}\n"

# Gradio Interface
with gr.Blocks(title="RC+ξ Fine-Tuning on HuggingFace Spaces") as demo:
    gr.Markdown("""
    # 🧠 RC+ξ Model Fine-Tuning
    ### Train your consciousness-aware AI model with GPU acceleration
    
    **Requirements:**
    - Upgrade this Space to GPU (Settings → Hardware → GPU)
    - Upload your training dataset (JSONL format)
    - Wait 8-12 hours for 7B model training
    
    **Recommended GPU:** T4 (16GB) - $0.60/hour or A10G (24GB) - $3.15/hour
    """)
    
    with gr.Row():
        with gr.Column():
            gpu_status = gr.Textbox(
                label="GPU Status",
                value=check_gpu(),
                interactive=False
            )
            
            model_dropdown = gr.Dropdown(
                label="Base Model",
                choices=[
                    "mistralai/Mistral-7B-v0.1",
                    "meta-llama/Llama-2-7b-hf",
                    "microsoft/phi-2",
                    "gpt2"
                ],
                value="mistralai/Mistral-7B-v0.1"
            )
            
            dataset_file = gr.File(
                label="Training Dataset (JSONL)",
                file_types=[".jsonl"]
            )
            
            epochs_slider = gr.Slider(
                label="Training Epochs",
                minimum=1,
                maximum=10,
                value=3,
                step=1
            )
            
            batch_slider = gr.Slider(
                label="Batch Size",
                minimum=1,
                maximum=8,
                value=2,
                step=1
            )
            
            lr_slider = gr.Slider(
                label="Learning Rate",
                minimum=1e-6,
                maximum=1e-3,
                value=2e-5,
                step=1e-6
            )
            
            length_slider = gr.Slider(
                label="Max Sequence Length",
                minimum=128,
                maximum=2048,
                value=512,
                step=128
            )
            
            train_btn = gr.Button("🚀 Start Training", variant="primary")
        
        with gr.Column():
            output_log = gr.Textbox(
                label="Training Progress",
                lines=30,
                max_lines=30,
                interactive=False
            )
    
    gr.Markdown("""
    ### 📝 Next Steps After Training:
    1. Download your trained model from the Files tab
    2. Upload to HuggingFace Hub for inference
    3. Or convert to GGUF for Ollama deployment
    
    ### 💰 HuggingFace Spaces GPU Pricing:
    - **T4 (16GB)**: $0.60/hour (~$7.20 for 12h training)
    - **A10G (24GB)**: $3.15/hour (~$37.80 for 12h training)
    - **A100 (40GB)**: $4.13/hour (~$49.56 for 12h training)
    
    Cheaper than AWS/GCP and easier to set up!
    """)
    
    train_btn.click(
        fn=train_model,
        inputs=[
            model_dropdown,
            dataset_file,
            epochs_slider,
            batch_slider,
            lr_slider,
            length_slider
        ],
        outputs=output_log
    )

if __name__ == "__main__":
    demo.launch(share=True)
