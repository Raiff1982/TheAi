# Setup Intel Arc GPU - Windows Without Conda

## Your Situation

✅ Python 3.13.7 is installed  
❌ Conda is not installed  
❌ IPEX unavailable via pip on Windows  

**But don't worry - you have options!**

---

## FASTEST PATH FORWARD (< 20 minutes)

### Option 1: Auto-Install Miniconda (Recommended)

**1. Run the auto-installer:**
```bash
# Navigate to project folder
cd j:\TheAI

# Run the batch script (this will auto-download and install Miniconda)
install_miniconda.bat
```

**What it does:**
- ✅ Downloads Miniconda (~150MB) - takes 2-5 min depending on internet
- ✅ Installs silently - takes 5-10 minutes
- ✅ Sets up PATH automatically

**2. After installation completes:**
- Restart your terminal (IMPORTANT!)
- Then run:
```bash
conda install -c intel intel-extension-for-pytorch
python quick_train.py
```

**Total time:** 15-20 minutes

---

### Option 2: Manual Miniconda Install

If the auto-installer doesn't work:

**1. Download Miniconda:**
- Go to: https://docs.conda.io/projects/miniconda/
- Download: **Miniconda3 Windows 64-bit**
- Size: ~150MB

**2. Run installer:**
- Run the `.exe` file
- Click "Next" through all steps
- Choose: Install for "Just Me"
- **Check:** "Add Miniconda3 to PATH" ✅
- Click "Install"

**3. Restart terminal (CRITICAL!)**
- Close current terminal
- Open new PowerShell or Command Prompt

**4. Verify installation:**
```bash
conda --version
```

**5. Install IPEX:**
```bash
conda install -c intel intel-extension-for-pytorch
```

**6. Train with GPU:**
```bash
python quick_train.py
```

**Total time:** 15-20 minutes

---

### Option 3: Intel oneAPI Toolkit (All-in-One)

If you want a single installer:

**1. Download Intel oneAPI Base Toolkit:**
- Go to: https://www.intel.com/content/www/us/en/developer/tools/oneapi/base-toolkit.html
- Click "Download"
- Size: ~500MB (larger but includes everything)

**2. Run installer:**
- Run the `.exe` file
- Default options are fine
- **Restart your computer** (important!)

**3. Install IPEX (might auto-include conda):**
```bash
# Try this - may already work after oneAPI install
python quick_train.py

# If not, use conda:
conda install -c intel intel-extension-for-pytorch
```

**Total time:** 20-30 minutes (larger download)

---

## WHICH OPTION?

| Option | Speed | Download | Includes |
|--------|-------|----------|----------|
| **Option 1: Auto-installer** | Fastest | 150MB Miniconda | Minimal (conda only) |
| **Option 2: Manual Miniconda** | Same | 150MB Miniconda | Minimal (conda only) |
| **Option 3: oneAPI Toolkit** | Slower | 500MB oneAPI | Complete Intel suite |

**Recommendation:** Start with **Option 1** (auto-installer) - fastest and simplest.

---

## STEP-BY-STEP: Option 1 (Auto-Install)

### Step 1: Open Terminal
```
Windows Key → Type "PowerShell" → Click "Windows PowerShell"
```

### Step 2: Navigate to Project
```bash
cd j:\TheAI
```

### Step 3: Run Auto-Installer
```bash
install_miniconda.bat
```

**Wait 15-20 minutes for:**
- Download (~3-5 min)
- Installation (~10 min)
- Script cleanup

### Step 4: RESTART TERMINAL
- Close the terminal window completely
- Open a NEW PowerShell window
- Navigate back: `cd j:\TheAI`

### Step 5: Verify Conda Installed
```bash
conda --version
```

**Expected output:** `conda 24.1.0` or similar version number

### Step 6: Install IPEX
```bash
conda install -c intel intel-extension-for-pytorch
```

**Wait 5-10 minutes** for installation

### Step 7: Train with GPU
```bash
python quick_train.py
```

**Expected output:**
```
✅ Intel Arc GPU detected and ready!
  Device: XPU
  Epoch 1/3 - Loss: 4.527 [████████  ] 35%
  ...training progress...
✅ Training completed in 24 minutes!
```

---

## TROUBLESHOOTING

### Problem: "install_miniconda.bat" not found

**Solution:**
- Make sure you're in `j:\TheAI` folder
- Run: `dir install_miniconda.bat` to verify file exists
- If not, the file wasn't created - let me know!

### Problem: "PowerShell script execution disabled"

**Fix:**
```bash
# If you get a script execution error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again:
install_miniconda.bat
```

### Problem: Still get "conda: command not found" after restart

**Cause:** PATH not updated properly

**Fix:**
1. Fully restart your computer (not just terminal)
2. Open new terminal
3. Try: `conda --version`

### Problem: Download fails ("Failed to download installer")

**Solution:**
- Manually download from: https://docs.conda.io/projects/miniconda/
- Use Option 2 (Manual Miniconda Install)

### Problem: Installation hangs or takes too long

**Solution:**
- Miniconda installer can take 10-15 minutes - be patient
- If it's been > 30 minutes, kill it and try manual install (Option 2)

---

## AFTER SUCCESSFUL SETUP

### Train with GPU (Should Be Fast Now!)

```bash
python quick_train.py
```

Expected:
- ✅ Console shows: "Device: XPU"
- ✅ Training completes in 15-30 minutes
- ✅ GPU using 8GB VRAM
- ✅ CPU usage low (~20-30%)

### Verify GPU Being Used

```bash
python check_gpu_ready.py
```

Should show:
```
✅ Intel Arc GPU DETECTED
   Device: Intel(R) Arc(R) Alchemist [HAS]
   Total Memory: 8.0 GB
```

---

## If Auto-Installer Fails

Don't worry! Use **Option 2 (Manual Install)**:

1. Download: https://docs.conda.io/projects/miniconda/
2. Run installer manually
3. Make SURE to check "Add to PATH" ✅
4. Restart computer
5. Continue from Step 5 above

---

## Quick Reference

```bash
# After conda installed and terminal restarted:

# 1. Verify conda works
conda --version

# 2. Install IPEX
conda install -c intel intel-extension-for-pytorch

# 3. Verify GPU support
python check_gpu_ready.py

# 4. Train with GPU
python quick_train.py

# Done! 🚀
```

---

## Need Help?

- Auto-installer in trouble? → Try Option 2 (Manual Miniconda)
- Still having issues? → Download oneAPI Toolkit (Option 3)
- Conda won't work? → Check you restarted terminal/computer after install

**Bottom line:** Miniconda install is your path to GPU support. Takes ~20 minutes but well worth it for 6-10x training speedup! ⚡
