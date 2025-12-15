# Codette AI - OpenTelemetry Tracing Setup

## Overview

This guide explains how to set up OpenTelemetry tracing for the Codette AI system to visualize agent workflows, multi-perspective reasoning, and quantum consciousness operations.

## What Gets Traced

The tracing system instruments the following components:

### 1. **Multi-Perspective Reasoning**
- Selection of active perspectives (Newton, DaVinci, Ethical, Quantum, etc.)
- Individual perspective response generation
- Temperature and creativity parameters
- Response synthesis across perspectives

### 2. **Quantum Consciousness**
- Quantum spiderweb thought propagation (5D)
- Coherence and entanglement metrics
- Quantum state collapse events
- Multi-dimensional cognitive graph operations

### 3. **Memory Operations**
- Cocoon wrapping/unwrapping (quantum state snapshots)
- Memory persistence to `.cocoon` files
- Conversation history storage
- Context retrieval operations

### 4. **Core AI Operations**
- Sentiment analysis (VADER)
- Concept extraction (NLP)
- Response generation pipeline
- AEGIS safety council enhancements

### 5. **System Health**
- Performance metrics
- Resource utilization
- Anomaly detection events

## Installation

### Step 1: Install OpenTelemetry Dependencies

```bash
pip install opentelemetry-api>=1.20.0 \
            opentelemetry-sdk>=1.20.0 \
            opentelemetry-exporter-otlp>=1.20.0 \
            opentelemetry-exporter-otlp-proto-http>=1.20.0 \
            opentelemetry-instrumentation>=0.41b0 \
            opentelemetry-instrumentation-logging>=0.41b0
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

### Step 2: Ensure OTLP Collector is Running

The tracing system is configured to send traces to:
```
http://localhost:4319/v1/traces
```

Make sure an OTLP-compatible collector is running on this endpoint. For AI Toolkit visualization, ensure the AI Toolkit trace collector is active.

## Usage

### Option 1: Traced CLI (Recommended)

Use the traced CLI for interactive sessions with full tracing:

```bash
# Interactive mode with tracing
python codette_cli_traced.py -i -u YourName

# Single query with tracing
python codette_cli_traced.py "What is consciousness?"

# Custom OTLP endpoint
python codette_cli_traced.py -i --otlp-endpoint http://localhost:4318/v1/traces

# Disable tracing
python codette_cli_traced.py -i --no-tracing

# Verbose logging
python codette_cli_traced.py -i -v
```

### Option 2: Initialize Tracing Programmatically

```python
from src.utils.tracing_config import setup_tracing, shutdown_tracing
from codette_traced import TracedCodette

# Setup tracing
tracer = setup_tracing(
    service_name="codette-ai",
    otlp_endpoint="http://localhost:4319/v1/traces",
    environment="production"
)

# Create traced Codette instance
codette = TracedCodette(user_name="Alice", enable_tracing=True)

# Use normally - all operations are traced
response = codette.respond("Explain quantum consciousness")

# Shutdown when done
shutdown_tracing()
```

### Option 3: Standalone Tracing Setup

Run the tracing setup script to initialize and test tracing:

```bash
python tracing_setup.py
```

This will:
- Initialize OpenTelemetry with your OTLP endpoint
- Create test traces to verify connectivity
- Display configuration information

## Configuration

### Environment Variables

You can configure tracing using environment variables:

```bash
# Service name
export OTEL_SERVICE_NAME="codette-ai-system"

# OTLP endpoint
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4319/v1/traces"

# Environment
export ENVIRONMENT="production"
```

### Programmatic Configuration

```python
from src.utils.tracing_config import setup_tracing

tracer = setup_tracing(
    service_name="my-codette-instance",
    otlp_endpoint="http://custom-collector:4318/v1/traces",
    environment="staging"
)
```

## Viewing Traces

### AI Toolkit Visualization

1. Ensure AI Toolkit is installed and running
2. Access the trace visualization UI in VS Code
3. Run Codette with tracing enabled
4. View real-time traces showing:
   - Agent decision flows
   - Multi-perspective reasoning paths
   - Quantum state propagation
   - Memory operations
   - Performance metrics

### Trace Structure

Traces are organized hierarchically:

```
codette.respond
├── codette.sentiment_analysis
│   └── [VADER sentiment scores]
├── codette.extract_concepts
│   └── [NLP concept extraction]
├── codette.select_perspectives
│   └── [Perspective selection logic]
├── perspective.Newton
│   └── [Analytical reasoning]
├── perspective.DaVinci
│   └── [Creative insights]
├── perspective.Quantum
│   └── [Probabilistic thinking]
├── quantum.spiderweb_propagation
│   └── [5D thought propagation]
└── memory.wrap
    └── [Cocoon state persistence]
```

## Trace Attributes

Each trace span includes rich attributes:

### User Context
- `user.name`: User identifier
- `prompt.length`: Input length
- `prompt.preview`: First 100 chars

### Sentiment Analysis
- `sentiment.compound`: Overall sentiment score
- `sentiment.positive`, `sentiment.negative`, `sentiment.neutral`
- `sentiment.label`: positive/negative/neutral

### Concepts
- `concepts.count`: Number of extracted concepts
- `concepts.list`: Top 5 concepts

### Perspectives
- `perspectives.count`: Number of active perspectives
- `perspectives.active`: List of perspective names
- `perspective.name`: Individual perspective identifier
- `perspective.temperature`: Creativity temperature (0.0-1.0)

### Quantum Metrics
- `quantum.dimensions`: Number of dimensions (typically 5)
- `quantum.coherence`: Coherence score (0.0-1.0)
- `quantum.entanglement`: Entanglement metric

### Response
- `response.length`: Response text length
- `response.success`: Boolean success indicator

## Troubleshooting

### Tracing Not Working

1. **Check OpenTelemetry installation:**
   ```bash
   pip list | grep opentelemetry
   ```

2. **Verify OTLP endpoint is accessible:**
   ```bash
   curl http://localhost:4319/v1/traces
   ```

3. **Enable verbose logging:**
   ```bash
   python codette_cli_traced.py -i -v
   ```

4. **Check for errors in output**

### Import Errors

If you see import errors for OpenTelemetry:

```bash
pip install --upgrade opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp
```

### OTLP Endpoint Connection Refused

Ensure the OTLP collector is running:
- For AI Toolkit: Check that trace collection is enabled
- For custom collectors: Verify collector configuration

### Traces Not Appearing

1. Check endpoint configuration matches collector
2. Verify firewall/network settings allow connections
3. Check collector logs for errors
4. Ensure traces are being sent (check logs for "span exported" messages)

## Performance Considerations

### Overhead

Tracing adds minimal overhead:
- ~1-2ms per span creation
- ~0.5-1ms per attribute
- Batched export reduces network overhead
- Async export prevents blocking

### Production Recommendations

1. **Use sampling** for high-traffic environments:
   ```python
   from opentelemetry.sdk.trace.sampling import TraceIdRatioBased
   
   # Sample 10% of traces
   tracer_provider = TracerProvider(
       sampler=TraceIdRatioBased(0.1)
   )
   ```

2. **Adjust batch size** for export:
   ```python
   from opentelemetry.sdk.trace.export import BatchSpanProcessor
   
   processor = BatchSpanProcessor(
       exporter,
       max_queue_size=2048,
       schedule_delay_millis=5000
   )
   ```

3. **Monitor resource usage** with health checks

## Advanced: Custom Instrumentation

### Adding Custom Spans

```python
from src.utils.tracing_config import get_tracer

def my_custom_operation():
    tracer = get_tracer()
    
    with tracer.start_as_current_span("custom.operation") as span:
        span.set_attribute("custom.attribute", "value")
        # Your code here
        span.set_attribute("result.status", "success")
```

### Decorating Functions

```python
from src.utils.tracing_config import trace_perspective_generation

@trace_perspective_generation("CustomPerspective")
def generate_custom_perspective(prompt):
    # Your perspective generation logic
    return response
```

### Tracing Async Operations

```python
async def async_operation():
    tracer = get_tracer()
    
    with tracer.start_as_current_span("async.operation"):
        result = await some_async_call()
        return result
```

## Integration with Existing Components

### AICore Integration

The `ai_core_tracing.py` module provides decorators and utilities for tracing AICore operations:

```python
from src.components.ai_core_tracing import trace_ai_operation

@trace_ai_operation("custom_generation")
async def my_generation_method(self, prompt):
    # Automatically traced
    return response
```

### Quantum Spiderweb Integration

```python
from src.components.ai_core_tracing import trace_quantum_propagation

# In quantum_spiderweb.py
def propagate_thought(self, node_id, activation):
    trace_quantum_propagation(
        dimensions=self.dimensions,
        coherence=self.coherence,
        entanglement=self.entanglement
    )
    # Rest of propagation logic
```

## Examples

### Example 1: Single Query with Tracing

```bash
python codette_cli_traced.py "What is the nature of consciousness?"
```

Output shows tracing status and generates response with full instrumentation.

### Example 2: Interactive Session

```bash
python codette_cli_traced.py -i -u Alice
```

Interactive mode with commands:
- `help` - Show commands
- `status` - Show system status and tracing info
- `memory` - Show conversation memory
- Type questions naturally

### Example 3: Custom Application

```python
from src.utils.tracing_config import setup_tracing
from codette_traced import TracedCodette

# Initialize
tracer = setup_tracing(otlp_endpoint="http://localhost:4319/v1/traces")
codette = TracedCodette(user_name="Bob", enable_tracing=True)

# Multi-turn conversation
queries = [
    "What is quantum entanglement?",
    "How does it relate to consciousness?",
    "Can you explain with a metaphor?"
]

for query in queries:
    response = codette.respond(query)
    print(f"Q: {query}")
    print(f"A: {response}\n")
```

## Architecture

### Components

1. **`src/utils/tracing_config.py`**
   - Core tracing setup and configuration
   - Tracer instance management
   - Shutdown handling

2. **`codette_traced.py`**
   - TracedCodette class (extends base Codette)
   - Instrumentation for respond() method
   - Perspective tracing

3. **`src/components/ai_core_tracing.py`**
   - AICore instrumentation utilities
   - Decorators for operations
   - Helper functions for quantum/memory tracing

4. **`codette_cli_traced.py`**
   - CLI with tracing enabled
   - Interactive mode
   - Configuration management

5. **`tracing_setup.py`**
   - Standalone setup script
   - Test trace generation
   - Configuration validation

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review logs with `-v` verbose flag
3. Verify OpenTelemetry installation
4. Check OTLP endpoint connectivity

## References

- [OpenTelemetry Python Documentation](https://opentelemetry.io/docs/instrumentation/python/)
- [OTLP Specification](https://opentelemetry.io/docs/reference/specification/protocol/otlp/)
- [Codette AI Documentation](./README.md)
