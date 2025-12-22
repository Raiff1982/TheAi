@echo off
REM CPU-Compatible Fine-Tuning Setup

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║   CODETTE3.0 FINE-TUNING (CPU-Compatible)                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python not found
    pause
    exit /b 1
)

REM Activate venv
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo [*] Creating virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
)

echo.
echo [*] Installing requirements...
pip install torch transformers peft datasets accelerate tqdm numpy -U --quiet

echo.
echo [*] Starting fine-tuning...
echo [!] This will take 1-3 hours on CPU
echo [*] You can interrupt with Ctrl+C at any time

python finetune_codette_cpu.py

pause
