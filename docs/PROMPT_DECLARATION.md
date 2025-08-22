# PROMPT_DECLARATION.md - AI Development Guidelines

## 🎯 Mission Statement

This is the frontier of digital trust and security. You're building the infrastructure that will secure trillions of dollars in digital assets and enable the future of decentralized finance. Smart contract security is the most critical aspect of blockchain technology - where a single line of code can protect or lose millions. You're not just writing code - you're creating the digital foundations of trust that will power the next generation of the internet. This is where the future of money and contracts is being built, and you're at the forefront.

## 🏗️ Technical Architecture

### Frontend Stack (Next.js 14)
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS with custom design system
- **State Management**: Zustand (global state) + React Query (server state)
- **UI Components**: Radix UI primitives + custom components
- **Animations**: Framer Motion
- **Real-time**: WebSocket connections for streaming analysis
- **Testing**: Jest + React Testing Library + Playwright (E2E)

### Backend Stack (FastAPI)
- **Framework**: FastAPI with async/await
- **Language**: Python 3.11+
- **Database**: PostgreSQL with pgvector for embeddings
- **ORM**: SQLAlchemy 2.0 (async)
- **Authentication**: JWT with refresh tokens
- **Caching**: Redis for sessions and analysis results
- **Queue System**: Celery for background tasks
- **AI Integration**: LangChain + LangGraph + OpenAI/Anthropic
- **Security Analysis**: Slither + Semgrep + Foundry + Echidna
- **Testing**: Pytest + pytest-asyncio

### AI/ML Infrastructure
- **RAG System**: Vector similarity search with pgvector
- **Embeddings**: OpenAI text-embedding-ada-002
- **LLM**: GPT-4 + Claude-3 for analysis
- **Streaming**: Real-time analysis updates via WebSocket
- **Prompt Engineering**: Structured prompts for consistent analysis

## 📋 Development Guidelines

### Code Quality Standards
1. **TypeScript Strict Mode**: No `any` types, proper interfaces
2. **Python Type Hints**: Full type annotations required
3. **Error Handling**: Comprehensive try-catch blocks
4. **Logging**: Structured logging with correlation IDs
5. **Testing**: 80%+ test coverage, E2E tests for critical flows
6. **Documentation**: Inline comments for complex logic
7. **Security**: Input validation, SQL injection prevention, XSS protection

### Security Requirements
- **Authentication**: JWT with refresh token rotation
- **Authorization**: Role-based access control (RBAC)
- **Input Validation**: Pydantic models for all API inputs
- **Rate Limiting**: Per-user and per-endpoint limits
- **CORS**: Production-ready CORS configuration
- **HTTPS**: All communications encrypted
- **Audit Logging**: All security events logged
- **Vulnerability Scanning**: Regular dependency updates

### Performance Targets
- **Frontend**: < 2s page load, < 500KB bundle size
- **Backend**: < 200ms API response time (95th percentile)
- **Database**: < 50ms query time
- **Concurrent Users**: Support 1000+ simultaneous users
- **Uptime**: 99.9% availability

## 🎨 UI/UX Design System

### Color Palette
```css
/* Primary Colors */
--primary-50: #eff6ff;
--primary-500: #3b82f6;
--primary-900: #1e3a8a;

/* Risk Levels */
--risk-low: #10b981;
--risk-medium: #f59e0b;
--risk-high: #ef4444;
--risk-critical: #7c2d12;

/* Semantic Colors */
--success: #10b981;
--warning: #f59e0b;
--error: #ef4444;
--info: #3b82f6;
```

### Typography
- **Primary Font**: Inter (sans-serif)
- **Code Font**: JetBrains Mono (monospace)
- **Heading Scale**: 2xl, xl, lg, md, sm, xs
- **Body Text**: Base 16px with 1.5 line height

### Component Patterns
- **Cards**: Consistent padding, rounded corners, subtle shadows
- **Buttons**: Primary, secondary, outline, ghost variants
- **Forms**: Proper validation states, error messages
- **Tables**: Sortable columns, pagination, responsive design
- **Modals**: Backdrop blur, smooth animations, keyboard navigation

## 🔧 Development Workflow

### Local Development Setup
```bash
# Frontend
cd apps/web
npm install
npm run dev

# Backend
cd apps/api
pip install -r requirements.txt
uvicorn main:app --reload

# Database
docker-compose up -d postgres redis
```

### Environment Configuration
```bash
# Required Environment Variables
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
DATABASE_URL=postgresql://user:pass@localhost:5432/clauselens
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
JWT_SECRET_KEY=your_jwt_secret
```

### Testing Strategy
```bash
# Frontend Tests
npm run test          # Unit tests
npm run test:e2e      # End-to-end tests
npm run test:coverage # Coverage report

# Backend Tests
pytest                # Unit tests
pytest --cov          # Coverage report
pytest --asyncio-mode=auto  # Async tests
```

## 📊 Data Models

### Core Entities
```typescript
// User Management
interface User {
  id: string;
  email: string;
  name: string;
  role: 'user' | 'admin' | 'analyst';
  created_at: Date;
  updated_at: Date;
}

// Project Management
interface Project {
  id: string;
  name: string;
  description: string;
  user_id: string;
  contracts: Contract[];
  created_at: Date;
  updated_at: Date;
}

// Contract Analysis
interface Contract {
  id: string;
  address: string;
  chain_id: number;
  name: string;
  source_code: string;
  abi: any[];
  analysis_status: 'pending' | 'analyzing' | 'completed' | 'failed';
  findings: SecurityFinding[];
  risks: RiskAssessment[];
  created_at: Date;
  updated_at: Date;
}

// Security Analysis
interface SecurityFinding {
  id: string;
  contract_id: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  category: 'access-control' | 'arithmetic' | 'reentrancy' | 'gas' | 'other';
  title: string;
  description: string;
  recommendation: string;
  line_number?: number;
  tool: 'slither' | 'semgrep' | 'ai-analysis';
  created_at: Date;
}

// Risk Assessment
interface RiskAssessment {
  id: string;
  contract_id: string;
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  category: 'financial' | 'operational' | 'technical' | 'regulatory';
  title: string;
  description: string;
  impact: string;
  probability: number; // 0-1
  mitigation: string;
  created_at: Date;
}
```

## 🔄 API Integration Patterns

### REST API Endpoints
```typescript
// Authentication
POST /api/v1/auth/login
POST /api/v1/auth/refresh
POST /api/v1/auth/logout

// Projects
GET    /api/v1/projects
POST   /api/v1/projects
GET    /api/v1/projects/{id}
PUT    /api/v1/projects/{id}
DELETE /api/v1/projects/{id}

// Contract Analysis
POST   /api/v1/contracts/analyze
POST   /api/v1/contracts/upload
GET    /api/v1/contracts/{id}/status
GET    /api/v1/contracts/{id}/results

// Reports
POST   /api/v1/reports/generate
GET    /api/v1/reports/{id}/status
GET    /api/v1/reports/{id}/download
```

### WebSocket Events
```typescript
// Real-time Updates
interface WebSocketMessage {
  type: 'analysis_progress' | 'analysis_complete' | 'error';
  data: any;
  timestamp: Date;
}

// Connection Management
ws://localhost:8000/ws/projects/{project_id}
ws://localhost:8000/ws/analysis/{analysis_id}
```

## 🧠 AI Integration Guidelines

### Prompt Engineering
```typescript
// Structured Analysis Prompts
const ANALYSIS_PROMPT = `
You are a smart contract security expert. Analyze the following contract:

Contract Address: {address}
Chain: {chain}
Source Code:
{source_code}

Provide analysis in the following JSON format:
{
  "findings": [
    {
      "severity": "high|medium|low|critical",
      "category": "access-control|arithmetic|reentrancy|gas|other",
      "title": "Brief title",
      "description": "Detailed description",
      "recommendation": "How to fix",
      "line_number": 123
    }
  ],
  "risks": [
    {
      "level": "high|medium|low|critical",
      "category": "financial|operational|technical|regulatory",
      "title": "Risk title",
      "description": "Risk description",
      "impact": "Potential impact",
      "probability": 0.8,
      "mitigation": "How to mitigate"
    }
  ]
}
`;
```

### Vector Search Integration
```python
# Embedding Generation
async def generate_embeddings(text: str) -> List[float]:
    response = await openai.Embedding.acreate(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

# Similarity Search
async def find_similar_contracts(embedding: List[float], limit: int = 5):
    query = """
    SELECT contract_id, similarity(embedding, $1) as score
    FROM contract_embeddings
    WHERE similarity(embedding, $1) > 0.7
    ORDER BY score DESC
    LIMIT $2
    """
    return await db.execute(query, [embedding, limit])
```

## 🚀 Deployment Strategy

### Frontend Deployment (Vercel)
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "installCommand": "npm install",
  "framework": "nextjs"
}
```

### Backend Deployment (Render)
```yaml
# render.yaml
services:
  - type: web
    name: clauselens-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: clauselens-db
          property: connectionString
```

### Database Migration
```python
# Alembic migrations
alembic revision --autogenerate -m "Add contract embeddings table"
alembic upgrade head
```

## 📈 Monitoring & Observability

### Logging Strategy
```python
# Structured Logging
import structlog

logger = structlog.get_logger()

logger.info(
    "contract_analysis_started",
    contract_address="0x123...",
    user_id="user_123",
    analysis_type="security"
)
```

### Metrics Collection
```python
# Prometheus Metrics
from prometheus_client import Counter, Histogram

analysis_requests = Counter('analysis_requests_total', 'Total analysis requests')
analysis_duration = Histogram('analysis_duration_seconds', 'Analysis duration')
```

### Error Tracking
```typescript
// Sentry Integration
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
});
```

## 🔍 Code Review Checklist

### Before Implementation
- [ ] Requirements clearly understood
- [ ] Security implications considered
- [ ] Performance impact evaluated
- [ ] Test strategy defined
- [ ] Error handling planned
- [ ] Logging requirements identified

### During Development
- [ ] TypeScript strict mode enabled
- [ ] All inputs validated
- [ ] Error boundaries implemented
- [ ] Loading states handled
- [ ] Accessibility requirements met
- [ ] Mobile responsiveness tested

### Before Deployment
- [ ] All tests passing
- [ ] Security scan completed
- [ ] Performance benchmarks met
- [ ] Documentation updated
- [ ] Environment variables configured
- [ ] Monitoring alerts set up

## 🎯 Success Criteria

### Technical Metrics
- **Test Coverage**: > 80%
- **Performance**: < 2s page load, < 200ms API response
- **Security**: Zero critical vulnerabilities
- **Uptime**: > 99.9%
- **User Satisfaction**: > 4.5/5

### Business Metrics
- **Analysis Accuracy**: > 95%
- **User Adoption**: > 1000 active users
- **Revenue Growth**: > 20% month-over-month
- **Customer Retention**: > 90%

---

**Remember**: You're building the future of smart contract security. Every decision, every line of code, every feature contributes to securing the digital economy. The stakes are high, but the impact is monumental.