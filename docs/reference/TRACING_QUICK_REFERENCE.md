# Codette AI Tracing - Quick Reference Card

## 🚀 Quick Start (3 Commands)

```bash
# 1. Install dependencies
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-http

# 2. Test setup
python tracing_setup.py

# 3. Run with tracing
python codette_cli_traced.py -i -u YourName
```

## 📋 Common Commands

```bash
# Interactive mode with tracing
python codette_cli_traced.py -i

# Single query
python codette_cli_traced.py "Your question here"

# Custom OTLP endpoint (your specified endpoint)
python codette_cli_traced.py -i --otlp-endpoint http://localhost:4319/v1/traces

# Verbose logging
python codette_cli_traced.py -i -v

# Disable tracing
python codette_cli_traced.py -i --no-tracing

# Full installation
python install_tracing.py
```

## 🎯 Interactive Mode Commands

Once in interactive mode:
- `help` - Show help
- `status` - System status
- `memory` - View conversation history
- `exit` or `quit` - Exit

## 🔍 What Gets Traced

| Component | Span Name | Key Attributes |
|-----------|-----------|----------------|
| **Response Generation** | `codette.respond` | user, prompt, response length |
| **Sentiment Analysis** | `codette.sentiment_analysis` | compound, positive, negative |
| **Concept Extraction** | `codette.extract_concepts` | tokens, keywords, concepts |
| **Perspective Selection** | `codette.select_perspectives` | perspectives count, list |
| **Newton (Analytical)** | `perspective.Newton` | temperature: 0.3 |
| **DaVinci (Creative)** | `perspective.DaVinci` | temperature: 0.9 |
| **Quantum** | `perspective.Quantum` | temperature: 0.8 |

## 🔧 Configuration

### Default Endpoint
```
http://localhost:4319/v1/traces
```

### Environment Variables
```bash
export OTEL_SERVICE_NAME="codette-ai-system"
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4319/v1/traces"
export ENVIRONMENT="development"
```

### Python API
```python
from src.utils.tracing_config import setup_tracing
from codette_traced import TracedCodette

# Setup
tracer = setup_tracing(
    service_name="my-app",
    otlp_endpoint="http://localhost:4319/v1/traces"
)

# Use
codette = TracedCodette(user_name="Alice", enable_tracing=True)
response = codette.respond("Question")
```

## 📊 Trace Hierarchy

```
codette.respond (ROOT)
├── codette.sentiment_analysis
├── codette.extract_concepts
├── codette.select_perspectives
├── perspective.Newton
├── perspective.DaVinci
├── perspective.Quantum
└── [response synthesis]
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Import errors | `pip install -r requirements.txt` |
| Connection refused | Check OTLP collector running on port 4319 |
| No traces visible | Verify endpoint in AI Toolkit |
| Slow performance | Check network latency, consider `--no-tracing` |

### Quick Diagnostics
```bash
# Test import
python -c "from opentelemetry import trace; print('OK')"

# Test endpoint
curl http://localhost:4319/v1/traces

# Verbose test
python codette_cli_traced.py -i -v
```

## 📚 Documentation Files

- `docs/TRACING_QUICKSTART.md` - 5-minute start guide
- `docs/TRACING_SETUP.md` - Full documentation
- `TRACING_IMPLEMENTATION_SUMMARY.md` - Technical details
- `README.md` - Main project docs

## 🔗 Key Files

| File | Purpose |
|------|---------|
| `src/utils/tracing_config.py` | Core tracing setup |
| `codette_traced.py` | Traced Codette class |
| `codette_cli_traced.py` | CLI with tracing |
| `src/components/ai_core_tracing.py` | AI Core utilities |
| `tracing_setup.py` | Setup & test script |
| `install_tracing.py` | Automated installer |

## 💡 Tips

1. **Always check endpoint first:** Ensure OTLP collector running
2. **Use verbose mode for debugging:** `-v` flag shows detailed logs
3. **Test with setup script:** `python tracing_setup.py` verifies config
4. **View in AI Toolkit:** Open trace visualization UI in VS Code
5. **Disable for performance testing:** Use `--no-tracing` flag

## ⚡ Performance

- **Overhead per operation:** 1-2ms
- **Total impact:** <5% typical usage
- **Batched export:** Non-blocking
- **Graceful degradation:** Works without tracing

## 🎨 Example Session

```bash
$ python codette_cli_traced.py -i -u Alice

Welcome Alice! I am Codette, your multi-perspective AI assistant.
🔍 Tracing is ENABLED - all operations are being traced
   OTLP Endpoint: http://localhost:4319/v1/traces

Alice: What is consciousness?

Codette: [Multi-perspective response with Newton, DaVinci, Quantum views...]

Alice: status
User: Alice
Memory entries: 1
Tracing enabled: ✓ YES

Alice: exit
Goodbye!
```

## 📞 Need Help?

1. Check troubleshooting section above
2. Review `docs/TRACING_SETUP.md`
3. Run diagnostics: `python tracing_setup.py`
4. Check logs with `-v` verbose flag

---

**Version:** 1.0 | **Date:** December 2025 | **Status:** Production Ready
