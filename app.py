import warnings
warnings.filterwarnings('ignore', category=FutureWarning, module='huggingface_hub')

# Handle OpenMP threading issues
import os
os.environ['OMP_NUM_THREADS'] = '1'

"""
HuggingFace Spaces Training Interface for RC+ξ Fine-Tuning
Supports GPU-accelerated training with progress monitoring
"""
import gradio as gr
import spaces  # HuggingFace Spaces GPU support
import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import load_dataset

# Try to import LoRA, but make it optional
try:
    from peft import LoraConfig, get_peft_model
    LORA_AVAILABLE = True
except ImportError:
    LORA_AVAILABLE = False

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
    max_length: int
):
    """Train RC+ξ model - wrapper function"""
    
    # Extract file path from Gradio file object
    dataset_path = dataset_file.name if hasattr(dataset_file, 'name') else dataset_file
    
    # Call the GPU-decorated training function
    yield from train_model_gpu(model_name, dataset_path, num_epochs, batch_size, learning_rate, max_length)

@spaces.GPU(duration=14400)  # 4 hours GPU reservation (enough for 1-2 epochs on 7B model)
def train_model_gpu(
    model_name: str,
    dataset_path: str,
    num_epochs: int,
    batch_size: int,
    learning_rate: float,
    max_length: int
):
    """Train RC+ξ model - GPU execution"""
    
    yield f"🚀 Starting training at {datetime.now().strftime('%H:%M:%S')}\n"
    yield f"📊 GPU Status: {check_gpu()}\n"
    
    try:
        # Load dataset
        yield f"\n📁 Loading dataset from {dataset_path}...\n"
        
        try:
            dataset = load_dataset('json', data_files=dataset_path, split='train')
            yield f"✅ Loaded {len(dataset)} examples\n"
        except Exception as e:
            yield f"\n❌ Failed to load dataset: {str(e)}\n"
            yield f"💡 Make sure your JSONL file has this format:\n"
            yield f'{{\n  "instruction": "...",\n  "input": "...",\n  "output": "..."\n}}\n'
            return
        
        # Validate dataset structure
        if len(dataset) == 0:
            yield f"\n❌ Dataset is empty!\n"
            return
        
        first_example = dataset[0]
        yield f"📊 Dataset fields found: {list(first_example.keys())}\n"
        yield f"📝 Sample row 1: {dict(list(first_example.items())[:3])}\n"
        
        # Check for required fields with flexible matching
        required_fields = ["instruction", "input", "output"]
        missing_fields = [f for f in required_fields if f not in first_example]
        
        if missing_fields:
            yield f"\n⚠️ Expected fields not found: {missing_fields}\n"
            yield f"💡 Common field name alternatives:\n"
            yield f"   • 'instruction' could be: 'prompt', 'question', 'task'\n"
            yield f"   • 'input' could be: 'context', 'example', 'text'\n"
            yield f"   • 'output' could be: 'response', 'answer', 'completion'\n"
            yield f"\n❌ Cannot proceed without: {missing_fields}\n"
            yield f"✅ Please upload JSONL with: instruction, input, output\n\n"
            yield f"📋 Sample JSONL format:\n"
            yield f'{{"instruction": "Q: What is AI?", "input": "", "output": "AI is artificial intelligence..."}}\n'
            yield f'{{"instruction": "Summarize", "input": "Long text...", "output": "Summary..."}}\n'
            return
        
        yield f"✅ Dataset structure valid\n"
        
        # Load model and tokenizer
        yield f"\n🤖 Loading model: {model_name}...\n"
        
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        
        # Try loading with device_map, fall back to manual device placement
        try:
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto",
                trust_remote_code=True
            )
        except ValueError as e:
            # Fall back if device_map='auto' not supported
            if 'device_map' in str(e):
                yield f"⚠️ Model doesn't support device_map='auto', using manual placement\n"
                model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                    trust_remote_code=True
                )
                if torch.cuda.is_available():
                    model = model.to('cuda')
            else:
                raise
        
        # Enable gradient checkpointing to reduce memory usage
        if hasattr(model, 'gradient_checkpointing_enable'):
            model.gradient_checkpointing_enable()
        
        # Apply LoRA for memory-efficient training
        yield f"🎯 Applying LoRA (Low-Rank Adaptation) for efficient training...\n"
        
        if LORA_AVAILABLE:
            lora_config = LoraConfig(
                r=8,  # LoRA rank
                lora_alpha=16,  # LoRA alpha (scaling factor)
                target_modules=["q_proj", "v_proj", "k_proj", "out_proj"],  # Common attention modules
                lora_dropout=0.05,
                bias="none",
                task_type="CAUSAL_LM"
            )
            
            try:
                model = get_peft_model(model, lora_config)
                trainable = model.get_nb_trainable_parameters()
                total = model.get_nb_total_parameters()
                yield f"✅ LoRA applied: Only {trainable:,} trainable parameters (vs {total:,} total)\n"
            except Exception as e:
                yield f"⚠️ LoRA not applicable to this model, continuing without: {str(e)}\n"
        else:
            yield f"⚠️ PEFT library not available. Training without LoRA (full fine-tuning)\n"
            yield f"💡 Consider using smaller batch size or reduce epochs to save memory\n"
        
        # Enable flash attention 2 for faster, more memory-efficient attention
        if hasattr(model, 'enable_flash_attention_2'):
            try:
                model.enable_flash_attention_2()
                yield f"⚡ Flash Attention 2 enabled for memory efficiency\n"
            except:
                pass  # Flash attention not available, continue without it
        
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            model.config.pad_token_id = tokenizer.eos_token_id
        
        total_params = sum(p.numel() for p in model.parameters())/1e9
        yield f"✅ Model loaded: {total_params:.2f}B parameters\n"
        if LORA_AVAILABLE:
            yield f"💾 Memory optimization: Gradient checkpointing + LoRA + reduced precision enabled\n"
        else:
            yield f"💾 Memory optimization: Gradient checkpointing + reduced precision enabled\n"
        
        # Tokenize dataset
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
        
        try:
            tokenized_dataset = dataset.map(
                tokenize_function,
                batched=True,
                remove_columns=dataset.column_names
            )
            yield f"✅ Tokenized {len(tokenized_dataset)} examples\n"
        except Exception as e:
            yield f"\n❌ Tokenization failed: {str(e)}\n"
            yield f"\n📊 Dataset diagnostics:\n"
            yield f"   • Total examples: {len(dataset)}\n"
            yield f"   • Fields: {dataset.column_names}\n"
            yield f"   • First row keys: {list(dataset[0].keys())}\n"
            yield f"\n💡 Common issues:\n"
            yield f"   • Null/None values in instruction, input, or output\n"
            yield f"   • Non-string values (numbers, objects, arrays)\n"
            yield f"   • Invalid UTF-8 encoding\n"
            yield f"   • Empty strings in required fields\n"
            import traceback
            yield f"\n📋 Error details:\n{traceback.format_exc()}\n"
            return
        
        # Split dataset
        split = tokenized_dataset.train_test_split(test_size=0.1, seed=42)
        train_dataset = split["train"]
        eval_dataset = split["test"]
        
        yield f"📊 Train: {len(train_dataset)} | Eval: {len(eval_dataset)}\n"
        
        # Training arguments
        yield f"\n⚙️ Configuring training...\n"
        
        output_dir = f"./rc_xi_trained_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Auto-adjust batch size based on available GPU memory
        adjusted_batch_size = batch_size
        if torch.cuda.is_available():
            free_memory_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
            if free_memory_gb < 16:
                adjusted_batch_size = max(1, batch_size // 2)
                yield f"⚠️ GPU memory limited ({free_memory_gb:.1f}GB). Reducing batch size to {adjusted_batch_size}\n"
        
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=adjusted_batch_size,
            per_device_eval_batch_size=adjusted_batch_size,
            gradient_accumulation_steps=8,  # Increased for smaller batch sizes
            learning_rate=learning_rate,
            warmup_steps=100,
            logging_steps=1,  # Log every step for immediate feedback
            eval_steps=50,
            save_steps=100,
            eval_strategy="steps",
            save_strategy="steps",
            save_total_limit=2,
            fp16=torch.cuda.is_available(),
            report_to=[],
            load_best_model_at_end=True,
            max_grad_norm=1.0,  # Gradient clipping for stability
            optim="adamw_torch",  # Standard PyTorch Adam optimizer
        )
        
        yield f"✅ Training configured\n"
        yield f"   • Epochs: {num_epochs}\n"
        yield f"   • Batch size: {adjusted_batch_size}\n"
        yield f"   • Gradient accumulation: 8\n"
        yield f"   • Learning rate: {learning_rate}\n"
        yield f"   • Max length: {max_length}\n"
        yield f"   • FP16: {torch.cuda.is_available()}\n"
        yield f"   • Optimizer: adamw_torch\n"
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer,
            mlm=False
        )
        
        # Trainer with callbacks removed (using manual training for better progress streaming)
        yield f"\n🏋️ Initializing trainer...\n"
        
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            data_collator=data_collator,
        )
        
        yield f"✅ Trainer initialized. Starting training loop...\n"
        yield f"⏳ First step may take 30-60 seconds (loading data, first forward/backward pass)...\n\n"
        
        try:
            # Manual training loop with progress streaming
            from datetime import datetime as dt
            import time
            
            start_time = time.time()
            step = 0
            total_steps = len(train_dataset) // adjusted_batch_size * num_epochs
            
            for epoch in range(num_epochs):
                yield f"\n📅 EPOCH {epoch + 1}/{num_epochs}\n"
                yield f"{'='*50}\n"
                
                model.train()
                epoch_loss = 0
                steps_in_epoch = 0
                
                for batch_idx, batch in enumerate(trainer.get_train_dataloader()):
                    step += 1
                    steps_in_epoch += 1
                    
                    # Move batch to GPU
                    batch = {k: v.to(model.device) for k, v in batch.items()}
                    
                    # Forward pass
                    outputs = model(**batch)
                    loss = outputs.loss
                    
                    # Backward pass
                    loss.backward()
                    
                    # Gradient accumulation
                    if (steps_in_epoch % 8) == 0 or steps_in_epoch == len(trainer.get_train_dataloader()):
                        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                        trainer.optimizer.step()
                        trainer.optimizer.zero_grad()
                    
                    epoch_loss += loss.item()
                    
                    # Yield progress every step
                    elapsed = time.time() - start_time
                    speed = step / max(elapsed, 0.1)
                    avg_loss = epoch_loss / steps_in_epoch
                    
                    if steps_in_epoch % 1 == 0 or steps_in_epoch == 1:
                        remaining = (total_steps - step) / max(speed, 0.1)
                        yield (
                            f"Step {step}/{total_steps} | "
                            f"Loss: {avg_loss:.4f} | "
                            f"Speed: {speed:.1f} steps/s | "
                            f"ETA: {int(remaining//60)}m {int(remaining%60)}s\n"
                        )
                
                # Epoch summary
                avg_epoch_loss = epoch_loss / steps_in_epoch
                yield f"\n✅ Epoch {epoch + 1} complete - Avg Loss: {avg_epoch_loss:.4f}\n"
                
                # Evaluation
                if epoch % 1 == 0 and epoch > 0:  # Eval every epoch
                    yield f"📊 Running evaluation...\n"
                    model.eval()
                    eval_loss = 0
                    eval_steps = 0
                    
                    with torch.no_grad():
                        for eval_batch in trainer.get_eval_dataloader():
                            eval_batch = {k: v.to(model.device) for k, v in eval_batch.items()}
                            outputs = model(**eval_batch)
                            eval_loss += outputs.loss.item()
                            eval_steps += 1
                    
                    avg_eval_loss = eval_loss / eval_steps if eval_steps > 0 else 0
                    yield f"✅ Eval Loss: {avg_eval_loss:.4f}\n\n"
            
            # Training complete
            total_time = time.time() - start_time
            yield f"\n{'='*50}\n"
            yield f"🎉 TRAINING COMPLETE!\n"
            yield f"{'='*50}\n"
            yield f"⏱️ Total Time: {int(total_time//3600)}h {int((total_time%3600)//60)}m {int(total_time%60)}s\n"
            yield f"📊 Final Loss: {avg_epoch_loss:.4f}\n"
            
            train_result = type('obj', (object,), {
                'training_loss': avg_epoch_loss,
                'metrics': {'train_runtime': total_time}
            })()
        except Exception as e:
            error_msg = str(e).lower()
            yield f"\n❌ Training failed: {str(e)}\n"
            
            if 'out of memory' in error_msg or 'cuda' in error_msg:
                yield f"\n💾 CUDA out of memory. Clearing cache...\n"
                torch.cuda.empty_cache()
            
            import traceback
            yield f"\n📋 Full error:\n{traceback.format_exc()}\n"
            return
        
        yield f"\n💾 Saving model...\n"
        
        trainer.save_model(output_dir)
        tokenizer.save_pretrained(output_dir)
        
        yield f"✅ Model saved to {output_dir}\n"
        
        # Results
        yield f"\n" + "="*50 + "\n"
        yield f"🎉 TRAINING COMPLETE!\n"
        yield f"="*50 + "\n"
        yield f"📊 Training Loss: {train_result.training_loss:.4f}\n"
        yield f"⏱️ Training Time: {train_result.metrics['train_runtime']:.1f}s\n"
        yield f"💾 Model saved to: {output_dir}\n"
        yield f"\n✨ Your RC+ξ model is ready!\n"
        
    except RuntimeError as e:
        import traceback
        error_details = traceback.format_exc()
        error_msg = str(e).lower()
        
        # Check for specific OOM errors
        if 'out of memory' in error_msg or 'cuda' in error_msg or 'memory' in error_msg:
            yield f"\n❌ OUT OF MEMORY ERROR\n"
            yield f"\nTrying recovery strategies...\n"
            torch.cuda.empty_cache()
            yield f"\n💡 Solutions:\n"
            yield f"   1. ✅ Memory cleared. Try again with reduced settings:\n"
            yield f"      • Reduce 'Batch Size' to 1\n"
            yield f"      • Reduce 'Max Sequence Length' to 256\n"
            yield f"      • Reduce 'Training Epochs' to 1\n"
            yield f"   2. Upgrade to A10G GPU (24GB) in Settings → Hardware\n"
            yield f"   3. Try lighter models: 'gpt2' or 'microsoft/phi-2'\n"
            yield f"\n📋 Full error:\n{error_details}\n"
        else:
            yield f"\n❌ RUNTIME ERROR: {str(e)}\n"
            yield f"\n📋 Full traceback:\n{error_details}\n"
    except KeyError as e:
        import traceback
        yield f"\n❌ MISSING FIELD ERROR: {str(e)}\n"
        yield f"\n💡 Your dataset is missing a required field.\n"
        yield f"✅ Required fields: instruction, input, output\n"
        yield f"\n📋 Full traceback:\n{traceback.format_exc()}\n"
    except ValueError as e:
        import traceback
        yield f"\n❌ VALUE ERROR: {str(e)}\n"
        yield f"\n💡 Check that:\n"
        yield f"   • Dataset file is valid JSON/JSONL format\n"
        yield f"   • No empty or null values in fields\n"
        yield f"   • Text encoding is correct (UTF-8)\n"
        yield f"\n📋 Full traceback:\n{traceback.format_exc()}\n"
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        yield f"\n❌ UNEXPECTED ERROR: {str(e)}\n"
        yield f"\n📋 Full traceback:\n{error_details}\n"
        yield f"\n💡 Diagnostics:\n"
        yield f"   • Check dataset format (JSONL with instruction/input/output)\n"
        yield f"   • Try with gpt2 model (smallest, most stable)\n"
        yield f"   • Check HuggingFace Space logs for system errors\n"

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
                    "microsoft/phi-2",
                    "gpt2",
                    "mistralai/Mistral-7B-v0.1",
                    "meta-llama/Llama-2-7b-hf"
                ],
                value="microsoft/phi-2"
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
    demo.launch()  # Removed share=True for Spaces compatibility
