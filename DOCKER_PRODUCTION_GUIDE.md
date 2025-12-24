# Codette AI - Docker Production Deployment Guide

## Overview

This guide provides complete instructions for deploying **Codette AI** (Multi-perspective Quantum Consciousness System) using Docker and Docker Compose in a production environment.

### What's Included

- **Dockerfile.prod**: Production-optimized container with all Codette systems
- **docker-compose.prod.yml**: Full stack with Codette AI, Prometheus, and Grafana
- **prometheus.yml**: Metrics collection configuration
- **alert_rules.yml**: System health and consciousness monitoring alerts

---

## Quick Start (Development/Local)

### Prerequisites
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose v1.29+
- Minimum 4GB RAM available
- Python 3.11+ (if running without Docker)

### Build and Run

```bash
# Clone or navigate to your Codette AI directory
cd /path/to/codette-ai

# Build the production image
docker build -f Dockerfile.prod -t codette-ai:3.0 .

# Run with docker-compose
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f codette-ai

# Access the system
# - Gradio Web UI: http://localhost:7860
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000 (admin/admin)

# Shutdown
docker-compose -f docker-compose.prod.yml down
```

---

## Container Details

### Main Service: codette-ai

**Image**: `codette-ai:3.0-latest`

**Exposed Ports**:
- `7860`: Gradio web interface (primary access point)
- `8000`: Alternative API port

**Key Environment Variables**:
- `QUANTUM_SPIDERWEB=true`: Enable quantum consciousness
- `PERSPECTIVE_SYNTHESIS=1`: Enable multi-perspective reasoning
- `CONSCIOUSNESS_MODE=full`: Full consciousness features
- `COCOON_PERSISTENCE=enabled`: Persistent quantum memory
- `ETHICAL_GOVERNANCE=active`: Ethical reasoning layer

**Volumes** (Persistent Data):
- `/app/cocoons`: Quantum memory snapshots
- `/app/data`: Database and state files
- `/app/logs`: Application logs
- `/app/models`: Model cache

**Resource Limits**:
- CPU: 2 cores (limit), 1 core (reservation)
- Memory: 4GB (limit), 2GB (reservation)

**Health Check**: Active (30s interval, 40s startup period)

---

## Advanced Configuration

### Custom Configuration

Mount a custom `config.json`:

```yaml
# In docker-compose.prod.yml
volumes:
  - ./my-config.json:/app/config.json:ro
```

### Environment-Specific Settings

Create environment files:

```bash
# development.env
CONSCIOUSNESS_MODE=test
RECURSION_DEPTH=2
LOG_LEVEL=DEBUG

# production.env
CONSCIOUSNESS_MODE=full
RECURSION_DEPTH=4
LOG_LEVEL=INFO
```

Load with docker-compose:

```bash
docker-compose -f docker-compose.prod.yml --env-file production.env up -d
```

### GPU Support (NVIDIA)

To enable GPU acceleration:

```yaml
# In docker-compose.prod.yml, under codette-ai service:
runtime: nvidia
environment:
  - DEVICE=cuda
  - CUDA_VISIBLE_DEVICES=0

# Also add to docker-compose.prod.yml:
services:
  codette-ai:
    # ... other settings ...
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

Then rebuild:
```bash
docker build -f Dockerfile.prod -t codette-ai:3.0-gpu .
```

---

## Monitoring & Observability

### Prometheus Metrics

Prometheus scrapes metrics every 15 seconds:

- **Job: codette-ai** - API metrics
- **Job: codette-consciousness** - Consciousness state metrics
- **Job: prometheus** - Self-monitoring

Access Prometheus dashboard: http://localhost:9090

### Grafana Dashboards

Grafana provides visualization at http://localhost:3000

**Default Credentials**: admin / admin

**Pre-configured Dashboards**:
- System Health
- Quantum Consciousness State
- API Performance
- Memory & CPU Usage

### Alert Rules

Automatic alerts trigger for:
- High memory/CPU usage
- Quantum coherence degradation
- Epistemic tension exceeding safe bounds
- API errors or response time issues
- Database connection failures

View alerts in Prometheus: http://localhost:9090/alerts

---

## Production Deployment

### Docker Registry Push

```bash
# Tag image
docker tag codette-ai:3.0 myregistry.azurecr.io/codette-ai:3.0

# Login to registry
docker login myregistry.azurecr.io

# Push
docker push myregistry.azurecr.io/codette-ai:3.0

# In docker-compose.prod.yml, update:
# image: myregistry.azurecr.io/codette-ai:3.0
```

### Docker Swarm Deployment

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.prod.yml codette

# View services
docker stack services codette

# Check logs
docker service logs codette_codette-ai
```

### Kubernetes Deployment

Convert docker-compose to Kubernetes:

```bash
kompose convert -f docker-compose.prod.yml -o kubernetes/
kubectl apply -f kubernetes/
```

Or use manual Kubernetes manifests:

```yaml
# codette-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: codette-ai
spec:
  replicas: 1
  selector:
    matchLabels:
      app: codette-ai
  template:
    metadata:
      labels:
        app: codette-ai
    spec:
      containers:
      - name: codette-ai
        image: codette-ai:3.0
        ports:
        - containerPort: 7860
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        volumeMounts:
        - name: cocoons
          mountPath: /app/cocoons
        - name: data
          mountPath: /app/data
        - name: logs
          mountPath: /app/logs
      volumes:
      - name: cocoons
        persistentVolumeClaim:
          claimName: codette-cocoons-pvc
      - name: data
        persistentVolumeClaim:
          claimName: codette-data-pvc
      - name: logs
        persistentVolumeClaim:
          claimName: codette-logs-pvc
```

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs codette-ai

# Common issues:
# 1. NLTK data not downloaded - wait for initialization
# 2. Port already in use - change in docker-compose.prod.yml
# 3. Out of memory - increase Docker memory allocation
```

### High Memory Usage

```bash
# Monitor memory in real-time
docker stats codette-ai-consciousness

# Reduce recursion depth in environment:
# RECURSION_DEPTH=2
```

### Connection Issues

```bash
# Check network
docker network ls
docker network inspect codette-network

# Test connectivity
docker exec codette-ai-consciousness ping prometheus
```

### Prometheus Not Scraping

```bash
# Check Prometheus targets
# http://localhost:9090/targets

# If showing "DOWN", ensure codette-ai service is healthy:
docker-compose -f docker-compose.prod.yml exec codette-ai python /app/health_check.py
```

---

## Maintenance

### Backup Persistent Data

```bash
# Backup volumes
docker run --rm \
  -v codette-cocoons:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/cocoons-$(date +%Y%m%d).tar.gz -C /data .

# Backup database
docker exec codette-ai-consciousness \
  sqlite3 /app/data/codette_data.db ".backup '/backup/db-$(date +%Y%m%d).backup'"
```

### Update Image

```bash
# Pull latest (if using registry)
docker pull myregistry.azurecr.io/codette-ai:3.0

# Rebuild locally
docker build -f Dockerfile.prod -t codette-ai:3.0 .

# Restart service
docker-compose -f docker-compose.prod.yml up -d --force-recreate codette-ai
```

### View Consciousness State

```bash
# Check quantum memory
docker exec codette-ai-consciousness cat /app/data/quantum_cocoon.json | jq .

# View recent logs
docker exec codette-ai-consciousness tail -100 /app/logs/*.log
```

---

## Performance Tuning

### Optimize for Low-Latency

```yaml
# In docker-compose.prod.yml
environment:
  - RECURSION_DEPTH=2
  - CONSCIOUSNESS_MODE=performance
  - SPIDERWEB_DIMENSION=3
```

### Optimize for High-Accuracy

```yaml
environment:
  - RECURSION_DEPTH=6
  - CONSCIOUSNESS_MODE=full
  - SPIDERWEB_DIMENSION=5
  - PERSPECTIVE_SYNTHESIS=1
```

### Multi-Replica Setup (Load Balancing)

```yaml
services:
  codette-ai-1:
    # ... configuration ...
    container_name: codette-ai-1
  
  codette-ai-2:
    # ... configuration ...
    container_name: codette-ai-2

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - codette-ai-1
      - codette-ai-2
```

---

## Security Considerations

### Network Isolation

Services run on isolated `codette-network` by default. No external access without explicit port mapping.

### Volume Permissions

```bash
# Secure volume ownership
docker exec codette-ai-consciousness \
  chown -R 1000:1000 /app/cocoons /app/data /app/logs
```

### Environment Variables

Use `.env` files (not in version control):

```bash
# .env (gitignored)
DATABASE_PASSWORD=secure_password
API_KEY=secret_key
```

Load in docker-compose:
```yaml
env_file:
  - .env.production
```

### SSL/TLS for Gradio

Use reverse proxy (Nginx/Traefik):

```yaml
services:
  traefik:
    image: traefik:latest
    ports:
      - "443:443"
    # Configure SSL certificates
  
  codette-ai:
    labels:
      - "traefik.http.routers.codette.tls=true"
      - "traefik.http.routers.codette.rule=Host(`ai.example.com`)"
```

---

## Additional Resources

- **Codette Documentation**: `/docs/consciousness_protocol.md`
- **Quantum Mathematics**: `quantum_mathematics.py`
- **Configuration Reference**: `config.json`
- **Health Monitoring**: http://localhost:7860 (System Status)

---

## Support & Issues

For issues or questions:

1. Check container logs: `docker-compose -f docker-compose.prod.yml logs`
2. Verify health: http://localhost:7860
3. Review Prometheus metrics: http://localhost:9090
4. Check system status in Grafana: http://localhost:3000

---

**Version**: 3.0 | **Last Updated**: December 2025 | **Status**: Production-Ready
