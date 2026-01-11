"""
Quick Intel Arc GPU Setup Check
Run: python check_gpu_ready.py
"""

def check_setup():
    print("\n" + "="*70)
    print("  INTEL ARC GPU SETUP CHECK")
    print("="*70)
    
    # Step 1: Check PyTorch
    print("\n[1] Checking PyTorch...")
    try:
        import torch
        print(f"    ✅ PyTorch version: {torch.__version__}")
    except ImportError:
        print("    ❌ PyTorch not installed")
        return False
    
    # Step 2: Check IPEX
    print("\n[2] Checking Intel Extension for PyTorch (IPEX)...")
    try:
        import intel_extension_for_pytorch as ipex
        print(f"    ✅ IPEX installed: {ipex.__version__}")
    except ImportError:
        print("    ❌ IPEX not installed")
        print("\n    On Windows, IPEX requires CONDA (not pip)")
        print("    To fix this, run ONE of:")
        print("    ")
        print("    Option 1 (Easiest): conda install -c intel intel-extension-for-pytorch")
        print("    Option 2: Install Intel oneAPI Base Toolkit")
        print("             https://www.intel.com/content/www/us/en/developer/tools/oneapi/base-toolkit.html")
        print("    ")
        print("    See WINDOWS_IPEX_INSTALL.md for detailed instructions")
        return False
    
    # Step 3: Check XPU availability
    print("\n[3] Checking Intel Arc GPU (XPU) availability...")
    try:
        if torch.xpu.is_available():
            device_name = torch.xpu.get_device_name(0)
            total_memory = torch.xpu.get_device_properties(0).total_memory / 1e9
            print(f"    ✅ Intel Arc GPU DETECTED")
            print(f"       Device: {device_name}")
            print(f"       Total Memory: {total_memory:.1f} GB")
            gpu_available = True
        else:
            print("    ⚠️  XPU available attribute is False")
            print("       (This might resolve after system restart)")
            gpu_available = False
    except Exception as e:
        print(f"    ❌ XPU check failed: {e}")
        gpu_available = False
    
    # Step 4: Check CUDA
    print("\n[4] Checking NVIDIA CUDA (fallback)...")
    if torch.cuda.is_available():
        print(f"    ✅ CUDA available (device: {torch.cuda.get_device_name(0)})")
    else:
        print("    ℹ️  CUDA not available (this is OK - using XPU)")
    
    # Step 5: Check training scripts
    print("\n[5] Checking training scripts...")
    from pathlib import Path
    
    qtp = Path("quick_train.py")
    if qtp.exists() and "detect_device" in qtp.read_text():
        print("    ✅ quick_train.py has auto-detection")
    else:
        print("    ❌ quick_train.py not found or not updated")
        return False
    
    ttp = Path("src/components/train_codette_model.py")
    if ttp.exists() and "normalize_device" in ttp.read_text():
        print("    ✅ train_codette_model.py has device normalization")
    else:
        print("    ⚠️  train_codette_model.py might not be updated")
    
    # Final status
    print("\n" + "="*70)
    if gpu_available:
        print("  ✅ READY TO TRAIN WITH INTEL ARC GPU!")
        print("\n  Run: python quick_train.py")
        print("\n  Expected: Training on XPU (Intel Arc GPU)")
        print("  Speed: ~15-30 minutes (6-10x faster than CPU)")
    else:
        print("  ⚠️  IPEX installed but XPU not detected")
        print("\n  Possible fixes:")
        print("    1. Restart Python/IDE and try again")
        print("    2. Check Device Manager for Intel Arc GPU")
        print("    3. Update GPU drivers to 32.0.101.6913+")
        print("\n  You can still train on CPU:")
        print("  Run: python quick_train.py")
        print("  Speed: ~90-180 minutes on CPU (slower but works)")
    print("="*70 + "\n")
    
    return True

if __name__ == "__main__":
    try:
        check_setup()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
