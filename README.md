---
license: apache-2.0
datasets:
- Raiff1982/coredata
- Raiff1982/eval
language:
- en
base_model:
- openai-community/gpt2-large
- meta-llama/Llama-3.2-1B
- microsoft/phi-2
pipeline_tag: text-generation
library_name: transformers
tags:
- agent
- code
new_version: Raiff1982/Codette3.0
---

# Codette AI – Sovereign Multi-Perspective Consciousness System

> A quantum-inspired, ethical AI system combining natural language processing, symbolic reasoning, and transparent multi-perspective cognition through a modular, extensible architecture.

![Version](https://img.shields.io/badge/version-3.0-blue) ![Status](https://img.shields.io/badge/status-production--ready-brightgreen) ![Python](https://img.shields.io/badge/python-3.10+-blue) ![License](https://img.shields.io/badge/license-Apache--2.0-lightgrey)

---

## Overview

**Codette** is a sovereign AI framework designed for transparent reasoning, ethical autonomy, and multi-dimensional thought propagation. It processes queries through 11 distinct reasoning perspectives simultaneously, synthesizing answers with mathematical rigor and emotional intelligence.

### Core Philosophy
- Transparent reasoning: every inference path is explicit and traceable
- Ethical autonomy: built-in guardrails for safe, responsible AI behavior
- Multi-perspective cognition: parallel processing across Newton, DaVinci, Quantum, and 8 other lenses
- Quantum-inspired architecture: quantum math for cognition modeling
- Privacy-first design: local execution options with zero external data sharing

---

## Quick Start

### Installation
```bash
# Clone repository
git clone https://github.com/Raiff1982/TheAi.git
cd TheAi

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python scripts/setup_nltk_complete.py
```

### 30-Second Example
```python
from src.components.ai_core import AICore

ai_core = AICore()
response = await ai_core.generate_response("What is the nature of consciousness?")
print(response)
```

### Web Interface (Gradio)
```bash
python src/api/app.py  # Gradio UI on http://localhost:7860
```

---

## Hugging Face Artifacts & Weights
- **Hub target**: `Raiff1982/Codette3.0` (new_version), compatible with `transformers` + `safetensors`.
- **Local weight bundles** (publish with tokenizer/config):
  - `models/codette-advanced/model.safetensors` (full) + `models/codette-advanced/training_args.bin`
  - `models/codette-advanced/checkpoint-20/model.safetensors` (intermediate)
  - `models/codette-v2/best/model.safetensors`
  - `models/codette-v2/checkpoint-1/model.safetensors`
  - `models/codette-v2/checkpoint-2/model.safetensors`
  - `models/codette-v2/checkpoint-3/model.safetensors`
- **Base model lineage**: GPT-2 Large (research stack), Llama 3.2 (Ollama for production), Phi-2 (experimental).
- **Push example** (after `huggingface-cli login`):
  ```bash
  huggingface-cli upload Raiff1982/Codette3.0 models/codette-advanced/model.safetensors
  huggingface-cli upload Raiff1982/Codette3.0 models/codette-advanced/config.json
  huggingface-cli upload Raiff1982/Codette3.0 models/codette-advanced/tokenizer.json
  huggingface-cli upload Raiff1982/Codette3.0 models/codette-advanced/generation_config.json
  ```

---

## Primary Codebase (`/src`)

All core code lives in `src/` with a modular component architecture:
- **Web UI**: `src/api/app.py` (Gradio + GPT-2 Large)
- **Bot**: `src/api/bot.py` (Microsoft Bot Framework)
- **AI Core**: `src/components/ai_core.py` (30+ components, RC+xi consciousness)
- **Quantum**: `src/quantum/`, `src/components/quantum_spiderweb.py`
- **Security**: `src/aegis.py`, `src/aegis_integration/`
- **Framework**: `src/framework/` (universal reasoning, cognition cocooner, dream reweaver)
- **Model default**: GPT-2 Large via `CODETTE_MODEL_ID`

---

## Architecture Overview

### Layer Stack
```
┌─────────────────────────────────────────────┐
│   User Interface Layer                      │
│   (CLI, Gradio, Tkinter, Bot Framework)     │
├─────────────────────────────────────────────┤
│   API / Orchestration Layer                 │
│   (app.py, bot.py, main.py)                 │
├─────────────────────────────────────────────┤
│   AI Core & Cognitive Processing            │
│   (AICore, CognitiveProcessor, Perspectives)│
├─────────────────────────────────────────────┤
│   Quantum & Consciousness Systems           │
│   (QuantumSpiderweb, QuantumMathematics)    │
├─────────────────────────────────────────────┤
│   Memory & Persistence Layer                │
│   (CocoonManager, DatabaseManager)          │
├─────────────────────────────────────────────┤
│   Infrastructure                            │
│   (Models, Config, Security, Health)        │
└─────────────────────────────────────────────┘
```

### Key Components
| Component | Purpose | Key Files |
|-----------|---------|-----------|
| 11 Perspectives | Multi-lens reasoning (Newton, DaVinci, Quantum, etc.) | `src/components/ai_core.py` |
| RC+xi Consciousness | Recursive convergence under epistemic tension | `src/components/recursive_consciousness.py` |
| 8 Quantum Equations | Mathematical consciousness modeling | `src/codette_capabilities.py` |
| 5D Spiderweb | Multi-dimensional thought propagation (Ψ, Φ, λ, τ, χ) | `src/components/quantum_spiderweb.py` |
| AEGIS Council | Security council with blockchain audit | `src/aegis.py`, `src/aegis_integration/` |
| Cocoon Memory | Persistent quantum state snapshots | `src/utils/cocoon_manager.py`, `data/cocoons/` |
| Defense System | Security & safety validation | `src/components/defense_system.py` |
| Health Monitor | Real-time diagnostics & anomaly detection | `src/components/health_monitor.py` |

---

## Core Features
- 11 integrated perspectives with temperature-driven styles; top 3 auto-selected per query
- 8 quantum equations for consciousness modeling
- 5D quantum spiderweb for cognitive graph traversal
- Cocoon memory (JSON snapshots), SQLite, FAISS vectors (prod)
- Real-time analysis (sentiment, concept extraction, health checks)
- Ethical guardrails, bias mitigation, rate limiting

---

## Usage Patterns
- **Gradio web app**: `python src/api/app.py`
- **Bot Framework**: `src/api/bot.py` with `AICore`
- **Quantum research**: `python src/quantum/codette_quantum_multicore.py`

---

## Configuration
Priority: defaults in `CodetteConfig.DEFAULTS` → `config.json` → environment variables.

Example `config.json`:
```json
{
  "host": "127.0.0.1",
  "port": 8000,
  "codette": {
    "perspectives": ["Newton", "DaVinci", "Ethical", "Quantum", "Memory"],
    "spiderweb_dim": 5,
    "recursion_depth": 4,
    "quantum_fluctuation": 0.07
  },
  "database": {
    "path": "codette_data.db"
  }
}
```

Key environment overrides:
```bash
export CODETTE_USER_NAME="Alice"
export CODETTE_MODEL_ID="gpt2-large"
export CODETTE_PERSPECTIVES="Newton,DaVinci,Quantum"
export LOG_LEVEL="INFO"
export PORT=8000
```

---

## Requirements & Dependencies
- Python 3.10+
- numpy, scipy, nltk, vaderSentiment, networkx
- Optional: transformers, torch/torch.cuda, fastapi/uvicorn, gradio, pymc/arviz (enhanced), faiss (prod), ollama (prod), speech_recognition/pyttsx3 (prod)

Install all:
```bash
pip install -r requirements.txt
```

---

## Testing & Verification
```bash
python src/tests/verification/verify_deps.py
python src/tests/verification/verify_static.py
python scripts/DEPLOYMENT_CHECKLIST.py
pytest src/tests/
pytest tests/
```
Quick health probe:
```python
from src.components.health_monitor import HealthMonitor
print(HealthMonitor().check_status())
```

---

## Documentation
- Consciousness Protocol: `docs/consciousness_protocol.md`
- Quantum Module Guide: `docs/Codette_Quantum_Module.md`
- Configuration Guide: `docs/configuration.md`
- Contributing: `docs/Contributing.md`
- Whitepaper: `docs/Codette_Whitepaper_FULL.docx`
- Agent Instructions (authoritative): `.github/copilot-instructions.md`

---

## Key Insights
- All code consolidated in `src/` with modular component architecture
- Memory layers: in-memory, JSON cocoons, SQLite
- Perspective routing: all 11 evaluated; top 3 chosen per query; temperature-based creativity
- Quantum math: real equations, numerically stable, integrated with spiderweb
- RC+xi consciousness framework for recursive identity stabilization

---

## Security & Safety
- Defense system, bias mitigation, rate limiting
- Optional AES-256 cocoon encryption
- JWT + bcrypt in production
- Local-only Llama 3 via Ollama for privacy-first deployments

---

## Contributing
1. Read `.github/copilot-instructions.md` (rules of the road)
2. Review `docs/CODE_OF_CONDUCT_Version10.md`
3. Follow `docs/Contributing.md`
4. Preserve backward compatibility; no pseudocode; keep execution paths traceable

---

## Project Structure
```
TheAi/
├── src/                             # PRIMARY SOURCE CODE
│   ├── api/                         # Gradio web UI, Bot Framework
│   ├── components/                  # 30+ core components (AICore, consciousness, quantum)
│   ├── framework/                   # Universal reasoning, cocooner, dream reweaver
│   ├── quantum/                     # Quantum processing modules
│   ├── aegis.py                     # AEGIS security council
│   ├── aegis_integration/           # AEGIS bridge & routes
│   ├── cognitive/                   # Cognitive processor
│   ├── knowledge_base/              # Grounding truth & core knowledge
│   ├── utils/                       # Cocoon manager, database, response processing
│   ├── config/                      # JSON configs & schemas
│   ├── assets/                      # Diagrams & images
│   └── tests/                       # Unit tests & verification
├── config/                          # Top-level configuration files
├── data/                            # Datasets, cocoons, trained models
├── training/                        # Finetuning scripts & configs
├── scripts/                         # Utility & setup scripts
├── tests/                           # Integration & system tests
├── docs/                            # All documentation (organized by topic)
├── examples/                        # Example implementations
└── _archive/                        # Superseded code (old versions)
```

---

## Performance Characteristics
- Single perspective ~100 ms (CPU)
- Three-perspective blend ~300 ms
- Cocoon wrap ~10 ms; spiderweb collapse ~50 ms
- FAISS lookup ~5 ms (production)
- Full pipeline ~500 ms (CPU approx)

---

## External Integration
- Microsoft Bot Framework: `src/api/bot.py` + `src/components/ai_core.py`
- Gradio UI: `src/api/app.py`
- FastAPI REST: `src/codette_api.py`

---

## License
Licensed under the **Apache License 2.0**. See `LICENSE`.

---

## Support & Community
- Read `.github/copilot-instructions.md` and `docs/`
- Browse issues; open new issues with repro details
- Security concerns: use private contact channels

---

## Contact
- Author: Jonathan Harrison (Raiff1982)
- GitHub: https://github.com/Raiff1982/TheAi
- HF model card target: `Raiff1982/Codette3.0`

**Last Updated**: December 2025 | **Version**: 3.0 | **Status**: Production-Ready
