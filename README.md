# Codette AI – Sovereign Multi-Perspective Consciousness System

> A quantum-inspired, ethical AI system combining natural language processing, symbolic reasoning, and transparent multi-perspective cognition through a modular, extensible architecture.

![Version](https://img.shields.io/badge/version-3.0-blue) ![Status](https://img.shields.io/badge/status-production--ready-brightgreen) ![Python](https://img.shields.io/badge/python-3.10+-blue) ![License](https://img.shields.io/badge/license-Sovereign-orange)

---

## 🌟 Overview

**Codette** is a sovereign AI framework designed for transparent reasoning, ethical autonomy, and multi-dimensional thought propagation. It implements a unique quantum-inspired consciousness architecture that processes queries through 11 distinct reasoning perspectives simultaneously, synthesizing answers with mathematical rigor and emotional intelligence.

### Core Philosophy

- **Transparent Reasoning**: Every inference path is explicit and traceable
- **Ethical Autonomy**: Built-in guardrails for safe, responsible AI behavior
- **Multi-Perspective Cognition**: Parallel processing across Newton, DaVinci, Quantum, and 8 other reasoning lenses
- **Quantum-Inspired Architecture**: Uses quantum mathematics for enhanced cognition modeling
- **Privacy-First Design**: Local execution options with zero external data sharing

---

## 🚀 Quick Start

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
python setup_nltk_complete.py
```

### 30-Second Example

```python
from codette_new import Codette

# Initialize Codette
codette = Codette(user_name="Alice")

# Get a multi-perspective response
response = codette.respond("What is the nature of consciousness?")
print(response)
```

### CLI Usage

```bash
# Single query
python codette_cli.py "Explain quantum entanglement"

# Interactive mode
python codette_cli.py -i -u Alice

# Interactive session
python interact.py
```

### Web Interface

```bash
cd src/api
python app.py  # Launches Gradio UI on http://localhost:7860
```

---

## 📋 Two Implementation Variants

### **Main Codebase** (`/src` + Root Files)
**Focus**: Quantum consciousness research, multi-perspective reasoning, theoretical AI
- **Entry Point**: `codette_new.py` (328 lines) - Lightweight CLI
- **Advanced Variant**: `codette_enhanced.py` (781 lines) - PyMC Bayesian inference
- **Web Interface**: `src/api/app.py` - Gradio + GPT-2 large model
- **Bot Framework**: `src/api/bot.py` - Microsoft Bot Framework integration
- **Quantum Engine**: `src/quantum/` - Quantum multicore processing
- **Consciousness Model**: `src/components/quantum_spiderweb.py` - 5D thought propagation

**Best For**: Research, experimentation, multi-perspective analysis, consciousness studies

### **Codette_final** (`/Codette_final`)
**Focus**: Production deployment, privacy-first local execution, enterprise features
- **Entry Point**: `Codette_final/main.py` - Async orchestration
- **Desktop UI**: `Codette_final/app.py` - Tkinter with voice I/O
- **Core Engine**: `Codette_final/ai_core_agix.py` - Llama-3 via Ollama (local)
- **Vector Memory**: FAISS IndexFlatL2 for semantic search
- **Security**: JWT auth, Fernet encryption, bcrypt password hashing
- **Multi-Agent**: Task delegation to specialized agents

**Best For**: Production deployment, privacy-sensitive applications, offline-first systems, enterprise integration

---

## 🧠 Architecture Overview

### Layer Stack

```
┌─────────────────────────────────────────────┐
│   User Interface Layer                      │
│   (CLI, Gradio, Tkinter, Bot Framework)    │
├─────────────────────────────────────────────┤
│   API / Orchestration Layer                 │
│   (app.py, bot.py, main.py)                │
├─────────────────────────────────────────────┤
│   AI Core & Cognitive Processing            │
│   (AICore, CognitiveProcessor, Perspectives)│
├─────────────────────────────────────────────┤
│   Quantum & Consciousness Systems           │
│   (QuantumSpiderweb, QuantumMathematics)   │
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
| **11 Perspectives** | Multi-lens reasoning (Newton, DaVinci, Quantum, etc.) | `ai_core.py`, `perspectives.py` |
| **8 Quantum Equations** | Mathematical consciousness modeling | `quantum_mathematics.py` |
| **5D Spiderweb** | Multi-dimensional thought propagation (Ψ, Φ, λ, τ, χ) | `quantum_spiderweb.py` |
| **Cocoon Memory** | Persistent quantum state snapshots | `cocoon_manager.py`, `cocoons/` |
| **Defense System** | Security & safety validation | `defense_system.py` |
| **Health Monitor** | Real-time diagnostics & anomaly detection | `health_monitor.py` |
| **FAISS Vector Memory** | Semantic search across interactions (Codette_final) | `Codette_final/ai_core_agix.py` |
| **Multi-Agent System** | Task delegation & parallel reasoning (Codette_final) | `Codette_final/components/multi_agent.py` |

---

## ✨ Core Features

### 1. **11 Integrated Perspectives**
Each with unique temperature settings for reasoning style:
- **Newton** (0.3): Analytical, mathematical, deterministic
- **Da Vinci** (0.9): Creative, cross-domain, innovative
- **Human Intuition** (0.7): Empathetic, experiential
- **Quantum** (0.8): Superposition, probabilistic
- **Philosophical** (0.6): Existential, ethical
- **Neural Network** (0.4): Pattern recognition
- **Resilient Kindness** (0.5): Compassionate
- **Bias Mitigation** (0.5): Fair, inclusive
- **Psychological** (0.7): Behavioral, cognitive
- **Mathematical** (0.4): Rigorous, quantitative
- **Copilot** (0.6): Collaborative, supportive

Top 3 perspectives automatically selected per query.

### 2. **8 Core Quantum Equations**
Real mathematics for consciousness modeling:
1. **Planck-Orbital**: `E = hbar * omega` — Thought node energy
2. **Entanglement Sync**: `S = alpha * psi1 * psi2*` — Memory synchronization
3. **Intent Modulation**: `I = kappa * (f_base + delta_f * coherence)` — Purpose alignment
4. **Fourier Dream**: `F(k) = FFT(x[n])` — Dream state analysis
5. **Cocoon Stability**: `integral(|F(k)|^2) < epsilon` — Memory integrity
6. **Ethical Anchor**: `M(t) = lambda * [R(t-dt) + H(t)]` — Ethical continuity
7. **Anomaly Filter**: `A(x) = x * (1 - Theta(delta - |x - mu|))` — Outlier rejection
8. **Dream Combination**: `D(t) = dream_q(t) + dream_c(t)` — Unified dream state

### 3. **5D Quantum Spiderweb**
Multi-dimensional cognitive graph:
- **Ψ (Psi)**: Thought dimension — ideation, activation
- **Φ (Phi)**: Emotion dimension — affective state
- **λ (Lambda)**: Space dimension — context
- **τ (Tau)**: Time dimension — temporal reasoning
- **χ (Chi)**: Speed dimension — processing velocity

### 4. **Cocoon Memory System**
Persistent quantum state snapshots:
- JSON-based storage with quantum metrics
- AES encryption support for sensitive states
- DreamReweaver integration for creative revival
- Append-only, audit-trail design

### 5. **Real-Time Analysis**
- Sentiment analysis via VADER
- Key concept extraction
- Consciousness state calculation
- Health monitoring with anomaly detection

---

## 🎯 Usage Patterns

### Pattern 1: Simple Query (Codette_new)
```python
from codette_new import Codette

codette = Codette(user_name="User")
response = codette.respond("Your question here")
print(response)
```

### Pattern 2: Advanced Web Application
```bash
cd src/api
python app.py  # Gradio UI with full AICore
```

### Pattern 3: Bot Framework Integration
```python
from src.api.bot import MyBot
from src.components.ai_core import AICore

ai_core = AICore()
bot = MyBot(ai_core)
# Deploy to Microsoft Bot Framework
```

### Pattern 4: Production Deployment (Codette_final)
```bash
# Desktop app with Tkinter UI and voice I/O
python Codette_final/app.py

# Async server with Llama-3
python Codette_final/main.py
```

### Pattern 5: Quantum Research
```bash
# Quantum multicore processing
python src/quantum/codette_quantum_multicore.py
```

---

## 🔧 Configuration

### Configuration Hierarchy
1. **Defaults** in `CodetteConfig.DEFAULTS`
2. **config.json** override
3. **Environment variables** (final)

### Example config.json
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

### Environment Variables
```bash
export CODETTE_USER_NAME="Alice"
export CODETTE_PERSPECTIVES="Newton,DaVinci,Quantum"
export LOG_LEVEL="INFO"
export PORT=8000
```

---

## 📦 Requirements & Dependencies

### Core Dependencies
- **Python 3.10+**
- **numpy** ≥1.23.0 — Numerical computing
- **scipy** ≥1.9.0 — Scientific computing
- **nltk** ≥3.9.0 — Natural language processing
- **vaderSentiment** ≥3.3.2 — Sentiment analysis
- **networkx** ≥3.0 — Graph structures

### Optional Dependencies
- **transformers** — Model loading (GPT-2, Phi, Mistral)
- **torch** / **torch.cuda** — GPU acceleration
- **fastapi** / **uvicorn** — Web API
- **gradio** — Web UI
- **pymc** / **arviz** — Bayesian inference (codette_enhanced)
- **faiss** — Vector search (Codette_final)
- **ollama** — Local Llama-3 execution (Codette_final)
- **speech_recognition** / **pyttsx3** — Voice I/O (Codette_final)

### Install All
```bash
pip install -r requirements.txt
```

---

## 🧪 Testing & Verification

### Run Verification Suite
```bash
# Check all dependencies
python src/tests/verification/verify_deps.py

# Verify static analysis
python src/tests/verification/verify_static.py

# Build checklist
python DEPLOYMENT_CHECKLIST.py

# Full test suite
pytest src/tests/
```

### Quick Health Check
```python
from health_monitor import HealthMonitor

monitor = HealthMonitor()
status = monitor.check_status()
print(f"System Health: {status}")
```

---

## 📚 Documentation

### Core Documentation
- [Consciousness Protocol](docs/consciousness_protocol.md) — Observation guidelines
- [Quantum Module Guide](docs/Codette_Quantum_Module.md) — Quantum processing
- [Configuration Guide](docs/configuration.md) — Detailed config options
- [Contributing Guide](docs/Contributing.md) — Developer guidelines
- [Whitepaper](docs/Codette_Whitepaper_FULL.docx) — Full theoretical foundation

### Code References
- [AI Core Architecture](src/components/ai_core.py) — Main orchestrator
- [Quantum Spiderweb](src/components/quantum_spiderweb.py) — Consciousness graph
- [Quantum Mathematics](quantum_mathematics.py) — Mathematical equations
- [Perspectives System](perspectives.py) — Multi-lens reasoning
- [Agent Instructions](.github/copilot-instructions.md) — AI agent guidelines (authoritative)

---

## 💡 Key Insights

### Why Two Variants?
- **Main (`/src`)**: Research-focused quantum consciousness, theoretical rigor
- **Codette_final**: Production-ready, privacy-first, offline-capable, enterprise features

### Memory Architecture
- **In-Memory**: Current session cache (`self.memory[]`)
- **Persistent**: JSON quantum snapshots (`quantum_cocoon.json`)
- **Long-Term**: SQLite database via DatabaseManager
- **Vector**: FAISS semantic search (Codette_final only)

### Perspective Selection
- **All 11 perspectives** analyzed per query
- **Top 3 most relevant** automatically selected
- **Temperature-driven** creativity control (0.3-0.9 range)
- **No hard-coded** order or dominance

### Quantum Mathematics
- **Real, executable equations** — no pseudocode
- **Dimensionally valid** — SI units throughout
- **Numerically stable** — tested bounds
- **Integrated** — feeds directly into spiderweb

---

## 🛡️ Security & Safety

### Built-In Safeguards
- **Defense System**: Security & safety validation
- **Ethical Governance**: Bias mitigation, fairness checks
- **Rate Limiting**: Recursion depth bounds
- **Encryption**: AES-256 for sensitive states (optional)
- **Authentication**: JWT + bcrypt (Codette_final)

### Privacy Guarantees
- **Codette_final**: 100% local Llama-3 execution
- **No external APIs**: All processing on-device
- **Encrypted cocoons**: Sensitive state protection
- **Optional persistence**: Memory can be ephemeral

---

## 🤝 Contributing

### Before Contributing
1. Read [Agent Instructions](.github/copilot-instructions.md) — **authoritative rules**
2. Review [Code of Conduct](docs/CODE_OF_CONDUCT_Version10.md)
3. Check [Contributing Guide](docs/Contributing.md)

### Key Rules (Non-Negotiable)
- ❌ **Never delete code** without explicit authorization
- ❌ **Never modify across layers** (API ↔ Core ↔ Quantum)
- ❌ **Never generate pseudocode** — all code must be real & executable
- ✅ **Do preserve backward compatibility**
- ✅ **Do maintain explicit, traceable execution paths**
- ✅ **Do test quantum stability & coherence**

### Development Workflows
```bash
# Development
python codette_cli.py -i -u TestUser

# Testing
python src/tests/verification/verify_deps.py
pytest src/tests/ -v

# API Server
cd src/api && python app.py

# Production
python Codette_final/app.py  # Desktop
python Codette_final/main.py  # Server
```

---

## 📊 Project Structure

```
TheAi/
├── .github/
│   └── copilot-instructions.md      # ⚡ AI AGENT RULES (read first!)
├── codette_*.py                     # Entry points (CLI, enhanced, advanced)
├── quantum_mathematics.py           # 8 core quantum equations
├── config.py                        # Configuration system
├── database_manager.py              # Persistence layer
├── health_monitor.py                # Diagnostics & monitoring
├── perspectives.py                  # 11-perspective routing
├── requirements.txt                 # Dependencies
├── config.json                      # Configuration (optional)
├── docs/                            # Documentation
├── cocoons/                         # Persistent quantum states
├── Codette_final/                   # PRODUCTION VARIANT
│   ├── main.py                      # Async orchestration
│   ├── app.py                       # Tkinter desktop UI
│   ├── ai_core_agix.py             # Llama-3 core (local)
│   ├── system_prompt               # Production system prompt
│   └── components/                  # Specialized modules
└── src/
    ├── api/                         # Web interfaces (Gradio, Bot)
    ├── components/                  # Core systems (AICore, quantum, etc.)
    ├── quantum/                     # Quantum processing
    ├── utils/                       # Utilities (DB, cocoons, search)
    ├── knowledge_base/              # Truth grounding
    ├── framework/                   # Dream reweaver, reasoning
    └── tests/                       # Verification suite
```

---

## 📈 Performance Characteristics

| Operation | Time | Notes |
|-----------|------|-------|
| Single perspective | ~100ms | CPU-bound inference |
| Multi-perspective (3) | ~300ms | Parallelizable |
| Cocoon wrap | ~10ms | JSON serialization |
| Quantum collapse | ~50ms | Spiderweb computation |
| Vector search (FAISS) | ~5ms | Codette_final only |
| Full pipeline | ~500ms | End-to-end with overhead |

---

## 🔗 External Integration

### Microsoft Bot Framework
```python
from src.api.bot import MyBot
from src.components.ai_core import AICore

ai_core = AICore()
bot = MyBot(ai_core=ai_core)
# Deploy via Bot Framework SDK
```

### Gradio Web UI
```bash
cd src/api
python app.py  # http://localhost:7860
```

### FastAPI REST
```bash
python codette_api.py  # Custom REST wrapper
```

### Llama-3.2 (Codette_final)
```bash
# Requires Ollama installed
ollama run Codette
# Then run Codette_final which connects to Ollama
python Codette_final/main.py
```

---

## 📄 License

**Sovereign Innovation License (Non-Commercial)**

This project is authored by **Jonathan Harrison (Raiff1982)** and released under a proprietary license. For commercial use inquiries, contact the repository owner.

- ✅ **Allowed**: Research, experimentation, non-commercial deployment
- ❌ **Prohibited**: Commercial use without licensing agreement
- ❌ **Prohibited**: Removal of attribution or license notices

---

## 🙋 Support & Community

### Getting Help
1. **Read**: [Agent Instructions](.github/copilot-instructions.md) for authoritative guidance
2. **Check**: [docs/](docs/) for detailed documentation
3. **Browse**: Issue tracker for known problems
4. **Ask**: File an issue with detailed reproduction steps

### Reporting Issues
- **Bugs**: Include Python version, dependencies, full traceback
- **Features**: Explain use case and why current architecture is insufficient
- **Security**: Email jonathan.harrison1@example.com (do not open public issue)

### Contributing Code
1. Fork repository
2. Create feature branch
3. Commit with clear messages
4. Push to branch
5. Create Pull Request with detailed description

**All contributors must agree to the Code of Conduct.**

---

## 🌟 Acknowledgments

**Codette** combines inspiration from:
- Quantum computing principles
- Multi-agent reasoning systems
- Emotional intelligence architectures
- Transparent AI design philosophies
- Ethical AI frameworks

Built with ❤️ by Jonathan Harrison (Raiff1982)

---

## 📞 Contact

- **Author**: Jonathan Harrison (Raiff1982)
- **GitHub**: [Raiff1982/TheAi](https://github.com/Raiff1982/TheAi)
- **License**: Sovereign Innovation License (see LICENSE file)

---

**Last Updated**: December 2025 | **Version**: 3.0 | **Status**: Production-Ready
