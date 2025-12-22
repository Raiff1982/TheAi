#!/usr/bin/env python
"""
Validate fine-tuning setup and check prerequisites
"""

import sys
import os
from pathlib import Path
import subprocess
import json


class SetupValidator:
    """Validate fine-tuning environment"""
    
    def __init__(self):
        self.workspace = Path(__file__).parent
        self.checks = []
        self.warnings = []
        self.errors = []
    
    def check(self, name: str, condition: bool, error_msg: str = "", warning: bool = False):
        """Record a check result"""
        status = "✓" if condition else ("⚠" if warning else "✗")
        self.checks.append((status, name))
        
        if not condition:
            if warning:
                self.warnings.append(f"  {name}: {error_msg}")
            else:
                self.errors.append(f"  {name}: {error_msg}")
    
    def validate_python(self):
        """Check Python version"""
        version = sys.version_info
        is_valid = version.major == 3 and version.minor >= 10
        self.check(
            "Python Version",
            is_valid,
            f"Need Python 3.10+, got {version.major}.{version.minor}",
        )
        return version
    
    def validate_files(self):
        """Check required files exist"""
        required_files = [
            "finetune_codette_unsloth.py",
            "test_finetuned.py",
            "finetune_requirements.txt",
            "FINETUNING_GUIDE.md",
            "recursive_continuity_dataset_codette.csv",
        ]
        
        for file in required_files:
            path = self.workspace / file
            exists = path.exists()
            self.check(
                f"File: {file}",
                exists,
                f"Not found at {path}",
            )
    
    def validate_gpu(self):
        """Check NVIDIA GPU availability"""
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                self.checks.append(("✓", f"GPU Detected: {output}"))
                
                # Check VRAM
                if "12" in output or "24" in output or "40" in output or "80" in output:
                    self.checks.append(("✓", "VRAM: Sufficient (8GB+)"))
                else:
                    self.warnings.append("  GPU VRAM might be low. 8GB+ recommended.")
                
                return True
            else:
                self.check(
                    "NVIDIA GPU",
                    False,
                    "nvidia-smi not found. Install NVIDIA drivers.",
                )
                return False
                
        except FileNotFoundError:
            self.check(
                "NVIDIA GPU",
                False,
                "nvidia-smi not found. Install NVIDIA drivers.",
            )
            return False
        except Exception as e:
            self.check(
                "NVIDIA GPU",
                False,
                str(e),
            )
            return False
    
    def validate_cuda(self):
        """Check CUDA availability"""
        try:
            result = subprocess.run(
                ["nvidia-smi"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def validate_packages(self):
        """Check Python packages"""
        packages = {
            "torch": "PyTorch",
            "transformers": "Hugging Face Transformers",
            "datasets": "Hugging Face Datasets",
            "accelerate": "Hugging Face Accelerate",
        }
        
        for package, name in packages.items():
            try:
                __import__(package)
                self.checks.append(("✓", f"Package: {name}"))
            except ImportError:
                self.check(
                    f"Package: {name}",
                    False,
                    f"Not installed. Run: pip install {package}",
                    warning=True
                )
    
    def validate_ollama(self):
        """Check Ollama availability"""
        try:
            result = subprocess.run(
                ["ollama", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                version = result.stdout.strip()
                self.checks.append(("✓", f"Ollama: {version}"))
                
                # Check if service is running
                try:
                    result = subprocess.run(
                        ["ollama", "list"],
                        capture_output=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        self.checks.append(("✓", "Ollama Service: Running"))
                    else:
                        self.warnings.append("  Ollama service not running. Start with: ollama serve")
                except:
                    self.warnings.append("  Ollama service not running. Start with: ollama serve")
                
                return True
            else:
                self.check(
                    "Ollama",
                    False,
                    "Not installed. Download from: https://ollama.ai",
                    warning=True
                )
                return False
                
        except FileNotFoundError:
            self.check(
                "Ollama",
                False,
                "Not installed. Download from: https://ollama.ai",
                warning=True
            )
            return False
        except Exception as e:
            self.check(
                "Ollama",
                False,
                str(e),
                warning=True
            )
            return False
    
    def validate_disk_space(self):
        """Check available disk space"""
        try:
            import shutil
            stat = shutil.disk_usage(self.workspace)
            free_gb = stat.free / (1024**3)
            
            is_ok = free_gb > 50
            msg = f"{free_gb:.1f}GB free"
            
            self.check(
                "Disk Space",
                is_ok,
                f"Need 50GB, have {msg}",
                warning=not is_ok
            )
        except Exception as e:
            self.check(
                "Disk Space",
                False,
                str(e),
                warning=True
            )
    
    def run_all_checks(self):
        """Run all validation checks"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║         CODETTE FINE-TUNING SETUP VALIDATOR                  ║
╚══════════════════════════════════════════════════════════════╝
""")
        
        print("\n[*] Validating environment...\n")
        
        version = self.validate_python()
        self.validate_files()
        self.validate_disk_space()
        gpu_available = self.validate_gpu()
        cuda_available = self.validate_cuda()
        self.validate_packages()
        ollama_available = self.validate_ollama()
        
        # Print results
        print("\n" + "─" * 60)
        for status, name in self.checks:
            print(f"  {status} {name}")
        
        if self.warnings:
            print("\n" + "─" * 60)
            print("⚠️  WARNINGS:\n")
            for warning in self.warnings:
                print(warning)
        
        if self.errors:
            print("\n" + "─" * 60)
            print("❌ ERRORS:\n")
            for error in self.errors:
                print(error)
        
        # Summary
        print("\n" + "=" * 60)
        
        if not self.errors:
            print("\n✅ SETUP COMPLETE - Ready to train!")
            print("\nNext steps:")
            print("  1. python finetune_codette_unsloth.py")
            print("\nNote:")
            if not ollama_available:
                print("  • Ollama not installed - install from https://ollama.ai")
            if not gpu_available:
                print("  • No GPU detected - training will be slow. GPU recommended.")
            print("\n" + "=" * 60)
            return True
        else:
            print("\n❌ SETUP INCOMPLETE - Fix errors above")
            print("\nRequired fixes:")
            for error in self.errors:
                print(error)
            print("\n" + "=" * 60)
            return False
    
    def generate_report(self):
        """Generate validation report"""
        report = {
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
            "workspace": str(self.workspace),
            "checks": len(self.checks),
            "warnings": len(self.warnings),
            "errors": len(self.errors),
            "status": "ready" if not self.errors else "incomplete",
        }
        
        report_path = self.workspace / "validation_report.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n[*] Report saved to: {report_path}")
        
        return report


def main():
    """Main entry point"""
    validator = SetupValidator()
    success = validator.run_all_checks()
    validator.generate_report()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
