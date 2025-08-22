# Frontend App Instructions - ClauseLens AI

This directory contains the Next.js 14 frontend application for ClauseLens AI.

## 🎯 Purpose
The frontend provides an intuitive user interface for smart contract analysis, featuring:
- Contract address input and validation
- Real-time analysis results display
- Interactive risk heatmaps and visualizations
- Clause explanations with citations
- Report generation and export functionality
- Dark/light theme support

## 📁 Structure

```
apps/web/
├── src/
│   ├── app/                 # Next.js 14 app router
│   │   ├── layout.tsx      # Root layout component
│   │   ├── page.tsx        # Home page
│   │   ├── globals.css     # Global styles
│   │   └── (routes)/       # Route groups
│   ├── components/         # React components
│   │   ├── ui/            # Base UI components
│   │   ├── layout/        # Layout components
│   │   ├── contract/      # Contract analysis components
│   │   ├── home/          # Home page components
│   │   └── providers/     # Context providers
│   ├── hooks/             # Custom React hooks
│   ├── lib/               # Utilities and API clients
│   ├── types/             # TypeScript type definitions
│   └── styles/            # Additional styles
├── public/                # Static assets
├── package.json           # Dependencies and scripts
├── next.config.js         # Next.js configuration
├── tailwind.config.js     # Tailwind CSS configuration
└── tsconfig.json          # TypeScript configuration
```

## 🚀 TODO: Implementation Tasks

### Phase 1: Core Components
- [ ] **TODO: Create base UI components** (`src/components/ui/`)
  - [ ] Button components with variants
  - [ ] Input and form components
  - [ ] Card and container components
  - [ ] Modal and dialog components
  - [ ] Toast notification system

- [ ] **TODO: Implement layout components** (`src/components/layout/`)
  - [ ] Header with navigation
  - [ ] Footer component
  - [ ] Sidebar for analysis results
  - [ ] Responsive layout wrapper

- [ ] **TODO: Build contract analysis interface** (`src/components/contract/`)
  - [ ] Contract address input with validation
  - [ ] Chain selector component
  - [ ] Analysis progress indicator
  - [ ] Results display components

### Phase 2: Pages and Routes
- [ ] **TODO: Create main pages** (`src/app/`)
  - [ ] Home page with hero section
  - [ ] Dashboard for user projects
  - [ ] Analysis results page
  - [ ] Report viewer page
  - [ ] Settings and profile pages

- [ ] **TODO: Implement route groups** (`src/app/(routes)/`)
  - [ ] Public routes (home, about, pricing)
  - [ ] Protected routes (dashboard, analysis)
  - [ ] API routes for server-side functionality

### Phase 3: State Management and API Integration
- [ ] **TODO: Set up state management** (`src/hooks/` and `src/providers/`)
  - [ ] React Query for server state
  - [ ] Zustand for client state
  - [ ] Authentication context
  - [ ] Theme context

- [ ] **TODO: Create API clients** (`src/lib/`)
  - [ ] REST API client
  - [ ] WebSocket client for real-time updates
  - [ ] File upload utilities
  - [ ] Error handling and retry logic

### Phase 4: Advanced Features
- [ ] **TODO: Implement data visualizations**
  - [ ] Risk heatmap component
  - [ ] Contract structure diagrams
  - [ ] Analysis progress charts
  - [ ] Interactive code viewer

- [ ] **TODO: Add export and sharing features**
  - [ ] PDF report generation
  - [ ] Markdown export
  - [ ] Shareable links
  - [ ] Social media integration

## 🎨 Design Guidelines

### Color Palette
- **Primary:** Blue (#0ea5e9) - Trust and technology
- **Secondary:** Gray (#64748b) - Neutral and professional
- **Success:** Green (#22c55e) - Low risk
- **Warning:** Yellow (#f59e0b) - Medium risk
- **Danger:** Red (#ef4444) - High risk
- **Critical:** Dark Red (#dc2626) - Critical risk

### Typography
- **Primary Font:** Inter - Clean and readable
- **Code Font:** JetBrains Mono - For code snippets
- **Headings:** Bold weights (600, 700)
- **Body:** Regular weight (400)

### Component Patterns
- Use consistent spacing (4px grid system)
- Implement proper focus states for accessibility
- Support both light and dark themes
- Ensure responsive design for all screen sizes
- Follow WCAG 2.1 AA accessibility guidelines

## 🔧 Development Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Run tests:**
   ```bash
   npm run test
   ```

4. **Build for production:**
   ```bash
   npm run build
   ```

## 📱 Responsive Design

The application must work seamlessly across:
- **Desktop:** 1024px and above
- **Tablet:** 768px - 1023px
- **Mobile:** 320px - 767px

## ♿ Accessibility Requirements

- WCAG 2.1 AA compliance
- Keyboard navigation support
- Screen reader compatibility
- High contrast mode support
- Focus management
- Semantic HTML structure

## 🧪 Testing Strategy

- **Unit tests:** Component functionality
- **Integration tests:** API interactions
- **E2E tests:** User workflows
- **Accessibility tests:** Screen reader and keyboard navigation
- **Performance tests:** Bundle size and loading times

## 📊 Performance Targets

- **First Contentful Paint:** < 1.5s
- **Largest Contentful Paint:** < 2.5s
- **Cumulative Layout Shift:** < 0.1
- **First Input Delay:** < 100ms
- **Bundle size:** < 500KB (gzipped)

## 🔒 Security Considerations

- Input validation and sanitization
- XSS prevention
- CSRF protection
- Secure communication (HTTPS)
- Content Security Policy
- Rate limiting on client side

## 📈 Analytics and Monitoring

- User interaction tracking
- Performance monitoring
- Error tracking and reporting
- A/B testing capabilities
- User feedback collection

## 🚀 Deployment

The frontend will be deployed to Vercel with:
- Automatic deployments from main branch
- Preview deployments for pull requests
- Edge caching for static assets
- CDN distribution for global performance
- Environment-specific configurations

## 📝 Code Quality

- TypeScript strict mode
- ESLint with Next.js rules
- Prettier for code formatting
- Pre-commit hooks for quality checks
- Conventional commit messages
- Comprehensive documentation

This frontend application serves as the primary interface for users to interact with the ClauseLens AI platform, providing a seamless and intuitive experience for smart contract analysis.
