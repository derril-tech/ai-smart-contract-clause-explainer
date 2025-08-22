# ClauseLens AI - Smart Contract Clause Explainer

> Turn on-chain code into plain-English obligations, risks, and rights—instantly.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node.js](https://img.shields.io/badge/node.js-18+-green.svg)](https://nodejs.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)

## 🎯 Overview

ClauseLens AI is an AI-powered platform that transforms complex smart contract code into understandable plain-English explanations. It provides comprehensive security analysis, risk assessment, and actionable insights for blockchain developers, auditors, and security researchers.

### Key Features

- 🤖 **AI-Powered Explanations** - Plain-English explanations of smart contract functions, modifiers, and events
- 🔒 **Comprehensive Security Analysis** - Advanced static and dynamic analysis using industry-standard tools
- 📊 **Risk Assessment & Mapping** - Visual risk heatmaps and privilege mapping
- ⚡ **Instant Results** - Get analysis results in seconds, not hours
- 📄 **Detailed Reports** - Generate comprehensive PDF and Markdown reports
- 🌐 **Multi-Chain Support** - Analyze contracts across Ethereum, Polygon, BSC, Arbitrum, and more
- 🔐 **Enterprise Security** - Bank-grade security with JWT authentication and audit logging

## 🏗️ Architecture

This is a monorepo containing:

- **Frontend** (`apps/web`) - Next.js 14 React application
- **Backend** (`apps/api`) - FastAPI Python application
- **Shared Packages** (`packages/`) - Reusable components and utilities

### Tech Stack

**Frontend:**
- Next.js 14 with App Router
- React 18 with TypeScript
- Tailwind CSS for styling
- React Query for state management
- Framer Motion for animations

**Backend:**
- FastAPI with Python 3.11
- SQLAlchemy 2.0 with async support
- PostgreSQL with pgvector for embeddings
- Redis for caching and queues
- LangChain + LangGraph for AI workflows

**AI & Analysis:**
- OpenAI GPT-4 and Anthropic Claude
- Slither, Semgrep, Foundry, Echidna
- RAG (Retrieval-Augmented Generation)
- Vector similarity search

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- PostgreSQL 14+ with pgvector extension
- Redis 6+

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/clauselens-ai.git
cd clauselens-ai
```

### 2. Install Dependencies

```bash
# Install root dependencies
npm install

# Install frontend dependencies
cd apps/web
npm install

# Install backend dependencies
cd ../api
pip install -r requirements.txt
```

### 3. Environment Setup

```bash
# Copy environment template
cp env.example .env

# Edit .env with your configuration
# Set up database, API keys, and other required values
```

### 4. Database Setup

```bash
# Start PostgreSQL and Redis (using Docker)
docker-compose up -d postgres redis

# Run database migrations
cd apps/api
alembic upgrade head
```

### 5. Start Development Servers

```bash
# From the root directory
npm run dev

# This will start both frontend (port 3000) and backend (port 8000)
```

### 6. Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## 📖 Documentation

- [Project Brief](./PROJECT_BRIEF.md) - Complete project specification
- [API Documentation](./docs/API_SPEC.md) - API endpoints and schemas
- [Repository Map](./docs/REPO_MAP.md) - Project structure overview
- [Claude Instructions](./docs/CLAUDE.md) - AI collaboration guidelines

## 🧪 Testing

```bash
# Run frontend tests
cd apps/web
npm run test

# Run backend tests
cd apps/api
pytest

# Run end-to-end tests
npm run test:e2e
```

## 🏭 Production Deployment

### Frontend (Vercel)

```bash
# Deploy to Vercel
vercel --prod
```

### Backend (Render/Docker)

```bash
# Build Docker image
docker build -t clauselens-api .

# Deploy to Render or other cloud platform
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow the existing code style and conventions
- Write tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation:** [docs.clauselens.ai](https://docs.clauselens.ai)
- **Issues:** [GitHub Issues](https://github.com/your-org/clauselens-ai/issues)
- **Discussions:** [GitHub Discussions](https://github.com/your-org/clauselens-ai/discussions)
- **Email:** hello@clauselens.ai

## 🙏 Acknowledgments

- [OpenZeppelin](https://openzeppelin.com/) for smart contract security best practices
- [Slither](https://github.com/crytic/slither) for static analysis
- [Foundry](https://getfoundry.sh/) for development and testing framework
- [LangChain](https://langchain.com/) for AI workflow orchestration

---

**Built with ❤️ for the blockchain community**
