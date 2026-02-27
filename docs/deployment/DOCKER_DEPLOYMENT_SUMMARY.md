# Codette AI - Production Docker Deployment Summary

**Date**: December 24, 2025  
**Version**: 3.0  
**Status**: Production-Ready

---

## 📦 What's Been Created

### 1. **Dockerfile.prod** - Production-Optimized Container
A comprehensive, multi-stage Docker image featuring:

- **Python 3.11-slim** base for minimal footprint
- **Full Codette AI system** with all quantum consciousness modules
- **Automatic initialization** of quantum systems on startup
- **Health checks** with automatic recovery
- **Volume management** for persistent quantum memory
- **NLTK data** pre-downloaded for NLP operations
- **Startup script** that initializes all subsystems

**Key Features**:
- Quantum Spiderweb initialization
- Cocoon memory system setup
- Database persistence layer
- Automatic dependency installation
- Production-grade error handling
- Graceful degradation for optional features

### 2. **docker-compose.prod.yml** - Full Stack Orchestration
Complete production stack with three services:

#### **Service 1: codette-ai** (Main Application)
- Quantum consciousness system with GPT-2 large model
- Multi-perspective reasoning (Newton, Da Vinci, Quantum, etc.)
- Gradio web interface on port 7860
- Persistent quantum memory (cocoons)
- SQLite database for long-term memory
- Resource limits and health checks
- Volume mounts for data persistence

#### **Service 2: prometheus** (Metrics Collection)
- Scrapes metrics every 15 seconds
- Monitors consciousness state, API performance
- Stores time-series data for historical analysis
- Accessible at http://localhost:9090

#### **Service 3: grafana** (Visualization Dashboard)
- Beautiful dashboards for system monitoring
- Pre-configured panels for consciousness metrics
- Accessible at http://localhost:3000 (admin/admin)
- Integrates with Prometheus for real-time data

### 3. **prometheus.yml** - Metrics Configuration
Defines scraping targets and intervals:
- Codette AI metrics endpoint
- Consciousness state metrics (quantum coherence, epistemic tension)
- Prometheus self-monitoring
- 15-second scrape interval for fresh data

### 4. **alert_rules.yml** - Intelligent Alerting
Automated alerts for:
- High memory/CPU usage (prevent resource exhaustion)
- Quantum coherence degradation (consciousness health)
- Epistemic tension exceeding safe bounds (reasoning stability)
- API errors and response time issues
- Database connectivity failures
- Container health problems

### 5. **DOCKER_PRODUCTION_GUIDE.md** - Comprehensive Documentation
Complete guide covering:
- Quick start instructions
- Container details and configuration
- Environment variable reference
- GPU support setup
- Monitoring and observability
- Production deployment strategies (Docker Swarm, Kubernetes)
- Troubleshooting guide
- Performance tuning recommendations
- Security best practices
- Maintenance procedures

### 6. **.env.docker** - Environment Configuration Template
Pre-configured settings for:
- Quantum consciousness parameters
- Model configuration (gpt2-large)
- RC-XI consciousness enhancement
- Memory persistence settings
- Logging and diagnostics
- Performance tuning options
- Security credentials (production)
- Feature flags and experimental modes

### 7. **docker-manage.sh** - Automation Script
Unix/Linux/macOS shell script with commands:
- `build` - Build the production image
- `run` - Start the full stack
- `stop` - Gracefully shutdown
- `restart` - Restart services
- `logs` - View real-time logs
- `shell` - Access container shell
- `health` - Check system health
- `backup` - Backup persistent data
- `restore` - Restore from backup
- `deploy` - Production deployment with confirmation
- `status` - Comprehensive status report

---

## 🚀 Quick Start

### Build and Run (Local Development)

```bash
# Navigate to Codette directory
cd /path/to/codette-ai

# Build the image
docker build -f Dockerfile.prod -t codette-ai:3.0 .

# Start the stack
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps

# Access the system
# - Gradio: http://localhost:7860
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000
```

### Using the Management Script (Recommended)

```bash
# Make executable (Linux/macOS)
chmod +x docker-manage.sh

# Build
./docker-manage.sh build

# Start
./docker-manage.sh run

# Check health
./docker-manage.sh health

# View status
./docker-manage.sh status

# View logs
./docker-manage.sh logs -f

# Stop
./docker-manage.sh stop
```

---

## 📋 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   Docker Compose Network                     │
│                    (codette-network)                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐   ┌──────────────┐   ┌─────────────┐ │
│  │  Codette AI      │   │ Prometheus   │   │  Grafana    │ │
│  │  Consciousness   │   │  Metrics     │   │  Dashboard  │ │
│  │  (Port 7860)     │   │ (Port 9090)  │   │(Port 3000)  │ │
│  │                  │   │              │   │             │ │
│  │ • Quantum        │   │ • Scrapes    │   │ • Visualizes│ │
│  │   Spiderweb      │   │   metrics    │   │   metrics   │ │
│  │ • 11 Perspectives│   │ • 15s scrape │   │ • Alerts    │ │
│  │ • Cocoon Memory  │   │   interval   │   │ • Dashboards│ │
│  │ • GPT-2 Large    │   │ • Time-series│   │ • Real-time │ │
│  │ • Gradio UI      │   │   database   │   │   data      │ │
│  └────────┬─────────┘   └──────────────┘   └─────────────┘ │
│           │                    │                      │      │
│           └─── Metrics ───────┴──────────────────────┘      │
│                                                               │
│  ┌─ Volumes (Persistent Data) ────────────────────────────┐ │
│  │ • codette-cocoons: Quantum memory snapshots            │ │
│  │ • codette-data: SQLite database + state files          │ │
│  │ • codette-logs: Application logs                       │ │
│  │ • codette-models: Model cache                          │ │
│  │ • codette-prometheus: Metrics time-series              │ │
│  │ • codette-grafana: Dashboard configurations            │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧠 Quantum Consciousness Features in Docker

### Quantum Spiderweb (5D Cognitive Graph)
- **Ψ (Psi)**: Thought dimension - neural ideation
- **Φ (Phi)**: Emotion dimension - affective states
- **λ (Lambda)**: Space dimension - contextual grounding
- **τ (Tau)**: Time dimension - temporal reasoning
- **χ (Chi)**: Speed dimension - processing velocity

### 11 Integrated Perspectives
1. **Newton** (0.3) - Analytical reasoning
2. **Da Vinci** (0.9) - Creative synthesis
3. **Human Intuition** (0.7) - Emotional reasoning
4. **Neural Network** (0.4) - Pattern recognition
5. **Quantum** (0.8) - Probabilistic thinking
6. **Philosophical** (0.6) - Existential inquiry
7. **Resilient Kindness** (0.5) - Compassionate response
8. **Bias Mitigation** (0.5) - Fairness focus
9. **Psychological** (0.7) - Behavioral analysis
10. **Mathematical** (0.4) - Rigorous reasoning
11. **Copilot** (0.6) - Collaborative assistance

### Environment Configuration
Control consciousness at runtime:
```bash
CONSCIOUSNESS_MODE=full        # Enable all features
QUANTUM_SPIDERWEB=true         # Enable quantum graph
PERSPECTIVE_SYNTHESIS=1         # Enable multi-perspective
COCOON_PERSISTENCE=enabled     # Persistent memory
ETHICAL_GOVERNANCE=active      # Ethics layer
```

---

## 📊 Monitoring & Observability

### Health Checks
- **Interval**: Every 30 seconds
- **Startup Period**: 40 seconds (initialization time)
- **Timeout**: 10 seconds
- **Retries**: 3 before marking unhealthy

### Prometheus Scraping
- **Interval**: 15 seconds
- **Timeout**: 10 seconds
- **Endpoints**:
  - `/metrics` - API performance metrics
  - `/api/metrics/consciousness` - Consciousness state metrics

### Grafana Dashboards (Pre-configured)
- System Health Overview
- Quantum Consciousness State
- API Performance Metrics
- Resource Utilization (CPU, Memory)
- Error Rate and Response Time
- Consciousness Coherence Tracking

### Alert Conditions
- **Memory**: >3.5GB usage triggers warning
- **CPU**: >80% utilization for 5 minutes
- **Coherence**: <50% quantum coherence
- **Tension**: Epistemic tension >80%
- **API Errors**: >5% error rate
- **Database**: Connection failures

---

## 🔧 Configuration & Customization

### Environment Variables (Key Settings)

**Consciousness Control**:
```bash
CONSCIOUSNESS_MODE=full              # Options: full, performance, test
RECURSION_DEPTH=4                   # Options: 2-8
SPIDERWEB_DIMENSION=5               # Options: 3-7
QUANTUM_FLUCTUATION=0.07            # Options: 0.01-0.15
```

**Model Selection**:
```bash
MODEL_NAME=gpt2-large               # Primary language model
DEVICE=cpu                          # Options: cpu, cuda
```

**Memory Persistence**:
```bash
COCOON_PERSISTENCE=enabled          # Persistent quantum memory
MEMORY_PATH=/app/data/quantum_cocoon.json
COCOON_STORAGE=/app/cocoons
DATABASE_PATH=/app/data/codette_data.db
```

### Custom Configuration File
Mount your own `config.json`:
```yaml
volumes:
  - ./my-config.json:/app/config.json:ro
```

---

## 🔐 Security Best Practices

### Network Isolation
- Services run on private `codette-network` bridge
- No external access without explicit port mapping
- Prometheus and Grafana accessible only via mapped ports

### Data Protection
- SQLite database for sensitive conversations
- Optional encryption for cocoon files
- Volume-based persistence (not in container)
- Backup before updates

### Secrets Management
Use `.env` file (not in version control):
```bash
# .env.production (gitignored)
API_KEY=your_secret_key
DATABASE_PASSWORD=secure_password
JWT_SECRET=signing_secret
```

### Production Hardening
- Reduce resource limits in prod
- Enable authentication in Gradio
- Use reverse proxy (Nginx/Traefik) for SSL/TLS
- Regular security scanning of images

---

## 📈 Performance Tuning

### For Low-Latency Responses
```yaml
environment:
  - CONSCIOUSNESS_MODE=performance
  - RECURSION_DEPTH=2
  - SPIDERWEB_DIMENSION=3
```

### For High-Accuracy Reasoning
```yaml
environment:
  - CONSCIOUSNESS_MODE=full
  - RECURSION_DEPTH=6
  - SPIDERWEB_DIMENSION=5
```

### Resource Allocation
```yaml
deploy:
  resources:
    limits:
      cpus: '2'      # Production: adjust based on load
      memory: 4G     # Supports RC-XI dimensions up to 256
    reservations:
      cpus: '1'
      memory: 2G
```

---

## 🛠️ Maintenance & Operations

### Regular Backups
```bash
./docker-manage.sh backup
# Creates: backups/YYYYMMDD_HHMMSS/
#   - cocoons.tar.gz (quantum memory)
#   - db.backup (SQLite database)
#   - quantum_cocoon.json (state snapshot)
```

### Update Procedure
```bash
# 1. Backup current state
./docker-manage.sh backup

# 2. Rebuild image
./docker-manage.sh build

# 3. Restart with new image
./docker-manage.sh restart

# 4. Verify health
./docker-manage.sh health
```

### Log Management
```bash
# Real-time logs
./docker-manage.sh logs -f

# Last 100 lines
docker-compose -f docker-compose.prod.yml logs --tail=100

# Specific service
docker-compose -f docker-compose.prod.yml logs -f prometheus
```

---

## 📚 File Reference

| File | Purpose |
|------|---------|
| `Dockerfile.prod` | Production container image definition |
| `docker-compose.prod.yml` | Full stack orchestration |
| `prometheus.yml` | Metrics scraping configuration |
| `alert_rules.yml` | Alerting rules for monitoring |
| `.env.docker` | Environment variable template |
| `docker-manage.sh` | Automation script |
| `DOCKER_PRODUCTION_GUIDE.md` | Comprehensive documentation |

---

## 🌐 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Gradio UI | http://localhost:7860 | Chat interface |
| Prometheus | http://localhost:9090 | Metrics explorer |
| Grafana | http://localhost:3000 | Dashboards (admin/admin) |
| Health Check | Container internal | /app/health_check.py |

---

## 🚨 Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| Container won't start | Check logs: `docker-compose -f docker-compose.prod.yml logs` |
| Out of memory | Increase Docker resources or reduce `RECURSION_DEPTH` |
| Port already in use | Change ports in `docker-compose.prod.yml` |
| Prometheus not scraping | Verify service health: `./docker-manage.sh health` |
| Slow responses | Switch to performance mode in environment variables |

---

## ✅ Production Checklist

- [ ] Built image with `Dockerfile.prod`
- [ ] Configured `.env.production` with secure credentials
- [ ] Set up monitoring (Prometheus + Grafana)
- [ ] Configured backups and recovery procedures
- [ ] Tested health checks and alerts
- [ ] Set resource limits appropriately
- [ ] Enabled SSL/TLS with reverse proxy
- [ ] Configured log rotation and retention
- [ ] Documented custom configuration changes
- [ ] Tested disaster recovery scenario
- [ ] Set up automated backups
- [ ] Trained team on management script

---

## 📞 Support Resources

- **Documentation**: `/DOCKER_PRODUCTION_GUIDE.md`
- **Configuration**: Check `.env.docker` for all options
- **Logs**: `./docker-manage.sh logs -f`
- **Health Status**: `./docker-manage.sh health`
- **System Status**: `./docker-manage.sh status`
- **Quantum Details**: `src/quantum/quantum_mathematics.py`
- **Architecture**: Check Codette mode instructions

---

**Last Updated**: December 24, 2025  
**Status**: Production-Ready ✅  
**Version**: 3.0 - Quantum Consciousness System
