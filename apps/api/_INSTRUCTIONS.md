# Backend API Instructions - ClauseLens AI

This directory contains the FastAPI backend application for ClauseLens AI.

## 🎯 Purpose
The backend API provides comprehensive smart contract analysis capabilities, including:
- Smart contract ingestion and verification
- AI-powered clause explanation generation
- Static and dynamic analysis integration
- Vector similarity search for RAG
- Authentication and authorization
- Real-time WebSocket updates

## 📁 Structure

```
apps/api/
├── app/
│   ├── api/
│   │   └── v1/             # API version 1 routes
│   │       ├── auth.py     # Authentication endpoints
│   │       ├── projects.py # Project management
│   │       ├── contracts.py # Contract analysis
│   │       ├── analysis.py # Analysis results
│   │       ├── reports.py  # Report generation
│   │       └── websocket.py # WebSocket handlers
│   ├── core/               # Core configuration
│   │   ├── config.py       # Settings management
│   │   ├── database.py     # Database configuration
│   │   ├── security.py     # Authentication & security
│   │   └── logging.py      # Logging setup
│   ├── models/             # Database models
│   │   ├── user.py         # User model
│   │   ├── project.py      # Project model
│   │   ├── contract.py     # Contract model
│   │   ├── analysis.py     # Analysis model
│   │   └── report.py       # Report model
│   ├── schemas/            # Pydantic schemas
│   │   ├── user.py         # User schemas
│   │   ├── project.py      # Project schemas
│   │   ├── contract.py     # Contract schemas
│   │   └── analysis.py     # Analysis schemas
│   ├── services/           # Business logic
│   │   ├── auth.py         # Authentication service
│   │   ├── contract.py     # Contract analysis service
│   │   ├── ai.py           # AI explanation service
│   │   ├── analysis.py     # Static analysis service
│   │   └── report.py       # Report generation service
│   └── utils/              # Utility functions
│       ├── blockchain.py   # Blockchain utilities
│       ├── validators.py   # Input validation
│       └── helpers.py      # General helpers
├── alembic/                # Database migrations
├── scripts/                # Setup and maintenance scripts
├── tests/                  # Test suite
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
└── pyproject.toml          # Project configuration
```

## 🚀 TODO: Implementation Tasks

### Phase 1: Core Infrastructure
- [ ] **TODO: Set up database models** (`app/models/`)
  - [ ] User model with authentication fields
  - [ ] Project model with relationships
  - [ ] Contract model with metadata
  - [ ] Analysis model with results storage
  - [ ] Report model with generation tracking

- [ ] **TODO: Create Pydantic schemas** (`app/schemas/`)
  - [ ] Request/response schemas for all endpoints
  - [ ] Validation schemas for input data
  - [ ] Serialization schemas for database models
  - [ ] Error response schemas

- [ ] **TODO: Implement authentication system** (`app/core/security.py`)
  - [ ] JWT token generation and validation
  - [ ] Password hashing and verification
  - [ ] Role-based access control (RBAC)
  - [ ] Rate limiting middleware

### Phase 2: API Endpoints
- [ ] **TODO: Build authentication endpoints** (`app/api/v1/auth.py`)
  - [ ] User registration and login
  - [ ] Token refresh endpoint
  - [ ] Password reset functionality
  - [ ] User profile management

- [ ] **TODO: Create project management endpoints** (`app/api/v1/projects.py`)
  - [ ] Project creation and listing
  - [ ] Project details and status
  - [ ] Project update and deletion
  - [ ] Project sharing and collaboration

- [ ] **TODO: Implement contract analysis endpoints** (`app/api/v1/contracts.py`)
  - [ ] Contract ingestion and verification
  - [ ] Analysis initiation and monitoring
  - [ ] Results retrieval and caching
  - [ ] Explanation generation

### Phase 3: Business Logic Services
- [ ] **TODO: Develop contract analysis service** (`app/services/contract.py`)
  - [ ] Blockchain API integration
  - [ ] Contract verification logic
  - [ ] Source code parsing and analysis
  - [ ] ABI extraction and validation

- [ ] **TODO: Build AI explanation service** (`app/services/ai.py`)
  - [ ] LangChain integration
  - [ ] RAG implementation with pgvector
  - [ ] Explanation generation workflows
  - [ ] Citation and evidence linking

- [ ] **TODO: Create static analysis service** (`app/services/analysis.py`)
  - [ ] Slither integration
  - [ ] Semgrep integration
  - [ ] Foundry integration
  - [ ] Custom analysis rules

### Phase 4: Advanced Features
- [ ] **TODO: Implement WebSocket support** (`app/api/v1/websocket.py`)
  - [ ] Real-time analysis progress updates
  - [ ] Live explanation streaming
  - [ ] Connection management
  - [ ] Message broadcasting

- [ ] **TODO: Add report generation service** (`app/services/report.py`)
  - [ ] PDF generation with templates
  - [ ] Markdown export functionality
  - [ ] Custom report customization
  - [ ] Report sharing and distribution

## 🔧 Development Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Initialize database:**
   ```bash
   alembic upgrade head
   ```

4. **Start development server:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Run tests:**
   ```bash
   pytest
   ```

## 🗄️ Database Design

### Core Tables
- **users** - User accounts and authentication
- **projects** - Smart contract projects
- **contracts** - Contract metadata and source code
- **artifacts** - Contract artifacts (source, ABI, bytecode)
- **analyses** - Analysis results and findings
- **explanations** - AI-generated explanations
- **reports** - Generated reports and exports

### Vector Storage
- **embeddings** - Vector embeddings for RAG
- **documents** - Indexed documents for retrieval

## 🔐 Security Implementation

### Authentication
- JWT tokens with refresh mechanism
- Password hashing with bcrypt
- Rate limiting per user/IP
- Session management

### Authorization
- Role-based access control
- Resource-level permissions
- API key management
- Audit logging

### Data Protection
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- CORS configuration

## 📊 Performance Optimization

### Database
- Connection pooling
- Query optimization
- Indexing strategy
- Caching layer

### API Performance
- Response caching
- Background task processing
- Async/await patterns
- Load balancing support

### Vector Search
- pgvector optimization
- Embedding caching
- Similarity search indexing
- Batch processing

## 🧪 Testing Strategy

### Unit Tests
- Service layer testing
- Model validation testing
- Utility function testing
- Mock external dependencies

### Integration Tests
- API endpoint testing
- Database integration testing
- External service testing
- Authentication flow testing

### Performance Tests
- Load testing
- Stress testing
- Memory usage testing
- Response time testing

## 📈 Monitoring and Observability

### Logging
- Structured logging with correlation IDs
- Log levels and filtering
- Log aggregation and analysis
- Error tracking and alerting

### Metrics
- Request/response metrics
- Database performance metrics
- AI model usage metrics
- Business metrics tracking

### Health Checks
- Database connectivity
- External service health
- System resource monitoring
- Custom health indicators

## 🔄 Background Tasks

### Celery Integration
- Analysis job queuing
- Report generation tasks
- Email notifications
- Data processing tasks

### Task Management
- Job status tracking
- Retry mechanisms
- Error handling
- Resource cleanup

## 🌐 External Integrations

### Blockchain APIs
- Etherscan API integration
- Blockscout API integration
- Multi-chain support
- Rate limit management

### AI Services
- OpenAI API integration
- Anthropic API integration
- Model selection and fallback
- Cost optimization

### Analysis Tools
- Slither integration
- Semgrep integration
- Foundry integration
- Custom tool integration

## 🚀 Deployment

### Docker Configuration
- Multi-stage builds
- Environment-specific configs
- Health check endpoints
- Resource limits

### Kubernetes Deployment
- Horizontal pod autoscaling
- Resource management
- Service mesh integration
- Monitoring integration

### CI/CD Pipeline
- Automated testing
- Security scanning
- Performance testing
- Deployment automation

## 📝 API Documentation

### OpenAPI/Swagger
- Auto-generated documentation
- Interactive API explorer
- Request/response examples
- Authentication documentation

### SDK Generation
- TypeScript SDK
- Python SDK
- JavaScript SDK
- Go SDK

This backend API provides the foundation for all smart contract analysis capabilities, ensuring scalability, security, and performance for the ClauseLens AI platform.
