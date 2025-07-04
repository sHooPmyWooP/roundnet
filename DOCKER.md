# Docker Usage Guide

This document explains how to run the Roundnet Player Management System in Docker containers.

## Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Start the application
docker-compose up -d

# Access at http://localhost:8501
```

### Option 2: Using Docker Build Scripts

```bash
# Build and run development version
./docker.sh build
./docker.sh run

# Or build and run production version
./docker.sh build-prod
./docker.sh run-prod
```

### Option 3: Manual Docker Commands

```bash
# Build the image
docker build -t roundnet:latest .

# Run the container
docker run -d \
  --name roundnet-app \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  roundnet:latest
```

## Docker Images

### Development Image (`Dockerfile`)
- Based on Python 3.13-slim
- Includes uv package manager
- Suitable for development and testing
- Single-stage build

### Production Image (`Dockerfile.prod`)
- Multi-stage build for optimized size
- Non-root user for security
- Minimal attack surface
- Optimized for production deployment

## Environment Variables

| Variable                               | Default   | Description               |
| -------------------------------------- | --------- | ------------------------- |
| `STREAMLIT_SERVER_PORT`                | `8501`    | Port for Streamlit server |
| `STREAMLIT_SERVER_ADDRESS`             | `0.0.0.0` | Server bind address       |
| `STREAMLIT_SERVER_HEADLESS`            | `true`    | Run without browser       |
| `STREAMLIT_BROWSER_GATHER_USAGE_STATS` | `false`   | Disable telemetry         |

## Data Persistence

Data is stored in the `/app/data` directory inside the container. To persist data between container restarts:

```bash
# Mount local data directory
docker run -v $(pwd)/data:/app/data roundnet:latest
```

## Development Mode

For development with live reload:

```bash
# Start development container
docker-compose --profile dev up -d roundnet-dev

# Access at http://localhost:8502
```

This mounts the source code directory for live reloading when files change.

## Docker Management Script

The `docker.sh` script provides convenient commands:

```bash
# Build images
./docker.sh build           # Development image
./docker.sh build-prod      # Production image

# Run containers
./docker.sh run             # Development container
./docker.sh run-prod        # Production container

# Compose operations
./docker.sh up              # Start with docker-compose
./docker.sh down            # Stop docker-compose
./docker.sh dev             # Development mode

# Maintenance
./docker.sh logs            # View logs
./docker.sh stop            # Stop container
./docker.sh restart         # Restart container
./docker.sh clean           # Clean up resources
```

## Health Checks

Both images include health checks that verify the Streamlit server is responding:

```bash
# Check container health
docker ps

# View health check logs
docker inspect roundnet-app | grep -A 10 Health
```

## Troubleshooting

### Container won't start
```bash
# Check logs
docker logs roundnet-app

# Or use the script
./docker.sh logs
```

### Permission issues with data directory
```bash
# Fix permissions
chmod 755 data/
```

### Port already in use
```bash
# Use different port
docker run -p 8502:8501 roundnet:latest

# Or with script
./docker.sh run roundnet:latest 8502
```

### Container cleanup
```bash
# Remove stopped containers and images
./docker.sh clean
```

## Production Deployment

For production deployment:

1. Use the production Dockerfile:
   ```bash
   docker build -f Dockerfile.prod -t roundnet:prod .
   ```

2. Run with proper resource limits:
   ```bash
   docker run -d \
     --name roundnet-prod \
     -p 80:8501 \
     -v /path/to/data:/app/data \
     --memory=512m \
     --cpus=0.5 \
     --restart=unless-stopped \
     roundnet:prod
   ```

3. Consider using a reverse proxy (nginx) for SSL termination and load balancing.

## Security Considerations

- Production image runs as non-root user
- Minimal base image reduces attack surface
- Health checks ensure service availability
- Data directory permissions are properly set
- No sensitive information in environment variables
