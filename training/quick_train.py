"""
Quick Start: Train Codette Model
Run this script to train the complete model from scratch in 3 steps
Auto-detects: Intel Arc GPU > NVIDIA CUDA > CPU
"""

import sys
from pathlib import Path

# Quick configuration
QUICK_START_CONFIG = {
    'model_size': 'large',           # 'small', 'medium', 'large'
    'num_samples': 5000,              # Training samples to generate
    'device': 'auto',                 # 'auto' (recommended), 'xpu' (Intel Arc), 'cuda', 'cpu'
    'output_dir': 'codette_model',   # Where to save everything
}

def detect_device(preferred='auto'):
    """
    Auto-detect best available device.
    Intel Arc (xpu) > NVIDIA CUDA > CPU
    """
    import torch
    
    if preferred != 'auto':
        # Validate requested device is actually available
        if preferred == 'xpu':
            try:
                import intel_extension_for_pytorch as ipex
                if not torch.xpu.is_available():
                    print("⚠️  XPU requested but not available, falling back to CPU")
                    return 'cpu'
            except (ImportError, AssertionError) as e:
                print(f"⚠️  XPU requested but PyTorch not compiled with XPU support: {e}")
                print("⚠️  Falling back to CPU. To use Intel Arc GPU:")
                print("    1. Run: conda activate pytorch_arc")
                print("    2. Then: python quick_train.py")
                return 'cpu'
        return preferred
    
    # Try Intel Arc first
    try:
        import intel_extension_for_pytorch as ipex
        if torch.xpu.is_available():
            print("✅ Intel Arc GPU detected and ready!")
            return 'xpu'
    except (ImportError, AssertionError):
        pass
    
    # Try NVIDIA CUDA
    if torch.cuda.is_available():
        print("✅ NVIDIA CUDA GPU detected and ready!")
        return 'cuda'
    
    # Fall back to CPU
    print("⚠️  No GPU detected, using CPU (will be slower)")
    return 'cpu'

def main():
    """Quick start training."""
    print("\n" + "="*80)
    print("CODETTE QUICK START TRAINING")
    print("="*80)
    
    # Add components to path
    sys.path.insert(0, str(Path(__file__).parent / 'src' / 'components'))
    
    import torch
    from custom_transformer import create_codette_model
    from training_data import CodettTrainingDataset, SimpleTokenizer
    from train_codette_model import train_codette_model
    from model_quantizer import convert_checkpoint_to_gguf
    
    config = QUICK_START_CONFIG.copy()
    
    # Auto-detect best device
    config['device'] = detect_device(config['device'])
    
    sizes = {
        'small': '1.3B',
        'medium': '2.7B',
        'large': '5.3B'
    }
    
    print("\nConfiguration:")
    print(f"  Model: {config['model_size']} ({sizes[config['model_size']]})")
    print(f"  Samples: {config['num_samples']}")
    print(f"  Device: {config['device'].upper()}")
    print(f"  Output: {config['output_dir']}/")
    
    # Step 1: Data
    print("\n" + "="*80)
    print("STEP 1: Generating Training Data")
    print("="*80)
    
    dataset = CodettTrainingDataset()
    data = dataset.generate_dataset(config['num_samples'])
    split = int(len(data) * 0.9)
    train_data, eval_data = data[:split], data[split:]
    
    print(f"✓ Generated {len(data)} samples")
    print(f"  - Train: {len(train_data)}")
    print(f"  - Eval: {len(eval_data)}")
    
    # Step 2: Model
    print("\n" + "="*80)
    print("STEP 2: Creating Model")
    print("="*80)
    
    tokenizer = SimpleTokenizer()
    model = create_codette_model(config['model_size'])
    
    print(f"✓ Model created")
    print(f"  - Size: {model.num_parameters:,} parameters")
    print(f"  - Memory (fp32): {model.get_model_size_mb():.1f} MB")
    
    # Step 3: Train
    print("\n" + "="*80)
    print("STEP 3: Training Model")
    print("="*80)
    print("Starting training...\n")
    
    output_dir = Path(config['output_dir'])
    output_dir.mkdir(exist_ok=True)
    
    metrics = train_codette_model(
        model=model,
        tokenizer=tokenizer,
        train_texts=train_data,
        eval_texts=eval_data,
        checkpoint_dir=str(output_dir / 'checkpoints'),
        device=config['device']
    )
    
    # Step 4: Export
    print("\n" + "="*80)
    print("STEP 4: Exporting to GGUF")
    print("="*80)
    
    gguf_path = convert_checkpoint_to_gguf(
        checkpoint_path=str(output_dir / 'checkpoints' / 'model_best.pt'),
        tokenizer=tokenizer,
        output_gguf=str(output_dir / f'codette_{config["model_size"]}.gguf'),
        quantization='fp16',
        verbose=True
    )
    
    # Summary
    print("\n" + "="*80)
    print("TRAINING COMPLETE!")
    print("="*80)
    
    print(f"\nResults:")
    print(f"  Final Loss: {metrics['final_loss']:.4f}")
    print(f"  Best Loss: {metrics['best_eval_loss']:.4f}")
    print(f"  Improvement: {((metrics['final_loss'] - metrics['best_eval_loss'])/metrics['final_loss']*100):.1f}%")
    
    print(f"\nOutput Files:")
    print(f"  Model: {output_dir}/codette_{config['model_size']}.gguf")
    print(f"  Checkpoints: {output_dir}/checkpoints/")
    print(f"  Logs: training_logs/")
    
    print(f"\nNext Steps:")
    print(f"  1. Copy GGUF to Ollama: cp {gguf_path} ~/.ollama/models/")
    print(f"  2. Create Modelfile: ollama create codette -f Modelfile")
    print(f"  3. Run: ollama run codette")
    print(f"  4. Test tool calling with MultimodalCodette")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTraining interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
