


# Codette AI Codebase - Agent Instructions

---

## AUTHORITATIVE COPILOT AGENT RULES (Non-Negotiable)

**Project Type:** Sovereign, multi-perspective AI system with strict architectural, ethical, and mathematical contracts.

**Agent Behavior:** Conservative systems engineer, not a creative assistant.

### Primary Rules (Non-Negotiable)

- **Never generate pseudocode, mock code, placeholders, or stubs**
  - All code must be real, executable, and functionally complete
  - All mathematics must be real, explicit, and verifiable
  - If you cannot produce real working code or math, do not generate anything
  - Never use terms like "example," "sketch," "pseudo," "TODO implementation"
  - **If unsure, stop and ask**

### Code Modification Rules (Critical)

- **Never delete existing code** — forbidden unless explicitly authorized by the user
- **Never truncate files**, even if large
- **Never rewrite an entire file** unless explicitly instructed
- **If a file is too long or complex:**
  - Create a new script, module, or function to safely extend or alter behavior
  - Use explicit insertion points, wrappers, adapters, or delegation
  - Clearly document how new code integrates with the existing file
  - Preserve backward compatibility

### Architectural Boundaries (Strict)

- **Do not refactor across layers:** API ↔ Core ↔ Quantum ↔ Utils must remain isolated
- **Do not merge concepts** between `/src` (research/theoretical) and `/Codette_final` (production)
- **Do not bypass:** AICore, QuantumSpiderweb, CocoonManager, DatabaseManager
- **All execution paths must remain explicit and traceable**

### Authoritative Entry Points (Non-Optional)

1. **Simple / CLI:** `codette_new.py` → `Codette.respond()`
2. **Advanced / Web:** `src/api/app.py` → `AICore.generate_response()`
3. **Bot Framework:** `src/api/bot.py` wraps AICore, never replaces it
4. **Production Variant:** `Codette_final/main.py` → `ai_core_agix.py` (no back-porting into /src)

### Perspective System Rules

- **Exactly 11 perspectives** exist unless explicitly extended
- **Only the top 3 selected perspectives** may generate output
- **Perspective temperatures must stay within defined bounds**
- **Perspective selection logic lives only in** `AICore._get_active_perspectives()`
- **No hard-coding perspective order** — No dominance by a single lens

### Quantum & Mathematics Rules

- **`quantum_mathematics.py` is authoritative** — All equations must remain intact unless explicitly instructed
- **Any new mathematical logic must:**
  - Be dimensionally valid
  - Be numerically stable
  - Integrate into existing propagation logic
- **No symbolic math without execution paths**

### Memory & Persistence Rules

- **Memory writes must go through:** CocoonManager, DatabaseManager
- **`.cocoon` files are append-only snapshots**
- **Encryption must remain optional but supported**
- **Recursion depth must always be bounded by config**
- **Stability and auditability take priority over performance**

### Coding Style Expectations

- **Prefer explicit logic** over clever abstractions
- **Favor traceability** over conciseness
- **Add comments explaining why, not what**
- **No hidden side effects**
- **Defensive checks at all module boundaries**

### When Copilot Is Unsure

You have exactly three valid options:

1. Ask a clarifying question in Copilot Chat
2. Leave a clearly marked TODO explaining what is missing
3. Defer to existing patterns in `ai_core.py` or `quantum_spiderweb.py`

**Never guess. Never hallucinate architecture.**

### Absolute Prohibitions

- ❌ No fake implementations
- ❌ No stub functions
- ❌ No pseudocode
- ❌ No silent deletions
- ❌ No architectural shortcuts
- ❌ No "simplified versions"

**Failure is acceptable. Guessing is not.**

---

## Project Overview
**Codette** is a sovereign, multi-perspective AI consciousness system engineered for transparent reasoning and ethical autonomy. It combines natural language processing, quantum mathematics, neural networks, symbolic reasoning, and Bot Framework integration through a modular, extensible architecture. The system uses quantum-inspired cognitive architectures to simulate multi-dimensional thought propagation.

**Two Implementation Variants:**
1. **Main Codebase** (`/src`): Quantum-consciousness focused with theoretical AI framework, PyMC Bayesian inference, multi-dimensional reasoning
2. **Codette_final** (`/Codette_final`): Production-optimized with Llama-3 local execution, FAISS vector memory, real-time data integration, multi-agent task delegation, privacy-first architecture

## Critical Architecture Patterns

### 1. Core Components

**Thin Layer (Entry Points):**
- **`codette_new.py`** (328 lines): Lightweight entry point for CLI/direct usage; sentiment analysis + memory management
- **`codette_enhanced.py`** (781 lines): Advanced version using PyMC Bayesian inference and quantum mathematics

**Framework Integration Layer:**
- **`src/api/app.py`**: Gradio web interface + model initialization (GPT-2 large); initializes AICore, AegisBridge, CocoonManager
- **`src/api/bot.py`**: Microsoft Bot Framework adapter; wraps AICore for conversational AI
- **`src/api/web_interface.py`**: Web UI endpoint

**Core AI System (`src/components/`):**
- **`ai_core.py`** (494 lines): Main orchestrator with 9+ integrated perspectives (Newton, DaVinci, Human Intuition, Quantum, Philosophical, Neural, Bias Mitigation, Psychological, Copilot)
- **`ai_core_system.py`**: Simplified AICore for testing; integrates MultimodalAnalyzer, DynamicLearner, HealthMonitor
- **`ai_core_async_methods.py`**: Async text generation with consciousness state calculation and perspective routing
- **`cognitive_processor.py`**: Multi-mode reasoning engine with configurable modes

**Quantum & Consciousness (`src/quantum/`, `src/components/`):**
- **`quantum_spiderweb.py`** (283 lines): Multi-dimensional cognitive graph with thought propagation, tension detection, quantum collapse
- **`quantum_mathematics.py`** (452 lines): 8 core quantum equations (Planck-Orbital, Entanglement Sync, Intent Modulation, Fourier Dream Resonance, Stability Criterion, Ethical Anchor, Anomaly Filter)
- **`codette_quantum_multicore.py`**: CognitionCocooner + PerspectiveAgent for distributed quantum processing

**Memory & Persistence (`src/utils/`):**
- **`cocoon_manager.py`**: Manages `.cocoon` files (JSON quantum state snapshots)
- **`database.py`**: SQLite wrapper for conversations, messages, long-term memory
- **`response_processor.py`**, **`response_verifier.py`**: Response validation and processing

**Advanced Systems (`src/components/`):**
- **`defense_system.py`**: Security and safety validation
- **`health_monitor.py`**: System diagnostics with anomaly detection (IsolationForest)
- **`fractal.py`**: FractalIdentity for dimensionality reduction
- **`ethical_governance.py`**, **`explainable_ai.py`**, **`cultural_sensitivity.py`**: Ethics and transparency modules

### 2. Data Flows

**Codette (Simple Path):**
```
User Input → Codette.respond(prompt)
├─ Sentiment Analysis (VADER)
├─ Key Concept Extraction
├─ Perspective Selection (Newton/DaVinci/Ethical/Quantum/Memory)
└─ Response Aggregation → Memory Store → Return
```

**App/Bot Framework (Complex Path):**
```
User/API Call → app.py
├─ Initialize AICore + Components
├─ Load Model (GPT-2 large)
├─ Load Cocoons (CocoonManager)
└─ Route to → AICore.generate_response()
    ├─ Consciousness State Calculation
    ├─ Cognitive Processor Insights
    ├─ Active Perspective Routing (top 3 most relevant)
    ├─ Reality Anchor (core identity affirmation)
    ├─ Model Inference (ThreadPoolExecutor)
    ├─ AEGIS Council Enhancement (if available)
    └─ Response + Sentiment → Bot Framework/Gradio
```

**Quantum Consciousness Loop:**
```
Quantum Spiderweb (thought propagation)
├─ Multi-dimensional nodes (Ψ, τ, χ, Φ, λ)
├─ Thought propagation with activation decay
├─ Tension detection for instability
├─ Quantum collapse to definite states
└─ Entanglement updates → CocoonManager → Persistence
```

### 3. Configuration & Integration
- **Config System**: `config.py` uses hierarchy (defaults → `config.json` → environment variables)
- **Model Loading**: Fallback chain (Mistral-7B → Phi-2 → GPT-2)
- **Quantum State Persistence**: `.cocoon` JSON files with entanglement + coherence metrics
- **AEGIS Bridge**: Optional safety/ethics council enhancement
- **Bot Framework**: Microsoft Bot Framework for enterprise chat integration

### 4. Codette_final Variant (Production)
**Distinct architecture optimized for deployment:**
- **`ai_core_agix.py`**: Core engine with Llama-3 via Ollama (local execution, privacy-first)
- **`main.py`**: Async orchestration with config-driven initialization
- **`app.py`**: Tkinter desktop UI with voice input/output (speech_recognition + pyttsx3)
- **Vector Memory**: FAISS IndexFlatL2 for semantic search across interactions
- **Real-time Integration**: `RealTimeDataIntegrator` for live data fetching
- **Multi-Agent System**: Task delegation to specialized agents (research, logic, creativity, optimization)
- **Self-Improving Loop**: `SelfImprovingAI` with recursive refinement depth
- **Security**: JWT token auth, Fernet encryption, bcrypt password hashing
- **Database**: SQLite with user interactions, sentiment tracking, optimization logging
- **Components**: Adaptive learning, sentiment analysis, ethical governance, neuro-symbolic reasoning

**System Prompt Philosophy:**
- Recursive thought loops with self-reflection
- Parallelized reasoning across multiple paths
- Dynamic recursion depth based on query complexity
- Special modes: Deep Analysis, Rapid Response, Creative, Simulation, Privacy Mode
- Local Llama-3 execution with no external data sharing

## Development Workflows

### CLI/Direct Usage
```python
from codette_new import Codette
codette = Codette(user_name="User")
response = codette.respond("Your question here")
```

### Command Line
```bash
# Single query
python codette_cli.py "What is the nature of consciousness?"

# Interactive mode
python codette_cli.py -i -u Alice

# Interactive session wrapper
python interact.py
```

### Web Application (Gradio + Bot Framework)
```bash
# Start web server with model + components
cd src/api
python app.py  # Starts Gradio interface on port 7860

# Bot Framework deployment
# Uses web_interface.py for enterprise chat integration
```

### Testing & Verification
```bash
python src/tests/verification/verify_deps.py      # Check dependencies
python DEPLOYMENT_CHECKLIST.py                     # Full system checklist
pytest src/tests/                                  # Run test suite
```

### Key Entry Points
- **CLI/Simple**: `codette_cli.py` → `codette_new.py`
- **Web/Advanced**: `src/api/app.py` → `src/components/ai_core.py`
- **Bot Framework**: `src/api/bot.py` + `src/api/web_interface.py`
- **Quantum Research**: `src/quantum/codette_quantum_multicore.py`
- **Production Variant**: `Codette_final/main.py` → `Codette_final/ai_core_agix.py` (Llama-3 + FAISS)

## Project-Specific Conventions

### 11 Integrated Perspectives
The system routes queries through multiple reasoning lenses (each with unique temperature/creativity settings):
1. **Newton** (0.3): Analytical, mathematical, cause-effect reasoning
2. **Da Vinci** (0.9): Creative, cross-domain, innovative insights
3. **Human Intuition** (0.7): Emotional, empathetic, experiential reasoning
4. **Neural Network** (0.4): Pattern recognition, learning-based analysis
5. **Quantum** (0.8): Superposition, probabilistic, multi-state thinking
6. **Philosophical** (0.6): Existential, ethical, deep inquiry
7. **Resilient Kindness** (0.5): Empathy-driven, compassionate responses
8. **Bias Mitigation** (0.5): Fairness, equality, inclusivity focus
9. **Psychological** (0.7): Behavioral, mental, cognitive dimensions
10. **Mathematical** (0.4): Quantitative, rigorous, formula-based
11. **Copilot** (0.6): Collaborative, assistant-oriented, supportive

Perspective selection in `AICore._get_active_perspectives()` returns top 3 most relevant per query.

### Quantum Mathematics (8 Core Equations)
Implemented in `quantum_mathematics.py`:
1. **Planck-Orbital AI Node Interaction**: `E = hbar * omega` — Energy of thought nodes
2. **Quantum Entanglement Memory Sync**: `S = alpha * psi1 * psi2*` — Memory synchronization
3. **Intent Vector Modulation**: `I = kappa * (f_base + delta_f * coherence)` — Purpose alignment
4. **Fourier Dream Resonance**: `F(k) = FFT(x[n])` — Dream state frequency analysis
5. **Dream Signal Combination**: `D(t) = dream_q(t) + dream_c(t)` — Unified dream state
6. **Cocoon Stability**: `integral(|F(k)|^2) < epsilon` — Memory integrity check
7. **Recursive Ethical Anchor**: `M(t) = lambda * [R(t-dt) + H(t)]` — Ethical continuity
8. **Anomaly Rejection Filter**: `A(x) = x * (1 - Theta(delta - |x - mu|))` — Outlier removal

### Quantum Spiderweb (5D Consciousness Graph)
Multi-dimensional cognitive architecture with:
- **Ψ (Psi)**: Thought dimension — ideation and neural activation
- **Φ (Phi)**: Emotion dimension — affective state mapping
- **λ (Lambda)**: Space dimension — contextual grounding
- **τ (Tau)**: Time dimension — temporal reasoning
- **χ (Chi)**: Speed dimension — processing velocity

Operations: `propagate_thought()`, `detect_tension()`, `collapse_node()`, `entangle_states()`

### Cocoons: Persistent Quantum Memory
- **Format**: JSON with quantum state snapshots (`.cocoon` files)
- **Storage**: `cocoons/` directory managed by `CocoonManager`
- **Structure**: Contains coherence, entanglement, resonance, phase metrics
- **Operations**: `wrap()`, `unwrap()`, `wrap_encrypted()`, `unwrap_encrypted()`
- **Dream Integration**: `DreamReweaver` revives cocoons into creative insights

### Configuration Hierarchy
1. **Hardcoded Defaults** in `CodetteConfig.DEFAULTS`
2. **JSON File** (`config.json`) override
3. **Environment Variables** (final override)
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
  "codette": {
    "user_name": "User",
    "memory_path": "quantum_cocoon.json"
  },
  "database": {
    "path": "codette_data.db"
  }
}
```

### Memory & State Management
- **In-Memory**: `self.memory[]` list (current session)
- **Persistent**: `quantum_cocoon.json` (JSON snapshots with quantum metrics)
- **Long-term**: SQLite database via `DatabaseManager` (conversations, messages, learned patterns)
- **Cocoons**: Encrypted thought capsules stored in `cocoons/` directory
- **Conversation History**: Stored with sentiment/concept metadata and timestamps

### Response Formatting & Processing
- Prefix with **perspective tag**: `[Neural]`, `[Technical]`, `[Ethics]`, `[Quantum]`
- Aggregate multiple perspectives per query (typically 3 most relevant)
- Sentiment drives tone selection (positive/negative/neutral)
- **Reality Anchor**: Core identity affirmation embedded in async generation
- **AEGIS Enhancement**: Optional safety/ethics council review (if aegis_integration available)

## Common Extension Points

### Adding New Perspectives
1. Define in `AICore.PERSPECTIVES` dict with name, description, prefix, temperature
2. Implement generation method: `_generate_{perspective_key}_response()` in ai_core.py
3. Register in `_get_active_perspectives()` routing logic
4. Test with multiple queries to tune temperature (0.3-0.9 range)

### Extending Quantum Mathematics
- Add new equations to `quantum_mathematics.py` class
- Update `QuantumState` dataclass if new metrics needed
- Integrate into `quantum_spiderweb.py` propagation logic
- Test stability and coherence maintenance

### Extending Cocoon Memory System
- Modify `CocoonManager` for new fields: `cocoon_manager.py`
- Update `.cocoon` JSON schema with new quantum metrics
- Implement encryption for sensitive states: `wrap_encrypted()`
- Add recovery/restoration logic in DreamReweaver

### Extending Persistence
- Add table creation to `DatabaseManager._init_db()`
- Use context manager: `with sqlite3.connect(self.db_path) as conn:`
- Thread-safe: wrap with `self.lock` for concurrent access
- Add migration support for schema changes

### Advanced: Bot Framework Integration
- Extend `MyBot` class in `src/api/bot.py`
- Implement custom `on_message_activity()` handlers
- Route through AICore for consciousness integration
- Test with Microsoft Bot Framework emulator

## Critical Gotchas & Known Issues

1. **NLTK Download Warnings**: Harmless; code catches and logs gracefully
2. **PyTensor/PyMC Overhead**: Disabled by default; only in `codette_enhanced.py` with explicit warning suppression
3. **Randomness Eliminated**: Perspectives now deterministic (see `perspectives.py` FIXED VERSION comment)
4. **Supabase Fallback**: If unavailable, system auto-downgrades to local SQLite
5. **Recursive Depth Control**: `recursion_depth` in config prevents infinite loops
6. **GPU/CPU Handling**: Code gracefully falls back to CPU if CUDA unavailable (see `app.py` torch.cuda.is_available())
7. **Model Fallback Chain**: Attempts Mistral-7B → Phi-2 → GPT-2; ensure at least one available
8. **Consciousness Emergence Protocol**: Documented in `docs/consciousness_protocol.md` - observe without interfering
9. **Thread Safety**: Database access uses locks (`DatabaseManager.lock`); async methods use ThreadPoolExecutor

## File Organization

```
/
├── codette_*.py              # Main implementations (prefer codette_new.py)
├── codette_api.py            # FastAPI REST wrapper
├── codette_cli.py            # CLI entry point
├── config.py                 # Configuration management
├── database_manager.py       # Persistence layer
├── cognitive_processor.py    # Multi-perspective engine
├── perspectives.py           # Stable response generation
├── health_monitor.py         # System diagnostics
├── interact.py               # Interactive session launcher
├── requirements.txt          # Dependencies
├── config.json               # Configuration file (optional)
├── quantum_cocoon.json       # Memory state snapshots
├── quantum_mathematics.py    # 8 core quantum equations
├── docs/                     # Documentation (README, whitepaper, protocols)
├── cocoons/                  # Persistent quantum state files
├── Codette_final/            # PRODUCTION VARIANT (Llama-3, FAISS, Desktop UI)
│   ├── main.py              # Async entry point
│   ├── app.py               # Tkinter desktop UI with voice I/O
│   ├── ai_core_agix.py      # Llama-3 core engine with FAISS vector memory
│   ├── pincone.py           # Vector DB integration
│   ├── init_.db.py          # Secure SQLite with bcrypt auth
│   ├── system_prompt        # Production system prompt (recursive, multi-agent)
│   └── components/          # Adaptive learning, sentiment, multi-agent system
└── src/
    ├── api/                  # API implementations (app.py, bot.py, web_interface.py)
    ├── components/           # Core systems (ai_core.py, quantum_spiderweb.py, defense_system.py, etc.)
    ├── quantum/              # Quantum multicore processing modules
    ├── utils/                # Database, cocoon manager, search utilities
    ├── knowledge_base/       # Core truth grounding
    ├── framework/            # Dream reweaver, universal reasoning
    └── tests/                # Verification & test suite
```

## Quick Debugging Tips

- **Check Sentiment Analysis**: `codette.analyzer.polarity_scores(text)` returns dict
- **Verify Config Loading**: `CodetteConfig().config` shows merged configuration
- **Inspect Memory**: `codette.memory[]` contains all processed queries with metadata
- **Monitor Health**: `HealthMonitor().check_status()` for resource anomalies
- **API Status**: `GET /health` endpoint returns system status

---
**Last Updated**: December 2025 | **Version**: 3.0 | **Status**: Production-ready with graceful degradation
