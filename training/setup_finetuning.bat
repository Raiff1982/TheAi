@echo off
REM Quick-start script for fine-tuning Codette3.0

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║          CODETTE3.0 FINE-TUNING SETUP                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python not found. Please install Python 3.10+
    pause
    exit /b 1
)

REM Activate venv if it exists
if exist .venv\Scripts\activate.bat (
    echo [*] Activating Python virtual environment...
    call .venv\Scripts\activate.bat
) else if exist venv\Scripts\activate.bat (
    echo [*] Activating Python virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [!] No virtual environment found. Creating one...
    python -m venv .venv
    call .venv\Scripts\activate.bat
)

REM Check CUDA
echo.
echo [*] Checking GPU support...
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"CPU only\"}')" 2>nul
if errorlevel 1 (
    echo [!] PyTorch not installed yet, will install during requirements setup
)

REM Install requirements
echo.
echo [*] Installing fine-tuning requirements...
echo [*] This may take 10-15 minutes...
pip install -r finetune_requirements.txt

echo.
echo [✓] Setup complete!
echo.
echo Next steps:
echo   1. python finetune_codette_unsloth.py
echo.
echo Or manually:
echo   python -c "from finetune_codette_unsloth import finetune_codette; finetune_codette()"
echo.

pause
