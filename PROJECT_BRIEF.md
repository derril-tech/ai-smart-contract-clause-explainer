# THE PROJECT BRIEF #

# Project Name #
smart-contract-clause-explainer

# Product Description / Presentation #


smart-contract-clause-explainer

ClauseLens AI — Smart Contract Clause Explainer
Tagline: Turn on-chain code into plain-English obligations, risks, and rights—instantly.
Important: ClauseLens provides technical explanations and security analysis only. It is not legal, financial, or investment advice. Always conduct independent audits and legal review.
________________________________________
1) Product Description / Presentation
Executive Summary
ClauseLens AI is an AI native explainer and risk mapping platform for smart contracts. Paste a contract address, upload source, or link to a repo; ClauseLens fetches verified source/ABI, runs static + differential + property based analyses, and produces plain English clause explanations for functions/modifiers/events—mapped to security risks, privileges, upgrade paths, and economic implications. It grounds all statements in retrieved evidence from code, ABIs, EIPs, and vetted libraries (e.g., OpenZeppelin), enforcing a cite or refuse policy. Built with Next.js 14 + FastAPI + PostgreSQL/pgvector + Redis, orchestrated via LangGraph (with LangChain tools) and a pluggable analyzer stack (Slither, Foundry, Echidna, Semgrep), ClauseLens shortens audit discovery, educates users, and reduces production risk.
Business Outcomes
•	Discovery time ↓ 70% for auditors and integrators via auto explanations and privilege maps.
•	Developer comprehension ↑ with explainer modes (beginner → expert) and code to English traceability.
•	Risk visibility ↑ with change diffs, proxy/upgrade trackers, and oracle/MEV exposure notes.
________________________________________
Core Capabilities
•	Auto Ingest & Verify: Fetch by chain + address (Etherscan/Blockscout style APIs), verify bytecode match, pull verified source/metadata/ABI, decode EIP 1967 proxies (Transparent/UUPS/Beacon), follow upgrade beacons.
•	Clause Explainer: Generate plain English explanations for functions, modifiers, events, access control, and state variables; highlight who can call what, when, and with which constraints; provide examples and state machine diagrams (Mermaid).
•	Risk & Privilege Mapping: Identify owner/admin roles, pause/blacklist/whitelist controls, mint/burn, withdraw, upgrade, fee and sweep functions; map to SWC categories and EIP references; show oracle dependencies and reentrancy/approval surfaces.
•	Static & Differential Analysis: Slither/semgrep rulesets; diff two versions/commits; highlight storage layout changes, initializer patterns, and delegatecall usage.
•	Invariant & Fuzz: Foundry/Echidna property scaffolding; run fuzz locally or via workers; report counterexamples.
•	Economic Notes: MEV/front running exposure (sandwichable calls), price oracle staleness, fee math edge cases, and liquidity assumptions (where detectable).
•	Compliance & Upgrades: Flag proxies, upgrade keys, timelocks, multisig enforcement; detect emergency stops (Pausable) and backdoor patterns.
•	Explainer Modes: ELI5, Engineer, Auditor; multi language output.
•	Docs & Education: Exportable reports (PDF/Markdown), shareable permalinks, and interactive code to clause tooltips.
________________________________________
Functional Modules (User Journeys)
1.	Discover → Enter chain+address or upload source; verify; pick networks (Eth/L2s/BSC/Polygon/AVAX; adapters for Solana/Aptos/Move optional).
2.	Explain → ClauseLens renders a Contract Overview: privileges, upgradeability, kill switches, fee paths, supported interfaces (ERC 165), and risk heatmap.
3.	Analyze → Run static checks and optional fuzz; view SWC hits, storage layout, and event/selector tables.
4.	Compare → Diff versions; highlight risky changes and migration notes.
5.	Report → Generate a human readable report with citations, diagrams, and checklists; export PDF/MD; share.
________________________________________
Non Functional Requirements
•	Performance: p95 API < 300ms for cached artifacts; first explanation stream < 1s; large projects chunked with progressive render.
•	Scale: 10k+ concurrent users; thousands of analyses/day; long running fuzz in job queue.
•	Reliability: 99.9% uptime; graceful degradation (read only explainers, cached results) on provider outages.
•	Security: Least privilege tokens; tenant isolation; signed provenance for ingested artifacts; tamper evident audit logs.
•	Accessibility: WCAG 2.1 AA; keyboard first; semantic tables and diagrams with alt text.
________________________________________
Frontend (Next.js 14 + React 18 + TypeScript + Tailwind)
•	Key Screens
o	Address Intake: chain selector, address checksum validator, verification status.
o	Overview & Risk Heatmap: privileges, upgradeability, proxy tree, role graph, SWC summary.
o	Clause Explorer: functions/modifiers/events with prose explanations, citations, and example calls; state machine viewer.
o	Analysis Console: static findings, storage layout diff, gas hotspots, oracles/MEV panel.
o	Diff Studio: version compare, storage layout changes, initializer/upgrade safety checklist.
o	Report Builder: pick sections, add reviewer notes, export to PDF/MD.
•	UX: Streaming explanations via WebSockets; copy able code blocks; diagram exports; dark/light themes.
•	State: React Query (server cache), Zustand/Context (UI state), file upload with resumable chunks.
________________________________________
Backend (FastAPI + Python 3.11 + Async SQLAlchemy 2.0)
•	Auth: JWT (access/refresh), SSO (SAML/OIDC), MFA; org/project scoping; row level security.
•	Services: ingestion (fetch/verify), metadata/ABI, analysis (static/fuzz), explanations, diffs, reports, projects, notifications.
•	Analyzers: Slither, Semgrep solidity, Foundry (forge test + storage layout), Echidna (fuzz), Bytecode utilities (4byte/selector decoding), abi mdbook generation.
•	Integrations: explorer APIs (Etherscan/Blockscout style), IPFS gateways (optional), version control (GitHub/GitLab), e sign/report attestation (optional), email/Slack webhooks.
•	Observability: OpenTelemetry tracing, Prometheus metrics, structured logs, model usage ledger.
________________________________________
AI Orchestration & Retrieval
•	Chosen Stack: LangGraph for deterministic, inspectable pipelines (ingest → verify → analyze → explain → report) with retries/timeouts; LangChain tools for retrieval/parsing; RAG over:
o	Verified source/ABI and commit history
o	Standards & patterns (EIPs/ERCs), SWC registry summaries, vetted library docs (e.g., OpenZeppelin)
o	Internal rulesets (org playbooks, prior audit notes)
•	Models: GPT 4 family for synthesis; Claude for long context reasoning, policy & safety review; small local LLMs optional for offline summarization.
•	Guardrails: cite or refuse; require source span for any claim; uncertainty bands; privilege escalation detector; unsafe recommendation filter.
________________________________________
Static & Runtime Analysis Stack
•	Static: Slither detectors; Semgrep rules; custom SSA/CFG passes for reentrancy/unchecked transfer; storage layout extractor.
•	Runtime/Property Based: Foundry invariants; Echidna fuzz harness templates (ERC 20/721/4626/Proxy); forked state simulations (optional connector).
•	Economics: simple MEV sandwich check (price impact + public mempool call), oracle staleness heuristics, fee path sanity.
________________________________________
Data Model (selected)
•	projects(id, org_id, name, chain_id, address, verification_status)
•	artifacts(project_id, type[source/bytecode/abi/metadata], url, checksum)
•	contracts(project_id, name, kind[implementation/proxy/beacon], inherits_json, interfaces_json)
•	symbols(contract_id, symbol_type[function/modifier/event/var], sig, visibility, mutability, selectors)
•	analyses(project_id, tool, status, findings_json, storage_layout_json, gas_profile)
•	explanations(contract_id, symbol_id?, mode[eli5/engineer/auditor], text, citations_json, risk_level)
•	diffs(project_id, base, head, storage_delta_json, findings_delta_json)
•	reports(project_id, version, mdx, pdf_url, reviewer_notes)
•	audits(actor, action, resource, purpose, timestamp)
________________________________________
API Surface (sample)
REST
•	POST /ingest → { chain_id, address | repo_url | files[] } → project_id
•	GET /projects/{id} → overview, proxy tree, privileges, supported interfaces
•	POST /analyze/{project_id} → run analyzers (slither/semgrep/foundry/echidna)
•	POST /explain/{contract_id} → clause explanations (mode, scope)
•	POST /diff/{project_id} → compare base/head → risks + storage changes
•	POST /report/{project_id} → build report (sections, mode)
WebSockets
•	/ws/projects/{id} → streaming ingest/analysis/explainer tokens
________________________________________
Security, Privacy & Compliance
•	Provenance: Signed digests of downloaded artifacts; immutability checks.
•	Secrets: Scoped explorer tokens; key rotation; IP allow lists for admin.
•	Governance: Immutable audit logs; evidence retention; export controls for reports.
•	Data Minimization: No wallet private keys; no transaction signing.
________________________________________
Deployment & Scaling
•	Frontend: Vercel (ISR, edge cache).
•	Backend: Render autoscaling; workers for analysis/fuzz; Redis queues & rate limits.
•	DB: Postgres + pgvector; PITR; nightly backups.
Env Vars (excerpt)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
DATABASE_URL=
REDIS_URL=
JWT_SECRET=
STORAGE_BUCKET=
SMTP_URL=
ETHERSCAN_API_KEYS={"1":"…","10":"…","42161":"…"}
BLOCKSCOUT_API_URLS=
ALLOWED_ORIGINS=
________________________________________
Success Metrics
•	First explainer token < 1s; full contract overview < 10s (avg cached).
•	0 unsupported claims (every statement has a code/evidence citation).
•	Reduction of manual discovery time by ≥70% in pilot audits.
•	Lighthouse ≥ 95; uptime 99.9%; tests >90%.
________________________________________
2) Framework Choice (Why LangGraph + LangChain + RAG + Analyzers)
•	LangGraph: deterministic, auditable state machines for high stakes pipelines; resilient retries/timeouts.
•	LangChain: mature retrievers/parsers; tool calling wrappers for analyzers; vector store abstraction to pgvector.
•	RAG: grounds prose in actual source/ABI + standards; adds citations and reduces hallucination.
•	Analyzer Stack: Slither/Foundry/Echidna/Semgrep provide objective signals that the LLM explains—not replaces.
________________________________________
3) Dev Team Brief
Goals
Ship a production ready explainer that turns smart contract code into trustworthy, cited prose and actionable risk maps.
Deliverables
1.	Next.js 14 frontend (Intake, Overview/Heatmap, Clause Explorer, Analysis Console, Diff Studio, Report Builder).
2.	FastAPI backend (ingest/verify/analyze/explain/diff/report) with WebSockets.
3.	Postgres schema with pgvector; Redis queues; integration adapters for explorers.
4.	LangGraph pipelines + LangChain retrievers; RAG + guardrails; analyzer integrations (Slither/Foundry/Echidna/Semgrep).
5.	CI/CD, tests (unit/integration/e2e), OpenAPI docs; Vercel + Render deploy configs.
Milestones
•	M1 (Weeks 1–2): Repos, auth/roles, ingest + verify, basic explainers for ERC 20/721.
•	M2 (Weeks 3–4): Static analysis (Slither/Semgrep), proxy detection, privileges map, report v1.
•	M3 (Weeks 5–6): Diff Studio, storage layout analysis, fuzz harness scaffolding, MEV/oracle panels.
•	M4 (Weeks 7–8): Hardening, performance, multi chain adapters, GA.
Definition of Done
•	All explanations have evidence links + risk level; proxy/upgradeability identified; audit logs immutable.
•	A11y (WCAG 2.1 AA) + perf (Lighthouse ≥ 95) pass; tests >90%; OpenAPI published.
Coding Standards
•	Ruff/Black/mypy; eslint/prettier; pre commit hooks; conventional commits; feature flags.
Repo Structure
/apps
  /web (Next.js 14)
  /api (FastAPI)
/packages
  /ui (tailwind components)
  /workflows (LangGraph graphs)
  /retrievers (LangChain tools)
  /analyzers (slither/semgrep/foundry/echidna adapters)
  /lib (shared clients/types)
/infra (IaC, deploy configs)
/tests (backend, frontend, e2e)
________________________________________
Critical Prompts for Claude (Smart Contract Explainer)
Prompt 1 — Project Setup & Architecture
"Create the complete project structure and architecture for ClauseLens AI. Set up Next.js 14 + TypeScript + Tailwind, FastAPI with async SQLAlchemy + JWT/SSO/MFA, PostgreSQL with pgvector, Redis, deploy configs for Vercel (frontend) and Render (backend), CI workflows, env templates, and scaffolding for LangGraph pipelines with LangChain tools and analyzer adapters (Slither/Foundry/Echidna/Semgrep)."
Prompt 2 — Core Backend Implementation
"Implement the FastAPI backend: projects/artifacts/contracts/symbols/analyses/explanations/diffs/reports models; explorer ingestion & verification; proxy detection (EIP 1967/UUPS/Transparent); static analyzers + storage layout; embeddings into pgvector; hybrid retrieval (BM25 + dense); JWT + RBAC + RLS; WebSockets for streaming; logging/OTel; immutable audit trails."
Prompt 3 — Frontend Components & UI
"Build the Next.js UI: Address Intake, Overview & Risk Heatmap, Clause Explorer with citations and state machine diagrams, Analysis Console (static findings, storage layout, oracle/MEV panels), Diff Studio, and Report Builder. Ensure dark/light themes and WCAG 2.1 AA."
Prompt 4 — AI Integration & Features
"Wire LangGraph flows (ingest → verify → analyze → explain → report) using LangChain retrievers over source/ABI/standards and internal rules. Enforce cite or refuse, privilege/risk mapping, uncertainty bands, explainer modes (ELI5/Engineer/Auditor), and exportable reports with diagrams."
Prompt 5 — Deployment & Optimization
"Prepare for production: Vercel + Render configs, pgvector tuning, Redis rate limits/queues, Playwright e2e tests, load/perf tests, OpenAPI docs, monitoring/alerts (Prometheus/Grafana), backups/PITR, a11y/perf audits, and SLO dashboards for p95 latency and explainer quality KPIs (coverage %, unsupported claim rate, time to overview)."
________________________________________
Roadmap (90 Days)
•	Day 30: ERC 20/721 explainer GA, proxy detection, static analysis v1, PDFs.
•	Day 60: Diff Studio, fuzz scaffolds, MEV/oracle panels, multi chain adapters.
•	Day 90: Auditor mode enhancements, custom rulesets, enterprise SSO/SAML, attested report signing.
________________________________________
One Slide Pitch
What: A trusted explainer that turns smart contract code into understandable clauses with risk maps.
Why it wins: Deterministic pipelines + analyzer signals + evidence grounded RAG + multi chain adapters.
Who: Protocol teams, auditors, integrators, VCs, compliance, and security researchers.
CTA: “Paste an address. Understand the contract.”





FOLLOW THIS 8 STEP PLAN TO PREPARE THE INFRASTRUCTURE
-----------------------------------------------------

# 🚀 Claude Fullstack Repo Prep – Optimized 8 Step Plan

  
The goal: build an extensive frontend + backend scaffold so Claude Code only has to finish ~20% of the work.  
Each step must be **completed ** before advancing  (this is important).
IMPORTANT: YOU ARE BUILDING ONLY THE INFRASTRUCTURE OF THE APPLICATION NOT THE APPLICATION ITSELF !!!. FOLLOW THE STEPS IN NUMERICAL ORDER !!! starting from step 1.
You are doing the groundwork for the application, including setting up the folder structure, configuration files, and any necessary boilerplate code.
IMPORTANT: the checklist in each step has to be checked off 100% before moving to the next step. And always provide comments to your code blocks so that even a non-tech person can understand what you have done.

---

## STEP 1 — Build the Rich Infrastructure
Create a **deep scaffold** for both frontend and backend so Claude code can recognize the architecture immediately.

- Build a **frontend app shell** with routing, placeholder pages, components, and styling setup.  
- Build a **backend app shell** with API structure, health endpoint, and config in place.  
- Include `REPO_MAP.md`, `API_SPEC.md`, and a draft `CLAUDE.md` in the `docs/` folder.  (create the docs folder if it does not  already exist)
- Add **TODO markers and folder-level `_INSTRUCTIONS.md`** files so Claude knows exactly where to add logic.

**Deliverables**
- Frontend app shell with routing, placeholder pages, components, and styling setup  
- Backend app shell with API structure, health endpoint, and config  
- `docs/REPO_MAP.md`, `docs/API_SPEC.md` (stub), and draft `docs/CLAUDE.md`  
- TODO markers + folder-level `_INSTRUCTIONS.md` files  

**Checklist**
- [ ] Frontend scaffold built  
- [ ] Backend scaffold built 
- [ ] Docs folder created with drafts (`REPO_MAP.md`, `API_SPEC.md`, `CLAUDE.md`)  
- [ ] TODO markers and `_INSTRUCTIONS.md` stubs in place  

---

## STEP 2 — Enrich the Scaffold
If the repo looks shallow, enrich it so Claude needs fewer leaps of imagination.  

Add:
- Sample frontend routes and components (`/`, `/about`, `/dashboard`)  
- Domain model stubs and types/interfaces  
- Mock data + fixtures for UI flows  
- README files with quick run instructions for both frontend and backend  
- Instructions embedded in folders (e.g. `CLAUDE_TASK: …`)

**Deliverables**
- Sample routes and pages (`/`, `/about`, `/dashboard`)  
- Domain model stubs and type definitions  
- Mock data and fixtures for UI flows  
- README files for frontend and backend with run instructions  
- Folder-level instructions (`_INSTRUCTIONS.md`)  

**Checklist**
- [ ] At least 2–3 sample routes/pages exist  
- [ ] Domain types/interfaces stubbed out  
- [ ] Mock data + fixtures included  
- [ ] README_FRONTEND.md and README_BACKEND.md added  
- [ ] Each folder has `_INSTRUCTIONS.md` where relevant 

---

## STEP 3 — Audit for Alignment
Check that the scaffold actually matches the product brief, tech specs, and UX /UI goals.
Add additional UI/UX elements (if needed) to make the application visually appealing (and update the design requirements after that)

- Do navigation and pages reflect the product’s main flows?  
- Do API endpoints match the UI needs?  
- Is the chosen tech stack consistent (no unused or conflicting libraries)?  
- Is the UX direction reflected (design tokens, layout, component stubs)?

**Deliverables**
- Alignment review across Product ↔ UI/UX ↔ Tech  
- Identify any missing flows, mismatched libraries, or conflicting instructions  

**Checklist**
- [ ] Navigation structure matches product journeys  
- [ ] Components/pages map to required features  
- [ ] API endpoints cover MVP needs  
- [ ] No contradictory or unused technologies  

---

## STEP 4 — Document the Architecture
Now make the docs **Claude-ready**:

- **REPO_MAP.md**: Full repo breakdown with roles of each folder  
- **API_SPEC.md**: Endpoints, payloads, error handling  
- **CLAUDE.md**: Editing rules, coding conventions, AI collaboration guidelines  

These three files are the **context backbone** Claude will use to understand the repo.

**Deliverables**
- `REPO_MAP.md`: full repo breakdown with folder purposes  
- `API_SPEC.md`: endpoints, models, error conventions  
- `CLAUDE.md`: collaboration rules, editing boundaries  

**Checklist**
- [ ] REPO_MAP.md fully describes structure  
- [ ] API_SPEC.md covers all MVP endpoints and schemas  
- [ ] CLAUDE.md includes project overview, editing rules, examples  

---

## STEP 5 — Improve the Prompt
Enhance the prompt (in `docs/PROMPT_DECLARATION.md`) with details Claude needs:

- FE/BE boundaries and data contracts  
- UX guidelines (states, accessibility, interaction patterns)  
- Performance budgets (bundle size, API latency)  
- Security constraints (auth, rate limits, PII handling)  
- Testing expectations (unit, integration, end-to-end)

**Deliverables**
- FE/BE boundaries and contracts  
- UX guidelines (states, accessibility, patterns)  
- Performance budgets (bundle size, latency targets)  
- Security constraints (auth, PII, rate limits)  
- Testing expectations  

**Checklist**
- [ ] Prompt includes FE/BE division of responsibility  
- [ ] UX principles and design tokens specified  
- [ ] Performance/security/testing requirements added  
- [ ] Prompt is concrete and actionable for Claude  

---

## STEP 6 — Expert Audit of the Prompt
Now do a **meticulous audit** of the one-page prompt declaration.

- Add Frontend Architecture, Backend Architecture, Design requirements, Core Integrations, Success Criteria, Implementation Guidelines and Security & Compliance categories from this Project Brief to the prompt declaration.
- Remove inconsistencies, duplicates, or unused technologies  
- Ensure Tech Stack → Product → Scaffold alignment (no mismatches)  
- Add UI/UX details that make the product visually appealing and usable  
- Double-check frontend and backend folders are ready  
- Confirm editing boundaries are clear (what Claude can/can’t touch)  
- Make the declaration **battle-tested and handoff-ready**

**Deliverables**
- Remove inconsistencies/duplicates  
- Ensure stack ↔ product ↔ scaffold alignment  
- Add UI/UX and accessibility details  
- Clarify file boundaries (editable vs do-not-touch)  
- Confirm prompt uses Claude-friendly syntax  

**Checklist**
- [ ] No unused or contradictory tech remains  
- [ ] UI/UX directives are product-specific and sufficient  
- [ ] Editing boundaries explicitly defined  
- [ ] Prompt syntax uses clear, imperative instructions  

---

## STEP 7 — Bird’s-Eye Repo Review
Do a quick top-level scan for missing pieces:

- All folders contain either code or `_INSTRUCTIONS.md`  
- `.env.example` files exist for both frontend and backend  
- CI/CD config is present and not trivially broken  
- Run scripts (`npm run dev`, `uvicorn …`) work end-to-end  
- No orphan TODOs without clear ownership

**Deliverables**
- Verify all core files exist  
- Confirm environment, CI, and scripts work end-to-end  

**Checklist**
- [ ] Every folder has code or `_INSTRUCTIONS.md`  
- [ ] `.env.example` present for both frontend and backend  
- [ ] CI pipeline triggers and passes basic checks  
- [ ] Dev script (`scripts/dev.sh`) runs both FE and BE  

---

## STEP 8 — Finalize CLAUDE.md
This is where Claude gets its **onboarding pack**. Make sure `CLAUDE.md` includes:

- **Project Overview**: one-paragraph purpose, stack, goals, target users  
- **Folder & File Structure**: what’s editable vs do-not-touch  
- **Coding Conventions**: style guides, naming rules, commenting expectations  
- **AI Collaboration Rules**: response format, edit rules, ambiguity handling  
- **Editing Rules**: full-file vs patches, locked files  
- **Dependencies & Setup**: frameworks, services, env vars  
- **Workflow & Tools**: how to run locally, FE/BE boundary, deployment notes  
- **Contextual Knowledge**: product quirks, domain rules, business logic caveats  
- **Examples**: good vs bad AI answer

**Deliverables**
- Project overview (purpose, stack, goals, users)  
- Folder & file structure with editable vs do-not-touch  
- Coding conventions (style, naming, commenting)  
- AI collaboration rules (response style, edit rules, ambiguity handling)  
- Dependencies and setup instructions  
- Workflow, deployment notes, contextual knowledge  
- Good vs bad answer examples  
- Fill out all the missing information in the CLAUDE.md file

**Checklist**
- [ ] Project overview section filled in  
- [ ] File boundaries clearly defined  
- [ ] Coding/style conventions included  
- [ ] AI collaboration & editing rules written  
- [ ] Dependencies & env notes covered  
- [ ] Workflow & deployment info added  
- [ ] Contextual knowledge documented  
- [ ] Good vs bad examples included  
- [ ] CLAUDE.md file does not miss any important information

---

# ✅ Outcome
When this 8-step plan is followed:
- The repo is a **rich, opinionated scaffold** (80% done).  
- Docs give Claude **clear boundaries + context**.  
- The one-page prompt is **battle-tested** and aligned.  
- Claude Code can safely and efficiently generate the missing 20%.  












