# Intel Arc GPU Setup Guide

## Your Hardware ✅

**Intel Arc 140V GPU (8GB)** on HP OmniBook 7 Flip Laptop
- Driver version: 32.0.101.6913 ✅ Already installed
- 16GB RAM (LPDDR5) ✅
- Intel Core Ultra 7 256V ✅

## Setup Options

### Option 1: Intel XPU (Recommended)

**What it does**: Native Intel Arc GPU acceleration via Intel's oneAPI toolkit

```bash
# 1. Install Intel Arc GPU drivers (you already have this)
# Driver 32.0.101.6913 is good ✅

# 2. Install Intel's PyTorch XPU support
pip install intel-extension-for-pytorch

# 3. Install Intel Data Parallel Extension (for best performance)
pip install intel-extension-for-pytorch-xpu

# 4. Verify installation
python -c "import intel_extension_for_pytorch as ipex; print('Intel XPU ready!')"
```

**Expected Performance**: 
- Speed: ~3-5x faster than CPU
- Memory: Uses your 8GB Arc GPU efficiently
- Training time: ~10-15 minutes instead of 90-180 minutes

### Option 2: Intel DPC++ (If XPU doesn't work)

Alternative backend using Data Parallel C++:

```bash
pip install intel-extension-for-pytorch[gpu]
```

### Option 3: Use CPU (No Setup)

If GPU setup doesn't work, training still works on CPU:
- Slower (~90-180 minutes for full training)
- More stable
- No driver dependencies

## Quick Enable Intel Arc GPU

### Step 1: Install Intel XPU Support

```bash
pip install intel-extension-for-pytorch
```

### Step 2: Update Your Training Script

Replace this line in `quick_train.py`:

```python
# OLD (line ~30)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
```

With this:

```python
# NEW - Intel Arc detection
device = get_best_device()

def get_best_device():
    """Detect best available device: Intel Arc > CUDA > CPU"""
    # Try Intel Arc first
    try:
        import intel_extension_for_pytorch as ipex
        if torch.xpu.is_available():
            print("✅ Using Intel Arc GPU")
            return 'xpu'
    except ImportError:
        pass
    
    # Try NVIDIA CUDA
    if torch.cuda.is_available():
        print("✅ Using NVIDIA CUDA GPU")
        return 'cuda'
    
    # Fall back to CPU
    print("⚠️  Using CPU (slower, but will work)")
    return 'cpu'
```

### Step 3: Test Detection

```bash
python -c "
import torch
try:
    import intel_extension_for_pytorch as ipex
    if torch.xpu.is_available():
        print('✅ Intel Arc GPU detected!')
    else:
        print('❌ Intel Arc GPU not detected')
except:
    print('❌ Intel extension not installed')
"
```

## Installation Commands (Copy-Paste)

### Complete Setup

```bash
# Step 1: Uninstall old PyTorch (if CPU-only)
pip uninstall torch -y

# Step 2: Install PyTorch with Intel support
pip install torch torchvision torchaudio intel-extension-for-pytorch

# Step 3: Verify
python -c "import torch; import intel_extension_for_pytorch as ipex; print('Ready for Intel Arc!')"

# Step 4: Run training
python quick_train.py
```

### Just Add Intel Support (Keep existing PyTorch)

```bash
pip install intel-extension-for-pytorch
python quick_train.py
```

## Update Training Script

I'll modify `quick_train.py` to auto-detect your Intel Arc GPU:
