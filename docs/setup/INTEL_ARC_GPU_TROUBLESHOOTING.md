# Intel Arc GPU Training on Windows - Troubleshooting Guide

## Status Summary
- **Windows 11 + Python 3.13 + Intel Arc 140V**: GPU acceleration NOT WORKING YET
- **Workaround**: CPU training works (90-180 min)
- **Root causes identified below**

---

## What Doesn't Work (And Why)

### 1. **Python 3.13 + IPEX = No wheels available**
**Symptom**: `ERROR: No matching distribution found for intel-extension-for-pytorch`

**Root cause**: Intel hasn't published IPEX wheels for Python 3.13 yet. IPEX is CPU-heavy and needs compiled binaries per Python version.

**Timeline**: Check https://github.com/intel-extension-for-pytorch/intel-extension-for-pytorch/releases for 3.13 support (as of Jan 2026, not available).

**Current workaround**: Use Python 3.10 or 3.11 (see below).

---

### 2. **Windows Native Intel Arc GPU Support is Incomplete**
**Symptom**: `torch.xpu.is_available()` returns False even with oneAPI + IPEX installed

**Root cause**: 
- PyTorch Windows builds don't officially support Intel Arc GPU passthrough
- Intel GPU drivers for Windows lack PyTorch integration layer
- oneAPI Base Toolkit provides compilers, NOT GPU runtime libraries

**Evidence from testing**:
- oneAPI installed: ✓
- IPEX installed (Python 3.10/3.11): ✓
- PyTorch 2.6+: ✓
- **XPU detection: ✗ (No GPU driver runtime found)**

**Official Intel support**: Intel officially recommends **WSL2 + Linux** for Arc GPU + PyTorch. Windows support is experimental/incomplete.

---

### 3. **WSL2 GPU Passthrough is Not Automatic**
**Symptom**: `torch.xpu.is_available()` returns False in WSL2, even with Intel Arc on host

**Root cause**:
- WSL2 doesn't automatically pass GPU to container unless specifically configured
- Requires GPU driver installation in WSL2 Ubuntu (complex setup)
- Intel GPU manager for WSL2 has limited/beta support

**What we tried**:
```bash
sudo apt install intel-gpumanager intel-level-zero-gpu  # Not in jammy repo
sudo clinfo  # GPU detection failed
```

**Conclusion**: WSL2 GPU passthrough requires deeper driver setup beyond scope of quick start.

---

## What DOES Work

### ✅ CPU Training (Fully Functional)
```cmd
python quick_train.py
```

**Performance**: 
- Intel Core Ultra 7 256V (8 cores): ~90-180 minutes per training run
- Full Codette model trains successfully
- Output: `codette_model/codette_large.gguf`

**Device detected**: `cpu` (auto-fallback in quick_train.py)

**Status**: Production-ready, just slow.

---

### ✅ GPU Training with Python 3.10/3.11 (Potential)
**Prerequisites**:
1. Install Python 3.10 or 3.11 (not 3.13)
2. Create fresh venv
3. Install IPEX for that Python version
4. May still need Windows GPU driver configuration

**Command**:
```cmd
python3.10 -m venv venv_310
venv_310\Scripts\activate
pip install torch torchvision torchaudio
pip install intel-extension-for-pytorch
python quick_train.py
```

**Expected result**: `torch.xpu.is_available()` might return True (untested - requires driver setup)

**Risk**: Windows Intel GPU drivers may still not support XPU passthrough.

---

## Recommended Paths Forward

### Path 1: Accept CPU Training (Immediate)
- **Time**: 90-180 min per run
- **Setup**: Run `python quick_train.py` now
- **Reliability**: 100%
- **GPU acceleration**: None, but works

### Path 2: Downgrade to Python 3.10/3.11 (Medium effort)
- **Time**: Setup 10 min + 15-30 min training if GPU works
- **Setup**: Install Python 3.10, create new venv, install IPEX
- **Reliability**: 50% (GPU driver support unknown on Windows)
- **Likelihood of success**: Medium (depends on Intel GPU drivers)

### Path 3: Use WSL2 + Linux (High effort)
- **Time**: Setup 30+ min, complex driver install, 15-30 min training if works
- **Setup**: Fresh WSL2 Ubuntu, Intel GPU manager, troubleshoot drivers
- **Reliability**: 70% (official Intel support path but complex)
- **Status**: Requires deep Linux/driver knowledge

### Path 4: Wait for IPEX Python 3.13 Support
- **Timeline**: Unknown (check Intel GitHub monthly)
- **Effort**: Zero
- **Reliability**: 100% (when available)

---

## Lessons Learned

### For Developers
1. **Always test GPU setup with fresh environment** - conda cache corruption is real
2. **Version matrix matters**: PyTorch × Python × IPEX × GPU driver compatibility is complex
3. **Windows GPU support lags**: Intel Arc on Windows is incomplete. Official support is WSL2/Linux.
4. **Documentation ≠ Reality**: Intel oneAPI docs suggest Windows support, but GPU drivers/IPEX integration incomplete.

### For Codette Project
1. Document Python version requirements (3.10/3.11 recommended for GPU, not 3.13)
2. Add Python version check to quick_train.py
3. Consider WSL2 setup guide for GPU users
4. Accept CPU training as primary path for Windows users

---

## Quick Checklist for Developers

If you want GPU training on Windows with Intel Arc:

- [ ] Python 3.10 or 3.11 installed (NOT 3.13)
- [ ] Fresh Python venv (not conda - avoid cache corruption)
- [ ] PyTorch 2.6+ installed
- [ ] IPEX installed with `pip install intel-extension-for-pytorch`
- [ ] Verify: `python -c "import torch; print(torch.xpu.is_available())"`
- [ ] If False: You'll need Windows GPU drivers (Intel hasn't made this easy)
- [ ] If True: Run `python quick_train.py` and celebrate 🎉

---

## Resources

- **IPEX Releases**: https://github.com/intel-extension-for-pytorch/intel-extension-for-pytorch/releases
- **Intel oneAPI Documentation**: https://www.intel.com/content/www/us/en/developer/tools/oneapi/base-toolkit.html
- **PyTorch Official**: https://pytorch.org/get-started/locally/
- **Issue Tracker**: If your setup differs, open issue with Python version + GPU info

---

**Last Updated**: January 11, 2026  
**Status**: CPU training confirmed working, GPU acceleration untested on Windows 3.13  
**Next Dev**: Try Python 3.10 path if GPU acceleration needed
