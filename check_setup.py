#!/usr/bin/env python
"""Simple setup validation script"""

import sys
import subprocess
from pathlib import Path

def validate():
    """Quick validation"""
    workspace = Path(__file__).parent
    
    print("\n[Codette Fine-Tuning Setup Validator]\n")
    
    # Check Python
    print(f"[*] Python: {sys.version.split()[0]}")
    if sys.version_info < (3, 10):
        print("[!] Warning: Need Python 3.10+\n")
    
    # Check files
    files_ok = 0
    files = [
        "finetune_codette_unsloth.py",
        "test_finetuned.py",
        "finetune_requirements.txt",
        "recursive_continuity_dataset_codette.csv",
    ]
    
    for f in files:
        if (workspace / f).exists():
            print(f"[OK] {f}")
            files_ok += 1
        else:
            print(f"[MISSING] {f}")
    
    # Check GPU
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            gpu = result.stdout.strip()
            print(f"[GPU] {gpu}")
        else:
            print("[NO GPU] CPU-only training (very slow)")
    except:
        print("[NO GPU] GPU not detected")
    
    # Check Ollama
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"[OLLAMA] {result.stdout.strip()}")
        else:
            print("[NO OLLAMA] Download from: https://ollama.ai")
    except:
        print("[NO OLLAMA] Not installed")
    
    print(f"\n[Summary] {files_ok}/{len(files)} files found")
    
    if files_ok == len(files):
        print("\n[SUCCESS] Ready to train!")
        print("[Next] python finetune_codette_unsloth.py\n")
        return 0
    else:
        print("\n[ERROR] Missing files. Check setup.\n")
        return 1

if __name__ == "__main__":
    sys.exit(validate())
