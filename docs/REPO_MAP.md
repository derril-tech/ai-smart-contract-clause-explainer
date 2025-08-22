# Repository Map - ClauseLens AI

This document provides a comprehensive overview of the ClauseLens AI repository structure, explaining the purpose and organization of each directory and file.

## 📁 Root Structure

```
ai-smart-contract-clause-explainer/
├── apps/                    # Main applications
│   ├── web/                # Next.js 14 frontend application
│   └── api/                # FastAPI backend application
├── packages/               # Shared packages and libraries
│   ├── ui/                 # Shared UI components
│   ├── workflows/          # LangGraph workflow definitions
│   ├── retrievers/         # LangChain retrieval tools
│   ├── analyzers/          # Smart contract analysis tools
│   └── lib/                # Shared utilities and types
├── docs/                   # Documentation
├── infra/                  # Infrastructure and deployment
├── tests/                  # Test suites
└── scripts/                # Development and deployment scripts
```

## 🎯 Apps Directory

### `/apps/web` - Frontend Application
**Technology Stack:** Next.js 14, React 18, TypeScript, Tailwind CSS

**Purpose:** The main user interface for ClauseLens AI, providing an intuitive way to analyze smart contracts.

**Key Directories:**
- `src/app/` - Next.js 14 app router pages and layouts
- `src/components/` - Reusable React components
- `src/hooks/` - Custom React hooks
- `src/lib/` - Frontend utilities and API clients
- `src/types/` - TypeScript type definitions
- `public/` - Static assets

**Main Features:**
- Contract address input and validation
- Real-time analysis results display
- Interactive risk heatmaps
- Clause explanations with citations
- Report generation and export
- Dark/light theme support

### `/apps/api` - Backend Application
**Technology Stack:** FastAPI, Python 3.11, SQLAlchemy 2.0, PostgreSQL

**Purpose:** The API server that handles smart contract analysis, AI processing, and data management.

**Key Directories:**
- `app/` - Main application code
  - `api/v1/` - API route definitions
  - `core/` - Core configuration and utilities
  - `models/` - Database models
  - `schemas/` - Pydantic schemas
  - `services/` - Business logic services
  - `utils/` - Utility functions
- `alembic/` - Database migrations
- `scripts/` - Database setup and maintenance scripts

**Main Features:**
- Smart contract ingestion and verification
- AI-powered clause explanation
- Static and dynamic analysis
- Vector similarity search
- Authentication and authorization
- WebSocket support for real-time updates

## 📦 Packages Directory

### `/packages/ui` - Shared UI Components
**Purpose:** Reusable UI components that can be shared between frontend applications.

**Contents:**
- Button components
- Form components
- Layout components
- Data visualization components
- Theme providers

### `/packages/workflows` - LangGraph Workflows
**Purpose:** AI workflow definitions using LangGraph for deterministic, auditable pipelines.

**Contents:**
- Contract analysis workflows
- Explanation generation workflows
- Risk assessment workflows
- Report generation workflows

### `/packages/retrievers` - LangChain Retrieval Tools
**Purpose:** RAG (Retrieval-Augmented Generation) tools for grounding AI responses in source code and documentation.

**Contents:**
- Source code retrievers
- ABI retrievers
- Standards and EIP retrievers
- Documentation retrievers

### `/packages/analyzers` - Smart Contract Analysis Tools
**Purpose:** Integration with static and dynamic analysis tools.

**Contents:**
- Slither integration
- Semgrep integration
- Foundry integration
- Echidna integration
- Custom analysis rules

### `/packages/lib` - Shared Libraries
**Purpose:** Common utilities, types, and configurations shared across the monorepo.

**Contents:**
- Type definitions
- API client utilities
- Common constants
- Validation schemas

## 📚 Documentation

### `/docs` - Project Documentation
- `PROJECT_BRIEF.md` - Complete project specification and requirements
- `PROMPT_DECLARATION.md` - AI collaboration guidelines and instructions
- `CLAUDE.md` - Claude-specific instructions and context
- `REPO_MAP.md` - This file - repository structure overview
- `API_SPEC.md` - API documentation and specifications

## 🏗️ Infrastructure

### `/infra` - Infrastructure and Deployment
**Purpose:** Infrastructure as Code and deployment configurations.

**Contents:**
- Docker configurations
- Kubernetes manifests
- Terraform configurations
- CI/CD pipelines
- Environment configurations

## 🧪 Testing

### `/tests` - Test Suites
**Purpose:** Comprehensive testing across all applications and packages.

**Contents:**
- Unit tests
- Integration tests
- End-to-end tests
- Performance tests
- Security tests

## 🔧 Scripts

### `/scripts` - Development and Deployment Scripts
**Purpose:** Automation scripts for development, testing, and deployment.

**Contents:**
- Development setup scripts
- Database initialization scripts
- Deployment scripts
- Monitoring and health check scripts

## 📋 Key Files

### Root Level
- `package.json` - Monorepo configuration and scripts
- `README.md` - Project overview and quick start
- `.env.example` - Environment variable templates
- `.gitignore` - Git ignore rules
- `docker-compose.yml` - Local development environment

### Frontend (`/apps/web`)
- `next.config.js` - Next.js configuration
- `tailwind.config.js` - Tailwind CSS configuration
- `tsconfig.json` - TypeScript configuration
- `package.json` - Frontend dependencies

### Backend (`/apps/api`)
- `requirements.txt` - Python dependencies
- `alembic.ini` - Database migration configuration
- `main.py` - FastAPI application entry point
- `pyproject.toml` - Python project configuration

## 🎯 Development Workflow

1. **Setup:** Use root `package.json` scripts for initial setup
2. **Development:** Run both frontend and backend in development mode
3. **Testing:** Execute tests from root or individual packages
4. **Building:** Build all applications and packages
5. **Deployment:** Use infrastructure configurations for deployment

## 🔒 Security Considerations

- Environment variables for sensitive configuration
- Authentication and authorization in API
- Input validation and sanitization
- Rate limiting and DDoS protection
- Secure communication (HTTPS/WSS)
- Audit logging for all operations

## 📊 Monitoring and Observability

- Structured logging with correlation IDs
- Metrics collection and monitoring
- Health check endpoints
- Performance monitoring
- Error tracking and alerting

This repository structure follows modern monorepo best practices, ensuring maintainability, scalability, and developer productivity while providing a solid foundation for the ClauseLens AI platform.
