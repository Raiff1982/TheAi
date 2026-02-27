# ⚡ GET CONDA NOW - Intel Arc GPU Setup

## You Need Conda (Miniconda)

Your system:
- ✅ Python 3.13.7 installed
- ❌ Conda NOT installed
- ❌ That's why IPEX won't install via pip

**Solution:** Get Miniconda (takes 20 minutes)

---

## RUN THIS NOW

### EASIEST: Auto-Installer (Copy & Paste)

Open PowerShell and paste this entire block:

```powershell
# Download and install Miniconda
Write-Host "Downloading Miniconda..." -ForegroundColor Green
$DownloadPath = "$env:USERPROFILE\Miniconda3-installer.exe"
$Url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"

try {
    # Download
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
    (New-Object System.Net.WebClient).DownloadFile($Url, $DownloadPath)
    
    Write-Host "✅ Download complete! Installing..." -ForegroundColor Green
    
    # Install
    & $DownloadPath /InstallationType=JustMe /RegisterPython=0 /S /D="$env:USERPROFILE\Miniconda3"
    
    Write-Host "✅ Installation starting..." -ForegroundColor Green
    Write-Host "⏳ This may take 5-10 minutes..." -ForegroundColor Yellow
    
    # Wait for installation
    Start-Sleep -Seconds 30
    
    if (Test-Path "$env:USERPROFILE\Miniconda3") {
        Write-Host "✅ Miniconda installed successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "NEXT STEPS:" -ForegroundColor Green
        Write-Host "1. Close this terminal completely" -ForegroundColor Yellow
        Write-Host "2. Open a NEW PowerShell window" -ForegroundColor Yellow
        Write-Host "3. Run: conda install -c intel intel-extension-for-pytorch" -ForegroundColor Yellow
        Write-Host "4. Run: python quick_train.py" -ForegroundColor Yellow
        
        # Cleanup
        Remove-Item $DownloadPath -Force
    }
} catch {
    Write-Host "❌ Installation failed: $_" -ForegroundColor Red
    Write-Host "Download manually from: https://docs.conda.io/projects/miniconda/" -ForegroundColor Yellow
}
```

---

## OR: Manual Download & Install

1. **Download Miniconda:**
   - https://docs.conda.io/projects/miniconda/
   - Choose: **Miniconda3 Windows 64-bit**

2. **Run installer:**
   - Double-click the `.exe` file
   - Accept defaults
   - ✅ CHECK "Add Miniconda3 to PATH"
   - Click Install

3. **Close all terminals, open a NEW one**

4. **Verify:**
   ```bash
   conda --version
   ```
   Should show: `conda X.X.X`

---

## After Miniconda is Installed

```bash
# 1. Install IPEX
conda install -c intel intel-extension-for-pytorch

# 2. Verify
python check_gpu_ready.py

# 3. Train with GPU!
python quick_train.py
```

**Expected:** Training completes in 15-30 minutes (not 90-180!)

---

## Still Not Working?

See detailed guide: **CONDA_SETUP_NO_CONDA.md**

---

## TL;DR

1. Get Miniconda: https://docs.conda.io/projects/miniconda/
2. Install it (check "Add to PATH")
3. Restart terminal
4. Run: `conda install -c intel intel-extension-for-pytorch`
5. Run: `python quick_train.py`

Done! GPU is now enabled! ⚡
