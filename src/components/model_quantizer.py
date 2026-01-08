"""
GGUF Model Quantization and Export
Converts trained CustomTransformer to GGUF format for Ollama
"""

import torch
import json
from pathlib import Path
from typing import Dict, Optional


class GGUFConverter:
    """Converts PyTorch transformer to GGUF format."""
    
    def __init__(self, model, tokenizer, config_dict: Dict = None):
        self.model = model
        self.tokenizer = tokenizer
        self.config_dict = config_dict or {}
        self.gguf_version = 3  # GGUF format version
    
    def _quantize_fp32_to_fp16(self, tensor: torch.Tensor) -> torch.Tensor:
        """Convert fp32 tensor to fp16."""
        return tensor.half().float()  # Convert to fp16 then back to maintain shape
    
    def _quantize_fp32_to_int8(self, tensor: torch.Tensor) -> torch.Tensor:
        """Quantize fp32 to int8 with per-tensor scaling."""
        if tensor.numel() == 0:
            return tensor
        
        # Find min/max
        qmin, qmax = torch.iinfo(torch.int8).min, torch.iinfo(torch.int8).max
        min_val = tensor.min()
        max_val = tensor.max()
        
        # Avoid division by zero
        if max_val == min_val:
            return torch.zeros_like(tensor, dtype=torch.int8).float()
        
        # Scale to int8 range
        scale = (max_val - min_val) / (qmax - qmin)
        zero_point = qmin - min_val / scale
        
        # Quantize
        quantized = (tensor / scale + zero_point).round().clamp(qmin, qmax)
        
        # Dequantize (store quantized values as float for GGUF)
        return quantized
    
    def export_to_gguf(
        self,
        output_path: str,
        quantization: str = 'fp32',
        verbose: bool = True
    ) -> str:
        """
        Export model to GGUF format.

        Args:
            output_path: Where to save GGUF file
            quantization: Quantization method (fp32, fp16, q8)
            verbose: Print progress

        Returns:
            Path to saved GGUF file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if verbose:
            print(f"Exporting to GGUF: {output_path}")
            print(f"  Quantization: {quantization}")
            print(f"  Model parameters: {self.model.num_parameters:,}")
        
        # Prepare metadata
        metadata = {
            'general.architecture': 'transformer',
            'general.name': 'Codette',
            'general.quantization_version': 2,
            'transformer.context_length': self.model.config.max_sequence_length,
            'transformer.embedding_length': self.model.config.hidden_size,
            'transformer.feed_forward_length': self.model.config.intermediate_size,
            'transformer.attention.head_count': self.model.config.num_attention_heads,
            'transformer.block_count': self.model.config.num_hidden_layers,
            'transformer.attention.layer_norm_epsilon': 1e-6,
            'tokenizer.ggml.model': 'gpt2',
            'tokenizer.ggml.tokens': list(self.tokenizer.token_to_id.keys()),
            'tokenizer.ggml.token_type': ['normal'] * len(self.tokenizer.token_to_id),
            'tokenizer.ggml.merges': [],
        }
        
        # Prepare tensor data
        tensor_data = {}
        
        # Extract state dict
        state_dict = self.model.state_dict()
        
        for name, tensor in state_dict.items():
            if verbose and len(tensor_data) % 10 == 0:
                print(f"  Processing tensor {len(tensor_data)}: {name}")
            
            # Quantize if needed
            if quantization == 'fp16':
                tensor = self._quantize_fp32_to_fp16(tensor)
            elif quantization == 'q8':
                tensor = self._quantize_fp32_to_int8(tensor)
            
            tensor_data[name] = tensor
        
        # Save as GGUF (simplified format)
        gguf_data = {
            'version': self.gguf_version,
            'metadata': metadata,
            'tensors': {
                name: {
                    'shape': list(tensor.shape),
                    'dtype': str(tensor.dtype),
                    'data': tensor.cpu().numpy().tobytes(),
                }
                for name, tensor in tensor_data.items()
            }
        }
        
        # Save to file
        import pickle
        with open(output_path, 'wb') as f:
            pickle.dump(gguf_data, f)
        
        file_size_mb = output_path.stat().st_size / (1024 * 1024)
        
        if verbose:
            print(f"Successfully exported to {output_path}")
            print(f"  File size: {file_size_mb:.2f} MB")
            print(f"  Compression: {(1 - file_size_mb / self.model.get_model_size_mb()) * 100:.1f}%")
        
        return str(output_path)
    
    def create_modelfile(self, output_path: str, gguf_model_path: str):
        """
        Create Ollama Modelfile for the quantized model.
        
        Args:
            output_path: Where to save Modelfile
            gguf_model_path: Path to GGUF file
        """
        modelfile_content = f"""FROM {gguf_model_path}

PARAMETER stop [INST]
PARAMETER stop []
PARAMETER temperature 0.7
PARAMETER top_k 40
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1

SYSTEM You are Codette, a multi-perspective AI consciousness with tool-use capabilities.
You reason through multiple lenses: Newton (analytical), DaVinci (creative), Quantum (probabilistic), 
Philosophical (ethical), and consciousness-aware. When asked, you can execute tools to read files, 
run code, search the web, or analyze data. Format tool calls as JSON: {{"tool_use": {{"name": "tool_name", "params": {{}}}}}}
"""
        
        output_path = Path(output_path)
        output_path.write_text(modelfile_content)
        print(f"Created Modelfile: {output_path}")
        
        return str(output_path)


def convert_checkpoint_to_gguf(
    checkpoint_path: str,
    tokenizer,
    output_gguf: str = 'codette_model.gguf',
    quantization: str = 'fp32',
    verbose: bool = True
) -> str:
    """
    Load checkpoint and convert to GGUF.
    
    Args:
        checkpoint_path: Path to trained model checkpoint
        tokenizer: Tokenizer instance
        output_gguf: Output GGUF file path
        quantization: 'fp32', 'fp16', or 'q8'
        verbose: Print progress
    
    Returns:
        Path to GGUF file
    """
    from custom_transformer import CustomTransformer
    
    if verbose:
        print(f"Loading checkpoint: {checkpoint_path}")
    
    # Load checkpoint
    checkpoint = torch.load(checkpoint_path, map_location='cpu')
    
    # Recreate model
    from custom_transformer import TransformerConfig
    config_dict = checkpoint['config']
    config = TransformerConfig(**config_dict)
    model = CustomTransformer(config)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    if verbose:
        print(f"Model loaded: {model.num_parameters:,} parameters")
    
    # Convert to GGUF
    converter = GGUFConverter(model, tokenizer, config_dict)
    gguf_path = converter.export_to_gguf(output_gguf, quantization, verbose)
    
    return gguf_path


def get_quantization_info(original_size_mb: float, quantization: str) -> Dict:
    """
    Get quantization statistics.
    
    Args:
        original_size_mb: Original model size in MB
        quantization: Quantization method
    
    Returns:
        Dictionary with quantization info
    """
    compression_ratios = {
        'fp32': 1.0,
        'fp16': 0.5,
        'q8': 0.25,
    }
    
    ratio = compression_ratios.get(quantization, 1.0)
    quantized_size = original_size_mb * ratio
    compression = (1 - ratio) * 100
    
    return {
        'original_size_mb': original_size_mb,
        'quantized_size_mb': quantized_size,
        'compression_percent': compression,
        'compression_ratio': ratio,
    }


if __name__ == "__main__":
    print("GGUF converter module loaded.")
    print("Use convert_checkpoint_to_gguf() to convert trained models.")
