#!/bin/bash

# Codette AI - Docker Management Script
# Simplifies common Docker and Docker Compose operations
# Usage: ./docker-manage.sh [command]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.prod.yml"
DOCKERFILE="Dockerfile.prod"
IMAGE_NAME="codette-ai"
IMAGE_TAG="3.0"
CONTAINER_NAME="codette-ai-consciousness"

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ️  ${NC}$1"
}

log_success() {
    echo -e "${GREEN}✅ ${NC}$1"
}

log_warning() {
    echo -e "${YELLOW}⚠️  ${NC}$1"
}

log_error() {
    echo -e "${RED}❌ ${NC}$1"
}

# Show usage
show_usage() {
    cat << EOF
Codette AI - Docker Management

USAGE:
    ./docker-manage.sh [COMMAND] [OPTIONS]

COMMANDS:
    build           Build the Docker image
    push            Push image to registry
    run             Start the Docker Compose stack
    stop            Stop the Docker Compose stack
    restart         Restart the Docker Compose stack
    logs            Show container logs
    shell           Open shell in running container
    ps              Show running containers
    health          Check system health
    backup          Backup persistent data
    restore         Restore from backup
    clean           Clean up containers and volumes
    deploy          Deploy to production (with confirmation)
    status          Show detailed status
    help            Show this help message

EXAMPLES:
    ./docker-manage.sh build
    ./docker-manage.sh run
    ./docker-manage.sh logs -f
    ./docker-manage.sh health
    ./docker-manage.sh deploy

EOF
}

# Build image
cmd_build() {
    log_info "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
    docker build -f "$DOCKERFILE" -t "${IMAGE_NAME}:${IMAGE_TAG}" .
    log_success "Image built successfully"
}

# Push to registry
cmd_push() {
    local registry="${1:-myregistry.azurecr.io}"
    log_info "Pushing image to registry: $registry"
    
    docker tag "${IMAGE_NAME}:${IMAGE_TAG}" "${registry}/${IMAGE_NAME}:${IMAGE_TAG}"
    docker push "${registry}/${IMAGE_NAME}:${IMAGE_TAG}"
    
    log_success "Image pushed to registry"
}

# Start containers
cmd_run() {
    log_info "Starting Codette AI stack..."
    docker-compose -f "$COMPOSE_FILE" up -d
    log_success "Stack started"
    
    sleep 3
    log_info "Waiting for services to initialize (30-40 seconds)..."
    sleep 37
    
    log_success "Services ready!"
    cmd_status
}

# Stop containers
cmd_stop() {
    log_info "Stopping Codette AI stack..."
    docker-compose -f "$COMPOSE_FILE" down
    log_success "Stack stopped"
}

# Restart containers
cmd_restart() {
    log_info "Restarting Codette AI stack..."
    docker-compose -f "$COMPOSE_FILE" restart
    log_success "Stack restarted"
}

# Show logs
cmd_logs() {
    log_info "Showing Codette AI logs (Ctrl+C to exit)..."
    docker-compose -f "$COMPOSE_FILE" logs "$@" codette-ai
}

# Open shell
cmd_shell() {
    log_info "Opening shell in container..."
    docker exec -it "$CONTAINER_NAME" /bin/bash
}

# Show running processes
cmd_ps() {
    log_info "Running containers:"
    docker-compose -f "$COMPOSE_FILE" ps
}

# Health check
cmd_health() {
    log_info "Checking Codette AI health..."
    
    if docker exec "$CONTAINER_NAME" python /app/health_check.py >/dev/null 2>&1; then
        log_success "Codette AI is healthy ✓"
    else
        log_error "Codette AI health check failed"
        return 1
    fi
    
    log_info "Checking Prometheus..."
    if curl -s http://localhost:9090/-/healthy >/dev/null 2>&1; then
        log_success "Prometheus is healthy ✓"
    else
        log_warning "Prometheus not available"
    fi
    
    log_info "Checking Gradio interface..."
    if curl -s http://localhost:7860/ >/dev/null 2>&1; then
        log_success "Gradio interface is available at http://localhost:7860 ✓"
    else
        log_warning "Gradio interface not available"
    fi
}

# Backup data
cmd_backup() {
    local backup_dir="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    log_info "Backing up persistent data to $backup_dir..."
    
    # Backup cocoons
    docker run --rm \
        -v codette-cocoons:/data \
        -v "$(pwd)/$backup_dir:/backup" \
        alpine tar czf /backup/cocoons.tar.gz -C /data . 2>/dev/null || true
    
    # Backup database
    docker exec "$CONTAINER_NAME" \
        sqlite3 /app/data/codette_data.db ".backup '/tmp/db.backup'" 2>/dev/null || true
    docker cp "$CONTAINER_NAME:/tmp/db.backup" "$backup_dir/db.backup" 2>/dev/null || true
    
    # Backup quantum state
    docker cp "$CONTAINER_NAME:/app/data/quantum_cocoon.json" "$backup_dir/" 2>/dev/null || true
    
    log_success "Backup completed: $backup_dir"
}

# Restore from backup
cmd_restore() {
    local backup_dir="${1:-.}"
    
    if [ ! -f "$backup_dir/cocoons.tar.gz" ]; then
        log_error "Backup not found in $backup_dir"
        return 1
    fi
    
    log_warning "This will restore data from $backup_dir"
    read -p "Continue? (y/N): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Restore cancelled"
        return 0
    fi
    
    log_info "Restoring backup..."
    
    docker run --rm \
        -v codette-cocoons:/data \
        -v "$(pwd)/$backup_dir:/backup" \
        alpine tar xzf /backup/cocoons.tar.gz -C /data
    
    if [ -f "$backup_dir/db.backup" ]; then
        docker cp "$backup_dir/db.backup" "$CONTAINER_NAME:/tmp/db.backup"
        docker exec "$CONTAINER_NAME" \
            sqlite3 /app/data/codette_data.db ".restore '/tmp/db.backup'"
    fi
    
    log_success "Restore completed"
}

# Clean up
cmd_clean() {
    log_warning "This will remove all containers, networks, and volumes"
    read -p "Continue? (y/N): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Clean cancelled"
        return 0
    fi
    
    log_info "Cleaning up..."
    docker-compose -f "$COMPOSE_FILE" down -v
    log_success "Cleanup completed"
}

# Deploy to production
cmd_deploy() {
    log_warning "Production deployment will start Codette AI services"
    read -p "Continue? (y/N): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Deployment cancelled"
        return 0
    fi
    
    log_info "Building image for production..."
    cmd_build
    
    log_info "Starting production stack..."
    docker-compose -f "$COMPOSE_FILE" up -d
    
    log_success "Production deployment completed!"
    sleep 40
    cmd_health
}

# Show status
cmd_status() {
    echo ""
    log_info "=== Codette AI Status ==="
    echo ""
    
    cmd_ps
    
    echo ""
    log_info "=== System Access Points ==="
    echo -e "Gradio Web UI:     ${BLUE}http://localhost:7860${NC}"
    echo -e "Prometheus:        ${BLUE}http://localhost:9090${NC}"
    echo -e "Grafana:           ${BLUE}http://localhost:3000${NC} (admin/admin)"
    echo ""
    
    cmd_health
    
    echo ""
    log_info "=== Docker Statistics ==="
    docker stats --no-stream "$CONTAINER_NAME" 2>/dev/null || log_warning "Container not running"
}

# Main command handler
main() {
    local command="${1:-help}"
    
    case "$command" in
        build)   cmd_build "$@" ;;
        push)    cmd_push "$@" ;;
        run)     cmd_run "$@" ;;
        stop)    cmd_stop "$@" ;;
        restart) cmd_restart "$@" ;;
        logs)    cmd_logs "$@" ;;
        shell)   cmd_shell "$@" ;;
        ps)      cmd_ps "$@" ;;
        health)  cmd_health "$@" ;;
        backup)  cmd_backup "$@" ;;
        restore) cmd_restore "$@" ;;
        clean)   cmd_clean "$@" ;;
        deploy)  cmd_deploy "$@" ;;
        status)  cmd_status "$@" ;;
        help)    show_usage ;;
        *)
            log_error "Unknown command: $command"
            echo ""
            show_usage
            exit 1
            ;;
    esac
}

# Run main if script is executed (not sourced)
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi
