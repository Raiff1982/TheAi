# ⚡ Quick Action Plan - Fix Intel Arc GPU Setup

## You Got This Error

```
ERROR: Could not find a version that satisfies the requirement intel-extension-for-pytorch
ERROR: No matching distribution found for intel-extension-for-pytorch
```

**This is normal on Windows.** IPEX requires conda, not pip.

---

## 🚀 Do THIS Now (Pick One)

### FASTEST FIX (If you have conda)

**1. Open terminal and run:**
```bash
conda install -c intel intel-extension-for-pytorch
```

**2. Then verify:**
```bash
python check_gpu_ready.py
```

**3. Train with GPU:**
```bash
python quick_train.py
```

**Time:** 5-10 minutes total

---

### EASY FIX (If you don't have conda)

**1. Install Miniconda:**
- Download: https://docs.conda.io/projects/miniconda/
- Choose Windows installer
- Run installer
- **Restart your terminal**

**2. Then install IPEX:**
```bash
conda install -c intel intel-extension-for-pytorch
```

**3. Verify and train:**
```bash
python check_gpu_ready.py
python quick_train.py
```

**Time:** 10-15 minutes total (most time is installer)

---

### COMPREHENSIVE FIX (All-in-one Intel toolkit)

**1. Install Intel oneAPI Base Toolkit:**
- Download: https://www.intel.com/content/www/us/en/developer/tools/oneapi/base-toolkit.html
- Run installer (includes conda + GPU support)
- **Restart your computer** (important!)

**2. Then run training:**
```bash
python quick_train.py
```

**Time:** 10-20 minutes total (largest download)

---

## Expected Result After Fix

After running one of the above:

```bash
python check_gpu_ready.py
```

Should output:
```
[2] Checking Intel Extension for PyTorch (IPEX)...
    ✅ IPEX installed: X.X.X

[3] Checking Intel Arc GPU (XPU) availability...
    ✅ Intel Arc GPU DETECTED
       Device: Intel(R) Arc(R) Alchemist [HAS]
       Total Memory: 8.0 GB

[5] Checking training scripts...
    ✅ quick_train.py has auto-detection
    ✅ train_codette_model.py has device normalization

========================================================================
✅ READY TO TRAIN WITH INTEL ARC GPU!

Run: python quick_train.py
Expected: Training on XPU (Intel Arc GPU)
Speed: ~15-30 minutes (6-10x faster than CPU)
========================================================================
```

---

## Then Train

```bash
python quick_train.py
```

Console will show:
```
CODETTE QUICK START TRAINING
==============================================================================

✅ Intel Arc GPU detected and ready!
  Device: XPU
  Training samples: 5000
  
Starting training...
  Epoch 1/3  - Loss: 4.527 [████████████          ] 35%
  Epoch 2/3  - Loss: 2.134 [████████████████████  ] 100%
  Epoch 3/3  - Loss: 1.234 [████████████████████  ] 100%
  
✅ Training completed in 24 minutes!
```

---

## Documentation

For more details, see:
- `WINDOWS_IPEX_INSTALL.md` - Detailed Windows installation guide
- `INTEL_ARC_QUICK_GUIDE.md` - Complete setup guide with troubleshooting
- `GPU_SETUP_NEXT_STEPS.md` - Next steps after setup

---

## Quick Checklist

- [ ] Chose and started one of the 3 fixes above
- [ ] conda installed: `conda --version` shows version
- [ ] IPEX installed: `conda list | grep intel-extension`
- [ ] GPU detected: `python check_gpu_ready.py` passes all checks
- [ ] Training runs: `python quick_train.py` completes successfully
- [ ] Performance good: Training took 15-30 minutes (not 90-180)

---

**Next step:** Pick one of the 3 fixes above and run it! ⚡
