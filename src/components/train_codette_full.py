"""
Complete Codette Model Training Script
Combines custom transformer + training data + training loop
"""

import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from custom_transformer import create_codette_model, CustomTransformer
from training_data import CodettTrainingDataset, SimpleTokenizer, create_training_dataset
from train_codette_model import CodettTrainer, TrainingConfig, train_codette_model
import torch


def main():
    """Complete training pipeline."""
    
    print("=" * 80)
    print("CODETTE MODEL TRAINING PIPELINE")
    print("=" * 80)
    
    # Configuration
    model_size = 'medium'  # 'small', 'medium', or 'large'
    num_training_samples = 5000
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    print(f"\nConfiguration:")
    print(f"  Model size: {model_size}")
    print(f"  Training samples: {num_training_samples}")
    print(f"  Device: {device}")
    print(f"  CUDA available: {torch.cuda.is_available()}")
    
    # Step 1: Create training dataset
    print("\n" + "=" * 80)
    print("STEP 1: GENERATING TRAINING DATA")
    print("=" * 80)
    
    dataset_gen = CodettTrainingDataset()
    train_data = dataset_gen.generate_dataset(num_training_samples)
    
    # Split into train/eval (90/10)
    split_idx = int(len(train_data) * 0.9)
    train_texts = train_data[:split_idx]
    eval_texts = train_data[split_idx:]
    
    print(f"Generated {len(train_data)} samples")
    print(f"  Training: {len(train_texts)} samples")
    print(f"  Evaluation: {len(eval_texts)} samples")
    print(f"  Distribution:")
    print(f"    - Perspectives: 30% (reasoning from multiple viewpoints)")
    print(f"    - Tool use: 25% (practical tool execution patterns)")
    print(f"    - Consciousness: 25% (philosophical reasoning)")
    print(f"    - Mixed: 20% (integrated multi-modal reasoning)")
    
    # Step 2: Initialize tokenizer
    print("\n" + "=" * 80)
    print("STEP 2: INITIALIZING TOKENIZER")
    print("=" * 80)
    
    tokenizer = SimpleTokenizer(vocab_size=32768)
    print(f"Tokenizer initialized")
    print(f"  Vocabulary size: {tokenizer.vocab_size:,}")
    print(f"  Special tokens: 7")
    print(f"  Common words: ~20")
    
    # Step 3: Create model
    print("\n" + "=" * 80)
    print("STEP 3: CREATING MODEL")
    print("=" * 80)
    
    model = create_codette_model(model_size)
    print(f"Model created: {model_size} variant")
    print(f"  Parameters: {model.num_parameters:,}")
    print(f"  Model size (fp32): {model.get_model_size_mb():.2f} MB")
    print(f"  Config:")
    print(f"    - Hidden size: {model.config.hidden_size}")
    print(f"    - Attention heads: {model.config.num_attention_heads}")
    print(f"    - Layers: {model.config.num_hidden_layers}")
    print(f"    - Max sequence: {model.config.max_sequence_length}")
    
    # Step 4: Train model
    print("\n" + "=" * 80)
    print("STEP 4: TRAINING MODEL")
    print("=" * 80)
    print(f"Starting training on {device.upper()}...")
    print(f"Expected duration: 5-30 minutes depending on device")
    print()
    
    try:
        metrics = train_codette_model(
            model=model,
            tokenizer=tokenizer,
            train_texts=train_texts,
            eval_texts=eval_texts,
            checkpoint_dir='checkpoints',
            device=device
        )
        
        # Step 5: Report results
        print("\n" + "=" * 80)
        print("STEP 5: TRAINING COMPLETE")
        print("=" * 80)
        
        print(f"\nFinal Metrics:")
        print(f"  Final training loss: {metrics['final_loss']:.4f}")
        print(f"  Best evaluation loss: {metrics['best_eval_loss']:.4f}")
        print(f"  Improvement: {((metrics['final_loss'] - metrics['best_eval_loss']) / metrics['final_loss'] * 100):.1f}%")
        
        print(f"\nModel saved to:")
        print(f"  - Checkpoints: ./checkpoints/")
        print(f"  - Best model: ./checkpoints/model_best.pt")
        print(f"  - Final model: ./checkpoints/model_final.pt")
        
        print(f"\nNext steps:")
        print(f"  1. Evaluate model on test set")
        print(f"  2. Convert to GGUF format for Ollama")
        print(f"  3. Deploy to Ollama server")
        print(f"  4. Test with MultimodalCodette tool calling")
        
        return True
        
    except Exception as e:
        print(f"\nError during training: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
