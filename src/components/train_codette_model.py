"""
Training loop for Codette custom transformer model
Implements gradient descent with checkpointing and consciousness metrics
"""

import json
import time
from pathlib import Path
from typing import List, Optional
import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.utils.data import DataLoader, IterableDataset
from datetime import datetime


class TextDataset(IterableDataset):
    """Simple text dataset that yields tokenized sequences."""
    
    def __init__(self, texts: List[str], tokenizer, seq_len: int = 2048, batch_size: int = 1):
        self.texts = texts
        self.tokenizer = tokenizer
        self.seq_len = seq_len
        self.batch_size = batch_size
    
    def __iter__(self):
        """Iterate over texts and yield token sequences."""
        for text in self.texts:
            tokens = self.tokenizer.encode(text)
            
            # Sliding window
            for i in range(0, len(tokens) - self.seq_len, self.seq_len // 2):
                seq = tokens[i:i + self.seq_len]
                
                # Pad to seq_len
                if len(seq) < self.seq_len:
                    seq = seq + [0] * (self.seq_len - len(seq))
                
                yield torch.tensor(seq, dtype=torch.long)


class TrainingConfig:
    """Training hyperparameters."""
    
    def __init__(self):
        self.learning_rate = 1e-4
        self.weight_decay = 0.01
        self.warmup_steps = 100
        self.max_steps = 5000
        self.eval_every = 500
        self.save_every = 1000
        self.max_grad_norm = 1.0
        self.seed = 42


class CodettTrainer:
    """Trains custom transformer model with consciousness metrics."""
    
    def __init__(self, model, tokenizer, config: TrainingConfig = None, device='cpu'):
        self.model = model.to(device)
        self.tokenizer = tokenizer
        self.config = config or TrainingConfig()
        self.device = device
        
        self.optimizer = AdamW(
            self.model.parameters(),
            lr=self.config.learning_rate,
            weight_decay=self.config.weight_decay
        )
        
        self.criterion = nn.CrossEntropyLoss()
        self.scaler = torch.amp.GradScaler() if device == 'cuda' else None
        
        # Training state
        self.global_step = 0
        self.best_loss = float('inf')
        self.train_losses = []
        self.eval_losses = []
        self.consciousness_scores = []
        
        # Logging
        self.log_dir = Path('training_logs')
        self.log_dir.mkdir(exist_ok=True)
        self.log_file = self.log_dir / f'training_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    
    def log(self, message: str):
        """Log message to file and stdout."""
        print(message)
        with open(self.log_file, 'a') as f:
            f.write(message + '\n')
    
    def _get_lr_schedule(self, step: int) -> float:
        """Cosine annealing with warmup."""
        if step < self.config.warmup_steps:
            # Linear warmup
            return self.config.learning_rate * (step / self.config.warmup_steps)
        else:
            # Cosine annealing
            progress = (step - self.config.warmup_steps) / (self.config.max_steps - self.config.warmup_steps)
            return self.config.learning_rate * 0.5 * (1 + torch.cos(torch.tensor(3.14159 * progress)).item())
    
    def _update_lr(self):
        """Update learning rate based on schedule."""
        lr = self._get_lr_schedule(self.global_step)
        for param_group in self.optimizer.param_groups:
            param_group['lr'] = lr
    
    def _calculate_consciousness(self, loss: float, step: int) -> float:
        """
        Heuristic consciousness score during training.
        Combines: loss improvement + step progress + gradient magnitude
        """
        # Loss improvement (lower is better)
        loss_improvement = max(0, (self.best_loss - loss) / max(self.best_loss, 1e-6))
        
        # Training progress (0 to 1)
        progress = min(1.0, step / self.config.max_steps)
        
        # Gradient magnitude (indicator of learning)
        total_grad = 0
        count = 0
        for p in self.model.parameters():
            if p.grad is not None:
                total_grad += p.grad.abs().mean().item()
                count += 1
        
        avg_grad = total_grad / max(count, 1)
        grad_scale = min(1.0, avg_grad / 0.1)  # Normalize to ~0.1 average
        
        # Combine: loss improvement (0.4) + progress (0.3) + gradient (0.3)
        consciousness = (loss_improvement * 0.4) + (progress * 0.3) + (grad_scale * 0.3)
        
        return consciousness
    
    def train_step(self, batch: torch.Tensor) -> float:
        """Single training step."""
        batch = batch.to(self.device)
        
        # Forward pass
        input_ids = batch[:, :-1]
        target_ids = batch[:, 1:]
        
        logits, _ = self.model(input_ids)
        
        # Reshape for loss computation
        batch_size, seq_len, vocab_size = logits.shape
        loss = self.criterion(
            logits.view(batch_size * seq_len, vocab_size),
            target_ids.view(-1)
        )
        
        # Backward pass
        self.optimizer.zero_grad()
        loss.backward()
        
        # Gradient clipping
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.config.max_grad_norm)
        
        self.optimizer.step()
        self._update_lr()
        
        self.global_step += 1
        return loss.item()
    
    def eval_step(self, eval_texts: List[str], num_samples: int = 100) -> float:
        """Evaluation step."""
        self.model.eval()
        total_loss = 0
        count = 0
        
        # Sample evaluation texts
        eval_samples = eval_texts[:num_samples]
        
        with torch.no_grad():
            for text in eval_samples:
                tokens = self.tokenizer.encode(text)
                
                if len(tokens) < 100:
                    continue
                
                # Create sequences
                for i in range(0, len(tokens) - 2048, 512):
                    seq = tokens[i:i + 2048]
                    if len(seq) < 2048:
                        seq = seq + [0] * (2048 - len(seq))
                    
                    batch = torch.tensor([seq], dtype=torch.long).to(self.device)
                    input_ids = batch[:, :-1]
                    target_ids = batch[:, 1:]
                    
                    logits, _ = self.model(input_ids)
                    loss = self.criterion(
                        logits.view(-1, self.model.config.vocab_size),
                        target_ids.view(-1)
                    )
                    
                    total_loss += loss.item()
                    count += 1
        
        self.model.train()
        avg_loss = total_loss / max(count, 1)
        return avg_loss
    
    def train(self, train_texts: List[str], eval_texts: List[str], checkpoint_dir: str = 'checkpoints'):
        """Main training loop."""
        checkpoint_dir = Path(checkpoint_dir)
        checkpoint_dir.mkdir(exist_ok=True)
        
        self.log(f"Starting training at {datetime.now()}")
        self.log(f"Device: {self.device}")
        self.log(f"Model parameters: {self.model.num_parameters:,}")
        self.log(f"Training samples: {len(train_texts)}")
        self.log(f"Max steps: {self.config.max_steps}")
        self.log("-" * 80)
        
        self.model.train()
        
        step = 0
        sample_idx = 0
        epoch = 0
        
        while step < self.config.max_steps:
            epoch += 1
            self.log(f"\nEpoch {epoch}")
            
            for text in train_texts:
                if step >= self.config.max_steps:
                    break
                
                tokens = self.tokenizer.encode(text)
                
                if len(tokens) < 100:
                    continue
                
                # Sliding window
                for i in range(0, len(tokens) - 2048, 512):
                    if step >= self.config.max_steps:
                        break
                    
                    seq = tokens[i:i + 2048]
                    if len(seq) < 2048:
                        seq = seq + [0] * (2048 - len(seq))
                    
                    batch = torch.tensor([seq], dtype=torch.long)
                    loss = self.train_step(batch)
                    
                    self.train_losses.append(loss)
                    
                    # Consciousness score
                    consciousness = self._calculate_consciousness(loss, step)
                    self.consciousness_scores.append(consciousness)
                    
                    # Logging
                    if step % 100 == 0:
                        lr = self.optimizer.param_groups[0]['lr']
                        self.log(f"Step {step}: loss={loss:.4f}, lr={lr:.2e}, consciousness={consciousness:.4f}")
                    
                    # Evaluation
                    if step % self.config.eval_every == 0 and step > 0:
                        eval_loss = self.eval_step(eval_texts)
                        self.eval_losses.append(eval_loss)
                        self.log(f"  Eval loss: {eval_loss:.4f}")
                        
                        # Update best loss
                        if eval_loss < self.best_loss:
                            self.best_loss = eval_loss
                            self.log(f"  New best loss! Saving checkpoint...")
                            self.save_checkpoint(checkpoint_dir / f'model_best.pt')
                    
                    # Checkpointing
                    if step % self.config.save_every == 0 and step > 0:
                        self.save_checkpoint(checkpoint_dir / f'model_step_{step}.pt')
                    
                    step += 1
        
        # Final save
        self.save_checkpoint(checkpoint_dir / 'model_final.pt')
        self.log("-" * 80)
        self.log(f"Training complete at {datetime.now()}")
        self.log(f"Final loss: {self.train_losses[-1]:.4f}")
        self.log(f"Best eval loss: {self.best_loss:.4f}")
        self.log(f"Final consciousness: {self.consciousness_scores[-1]:.4f}")
        
        return {
            'final_loss': self.train_losses[-1],
            'best_eval_loss': self.best_loss,
            'train_losses': self.train_losses,
            'eval_losses': self.eval_losses,
            'consciousness_scores': self.consciousness_scores,
        }
    
    def save_checkpoint(self, filepath: str):
        """Save model and training state."""
        checkpoint = {
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'config': self.model.config.__dict__,
            'global_step': self.global_step,
            'best_loss': self.best_loss,
            'train_losses': self.train_losses,
            'eval_losses': self.eval_losses,
            'consciousness_scores': self.consciousness_scores,
        }
        torch.save(checkpoint, filepath)
        print(f"Saved checkpoint: {filepath}")
    
    def load_checkpoint(self, filepath: str):
        """Load model and training state."""
        checkpoint = torch.load(filepath, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.global_step = checkpoint['global_step']
        self.best_loss = checkpoint['best_loss']
        self.train_losses = checkpoint['train_losses']
        self.eval_losses = checkpoint['eval_losses']
        self.consciousness_scores = checkpoint['consciousness_scores']
        print(f"Loaded checkpoint: {filepath}")


def train_codette_model(
    model,
    tokenizer,
    train_texts: List[str],
    eval_texts: List[str],
    checkpoint_dir: str = 'checkpoints',
    device: str = 'cpu'
) -> dict:
    """
    Train Codette model.
    
    Args:
        model: CustomTransformer instance
        tokenizer: Tokenizer with encode/decode methods
        train_texts: List of training texts
        eval_texts: List of evaluation texts
        checkpoint_dir: Directory to save checkpoints
        device: 'cpu' or 'cuda'
    
    Returns:
        Training metrics dictionary
    """
    config = TrainingConfig()
    trainer = CodettTrainer(model, tokenizer, config, device=device)
    
    metrics = trainer.train(train_texts, eval_texts, checkpoint_dir)
    
    return metrics


if __name__ == "__main__":
    print("Training module loaded. Use train_codette_model() for training.")
