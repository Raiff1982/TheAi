#!/usr/bin/env python
"""
Codette Training Setup - One Click
Installs dependencies and starts training
"""

import subprocess
import sys
import os

def run(cmd, description=""):
    """Run a command and return success status"""
    if description:
        print(f"\n{description}...", end=" ", flush=True)
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            if description:
                print("✓")
            return True
        else:
            if description:
                print("✗")
            if result.stderr:
                print(f"  Error: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"✗ Exception: {e}")
        return False

def main():
    print("=" * 70)
    print("  CODETTE AI TRAINING - SETUP")
    print("=" * 70)
    
    # Step 1: Upgrade pip
    print("\n[1/3] Updating pip...")
    run("pip install --upgrade pip", "  Upgrading pip")
    
    # Step 2: Install PyTorch
    print("\n[2/3] Installing PyTorch...")
    print("  This will take 5-10 minutes...")
    
    # Use generic torch (no version pinning to avoid conflicts)
    if not run("pip install --no-cache-dir torch torchvision torchaudio", "  Installing PyTorch"):
        print("\n  ERROR: PyTorch installation failed")
        print("  Try manually: pip install torch --upgrade")
        return False
    
    # Step 3: Install IPEX (optional)
    print("\n[3/3] Installing Intel Extension for PyTorch...")
    ipex_result = run("conda install -c  intel-extension-for-pytorch", "  Installing IPEX")
    if ipex_result:
        print("  IPEX installed (GPU acceleration enabled)")
    else:
        print("  Note: IPEX not available for Python 3.13 (CPU training will work fine)")
    
    
    # Verify PyTorch works
    print("\n" + "=" * 70)
    print("  VERIFYING INSTALLATION")
    print("=" * 70)
    
    try:
        import torch
        print(f"\n✓ PyTorch {torch.__version__} installed successfully")
        print(f"  CPU threads: {torch.get_num_threads()}")
        
        try:
            import intel_extension_for_pytorch as ipex
            xpu_available = torch.xpu.is_available()
            print(f"✓ IPEX available, XPU: {xpu_available}")
        except ImportError:
            print("  IPEX not available (CPU training mode)")
    except ImportError as e:
        print(f"\n✗ PyTorch import failed: {e}")
        return False
    
    # Step 4: Run training
    print("\n" + "=" * 70)
    print("  STARTING CODETTE TRAINING")
    print("=" * 70)
    print()
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        result = subprocess.run([sys.executable, "quick_train.py"], timeout=86400)
        return result.returncode == 0
    except KeyboardInterrupt:
        print("\n\nTraining interrupted by user")
        return False
    except Exception as e:
        print(f"\nTraining error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n" + "=" * 70)
        print("  SUCCESS! Codette model trained")
        print("=" * 70)
        print("\nResults saved to:")
        print("  - Model: codette_model/codette_*.gguf")
        print("  - Logs: training_logs/")
        print()
    else:
        print("\nTraining failed. Check errors above.")
    
    sys.exit(0 if success else 1)
