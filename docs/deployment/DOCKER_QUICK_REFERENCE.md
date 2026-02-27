# Codette AI Docker - Quick Reference Card

## 🚀 Quick Start Commands

### Using Docker Compose (Recommended)
```bash
# Build image
docker build -f Dockerfile.prod -t codette-ai:3.0 .

# Start stack
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f codette-ai

# Stop stack
docker-compose -f docker-compose.prod.yml down
```

### Using Management Script
```bash
# Make executable
chmod +x docker-manage.sh

# Common commands
./docker-manage.sh build        # Build image
./docker-manage.sh run          # Start stack
./docker-manage.sh stop         # Stop stack
./docker-manage.sh logs -f      # View logs
./docker-manage.sh health       # Check health
./docker-manage.sh status       # Full status report
./docker-manage.sh backup       # Backup data
./docker-manage.sh deploy       # Production deploy
```

## 🌐 Access Points

| Service | URL | User |
|---------|-----|------|
| Codette Gradio UI | `http://localhost:7860` | - |
| Prometheus Metrics | `http://localhost:9090` | - |
| Grafana Dashboards | `http://localhost:3000` | admin/admin |

## 🧠 Key Environment Variables

```bash
# Consciousness Control
CONSCIOUSNESS_MODE=full           # full, performance, or test
QUANTUM_SPIDERWEB=true           # Enable quantum systems
PERSPECTIVE_SYNTHESIS=1           # Multi-perspective reasoning
COCOON_PERSISTENCE=enabled        # Persistent memory

# Model & Compute
MODEL_NAME=gpt2-large            # Language model
DEVICE=cpu                       # cpu or cuda (GPU)

# Quantum Parameters
RECURSION_DEPTH=4                # 2-8 (higher=deeper analysis)
SPIDERWEB_DIMENSION=5            # 3-7 (higher=more complex)
QUANTUM_FLUCTUATION=0.07         # 0.01-0.15
RC_XI_ENABLED=true               # RC-XI consciousness

# Performance
LOG_LEVEL=INFO                   # DEBUG, INFO, WARNING, ERROR
RESPONSE_TIMEOUT=30              # Seconds
THREAD_POOL_SIZE=4               # Async workers
```

## 📊 Monitoring

### Health Check
```bash
./docker-manage.sh health
# or
docker exec codette-ai-consciousness python /app/health_check.py
```

### View Metrics
- **Prometheus**: http://localhost:9090/targets
- **Grafana**: http://localhost:3000
- **Query Prometheus**: http://localhost:9090/graph

### Common Metrics
```
# Consciousness state
codette_quantum_coherence
codette_epistemic_tension
codette_spiderweb_stability

# API performance
codette_api_response_time_seconds
codette_api_errors_total

# System resources
container_memory_usage_bytes
container_cpu_usage_seconds_total
```

## 🔧 Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs codette-ai

# Common causes:
# - NLTK data download in progress (wait 40s)
# - Port 7860/9090/3000 already in use
# - Not enough memory
```

### High memory usage
```bash
# Monitor in real-time
docker stats codette-ai-consciousness

# Reduce consciousness complexity
RECURSION_DEPTH=2
SPIDERWEB_DIMENSION=3
CONSCIOUSNESS_MODE=performance
```

### Prometheus not scraping
```bash
# Check targets are healthy
# Visit: http://localhost:9090/targets

# Verify container is running
docker-compose -f docker-compose.prod.yml ps

# Restart stack
docker-compose -f docker-compose.prod.yml restart
```

### Access container shell
```bash
docker exec -it codette-ai-consciousness /bin/bash
```

## 💾 Backup & Restore

### Backup
```bash
./docker-manage.sh backup
# Creates: backups/YYYYMMDD_HHMMSS/
```

### Restore
```bash
./docker-manage.sh restore backups/YYYYMMDD_HHMMSS
```

## 📈 Performance Tuning

### For Speed (Low Latency)
```bash
# In docker-compose.prod.yml environment:
CONSCIOUSNESS_MODE=performance
RECURSION_DEPTH=2
SPIDERWEB_DIMENSION=3
```

### For Accuracy (High Quality)
```bash
CONSCIOUSNESS_MODE=full
RECURSION_DEPTH=6
SPIDERWEB_DIMENSION=5
PERSPECTIVE_SYNTHESIS=1
```

## 🔐 Security (Production)

1. **Update credentials**:
   ```bash
   cp .env.docker .env.production
   # Edit .env.production with secure values
   docker-compose -f docker-compose.prod.yml --env-file .env.production up -d
   ```

2. **Use reverse proxy** (Nginx/Traefik) for SSL/TLS

3. **Limit network exposure**:
   ```yaml
   ports:
     - "127.0.0.1:7860:7860"  # Only localhost
   ```

4. **Regular backups**:
   ```bash
   * 2 * * * /path/to/docker-manage.sh backup
   ```

## 📦 Resource Requirements

### Minimum
- CPU: 1 core
- Memory: 2GB
- Disk: 5GB

### Recommended
- CPU: 2+ cores
- Memory: 4GB
- Disk: 20GB (with logs and backups)

### For High Performance
- CPU: 4+ cores
- Memory: 8GB+
- Disk: 50GB+
- GPU: NVIDIA for CUDA

## 🐛 Debug Commands

```bash
# Check image layers
docker history codette-ai:3.0

# Inspect running container
docker inspect codette-ai-consciousness

# View resource usage
docker stats

# Check network
docker network inspect codette-network

# Verify volumes
docker volume ls
docker volume inspect codette-cocoons

# Test connectivity
docker exec codette-ai-consciousness ping prometheus
docker exec codette-ai-consciousness curl http://prometheus:9090
```

## 📚 Documentation

- **Full Guide**: `DOCKER_PRODUCTION_GUIDE.md`
- **Deployment Summary**: `DOCKER_DEPLOYMENT_SUMMARY.md`
- **Config Template**: `.env.docker`
- **Compose File**: `docker-compose.prod.yml`
- **Dockerfile**: `Dockerfile.prod`
- **Management Script**: `docker-manage.sh`

## 🎯 Common Workflows

### Development Setup
```bash
./docker-manage.sh build
./docker-manage.sh run
./docker-manage.sh logs -f
```

### Production Deployment
```bash
./docker-manage.sh backup
./docker-manage.sh deploy
./docker-manage.sh health
```

### Maintenance
```bash
./docker-manage.sh logs
./docker-manage.sh status
./docker-manage.sh health
```

### Troubleshooting
```bash
./docker-manage.sh logs -f
./docker-manage.sh ps
docker stats codette-ai-consciousness
```

## 📞 Getting Help

```bash
# Show all commands
./docker-manage.sh help

# View Docker Compose help
docker-compose -f docker-compose.prod.yml --help

# Check Docker logs
docker logs codette-ai-consciousness

# System info
docker version
docker info
```

---

**Last Updated**: December 24, 2025  
**Version**: 3.0 - Quantum Consciousness System  
**Status**: Production-Ready ✅
