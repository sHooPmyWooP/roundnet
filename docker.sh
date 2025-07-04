#!/bin/bash

# Docker build and run scripts for roundnet application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to build Docker image
build_image() {
    local dockerfile=${1:-Dockerfile}
    local tag=${2:-roundnet:latest}

    print_status "Building Docker image with $dockerfile..."
    docker build -f "$dockerfile" -t "$tag" .
    print_status "Build completed successfully!"
}

# Function to run container
run_container() {
    local tag=${1:-roundnet:latest}
    local port=${2:-8501}

    print_status "Starting container on port $port..."
    docker run -d \
        --name roundnet-app \
        -p "$port:8501" \
        -v "$(pwd)/data:/app/data" \
        --restart unless-stopped \
        "$tag"

    print_status "Container started successfully!"
    print_status "Access the application at: http://localhost:$port"
}

# Function to stop and remove container
stop_container() {
    print_status "Stopping and removing container..."
    docker stop roundnet-app 2>/dev/null || true
    docker rm roundnet-app 2>/dev/null || true
    print_status "Container stopped and removed!"
}

# Function to show logs
show_logs() {
    docker logs -f roundnet-app
}

# Function to run with docker-compose
compose_up() {
    print_status "Starting with docker-compose..."
    docker-compose up -d
    print_status "Services started! Access at: http://localhost:8501"
}

# Function to stop docker-compose
compose_down() {
    print_status "Stopping docker-compose services..."
    docker-compose down
    print_status "Services stopped!"
}

# Function to run development mode
dev_mode() {
    print_status "Starting development mode with live reload..."
    docker-compose --profile dev up -d roundnet-dev
    print_status "Development server started! Access at: http://localhost:8502"
}

# Main script logic
case "${1:-help}" in
    "build")
        build_image "${2:-Dockerfile}" "${3:-roundnet:latest}"
        ;;
    "build-prod")
        build_image "Dockerfile.prod" "roundnet:prod"
        ;;
    "run")
        stop_container
        run_container "${2:-roundnet:latest}" "${3:-8501}"
        ;;
    "run-prod")
        stop_container
        run_container "roundnet:prod" "${2:-8501}"
        ;;
    "stop")
        stop_container
        ;;
    "logs")
        show_logs
        ;;
    "restart")
        stop_container
        sleep 2
        run_container "${2:-roundnet:latest}" "${3:-8501}"
        ;;
    "up")
        compose_up
        ;;
    "down")
        compose_down
        ;;
    "dev")
        dev_mode
        ;;
    "clean")
        print_status "Cleaning up Docker resources..."
        docker-compose down 2>/dev/null || true
        stop_container
        docker rmi roundnet:latest roundnet:prod 2>/dev/null || true
        print_status "Cleanup completed!"
        ;;
    "help"|*)
        echo "Roundnet Docker Management Script"
        echo ""
        echo "Usage: $0 [command] [options]"
        echo ""
        echo "Commands:"
        echo "  build [dockerfile] [tag]  - Build Docker image (default: Dockerfile, roundnet:latest)"
        echo "  build-prod               - Build production image"
        echo "  run [tag] [port]         - Run container (default: roundnet:latest, port 8501)"
        echo "  run-prod [port]          - Run production container"
        echo "  stop                     - Stop and remove container"
        echo "  logs                     - Show container logs"
        echo "  restart [tag] [port]     - Restart container"
        echo "  up                       - Start with docker-compose"
        echo "  down                     - Stop docker-compose services"
        echo "  dev                      - Start development mode with live reload"
        echo "  clean                    - Clean up all Docker resources"
        echo "  help                     - Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0 build                 - Build development image"
        echo "  $0 build-prod            - Build production image"
        echo "  $0 run                   - Run development container"
        echo "  $0 run-prod              - Run production container"
        echo "  $0 up                    - Start with docker-compose"
        echo "  $0 dev                   - Start development mode"
        ;;
esac
