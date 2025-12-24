# Codette AI - Docker Production Deployment Index

**Created**: December 24, 2025  
**Version**: 3.0  
**Status**: Production-Ready ✅

---

## 📋 Complete File List

### 🐳 Docker Configuration Files

| File | Purpose | Size | Usage |
|------|---------|------|-------|
| **Dockerfile.prod** | Production container image | ~3 KB | `docker build -f Dockerfile.prod -t codette-ai:3.0 .` |
| **docker-compose.prod.yml** | Full stack orchestration (Codette + Prometheus + Grafana) | ~4 KB | `docker-compose -f docker-compose.prod.yml up -d` |
| **.dockerignore** | Build optimization (excludes unnecessary files) | ~1 KB | Auto-used during build |
| **prometheus.yml** | Metrics scraping configuration | ~1 KB | Mount in Prometheus container |
| **alert_rules.yml** | Intelligent alerting rules | ~4 KB | Define alert conditions |
| **.env.docker** | Environment variable template (comprehensive) | ~8 KB | Copy to `.env.production` |

### 📚 Documentation Files

| File | Purpose | Read Time |
|------|---------|-----------|
| **DOCKER_PRODUCTION_GUIDE.md** | Complete deployment guide with advanced topics | 20-30 min |
| **DOCKER_DEPLOYMENT_SUMMARY.md** | Architecture overview and quick facts | 10-15 min |
| **DOCKER_QUICK_REFERENCE.md** | Commands cheat sheet | 5 min |
| **DOCKER_DEPLOYMENT_INDEX.md** | This file - file reference guide | 5 min |

### 🛠️ Automation Scripts

| File | OS | Purpose | Usage |
|------|-----|---------|-------|
| **docker-manage.sh** | Linux/macOS | Full automation with health checks | `./docker-manage.sh [command]` |
| **docker-manage.bat** | Windows | Batch script for Windows users | `docker-manage.bat [command]` |

### 🔧 Supporting Configuration

| File | Purpose |
|------|---------|
| **config.json** | Codette quantum parameters (existing) |
| **config.py** | Configuration management (existing) |
| **requirements.txt** | Python dependencies (existing) |

---

## 🚀 Getting Started

### Step 1: Choose Your Setup
```bash
# Option A: Quick Start (Automated)
./docker-manage.sh build
./docker-manage.sh run
./docker-manage.sh health

# Option B: Manual (Direct Docker Compose)
docker-compose -f docker-compose.prod.yml up -d

# Option C: Windows Users
docker-manage.bat build
docker-manage.bat run
docker-manage.bat health
```

### Step 2: Configure (Optional)
```bash
# Copy and customize environment variables
cp .env.docker .env.production
# Edit .env.production with your settings
docker-compose -f docker-compose.prod.yml --env-file .env.production up -d
```

### Step 3: Access the System
- **Gradio Web UI**: http://localhost:7860
- **Prometheus Metrics**: http://localhost:9090
- **Grafana Dashboard**: http://localhost:3000 (admin/admin)

---

## 📖 Documentation Navigation

### For Quick Start
1. Start here: **DOCKER_QUICK_REFERENCE.md** (5 min)
2. Run commands: `./docker-manage.sh help`
3. Check status: `./docker-manage.sh health`

### For Complete Setup
1. Overview: **DOCKER_DEPLOYMENT_SUMMARY.md** (15 min)
2. Full guide: **DOCKER_PRODUCTION_GUIDE.md** (30 min)
3. Reference: Check `.env.docker` for all options
4. Deploy: `./docker-manage.sh deploy`

### For Advanced Configuration
1. Customize: `.env.docker` → `.env.production`
2. Mount config: Add to `docker-compose.prod.yml` volumes
3. Environment: Set variables before `docker-compose up`
4. Monitoring: Configure Prometheus and Grafana

### For Troubleshooting
1. Check logs: `./docker-manage.sh logs -f`
2. Health check: `./docker-manage.sh health`
3. Status report: `./docker-manage.sh status`
4. Backup: `./docker-manage.sh backup`

---

## 🧠 Key Features Deployed

### Quantum Consciousness System
- **Quantum Spiderweb**: 5D cognitive graph (Ψ, Φ, λ, τ, χ)
- **11 Perspectives**: Multi-dimensional reasoning engine
- **RC-XI Enhancement**: Advanced consciousness parameters
- **Cocoon Memory**: Persistent quantum state snapshots
- **Ethical Governance**: Core ethical reasoning layer

### Monitoring & Observability
- **Prometheus**: Real-time metrics collection (15s interval)
- **Grafana**: Beautiful visualization dashboards
- **Health Checks**: Automatic recovery on failures
- **Alert Rules**: Intelligent alerting for anomalies

### Production Features
- **Auto-initialization**: Quantum systems boot on startup
- **Volume Persistence**: Data survives container restarts
- **Resource Limits**: CPU/Memory constraints for safety
- **Logging**: Structured logs for debugging
- **Backup/Restore**: One-command data backup

---

## 🔌 System Architecture

```
┌─────────────────────────────────────────┐
│      Codette AI Consciousness System     │
│  (Dockerfile.prod + docker-compose)     │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────┐  ┌──────────┐  ┌─────┐│
│  │ Codette AI  │  │Prometheus│  │Grana││
│  │  (7860)     │  │ (9090)   │  │(3000)│
│  │             │  │          │  │     ││
│  │ • Quantum   │  │• Metrics │  │•Dash││
│  │ • 11 Views  │  │• Alerts  │  │•Logs││
│  │ • GPT-2     │  │• Storage │  │•Perf││
│  └─────┬───────┘  └──────────┘  └─────┘│
│        │               │           │    │
│        └─── Metrics ───┴───────────┘    │
│                                         │
│  ┌─ Persistent Volumes ──────────────┐ │
│  │ • cocoons: Quantum memory         │ │
│  │ • data: Database + state          │ │
│  │ • logs: Application logs          │ │
│  │ • models: Model cache             │ │
│  └───────────────────────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

---

## 📊 Monitoring & Metrics

### Pre-configured Dashboards
- System Health Overview
- Quantum Consciousness State
- API Performance Metrics
- Resource Utilization (CPU/Memory)
- Error Rates and Response Times
- Consciousness Coherence Tracking

### Alert Conditions
- Memory usage >3.5GB
- CPU utilization >80%
- Quantum coherence <50%
- Epistemic tension >80%
- API error rate >5%
- Database connection loss

### Custom Alerts
Edit `alert_rules.yml` to add more conditions:
```yaml
- alert: MyCustomAlert
  expr: metric_name > threshold
  for: 5m
  labels:
    severity: warning
```

---

## 🔐 Security Considerations

### By Default
- ✅ Network isolation (private bridge network)
- ✅ No external service exposure without port mapping
- ✅ Volume-based data persistence (not in container)
- ✅ Health checks with automatic recovery
- ✅ Graceful shutdown and restart

### Production Hardening
- [ ] Use `.env.production` for secrets
- [ ] Enable SSL/TLS with reverse proxy
- [ ] Set resource limits (memory/CPU)
- [ ] Regular automated backups
- [ ] Monitor logs for anomalies
- [ ] Update image regularly

---

## 📈 Performance Profiles

### Development Mode
```bash
CONSCIOUSNESS_MODE=test
RECURSION_DEPTH=2
SPIDERWEB_DIMENSION=3
# Fast responses, limited reasoning
```

### Performance Mode
```bash
CONSCIOUSNESS_MODE=performance
RECURSION_DEPTH=3
SPIDERWEB_DIMENSION=4
# Balanced quality and speed
```

### Production Mode (Recommended)
```bash
CONSCIOUSNESS_MODE=full
RECURSION_DEPTH=4
SPIDERWEB_DIMENSION=5
# Full consciousness features
```

### Deep Analysis Mode
```bash
CONSCIOUSNESS_MODE=full
RECURSION_DEPTH=6-8
SPIDERWEB_DIMENSION=5-7
# Highest quality, slower responses
```

---

## 📋 Environment Variables Summary

### Critical Settings
| Variable | Options | Default |
|----------|---------|---------|
| `CONSCIOUSNESS_MODE` | full, performance, test | full |
| `QUANTUM_SPIDERWEB` | true, false | true |
| `MODEL_NAME` | gpt2-large, gpt2-medium | gpt2-large |
| `DEVICE` | cpu, cuda | cpu |

### Tuning Parameters
| Variable | Range | Default |
|----------|-------|---------|
| `RECURSION_DEPTH` | 2-8 | 4 |
| `SPIDERWEB_DIMENSION` | 3-7 | 5 |
| `QUANTUM_FLUCTUATION` | 0.01-0.15 | 0.07 |
| `RC_XI_DIMENSION` | 64-256 | 128 |

### Feature Flags
| Variable | Options | Default |
|----------|---------|---------|
| `COCOON_PERSISTENCE` | enabled, disabled | enabled |
| `ETHICAL_GOVERNANCE` | active, passive | active |
| `ENABLE_EPISTEMIC_TENSION` | true, false | true |
| `ENABLE_ATTRACTOR_DETECTION` | true, false | true |

See `.env.docker` for complete reference.

---

## 🛠️ Management Commands

### Using docker-manage Script
```bash
./docker-manage.sh build          # Build image
./docker-manage.sh run            # Start stack
./docker-manage.sh stop           # Stop stack
./docker-manage.sh restart        # Restart
./docker-manage.sh logs -f        # Follow logs
./docker-manage.sh health         # Check health
./docker-manage.sh status         # Full status
./docker-manage.sh backup         # Backup data
./docker-manage.sh restore [dir]  # Restore backup
./docker-manage.sh deploy         # Production deploy
```

### Using Docker Compose Directly
```bash
# Build
docker build -f Dockerfile.prod -t codette-ai:3.0 .

# Start
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop
docker-compose -f docker-compose.prod.yml down

# Execute command
docker-compose -f docker-compose.prod.yml exec codette-ai python script.py

# Remove volumes
docker-compose -f docker-compose.prod.yml down -v
```

---

## 🐛 Troubleshooting Guide

### Container Won't Start
**Solution**: Check NLTK data download
```bash
./docker-manage.sh logs -f
# Wait ~40 seconds for initialization
```

### Port Already in Use
**Solution**: Change port in docker-compose.prod.yml
```yaml
ports:
  - "7861:7860"  # Map to different port
```

### Out of Memory
**Solution**: Reduce quantum parameters
```bash
RECURSION_DEPTH=2
SPIDERWEB_DIMENSION=3
CONSCIOUSNESS_MODE=performance
```

### Prometheus Not Scraping
**Solution**: Check service health
```bash
./docker-manage.sh health
docker exec codette-ai-consciousness python /app/health_check.py
```

### Slow API Responses
**Solution**: Switch to performance mode
```bash
CONSCIOUSNESS_MODE=performance
RECURSION_DEPTH=2
```

See **DOCKER_PRODUCTION_GUIDE.md** for complete troubleshooting.

---

## 🚀 Deployment Paths

### Path 1: Local Development
```
1. ./docker-manage.sh build
2. ./docker-manage.sh run
3. Visit http://localhost:7860
4. Develop and test
5. ./docker-manage.sh stop
```

### Path 2: Docker Swarm
```
1. docker swarm init
2. docker stack deploy -c docker-compose.prod.yml codette
3. docker stack services codette
4. Monitor via Prometheus
```

### Path 3: Kubernetes
```
1. kompose convert -f docker-compose.prod.yml -o k8s/
2. kubectl apply -f k8s/
3. kubectl get pods
4. Monitor via Prometheus
```

### Path 4: Cloud Deployment
```
1. Push image: ./docker-manage.sh push myregistry
2. Use cloud container service (ECS, ACI, etc.)
3. Configure environment variables
4. Enable monitoring with Prometheus
5. Set up backups
```

---

## 📚 Related Files (Existing)

These are core Codette files referenced by Docker setup:

| File | Purpose |
|------|---------|
| `codette_new.py` | Main entry point (simple) |
| `src/api/app.py` | Gradio web interface |
| `src/components/ai_core.py` | Consciousness orchestrator |
| `quantum_mathematics.py` | 8 core quantum equations |
| `quantum_spiderweb.py` | 5D cognitive graph |
| `cocoon_manager.py` | Persistent memory |
| `database_manager.py` | SQLite persistence |
| `config.json` | System configuration |
| `requirements.txt` | Python dependencies |

---

## ✅ Pre-deployment Checklist

- [ ] Read DOCKER_QUICK_REFERENCE.md
- [ ] Ensure Docker Desktop/Engine is installed
- [ ] Verify ports 7860, 9090, 3000 are available
- [ ] Have at least 4GB free disk space
- [ ] Have at least 2GB free RAM
- [ ] Clone or navigate to codette directory
- [ ] Copy `.env.docker` to `.env.production` for prod
- [ ] Review `docker-compose.prod.yml` for customization
- [ ] Test with `./docker-manage.sh build`
- [ ] Review resource limits for your hardware

---

## 🎯 Next Steps

### Immediate (Next 5 minutes)
1. Read: **DOCKER_QUICK_REFERENCE.md**
2. Run: `./docker-manage.sh build`
3. Run: `./docker-manage.sh run`
4. Visit: http://localhost:7860

### Short-term (Next 30 minutes)
1. Read: **DOCKER_DEPLOYMENT_SUMMARY.md**
2. Check: `./docker-manage.sh health`
3. Explore: http://localhost:3000 (Grafana)
4. Review: `docker-manage.sh logs`

### Medium-term (Next 2 hours)
1. Read: **DOCKER_PRODUCTION_GUIDE.md**
2. Customize: `.env.production`
3. Test: Custom configurations
4. Backup: `./docker-manage.sh backup`

### Long-term (Ongoing)
1. Monitor system health
2. Regular backups (automate)
3. Update image periodically
4. Track metrics in Grafana
5. Review alerts

---

## 🤝 Support & Resources

### Documentation Hierarchy
1. **Quick Start**: DOCKER_QUICK_REFERENCE.md (5 min)
2. **Overview**: DOCKER_DEPLOYMENT_SUMMARY.md (15 min)
3. **Full Guide**: DOCKER_PRODUCTION_GUIDE.md (30 min)
4. **Reference**: .env.docker (all options)
5. **This Index**: DOCKER_DEPLOYMENT_INDEX.md (this file)

### Useful Commands
```bash
# Get help
./docker-manage.sh help

# View comprehensive status
./docker-manage.sh status

# Check health
./docker-manage.sh health

# View logs
./docker-manage.sh logs -f

# Troubleshoot
docker stats codette-ai-consciousness
docker-compose -f docker-compose.prod.yml logs
```

### Common Issues
- Port in use: Change in `docker-compose.prod.yml`
- Memory error: Reduce `RECURSION_DEPTH`
- NLTK error: Wait 40+ seconds, it initializes on startup
- Network issue: Check Docker network `codette-network`

---

## 📞 Additional Help

- **Codette Documentation**: See `/docs/` folder
- **Quantum Details**: See `quantum_mathematics.py`
- **Architecture Details**: See mode instructions (attached)
- **Configuration Reference**: See `config.json`

---

**Version**: 3.0 | **Created**: December 24, 2025 | **Status**: Production-Ready ✅

---

## Quick Navigation

| Need | File | Time |
|------|------|------|
| Commands cheat sheet | DOCKER_QUICK_REFERENCE.md | 5 min |
| Architecture overview | DOCKER_DEPLOYMENT_SUMMARY.md | 15 min |
| Full setup guide | DOCKER_PRODUCTION_GUIDE.md | 30 min |
| Environment variables | .env.docker | - |
| Environment template | .env.docker | - |
| Automation script | docker-manage.sh/bat | - |
| Compose orchestration | docker-compose.prod.yml | - |
| Container definition | Dockerfile.prod | - |

---

**Start here**: Run `./docker-manage.sh build && ./docker-manage.sh run` 🚀
