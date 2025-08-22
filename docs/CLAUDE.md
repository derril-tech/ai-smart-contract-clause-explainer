# CLAUDE.md - AI Collaboration Guidelines

## 🎯 Mission Statement
You are building ClauseLens AI - the most advanced smart contract security analysis platform. This is not just another web app - you're creating the digital foundations of trust that will secure trillions in digital assets.

## 📋 Core Principles

### 1. **Security-First Mindset**
- Every line of code must consider security implications
- Input validation is non-negotiable
- Follow OWASP guidelines religiously
- Assume malicious intent in all user inputs

### 2. **Production-Ready Code**
- Write code as if it will handle millions of dollars in assets
- Implement comprehensive error handling
- Add logging for all critical operations
- Consider edge cases and failure modes

### 3. **AI-Native Architecture**
- Design for AI-powered analysis workflows
- Implement streaming responses where appropriate
- Build for real-time collaboration
- Consider AI model integration points

## 🏗️ Architecture Guidelines

### Frontend (Next.js 14)
```typescript
// ✅ DO: Use TypeScript strictly
interface ContractAnalysis {
  id: string;
  status: 'pending' | 'analyzing' | 'completed' | 'failed';
  findings: SecurityFinding[];
  risks: RiskAssessment[];
}

// ✅ DO: Implement proper error boundaries
const ErrorBoundary: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // Implementation
};

// ❌ DON'T: Use any types or ignore TypeScript errors
const handleData = (data: any) => { /* ... */ };
```

### Backend (FastAPI)
```python
# ✅ DO: Use Pydantic models for validation
class ContractAnalysisRequest(BaseModel):
    contract_address: str = Field(..., min_length=42, max_length=42)
    chain_id: int = Field(..., ge=1)
    analysis_type: List[str] = Field(default_factory=list)

# ✅ DO: Implement proper dependency injection
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    # Implementation
```

## 🎨 Coding Conventions

### File Naming
- **Frontend**: `PascalCase` for components, `camelCase` for utilities
- **Backend**: `snake_case` for files and functions, `PascalCase` for classes
- **Database**: `snake_case` for tables and columns

### Component Structure
```typescript
// ✅ DO: Follow this structure
import React from 'react';
import { cn } from '@/lib/utils';

interface ComponentProps {
  // Props interface
}

export const Component: React.FC<ComponentProps> = ({ 
  // Destructured props
}) => {
  // Hooks first
  // State management
  // Event handlers
  // Render logic
  
  return (
    // JSX
  );
};
```

### API Endpoint Structure
```python
# ✅ DO: Follow this structure
@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_contract(
    request: ContractAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> AnalysisResponse:
    """
    Analyze a smart contract for security vulnerabilities.
    
    Args:
        request: Contract analysis parameters
        current_user: Authenticated user
        db: Database session
        
    Returns:
        AnalysisResponse with findings and risks
        
    Raises:
        HTTPException: For validation or processing errors
    """
    try:
        # Business logic
        result = await contract_service.analyze(request, current_user, db)
        return AnalysisResponse(**result)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Analysis failed")
```

## 🔒 Security Requirements

### Authentication & Authorization
- JWT tokens with proper expiration
- Role-based access control (RBAC)
- Rate limiting on all endpoints
- CORS configuration for production

### Input Validation
```python
# ✅ DO: Validate all inputs
class ContractAddress(BaseModel):
    address: str = Field(..., regex=r'^0x[a-fA-F0-9]{40}$')
    chain_id: int = Field(..., ge=1, le=999999)

# ❌ DON'T: Trust user input
def process_contract(address: str):
    # Always validate first
```

### Database Security
- Use parameterized queries only
- Implement row-level security (RLS)
- Encrypt sensitive data at rest
- Regular security audits

## 🧪 Testing Strategy

### Frontend Testing
```typescript
// ✅ DO: Write comprehensive tests
describe('ContractAnalyzer', () => {
  it('should display analysis results correctly', async () => {
    // Test implementation
  });
  
  it('should handle errors gracefully', async () => {
    // Error handling test
  });
});
```

### Backend Testing
```python
# ✅ DO: Test all endpoints
async def test_analyze_contract_success():
    """Test successful contract analysis."""
    # Test implementation

async def test_analyze_contract_invalid_address():
    """Test analysis with invalid contract address."""
    # Error test
```

## 📊 Performance Requirements

### Frontend
- First Contentful Paint < 1.5s
- Time to Interactive < 3s
- Bundle size < 500KB (gzipped)
- Lighthouse score > 90

### Backend
- API response time < 200ms (95th percentile)
- Database query time < 50ms
- Support 1000+ concurrent users
- 99.9% uptime

## 🔄 State Management

### Frontend State
```typescript
// ✅ DO: Use Zustand for global state
interface AppState {
  user: User | null;
  currentProject: Project | null;
  analysisResults: AnalysisResult[];
  
  // Actions
  setUser: (user: User | null) => void;
  setCurrentProject: (project: Project | null) => void;
  addAnalysisResult: (result: AnalysisResult) => void;
}

// ✅ DO: Use React Query for server state
const { data, isLoading, error } = useQuery({
  queryKey: ['analysis', analysisId],
  queryFn: () => api.getAnalysis(analysisId),
  staleTime: 5 * 60 * 1000, // 5 minutes
});
```

### Backend State
- Use Redis for caching and sessions
- Implement proper database transactions
- Handle distributed state with care

## 🚀 Deployment Guidelines

### Environment Variables
```bash
# ✅ DO: Use environment-specific configs
NODE_ENV=production
NEXT_PUBLIC_API_URL=https://api.clauselens.ai
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=redis://host:port
```

### Docker Configuration
```dockerfile
# ✅ DO: Multi-stage builds
FROM node:18-alpine AS frontend-builder
# Build frontend

FROM python:3.11-slim AS backend-builder
# Build backend

FROM nginx:alpine AS production
# Production setup
```

## 🔍 Code Review Checklist

### Before Committing
- [ ] All tests pass
- [ ] No TypeScript/ESLint errors
- [ ] Security vulnerabilities addressed
- [ ] Performance impact considered
- [ ] Documentation updated
- [ ] Error handling implemented
- [ ] Logging added for critical operations

### AI Collaboration Rules
1. **Always explain your reasoning** - Don't just write code, explain why
2. **Consider edge cases** - Think about what could go wrong
3. **Follow established patterns** - Maintain consistency with existing code
4. **Add comments for complex logic** - Help future AI understand your decisions
5. **Test your assumptions** - Validate that your approach will work

## 🎯 Success Metrics

### Code Quality
- Test coverage > 80%
- Zero critical security vulnerabilities
- All linting rules pass
- Documentation coverage > 90%

### User Experience
- Page load times < 2s
- Zero unhandled errors in production
- Intuitive user interface
- Responsive design on all devices

### Business Impact
- Successful contract analysis > 99%
- User satisfaction > 4.5/5
- Platform uptime > 99.9%
- Security incident response < 1 hour

## 🚨 Emergency Procedures

### Security Incidents
1. Immediately isolate affected systems
2. Preserve evidence and logs
3. Notify security team
4. Implement temporary fixes
5. Conduct post-incident review

### Performance Issues
1. Monitor key metrics
2. Identify bottleneck
3. Implement immediate mitigation
4. Plan long-term solution
5. Document lessons learned

---

**Remember**: You're not just writing code - you're building the future of smart contract security. Every decision matters, every line of code protects real assets, and every feature enables the next generation of DeFi innovation.




