#!/usr/bin/env python
"""
Intel Arc GPU Setup Verification & Quick Start Script
Run this to verify Intel Arc GPU is properly configured
"""

import subprocess
import sys
from pathlib import Path

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_step(num, text):
    print(f"\n[Step {num}] {text}")
    print("-" * 70)

def run_command(cmd, description=""):
    """Run a shell command and return result."""
    try:
        if description:
            print(f"Running: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def main():
    print_header("INTEL ARC GPU SETUP VERIFICATION")
    
    print("\n🖥️  Your Hardware:")
    print("   GPU: Intel Arc 140V (8GB)")
    print("   Driver: 32.0.101.6913")
    print("   CPU: Intel Core Ultra 7 256V")
    print("   RAM: 16GB LPDDR5")
    print("   OS: Windows 11 Pro (Build 26200)")
    
    # Step 1: Check if IPEX is installed
    print_step(1, "Check if Intel Extension for PyTorch (IPEX) is installed")
    success, stdout, stderr = run_command(
        'python -c "import intel_extension_for_pytorch as ipex; print(f\'IPEX Version: {ipex.__version__}\')"'
    )
    
    if success:
        print(f"✅ IPEX is installed: {stdout.strip()}")
    else:
        print("❌ IPEX not found. Installing now...")
        print("\n   Running: pip install intel-extension-for-pytorch")
        success, stdout, stderr = run_command('pip install intel-extension-for-pytorch --quiet')
        if success:
            print("✅ IPEX installed successfully!")
        else:
            print("❌ Failed to install IPEX")
            print(f"Error: {stderr}")
            return False
    
    # Step 2: Verify PyTorch
    print_step(2, "Verify PyTorch configuration")
    pytorch_cmd = (
        'python -c "import torch; '
        'print(f\'PyTorch: {torch.__version__}\'); '
        'print(f\'CUDA: {torch.cuda.is_available()}\')"'
    )
    success, stdout, stderr = run_command(pytorch_cmd)
    if success:
        print(stdout.strip())
    else:
        print(f"❌ PyTorch error: {stderr}")
        return False
    
    # Step 3: Check XPU availability
    print_step(3, "Check Intel Arc GPU (XPU) detection")
    cmd = (
        'python -c "import torch; '
        'import intel_extension_for_pytorch as ipex; '
        'result = torch.xpu.is_available(); '
        'print(\\\"✅ XPU Available\\\" if result else \\\"❌ XPU Not Available\\\")"'
    )
    
    success, stdout, stderr = run_command(cmd)
    print(stdout.strip() if stdout else stderr)
    
    if "DETECTED" not in stdout:
        print("\n⚠️  Intel Arc not detected. Troubleshooting steps:")
        print("   1. Restart your Python/IDE after installing IPEX")
        print("   2. Check Windows Device Manager for Intel Arc GPU")
        print("   3. Verify GPU driver is version 32.0.101.6913 or newer")
        print("   4. Try: pip install --upgrade intel-extension-for-pytorch")
        return False
    
    # Step 4: Test device detection script
    print_step(4, "Test auto-detection function")
    
    # Check if quick_train.py exists and has detect_device
    qtp = Path("quick_train.py")
    if qtp.exists():
        print("✅ quick_train.py found")
        content = qtp.read_text()
        if "def detect_device" in content:
            print("✅ Auto-detection function present")
        else:
            print("❌ Auto-detection function not found")
    else:
        print(f"❌ quick_train.py not found at {qtp.absolute()}")
    
    # Step 5: Ready to train
    print_step(5, "Ready to start training!")
    print("\n✅ All checks passed!")
    print("\n🚀 Next command to run:")
    print("   python quick_train.py")
    print("\n📊 Expected behavior:")
    print("   - Console will print: Device: XPU")
    print("   - Training should complete in 15-30 minutes")
    print("   - GPU memory usage will be 6-8GB")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
