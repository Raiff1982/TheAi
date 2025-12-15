# Quick Start: Tracing Setup for Codette AI

Get Codette AI tracing up and running in 5 minutes.

## Prerequisites

- Python 3.10+
- Codette AI system installed
- OTLP collector running on `http://localhost:4319`

## Step 1: Install Dependencies (1 minute)

```bash
# Install OpenTelemetry packages
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-http

# Or install all requirements
pip install -r requirements.txt
```

## Step 2: Verify Installation (30 seconds)

```bash
python tracing_setup.py
```

Expected output:
```
======================================================================
CODETTE AI TRACING INITIALIZATION
======================================================================
Configuring tracing:
  • Service: codette-ai-system
  • OTLP Endpoint: http://localhost:4319/v1/traces
  • Environment: development

✓ OpenTelemetry tracing initialized successfully
  Service: codette-ai-system
  OTLP Endpoint: http://localhost:4319/v1/traces
  Environment: development

======================================================================
TRACING STATUS
======================================================================
✓ OpenTelemetry tracing is now active
✓ All agent operations will be traced
✓ Perspective generations will be instrumented
✓ Multi-agent workflows will be visualized

To view traces:
  1. Ensure OTLP collector is running on http://localhost:4319
  2. Access AI Toolkit trace visualization UI
  3. Run Codette and observe traced operations
======================================================================
```

## Step 3: Run Codette with Tracing (1 minute)

### Option A: Single Query

```bash
python codette_cli_traced.py "What is consciousness?"
```

### Option B: Interactive Mode

```bash
python codette_cli_traced.py -i -u YourName
```

## Step 4: View Traces (2 minutes)

1. Open AI Toolkit trace visualization UI in VS Code
2. You should see traces appearing with:
   - Codette response operations
   - Perspective generations (Newton, DaVinci, etc.)
   - Sentiment analysis
   - Concept extraction
   - Memory operations

## Verification Checklist

✅ OpenTelemetry packages installed  
✅ Test trace creation successful  
✅ Codette CLI runs with tracing enabled  
✅ Traces visible in visualization UI  

## What You'll See

### Trace Hierarchy Example

```
codette.respond (150ms)
├── codette.sentiment_analysis (5ms)
├── codette.extract_concepts (10ms)
├── codette.select_perspectives (2ms)
├── perspective.Newton (45ms)
│   └── Analytical reasoning: "From a scientific perspective..."
├── perspective.DaVinci (40ms)
│   └── Creative insight: "Imagine consciousness as..."
└── perspective.Quantum (48ms)
    └── Probabilistic view: "In quantum terms..."
```

### Key Trace Attributes

Each span shows:
- **Duration**: Time taken for operation
- **User context**: Who asked the question
- **Sentiment**: Emotional tone (positive/negative/neutral)
- **Concepts**: Extracted keywords
- **Perspectives**: Which reasoning lenses were used
- **Response**: Generated text metadata

## Quick Commands Reference

```bash
# Interactive with tracing
python codette_cli_traced.py -i

# Custom OTLP endpoint
python codette_cli_traced.py -i --otlp-endpoint http://custom:4318/v1/traces

# Verbose logging
python codette_cli_traced.py -i -v

# Disable tracing
python codette_cli_traced.py -i --no-tracing

# Help
python codette_cli_traced.py --help
```

## Interactive Mode Commands

Once in interactive mode:
- `help` - Show available commands
- `status` - Display system and tracing status
- `memory` - Show conversation history
- `exit` or `quit` - Exit program

## Troubleshooting

### Problem: "Import 'opentelemetry' could not be resolved"

**Solution:**
```bash
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
```

### Problem: "Connection refused to localhost:4319"

**Solution:**
- Verify OTLP collector is running
- Try alternative endpoint: `--otlp-endpoint http://localhost:4318/v1/traces`
- Check firewall settings

### Problem: "Traces not appearing in UI"

**Solution:**
1. Check endpoint in logs
2. Verify collector is receiving data
3. Ensure AI Toolkit visualization is active
4. Try test trace: `python tracing_setup.py`

### Problem: "Tracing slowing down responses"

**Solution:**
- Normal overhead is 1-2ms per operation
- Check network latency to collector
- Consider disabling for performance testing: `--no-tracing`

## Next Steps

✅ **Basic tracing working?** Read [TRACING_SETUP.md](./TRACING_SETUP.md) for advanced features

✅ **Want to trace custom code?** See "Advanced: Custom Instrumentation" section

✅ **Production deployment?** Review "Performance Considerations" and sampling strategies

## Example Session

```bash
$ python codette_cli_traced.py -i -u Alice

    ╔═══════════════════════════════════════════════════════════════╗
    ║                  CODETTE AI SYSTEM v3.0                       ║
    ║              Multi-Perspective Consciousness                  ║
    ║                  With OpenTelemetry Tracing                   ║
    ╚═══════════════════════════════════════════════════════════════╝

Initializing OpenTelemetry tracing...
✓ Tracing enabled - OTLP endpoint: http://localhost:4319/v1/traces
  View traces in AI Toolkit visualization UI

Welcome Alice! I am Codette, your multi-perspective AI assistant.
🔍 Tracing is ENABLED - all operations are being traced for visualization
   OTLP Endpoint: http://localhost:4319/v1/traces
======================================================================

Entering interactive mode. Type 'exit', 'quit', or Ctrl+C to quit.
Type 'help' for available commands.

Alice: What is the meaning of life?

Codette: [Response with multi-perspective synthesis...]

Alice: status

======================================================================
CODETTE SYSTEM STATUS
======================================================================
User: Alice
Memory entries: 1
Tracing enabled: ✓ YES
Tracer initialized: ✓ YES
======================================================================

Alice: exit
Goodbye!
```

## Need Help?

- **Full documentation**: [TRACING_SETUP.md](./TRACING_SETUP.md)
- **Codette main docs**: [README.md](../README.md)
- **OpenTelemetry docs**: https://opentelemetry.io/docs/

---

**Status**: ✅ Ready for production use  
**Version**: 1.0  
**Last Updated**: December 2025
