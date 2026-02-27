"""
Local convenience runner for the official HF `run_clm.py` script.

Why: The SageMaker launcher now lives in `launch_sagemaker.py` to avoid pulling
`sagemaker` into local environments. This file simply forwards arguments to the
Hugging Face example script if it is present.

Usage:
    python run_clm.py --model_name_or_path openai-community/gpt2-large ...

Requirements:
    - transformers>=4.56.2, datasets, accelerate, torch (GPU optional)
    - `examples/pytorch/language-modeling/run_clm.py` available in this repo
      (from the HF Transformers checkout).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


HF_RUN_CLM = Path(__file__).parent / "examples" / "pytorch" / "language-modeling" / "run_clm.py"


def main() -> int:
    if not HF_RUN_CLM.exists():
        msg = (
            "Missing HF example script at "
            f"{HF_RUN_CLM}. Clone/checkout `transformers` with examples or "
            "point directly to the script you want to run."
        )
        raise SystemExit(msg)

    cmd = [sys.executable, str(HF_RUN_CLM), *sys.argv[1:]]
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())

