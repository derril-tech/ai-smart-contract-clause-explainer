# Deployment Guide - ClauseLens AI

## 🚀 Overview

This guide covers deploying ClauseLens AI to various environments, from local development to production. The application consists of:

- **Frontend**: Next.js 14 application
- **Backend**: FastAPI application
- **Database**: PostgreSQL with pgvector
- **Cache**: Redis
- **Queue**: Celery with Redis broker
- **Monitoring**: Prometheus + Grafana

## 📋 Prerequisites

### Required Software
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### Required Accounts
- OpenAI API key
- Anthropic API key
- Docker Hub account (for production)
- GitHub account (for CI/CD)

## 🏠 Local Development

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/clauselens-ai.git
   cd clauselens-ai
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

3. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Grafana: http://localhost:3001 (admin/admin)

### Manual Setup

1. **Backend Setup**
   ```bash
   cd apps/api
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

2. **Frontend Setup**
   ```bash
   cd apps/web
   npm install
   npm run dev
   ```

3. **Database Setup**
   ```bash
   # Start PostgreSQL and Redis
   docker-compose up -d postgres redis
   
   # Run migrations
   cd apps/api
   alembic upgrade head
   ```

## 🧪 Staging Environment

### Deployment Options

#### Option 1: Docker Compose (Recommended)
```bash
# Deploy to staging server
git clone https://github.com/your-org/clauselens-ai.git
cd clauselens-ai
cp .env.example .env.staging
# Configure staging environment variables
docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d
```

#### Option 2: Kubernetes
```bash
# Apply staging configuration
kubectl apply -f k8s/staging/
kubectl get pods -n clauselens-staging
```

#### Option 3: Cloud Platforms

**Render (Recommended for small teams)**
1. Connect GitHub repository to Render
2. Create new Web Service for backend
3. Create new Static Site for frontend
4. Configure environment variables
5. Deploy

**Railway**
1. Connect GitHub repository
2. Add PostgreSQL and Redis services
3. Configure environment variables
4. Deploy

### Staging Configuration

Create `docker-compose.staging.yml`:
```yaml
version: '3.8'
services:
  api:
    environment:
      - ENVIRONMENT=staging
      - DATABASE_URL=${STAGING_DATABASE_URL}
      - REDIS_URL=${STAGING_REDIS_URL}
    ports:
      - "8000:8000"
  
  web:
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_URL=${STAGING_API_URL}
    ports:
      - "3000:3000"
```

## 🌐 Production Environment

### Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │   CDN (CloudFlare) │    │   Monitoring   │
│   (Nginx/ALB)   │    │                 │    │   (Prometheus)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Database      │
│   (Next.js)     │    │   (FastAPI)     │    │   (PostgreSQL)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cache         │    │   Queue         │    │   Storage       │
│   (Redis)       │    │   (Celery)      │    │   (S3/MinIO)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Deployment Options

#### Option 1: Kubernetes (Enterprise)

**Prerequisites:**
- Kubernetes cluster (EKS, GKE, AKS)
- Helm 3.x
- kubectl configured

**Deployment:**
```bash
# Add Helm repository
helm repo add clauselens https://charts.clauselens.ai
helm repo update

# Install with custom values
helm install clauselens clauselens/clauselens-ai \
  --namespace clauselens \
  --create-namespace \
  --values values-production.yaml
```

**Production values.yaml:**
```yaml
# values-production.yaml
global:
  environment: production
  
frontend:
  replicas: 3
  resources:
    requests:
      memory: "256Mi"
      cpu: "250m"
    limits:
      memory: "512Mi"
      cpu: "500m"
  
backend:
  replicas: 5
  resources:
    requests:
      memory: "512Mi"
      cpu: "500m"
    limits:
      memory: "1Gi"
      cpu: "1000m"
  
database:
  postgresql:
    enabled: false  # Use managed service
    external:
      host: your-rds-endpoint
      port: 5432
      database: clauselens
      username: clauselens
  
redis:
  enabled: false  # Use managed service
  external:
    host: your-elasticache-endpoint
    port: 6379
  
monitoring:
  enabled: true
  prometheus:
    retention: 30d
  grafana:
    adminPassword: your-secure-password
```

#### Option 2: Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.prod.yml clauselens
```

#### Option 3: Cloud Platforms

**AWS ECS/Fargate**
1. Create ECS cluster
2. Create task definitions for frontend and backend
3. Create ALB for load balancing
4. Configure auto-scaling
5. Set up RDS and ElastiCache

**Google Cloud Run**
1. Build and push Docker images
2. Deploy frontend to Cloud Run
3. Deploy backend to Cloud Run
4. Configure Cloud SQL and Memorystore
5. Set up Cloud Load Balancing

**Azure Container Instances**
1. Create container registry
2. Deploy containers to ACI
3. Configure Azure Database for PostgreSQL
4. Set up Azure Cache for Redis
5. Configure Application Gateway

### Production Configuration

#### Environment Variables
```bash
# Production .env
ENVIRONMENT=production
DATABASE_URL=postgresql://user:pass@host:5432/clauselens
REDIS_URL=redis://:password@host:6379
SECRET_KEY=your-very-secure-secret-key
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# Security
CORS_ORIGINS=https://your-domain.com
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Monitoring
SENTRY_DSN=your-sentry-dsn
PROMETHEUS_ENABLED=true

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_PER_HOUR=1000
```

#### SSL/TLS Configuration
```nginx
# nginx.conf
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/ssl/certs/clauselens.crt;
    ssl_certificate_key /etc/ssl/private/clauselens.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Proxy to backend
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Serve frontend
    location / {
        root /app/frontend/.next;
        try_files $uri $uri/ /index.html;
    }
}
```

## 🔧 CI/CD Pipeline

### GitHub Actions

The repository includes a comprehensive CI/CD pipeline:

1. **Lint & Security**: Code quality and vulnerability scanning
2. **Testing**: Unit, integration, and E2E tests
3. **Build**: Docker image building and pushing
4. **Deploy**: Automatic deployment to staging/production

### Manual Deployment

```bash
# Build and push Docker images
docker build -t clauselens/clauselens-ai:latest .
docker push clauselens/clauselens-ai:latest

# Deploy to production
kubectl apply -f k8s/production/
# or
docker stack deploy -c docker-compose.prod.yml clauselens
```

## 📊 Monitoring & Observability

### Health Checks

```bash
# Application health
curl https://your-domain.com/health

# Database health
curl https://your-domain.com/api/v1/health/db

# Redis health
curl https://your-domain.com/api/v1/health/redis
```

### Metrics & Logging

**Prometheus Metrics:**
- Request duration
- Error rates
- Database connection pool
- Redis operations
- Analysis job metrics

**Grafana Dashboards:**
- Application performance
- Infrastructure metrics
- Business metrics
- Security alerts

**Log Aggregation:**
- Structured logging with correlation IDs
- Centralized log collection (ELK stack)
- Error tracking with Sentry

### Alerting

Configure alerts for:
- High error rates (>5%)
- Slow response times (>2s)
- Database connection issues
- Redis memory usage
- Disk space usage
- SSL certificate expiration

## 🔒 Security

### Security Checklist

- [ ] HTTPS enabled with valid certificates
- [ ] Security headers configured
- [ ] Rate limiting enabled
- [ ] Input validation implemented
- [ ] SQL injection prevention
- [ ] XSS protection
- [ ] CSRF protection
- [ ] Secrets management
- [ ] Regular security updates
- [ ] Vulnerability scanning
- [ ] Access logging
- [ ] Backup encryption

### Secrets Management

**AWS Secrets Manager:**
```bash
# Store secrets
aws secretsmanager create-secret \
  --name clauselens/production \
  --secret-string '{"DATABASE_URL":"...","SECRET_KEY":"..."}'

# Retrieve in application
aws secretsmanager get-secret-value --secret-id clauselens/production
```

**HashiCorp Vault:**
```bash
# Store secrets
vault kv put secret/clauselens/production \
  DATABASE_URL="postgresql://..." \
  SECRET_KEY="your-secret-key"

# Retrieve in application
vault kv get secret/clauselens/production
```

## 📈 Scaling

### Horizontal Scaling

**Backend API:**
```yaml
# Kubernetes HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: clauselens-api
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: clauselens-api
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

**Database Scaling:**
- Read replicas for read-heavy workloads
- Connection pooling (PgBouncer)
- Query optimization
- Index optimization

**Cache Scaling:**
- Redis Cluster for high availability
- Cache warming strategies
- Cache invalidation policies

### Performance Optimization

1. **Frontend:**
   - Code splitting
   - Image optimization
   - CDN for static assets
   - Service worker for caching

2. **Backend:**
   - Database query optimization
   - Redis caching
   - Async processing
   - Connection pooling

3. **Infrastructure:**
   - Load balancing
   - Auto-scaling
   - CDN
   - Database optimization

## 🚨 Disaster Recovery

### Backup Strategy

**Database Backups:**
```bash
# Automated daily backups
pg_dump -h host -U user -d clauselens | gzip > backup_$(date +%Y%m%d).sql.gz

# Point-in-time recovery
pg_restore -h host -U user -d clauselens backup_file.sql
```

**Application Data:**
- User uploads to S3/MinIO
- Configuration backups
- Log archives

### Recovery Procedures

1. **Database Recovery:**
   - Restore from latest backup
   - Apply transaction logs
   - Verify data integrity

2. **Application Recovery:**
   - Deploy from backup images
   - Restore configuration
   - Verify functionality

3. **Infrastructure Recovery:**
   - Recreate infrastructure
   - Restore from backups
   - Update DNS records

## 📞 Support

### Troubleshooting

**Common Issues:**
1. Database connection errors
2. Redis connection issues
3. API rate limiting
4. SSL certificate problems
5. Memory leaks

**Debug Commands:**
```bash
# Check application logs
kubectl logs -f deployment/clauselens-api

# Check database connectivity
kubectl exec -it pod/clauselens-api -- pg_isready -h db

# Check Redis connectivity
kubectl exec -it pod/clauselens-api -- redis-cli -h redis ping

# Monitor resources
kubectl top pods
```

### Getting Help

- **Documentation**: Check `/docs` directory
- **Issues**: Create GitHub issue
- **Discussions**: Use GitHub Discussions
- **Email**: support@clauselens.ai

---

**Remember**: Always test deployments in staging first, and have a rollback plan ready for production deployments.
