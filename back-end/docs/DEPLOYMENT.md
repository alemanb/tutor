# Deployment Guide

Production deployment guide for the Educational Multi-Agent System.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Docker Deployment](#docker-deployment)
- [Manual Deployment](#manual-deployment)
- [Environment Configuration](#environment-configuration)
- [Monitoring](#monitoring)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

- **OS**: Linux (Ubuntu 20.04+ recommended)
- **RAM**: 2GB minimum, 4GB recommended
- **CPU**: 2 cores minimum
- **Disk**: 5GB available space
- **Network**: Outbound HTTPS access (for Anthropic API)

### Required Software

- Docker 20.10+
- Docker Compose 2.0+
- SSL certificate (for HTTPS)
- Domain name (for production)

---

## Docker Deployment

### Quick Start

1. **Clone Repository**
   ```bash
   git clone https://github.com/your-org/tutor.git
   cd tutor/back-end
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   nano .env  # Add ANTHROPIC_API_KEY
   ```

3. **Start Services**
   ```bash
   docker-compose up -d
   ```

4. **Verify Deployment**
   ```bash
   curl http://localhost:8000/health
   ```

### Build and Run

```bash
# Build the image
docker build -t educational-agent-api:latest .

# Run container
docker run -d \
  --name educational-agent-api \
  -p 8000:8000 \
  -e ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY}" \
  --restart unless-stopped \
  educational-agent-api:latest

# Check logs
docker logs -f educational-agent-api

# Stop container
docker stop educational-agent-api
```

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

---

## Manual Deployment

### Using systemd

1. **Create Service File**
   ```bash
   sudo nano /etc/systemd/system/educational-agent-api.service
   ```

   ```ini
   [Unit]
   Description=Educational Multi-Agent API
   After=network.target

   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/opt/educational-agent
   Environment="ANTHROPIC_API_KEY=your-key"
   ExecStart=/opt/educational-agent/.venv/bin/uvicorn src.agents.server:app --host 0.0.0.0 --port 8000
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

2. **Enable and Start Service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable educational-agent-api
   sudo systemctl start educational-agent-api
   sudo systemctl status educational-agent-api
   ```

### Using Gunicorn

```bash
# Install gunicorn
uv add gunicorn

# Run with gunicorn
gunicorn src.agents.server:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile /var/log/educational-agent/access.log \
  --error-logfile /var/log/educational-agent/error.log
```

---

## Nginx Reverse Proxy

### Configuration

```nginx
upstream educational_agent {
    server localhost:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Timeouts for long-running requests
    proxy_read_timeout 120s;
    proxy_connect_timeout 120s;
    proxy_send_timeout 120s;

    location / {
        proxy_pass http://educational_agent;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files (if needed)
    location /static/ {
        alias /opt/educational-agent/static/;
    }

    # Health check
    location /health {
        proxy_pass http://educational_agent/health;
        access_log off;
    }
}
```

### Enable Configuration

```bash
sudo ln -s /etc/nginx/sites-available/educational-agent /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Environment Configuration

### Production .env

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-api03-your-production-key

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=false
LOG_LEVEL=WARNING

# Security
ALLOWED_ORIGINS=https://your-domain.com

# Performance
MAX_WORKERS=4
TIMEOUT=120
```

### Environment Variables

| Variable | Production Value | Notes |
|----------|-----------------|-------|
| `DEBUG` | `false` | Disable debug mode |
| `LOG_LEVEL` | `WARNING` or `ERROR` | Reduce log verbosity |
| `ALLOWED_ORIGINS` | Specific domain(s) | Restrict CORS |

---

## Monitoring

### Health Checks

```bash
# Basic health check
curl https://your-domain.com/health

# Readiness check
curl https://your-domain.com/health/ready

# Detailed status
curl https://your-domain.com/api/v1/agents/info
```

### Logging

```bash
# Docker logs
docker logs -f educational-agent-api

# Systemd logs
sudo journalctl -u educational-agent-api -f

# Application logs
tail -f /var/log/educational-agent/error.log
```

### Monitoring Tools

**Prometheus + Grafana** (recommended):

1. Add prometheus client:
   ```bash
   uv add prometheus-fastapi-instrumentator
   ```

2. Update `server.py`:
   ```python
   from prometheus_fastapi_instrumentator import Instrumentator

   Instrumentator().instrument(app).expose(app)
   ```

3. Access metrics at `/metrics`

---

## Security Considerations

### 1. API Key Management

- Never commit API keys to version control
- Use environment variables or secrets management
- Rotate keys regularly
- Use separate keys for production/development

### 2. CORS Configuration

Update `server.py` for production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # Specific domain
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Limit methods
    allow_headers=["*"],
)
```

### 3. Rate Limiting

Add rate limiting middleware:

```bash
uv add slowapi
```

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/v1/generate")
@limiter.limit("5/minute")
async def generate_code(request: Request, ...):
    ...
```

### 4. HTTPS Only

- Always use HTTPS in production
- Use Let's Encrypt for free SSL certificates
- Redirect HTTP to HTTPS

### 5. Input Validation

- Pydantic models validate all inputs
- Add additional validation for prompt length
- Sanitize user inputs

---

## Scaling

### Horizontal Scaling

```yaml
# docker-compose.yml for multiple instances
services:
  api:
    image: educational-agent-api:latest
    deploy:
      replicas: 3
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - api
```

### Load Balancing

Use Nginx or cloud load balancer:

```nginx
upstream educational_agent {
    least_conn;
    server api-1:8000;
    server api-2:8000;
    server api-3:8000;
}
```

---

## Backup and Recovery

### Backup Considerations

The application is stateless, so backups are minimal:

1. **Environment Configuration**: Backup `.env` file
2. **Database** (if using AgentOS): Regular PostgreSQL backups
3. **Logs**: Archive logs periodically

### Disaster Recovery

```bash
# Export Docker image
docker save educational-agent-api:latest > backup.tar

# Restore Docker image
docker load < backup.tar

# Restore from backup
docker-compose down
cp .env.backup .env
docker-compose up -d
```

---

## Troubleshooting

### Issue: Container won't start

```bash
# Check logs
docker logs educational-agent-api

# Common causes:
# - Missing ANTHROPIC_API_KEY
# - Port 8000 already in use
# - Invalid configuration
```

### Issue: 500 errors

```bash
# Check API key
echo $ANTHROPIC_API_KEY

# Verify API key has credits
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"

# Check logs for detailed error
docker logs -f educational-agent-api
```

### Issue: Slow responses

- Increase timeout settings
- Check Anthropic API status
- Monitor server resources
- Consider adding caching

---

## Production Checklist

- [ ] ANTHROPIC_API_KEY configured
- [ ] DEBUG=false in production
- [ ] HTTPS enabled with valid certificate
- [ ] CORS configured for specific domain
- [ ] Rate limiting implemented
- [ ] Logging configured
- [ ] Monitoring set up
- [ ] Backups configured
- [ ] Health checks working
- [ ] Firewall configured
- [ ] Regular security updates scheduled

---

## Cloud Deployment

### AWS

1. Use ECS or EKS for container orchestration
2. Store API key in AWS Secrets Manager
3. Use Application Load Balancer
4. Enable CloudWatch for logging

### Google Cloud

1. Use Cloud Run for serverless deployment
2. Store API key in Secret Manager
3. Use Cloud Load Balancing
4. Enable Cloud Logging

### Azure

1. Use Azure Container Instances or AKS
2. Store API key in Key Vault
3. Use Azure Load Balancer
4. Enable Azure Monitor

---

**Last Updated**: November 6, 2025
