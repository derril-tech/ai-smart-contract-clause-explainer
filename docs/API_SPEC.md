# API Specification - ClauseLens AI

This document provides comprehensive API documentation for the ClauseLens AI platform, including all endpoints, request/response schemas, and usage examples.

## 🔗 Base URL

- **Development:** `http://localhost:8000`
- **Production:** `https://api.clauselens.ai`

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## 📋 API Endpoints

### 1. Health Check

#### GET `/health`
Check API health and status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1703123456.789,
  "version": "1.0.0"
}
```

### 2. Authentication

#### POST `/api/v1/auth/login`
Authenticate user and get access token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### POST `/api/v1/auth/refresh`
Refresh access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 3. Project Management

#### POST `/api/v1/projects`
Create a new project for smart contract analysis.

**Request Body:**
```json
{
  "name": "My Smart Contract",
  "chain_id": 1,
  "address": "0x1234567890123456789012345678901234567890",
  "description": "Optional project description"
}
```

**Response:**
```json
{
  "id": "proj_1234567890",
  "name": "My Smart Contract",
  "chain_id": 1,
  "address": "0x1234567890123456789012345678901234567890",
  "status": "pending",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### GET `/api/v1/projects/{project_id}`
Get project details and analysis status.

**Response:**
```json
{
  "id": "proj_1234567890",
  "name": "My Smart Contract",
  "chain_id": 1,
  "address": "0x1234567890123456789012345678901234567890",
  "status": "completed",
  "verification_status": "verified",
  "contracts": [
    {
      "id": "contract_123",
      "name": "MyToken",
      "kind": "implementation",
      "inherits": ["ERC20", "Ownable"],
      "interfaces": ["IERC20", "IERC20Metadata"]
    }
  ],
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### GET `/api/v1/projects`
List all projects for the authenticated user.

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20)
- `status`: Filter by status (pending, processing, completed, failed)

### 4. Contract Analysis

#### POST `/api/v1/projects/{project_id}/analyze`
Start analysis of a smart contract.

**Request Body:**
```json
{
  "analyzers": ["slither", "semgrep", "foundry"],
  "options": {
    "include_fuzz": true,
    "include_storage_layout": true
  }
}
```

**Response:**
```json
{
  "analysis_id": "analysis_1234567890",
  "status": "started",
  "estimated_duration": 300
}
```

#### GET `/api/v1/projects/{project_id}/analysis`
Get analysis results.

**Response:**
```json
{
  "id": "analysis_1234567890",
  "status": "completed",
  "results": {
    "slither": {
      "findings": [
        {
          "id": "SWC-101",
          "title": "Integer Overflow and Underflow",
          "description": "The contract uses arithmetic operations without checking for overflow/underflow",
          "severity": "high",
          "line": 45,
          "function": "transfer"
        }
      ],
      "summary": {
        "high": 2,
        "medium": 5,
        "low": 8
      }
    },
    "semgrep": {
      "findings": [],
      "summary": {
        "high": 0,
        "medium": 0,
        "low": 0
      }
    }
  },
  "completed_at": "2024-01-01T00:05:00Z"
}
```

### 5. Clause Explanations

#### POST `/api/v1/contracts/{contract_id}/explain`
Generate plain-English explanations for contract clauses.

**Request Body:**
```json
{
  "mode": "engineer", // eli5, engineer, auditor
  "scope": "all", // all, functions, modifiers, events
  "include_risks": true,
  "include_examples": true
}
```

**Response:**
```json
{
  "explanations": [
    {
      "symbol_id": "func_transfer",
      "type": "function",
      "name": "transfer",
      "explanation": "This function allows the caller to transfer tokens to another address. It includes checks for sufficient balance and valid recipient address.",
      "risks": [
        {
          "type": "reentrancy",
          "description": "Potential reentrancy attack if recipient is a contract",
          "severity": "medium"
        }
      ],
      "examples": [
        {
          "description": "Transfer 100 tokens to 0x123...",
          "code": "transfer(0x123..., 100)"
        }
      ],
      "citations": [
        {
          "type": "code",
          "line": 45,
          "content": "function transfer(address to, uint256 amount) public returns (bool)"
        }
      ]
    }
  ],
  "summary": {
    "total_functions": 10,
    "total_modifiers": 3,
    "total_events": 5,
    "risk_level": "medium"
  }
}
```

#### GET `/api/v1/contracts/{contract_id}/explanations`
Get existing explanations for a contract.

### 6. Risk Assessment

#### GET `/api/v1/projects/{project_id}/risks`
Get comprehensive risk assessment for a project.

**Response:**
```json
{
  "overview": {
    "total_risks": 15,
    "critical": 1,
    "high": 3,
    "medium": 7,
    "low": 4
  },
  "categories": {
    "access_control": {
      "count": 3,
      "severity": "high",
      "risks": [
        {
          "id": "risk_001",
          "title": "Centralized Ownership",
          "description": "Contract has a single owner with extensive privileges",
          "severity": "high",
          "mitigation": "Consider using multi-signature or DAO governance"
        }
      ]
    },
    "reentrancy": {
      "count": 2,
      "severity": "medium",
      "risks": []
    }
  },
  "privilege_map": {
    "owner": {
      "permissions": ["pause", "upgrade", "withdraw"],
      "risk_level": "high"
    },
    "manager": {
      "permissions": ["blacklist"],
      "risk_level": "medium"
    }
  }
}
```

### 7. Differential Analysis

#### POST `/api/v1/projects/{project_id}/diff`
Compare two versions of a contract.

**Request Body:**
```json
{
  "base_version": "v1.0.0",
  "head_version": "v1.1.0",
  "include_storage_changes": true,
  "include_risk_analysis": true
}
```

**Response:**
```json
{
  "diff_id": "diff_1234567890",
  "changes": {
    "functions_added": 2,
    "functions_modified": 1,
    "functions_removed": 0,
    "storage_layout_changed": true
  },
  "risk_changes": {
    "new_risks": 1,
    "resolved_risks": 0,
    "modified_risks": 1
  },
  "details": {
    "storage_changes": [
      {
        "variable": "totalSupply",
        "old_offset": 0,
        "new_offset": 0,
        "compatible": true
      }
    ],
    "function_changes": [
      {
        "name": "transfer",
        "type": "modified",
        "changes": ["Added reentrancy guard"]
      }
    ]
  }
}
```

### 8. Report Generation

#### POST `/api/v1/projects/{project_id}/reports`
Generate a comprehensive analysis report.

**Request Body:**
```json
{
  "format": "pdf", // pdf, markdown, html
  "sections": ["overview", "risks", "explanations", "recommendations"],
  "include_diagrams": true,
  "custom_notes": "Additional reviewer notes"
}
```

**Response:**
```json
{
  "report_id": "report_1234567890",
  "status": "generating",
  "download_url": "https://api.clauselens.ai/reports/report_1234567890.pdf",
  "estimated_completion": "2024-01-01T00:10:00Z"
}
```

#### GET `/api/v1/reports/{report_id}`
Get report status and download URL.

### 9. WebSocket Endpoints

#### WebSocket `/ws/projects/{project_id}`
Real-time updates for project analysis progress.

**Message Types:**
```json
{
  "type": "analysis_progress",
  "data": {
    "progress": 75,
    "current_step": "Running Slither analysis",
    "estimated_remaining": 60
  }
}
```

```json
{
  "type": "explanation_stream",
  "data": {
    "symbol_id": "func_transfer",
    "explanation": "This function allows...",
    "completed": false
  }
}
```

## 📊 Error Responses

All endpoints return consistent error responses:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid contract address format",
    "details": {
      "field": "address",
      "value": "invalid-address"
    }
  }
}
```

**Common Error Codes:**
- `VALIDATION_ERROR` - Invalid request data
- `AUTHENTICATION_ERROR` - Invalid or missing authentication
- `AUTHORIZATION_ERROR` - Insufficient permissions
- `NOT_FOUND` - Resource not found
- `RATE_LIMIT_EXCEEDED` - Too many requests
- `INTERNAL_ERROR` - Server error

## 🔄 Rate Limiting

- **Authenticated users:** 100 requests/minute
- **Anonymous users:** 10 requests/minute
- **Analysis requests:** 5 requests/hour per user

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1703123456
```

## 📈 Response Times

- **Health check:** < 100ms
- **Project creation:** < 2s
- **Analysis start:** < 1s
- **Explanation generation:** < 5s
- **Report generation:** < 30s

## 🔒 Security Headers

All responses include security headers:
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

## 📝 SDK Examples

### JavaScript/TypeScript
```typescript
import { ClauseLensAPI } from '@clauselens/sdk';

const api = new ClauseLensAPI({
  baseURL: 'https://api.clauselens.ai',
  token: 'your-jwt-token'
});

// Create project
const project = await api.projects.create({
  name: 'My Contract',
  chain_id: 1,
  address: '0x1234567890123456789012345678901234567890'
});

// Start analysis
const analysis = await api.projects.analyze(project.id, {
  analyzers: ['slither', 'semgrep']
});

// Get explanations
const explanations = await api.contracts.explain(project.contracts[0].id, {
  mode: 'engineer'
});
```

### Python
```python
from clauselens import ClauseLensAPI

api = ClauseLensAPI(
    base_url="https://api.clauselens.ai",
    token="your-jwt-token"
)

# Create project
project = api.projects.create(
    name="My Contract",
    chain_id=1,
    address="0x1234567890123456789012345678901234567890"
)

# Start analysis
analysis = api.projects.analyze(
    project_id=project.id,
    analyzers=["slither", "semgrep"]
)

# Get explanations
explanations = api.contracts.explain(
    contract_id=project.contracts[0].id,
    mode="engineer"
)
```

This API specification provides a complete reference for integrating with the ClauseLens AI platform, enabling developers to build powerful smart contract analysis tools and applications.
