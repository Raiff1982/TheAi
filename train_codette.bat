python -m pip install --upgrade intel-extension-for-pytorch@echo off
REM One-click Codette Training Setup - No Conda Required
REM Uses system Python + pip only

setlocal enabledelayedexpansion

echo ============================================================
echo  Codette AI Training - Setup (No Conda)
echo ============================================================

cd /d "%~dp0"

REM Check if Python is installed
echo.
echo [1/3] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

python --version
echo OK - Python found

REM Activate Intel oneAPI (optional, but improves performance)
echo.
echo [2/3] Loading Intel oneAPI environment...
call "Program Files (x86)InteloneAPI\2025.3\oneapi-vars.bat" >nul 2>&1
if errorlevel 1 (
    echo WARNING: Intel oneAPI not found
    echo Proceeding with standard PyTorch
) else (
    echo OK - Intel oneAPI loaded
)

REM Install PyTorch + dependencies
echo.
echo [3/3] Installing PyTorch and dependencies...
echo This may take 5-10 minutes on first run...
echo.

pip install --upgrade pip setuptools wheel

REM Try PyTorch 2.6+ (latest available)
echo.
echo Attempting PyTorch 2.6.0...
pip install --no-cache-dir torch torchvision torchaudio

if errorlevel 1 (
    echo.
    echo ERROR: PyTorch installation failed
    pause
    exit /b 1
)

REM Verify PyTorch works
echo.
echo Verifying PyTorch installation...
python -c "import torch; print(f'PyTorch {torch.__version__} OK')" >nul 2>&1
if errorlevel 1 (
    echo ERROR: PyTorch verification failed
    pause
    exit /b 1
)

REM Try to install IPEX (optional - won't fail if it doesn't work)
echo.
echo Attempting Intel Extension for PyTorch...
pip install --no-cache-dir intel-extension-for-pytorch >nul 2>&1
python -c "import intel_extension_for_pytorch; print('IPEX OK')" >nul 2>&1
if not errorlevel 1 (
    echo IPEX installed successfully
) else (
    echo IPEX not available - will use CPU training
)

REM Start training
echo.
echo ============================================================
echo  Starting Codette Training...
echo ============================================================
echo.
echo Device detection (GPU or CPU will be chosen automatically):
python -c "import torch; print(f'  CPU cores: {torch.get_num_threads()}')" 2>nul

echo.
python quick_train.py

REM Show results location
if errorlevel 1 (
    echo.
    echo ERROR: Training failed
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  SUCCESS!
echo ============================================================
echo.
echo Codette model saved to: codette_model\
echo View results in: training_logs\
echo.
pause
