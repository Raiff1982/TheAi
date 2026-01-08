"""
Custom Transformer Architecture for Codette
Train from scratch with 3-7B parameters, CPU-optimized
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple
from dataclasses import dataclass


@dataclass
class TransformerConfig:
    """Configuration for custom transformer model."""
    vocab_size: int = 32768  # Token vocabulary
    hidden_size: int = 2048  # 2K hidden (3B model)
    num_hidden_layers: int = 24
    num_attention_heads: int = 32
    intermediate_size: int = 8192  # 4x hidden for FFN
    max_sequence_length: int = 2048
    hidden_dropout_prob: float = 0.1
    attention_probs_dropout_prob: float = 0.1
    initializer_range: float = 0.02
    layer_norm_eps: float = 1e-12
    use_cache: bool = True
    num_labels: int = 2
    type_vocab_size: int = 2
    
    @property
    def num_parameters(self) -> int:
        """Estimate total parameters (approximate)."""
        # Transformer parameters: roughly 12 * hidden_size^2 + 4 * hidden_size * intermediate
        return int(12 * (self.hidden_size ** 2) * self.num_hidden_layers + 
                   4 * self.hidden_size * self.intermediate_size * self.num_hidden_layers)

    def to_dict(self):
        """Convert to dict for serialization."""
        return {
            'vocab_size': self.vocab_size,
            'hidden_size': self.hidden_size,
            'num_hidden_layers': self.num_hidden_layers,
            'num_attention_heads': self.num_attention_heads,
            'intermediate_size': self.intermediate_size,
            'max_sequence_length': self.max_sequence_length,
            'hidden_dropout_prob': self.hidden_dropout_prob,
            'attention_probs_dropout_prob': self.attention_probs_dropout_prob,
        }


class RoPEPositionalEmbedding(nn.Module):
    """Rotary Position Embeddings (RoPE) - more efficient than absolute positional encodings."""
    
    def __init__(self, dim: int, max_seq_length: int = 2048):
        super().__init__()
        self.dim = dim
        self.max_seq_length = max_seq_length
        
        # Pre-compute angles for positions
        inv_freq = 1.0 / (10000 ** (torch.arange(0, dim, 2).float() / dim))
        self.register_buffer("inv_freq", inv_freq)
    
    def forward(self, x: torch.Tensor, seq_len: Optional[int] = None) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Generate sin and cos components for rotary embeddings.
        
        Args:
            x: Input tensor (batch_size, seq_len, dim)
            seq_len: Sequence length (if None, use x.shape[1])
            
        Returns:
            (sin_cache, cos_cache) for use in attention heads
        """
        seq_len = seq_len or x.shape[1]
        
        # Generate position indices
        t = torch.arange(seq_len, device=x.device, dtype=self.inv_freq.dtype)
        
        # Compute angles: outer product of positions and frequencies
        freqs = torch.outer(t, self.inv_freq)
        
        # Duplicate for even/odd dimensions
        emb = torch.cat([freqs, freqs], dim=-1)
        
        return emb.sin().unsqueeze(0), emb.cos().unsqueeze(0)


def rotate_half(x: torch.Tensor) -> torch.Tensor:
    """Rotate half the hidden dims of the input."""
    x1 = x[..., : x.shape[-1] // 2]
    x2 = x[..., x.shape[-1] // 2 :]
    return torch.cat((-x2, x1), dim=-1)


def apply_rotary_emb(x: torch.Tensor, sin: torch.Tensor, cos: torch.Tensor) -> torch.Tensor:
    """Apply rotary embeddings to query/key tensors."""
    return (x * cos) + (rotate_half(x) * sin)


class MultiHeadAttention(nn.Module):
    """Multi-head self-attention with RoPE positional embeddings."""
    
    def __init__(self, config: TransformerConfig):
        super().__init__()
        self.num_heads = config.num_attention_heads
        self.head_dim = config.hidden_size // config.num_attention_heads
        
        assert config.hidden_size % config.num_attention_heads == 0, \
            f"hidden_size ({config.hidden_size}) must be divisible by num_attention_heads ({config.num_attention_heads})"
        
        self.query = nn.Linear(config.hidden_size, config.hidden_size)
        self.key = nn.Linear(config.hidden_size, config.hidden_size)
        self.value = nn.Linear(config.hidden_size, config.hidden_size)
        self.output = nn.Linear(config.hidden_size, config.hidden_size)
        
        self.dropout = nn.Dropout(config.attention_probs_dropout_prob)
        self.rope = RoPEPositionalEmbedding(self.head_dim, config.max_sequence_length)
    
    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Args:
            hidden_states: (batch_size, seq_len, hidden_size)
            attention_mask: (batch_size, 1, 1, seq_len) - 0 for attend, -inf for mask
            
        Returns:
            (output, attention_weights)
        """
        batch_size, seq_len, _ = hidden_states.shape
        
        # Project to Q, K, V
        q = self.query(hidden_states)
        k = self.key(hidden_states)
        v = self.value(hidden_states)
        
        # Reshape for multi-head attention
        q = q.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        k = k.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        v = v.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        
        # Apply RoPE
        sin, cos = self.rope(q, seq_len)
        q = apply_rotary_emb(q, sin, cos)
        k = apply_rotary_emb(k, sin, cos)
        
        # Scaled dot-product attention
        scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.head_dim)
        
        if attention_mask is not None:
            scores = scores + attention_mask
        
        attn_weights = F.softmax(scores, dim=-1)
        attn_weights = self.dropout(attn_weights)
        
        # Apply attention to values
        context = torch.matmul(attn_weights, v)
        
        # Reshape back
        context = context.transpose(1, 2).contiguous()
        context = context.view(batch_size, seq_len, -1)
        
        # Final linear projection
        output = self.output(context)
        
        return output, attn_weights


class FeedForwardNetwork(nn.Module):
    """Position-wise feed-forward network with GELU activation."""
    
    def __init__(self, config: TransformerConfig):
        super().__init__()
        self.dense1 = nn.Linear(config.hidden_size, config.intermediate_size)
        self.dense2 = nn.Linear(config.intermediate_size, config.hidden_size)
        self.activation = nn.GELU()
        self.dropout = nn.Dropout(config.hidden_dropout_prob)
    
    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        hidden_states = self.dense1(hidden_states)
        hidden_states = self.activation(hidden_states)
        hidden_states = self.dropout(hidden_states)
        hidden_states = self.dense2(hidden_states)
        return hidden_states


class TransformerLayer(nn.Module):
    """Single transformer layer with attention + FFN."""
    
    def __init__(self, config: TransformerConfig):
        super().__init__()
        self.attention = MultiHeadAttention(config)
        self.attention_norm = nn.LayerNorm(config.hidden_size, eps=config.layer_norm_eps)
        
        self.ffn = FeedForwardNetwork(config)
        self.ffn_norm = nn.LayerNorm(config.hidden_size, eps=config.layer_norm_eps)
        
        self.dropout = nn.Dropout(config.hidden_dropout_prob)
    
    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Args:
            hidden_states: (batch_size, seq_len, hidden_size)
            attention_mask: Optional attention mask
            
        Returns:
            (output, attention_weights)
        """
        # Self-attention with residual connection and layer norm
        normed = self.attention_norm(hidden_states)
        attn_output, attn_weights = self.attention(normed, attention_mask)
        hidden_states = hidden_states + self.dropout(attn_output)
        
        # Feed-forward with residual connection and layer norm
        normed = self.ffn_norm(hidden_states)
        ffn_output = self.ffn(normed)
        hidden_states = hidden_states + self.dropout(ffn_output)
        
        return hidden_states, attn_weights


class CustomTransformer(nn.Module):
    """
    Custom Transformer LM for Codette (3-7B parameters).
    Trained from scratch on consciousness + tool-use + reasoning data.
    """
    
    def __init__(self, config: TransformerConfig):
        super().__init__()
        self.config = config
        
        # Token embeddings
        self.token_embedding = nn.Embedding(config.vocab_size, config.hidden_size)
        self.embedding_dropout = nn.Dropout(config.hidden_dropout_prob)
        
        # Transformer layers
        self.layers = nn.ModuleList([
            TransformerLayer(config) for _ in range(config.num_hidden_layers)
        ])
        
        # Output layer norm
        self.output_norm = nn.LayerNorm(config.hidden_size, eps=config.layer_norm_eps)
        
        # Language model head
        self.lm_head = nn.Linear(config.hidden_size, config.vocab_size, bias=False)
        
        # Weight tying: tie embedding and output weights
        self.lm_head.weight = self.token_embedding.weight
        
        # Initialize weights
        self._init_weights()
    
    def _init_weights(self):
        """Initialize model weights with careful scaling."""
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.normal_(module.weight, mean=0.0, std=self.config.initializer_range)
                if module.bias is not None:
                    nn.init.constant_(module.bias, 0.0)
            elif isinstance(module, nn.Embedding):
                nn.init.normal_(module.weight, mean=0.0, std=self.config.initializer_range)
            elif isinstance(module, nn.LayerNorm):
                nn.init.constant_(module.bias, 0.0)
                nn.init.constant_(module.weight, 1.0)
    
    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, list]:
        """
        Args:
            input_ids: (batch_size, seq_len) token indices
            attention_mask: (batch_size, seq_len) - 1 for attend, 0 for mask
            
        Returns:
            (logits, layer_outputs)
            - logits: (batch_size, seq_len, vocab_size)
            - layer_outputs: list of attention weights from each layer
        """
        batch_size, seq_len = input_ids.shape
        
        # Embed tokens
        hidden_states = self.token_embedding(input_ids)
        hidden_states = self.embedding_dropout(hidden_states)
        
        # Prepare attention mask for broadcasting
        if attention_mask is not None:
            # attention_mask: (batch_size, seq_len) -> (batch_size, 1, 1, seq_len)
            attention_mask = attention_mask[:, None, None, :].to(dtype=hidden_states.dtype)
            attention_mask = (1.0 - attention_mask) * -10000.0  # Convert to large negative for masking
        
        # Pass through transformer layers
        layer_outputs = []
        for layer in self.layers:
            hidden_states, attn_weights = layer(hidden_states, attention_mask)
            layer_outputs.append(attn_weights)
        
        # Final layer norm
        hidden_states = self.output_norm(hidden_states)
        
        # Project to vocabulary
        logits = self.lm_head(hidden_states)
        
        return logits, layer_outputs
    
    @property
    def num_parameters(self) -> int:
        """Get total number of parameters."""
        return sum(p.numel() for p in self.parameters())
    
    def get_model_size_mb(self) -> float:
        """Get approximate model size in MB (for fp32)."""
        return self.num_parameters * 4 / (1024 ** 2)
    
    def save_checkpoint(self, path: str):
        """Save model checkpoint."""
        torch.save({
            'config': self.config.to_dict(),
            'state_dict': self.state_dict(),
        }, path)
    
    @classmethod
    def from_checkpoint(cls, path: str) -> 'CustomTransformer':
        """Load model from checkpoint."""
        checkpoint = torch.load(path, map_location='cpu')
        config = TransformerConfig(**checkpoint['config'])
        model = cls(config)
        model.load_state_dict(checkpoint['state_dict'])
        return model


def create_codette_model(size: str = 'medium') -> CustomTransformer:
    """
    Create a Codette model with predefined size.
    
    Args:
        size: 'small' (1.3B), 'medium' (2.7B), 'large' (5.3B)
        
    Returns:
        CustomTransformer model
    """
    configs = {
        'small': TransformerConfig(
            hidden_size=1024,
            num_hidden_layers=18,
            num_attention_heads=16,
            intermediate_size=4096,
        ),
        'medium': TransformerConfig(
            hidden_size=2048,
            num_hidden_layers=24,
            num_attention_heads=32,
            intermediate_size=8192,
        ),
        'large': TransformerConfig(
            hidden_size=3072,
            num_hidden_layers=32,
            num_attention_heads=48,
            intermediate_size=12288,
        ),
    }
    
    config = configs.get(size, configs['medium'])
    model = CustomTransformer(config)
    
    print(f"Created {size} Codette model:")
    print(f"  Parameters: {model.num_parameters:,}")
    print(f"  Size (fp32): {model.get_model_size_mb():.2f} MB")
    print(f"  Hidden size: {config.hidden_size}")
    print(f"  Layers: {config.num_hidden_layers}")
    print(f"  Heads: {config.num_attention_heads}")
    
    return model
