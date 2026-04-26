# AGENTS.md - System Kernel

## Project Context

**Name:** Single-Pane-of-Glass Supervisor Dashboard
**Purpose:** A single-pane-of-glass supervisor dashboard acting as a thin layer on top of agent runtimes like OpenClaw and Hermes
**Stack:** Definition (Example), An autonomous AI instance running on a remote server or container. ("Lead Gen Agent" (powered by Hermes)), A logical grouping of agents belonging to a specific company or project. ("X Marketing", "Acme Corp"), The primary human user of the dashboard (technical entrepreneur). (The person viewing the dashboard UI.), A single unit of work being executed by an Agent. ("Scrape target website for leads."), A scheduled task configured directly on an Agent. ("Daily CRM sync at midnight."), An active operational period or interaction thread with an Agent. (A chat thread history with the Lead Gen Agent.), The primary directory on the Agent's remote filesystem where it stores output, state, and logs. (`/opt/hermes/workspace`), Python (3.11+), FastAPI (0.109+), SQLite (3+), SQLAlchemy (2.0+), AsyncSSH (2.14+), React (18+), Tailwind CSS (3.4+), Docker & Docker Compose (24+), Type (Constraints), UUID (PK, auto-generated), string (max 100 chars, required), string (required), string (required), string (required), string (required), string (required), datetime (auto, UTC), Type (Required), string (Yes), string (Yes), string (Yes), string (Yes), string (Yes), string (Yes), Type (Description), UUID (Created agent ID), string (Agent name), string (Group name), Type (Required), string (Yes), Type (Description), string (Agent's direct response (proxied from native API)), Purpose (Contains), HTTP route handlers (`agents.py`, `proxy.py`, `ssh.py`), Database models (SQLAlchemy) (`agent.py`), Pydantic request/response schemas (`agent_schemas.py`), Business logic & external clients (`agent_service.py`, `ssh_service.py`, `crypto_service.py`), Config, database connection (`config.py`, `database.py`), Reusable UI components (`AgentCard.tsx`, `ChatTerminal.tsx`, `FileBrowser.tsx`), Main views (`Dashboard.tsx`, `AgentDetail.tsx`), API clients (`api.ts`), Deployment configuration (Defines frontend, backend, and volume mounts), Project documentation (`PRD.md`, `ARCH.md`), HTTP Status (When Used), 400 (Request body fails schema validation), 404 (Requested agent does not exist in registry), 502 (The backend could not reach the agent via API or SSH), 401 (Invalid SSH credentials for the target agent), 500 (Unexpected dashboard server error), Purpose (Auth Method), Task/status polling, messaging (Native Agent API Auth), Task/status polling, messaging (Native Agent API Auth), File system reading, Log tailing (Password (encrypted locally)), Target (Measurement), < 500ms (SQLite query + UI render time), 5 seconds (Strict timeout to prevent hanging the UI on dead agent connections), 15 minutes (Auto-refresh interval for task and status updates on the frontend)

## Core Domain Entities

- Agent
- Business Group
- Operator
- Task
- Cron Job
- Session
- Workspace
- Layer
- Runtime
- Backend Framework
- Database
- ORM
- SSH Client
- Frontend
- Styling
- Containerization
- Field
- id
- name
- ip_address
- ssh_username
- ssh_password
- api_endpoint
- business_group
- created_at
- Field
- name
- ip_address
- ssh_username
- ssh_password
- api_endpoint
- business_group
- Field
- id
- name
- business_group
- Field
- message
- Field
- reply
- Path
- `backend/api/`
- `backend/models/`
- `backend/schemas/`
- `backend/services/`
- `backend/core/`
- `frontend/src/components/`
- `frontend/src/pages/`
- `frontend/src/services/`
- `docker-compose.yml`
- `docs/`
- Code
- VALIDATION_ERROR
- NOT_FOUND
- AGENT_UNREACHABLE
- SSH_AUTH_FAILED
- INTERNAL_ERROR
- System
- OpenClaw API
- Hermes API
- Agent SSH
- Requirement
- Agent List Load Time
- SSH Command Timeout
- API Polling Interval

---

## 1. The Prime Directive

You are an agent operating on the Single-Pane-of-Glass Supervisor Dashboard codebase.

**Before writing ANY code:**
1. Read `docs/PRD.md` to understand WHAT we are building
2. Read `docs/ARCH.md` to understand HOW we structure it
3. Consult `docs/RESEARCH.md` for proven patterns to follow
4. Check `directives/` for your current assignment

**Core Rules:**
- Use ONLY the technologies defined in ARCH.md Tech Stack
- Use ONLY the terms defined in ARCH.md Dictionary
- Follow ONLY the API contracts defined in ARCH.md
- Place code ONLY in the directories specified in ARCH.md

---

## 2. The 3-Layer Workflow

### Layer 1: Directives (Orders)
- Location: `directives/`
- Purpose: Task assignments with specific acceptance criteria
- Action: Read the lowest-numbered incomplete directive

### Layer 2: Orchestration (Planning)
- Location: `docs/plans/`
- Purpose: Granular implementation plans for each directive
- Action: Before coding, break the directive into tasks following `docs/methodology/implementation-planning.md`

### Layer 3: Execution (Automation)
- Location: `execution/`
- Purpose: Reusable scripts for repetitive tasks
- Examples: `run_migrations.py`, `seed_data.py`, `run_tests.py`

---

## 3. The TDD Iron Law

**NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.**

### The Mandatory Cycle

For every piece of functionality:

1. **RED:** Write a test in `tests/` that describes the expected behavior. Run it. Confirm it **fails** — and fails for the *right reason* (assertion failure, not import error).
2. **GREEN:** Write the **minimum** code in `src/` to make the test pass. Run all tests. Confirm they **all pass**.
3. **REFACTOR:** Clean up the code while keeping tests green. Run all tests again. Confirm they still pass.
4. **COMMIT:** Only after all tests pass.

### The Nuclear Rule

If you write production code before writing its test:
- **Delete it.** Not "keep as reference." Not "adapt it while writing tests." Delete means delete.
- Write the test first.
- Implement fresh, guided by the failing test.

### Test File Locations

Mirror the source structure:
- `backend/api/agents.py` → `tests/api/test_agents.py`

### TDD Rationalizations Table

| Excuse | Reality |
|--------|---------|
| "This is too simple to test" | Simple code breaks. The test takes 30 seconds to write. |
| "I'll write tests after" | Tests that pass immediately prove nothing — they describe what the code *does*, not what it *should* do. |
| "I already tested it manually" | Manual testing has no record and can't be re-run. |
| "Deleting my work is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt with interest. |
| "I'll keep it as reference and write tests first" | You'll adapt it. That's tests-after with extra steps. Delete means delete. |
| "I need to explore first" | Explore freely. Then throw away the exploration and start with TDD. |
| "The test is hard to write — the design isn't clear yet" | Listen to the test. Hard to test = hard to use. Redesign. |
| "TDD will slow me down" | TDD is faster than debugging. Every shortcut becomes a debugging session. |
| "TDD is dogmatic; I'm being pragmatic" | TDD IS pragmatic. "Pragmatic" shortcuts = debugging in production. |
| "This is different because..." | It's not. Delete the code. Start with the test. |

---

## 4. Implementation Planning

**Before coding any directive, create an implementation plan.**

See `docs/methodology/implementation-planning.md` for the full template.

**The rule:** Write every plan as if the implementer is an enthusiastic junior engineer with no project context and an aversion to testing.

Plans are saved to `docs/plans/YYYY-MM-DD-<feature-name>.md`.

---

## 5. Review Gates

**Every completed task goes through two review stages before moving on.**

See `docs/methodology/review-gates.md` for checklists.

### Gate 1: Spec Compliance Review
### Gate 2: Code Quality Review

### Batch Checkpoints
After every 3 completed tasks, pause and produce a progress report.

---

## 6. Verification Before Completion

**NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE.**

Before marking any task, directive, or feature as "done":
1. **Run the verification command** (test suite, linter, type checker)
2. **Read the actual output** — not from memory, not assumed
3. **Include the evidence** in your completion report

---

## 7. Systematic Debugging

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**

When something breaks, follow the 4-phase process:
1. Root Cause Investigation
2. Pattern Analysis
3. Hypothesis and Testing
4. Implementation

---

## 8. Anti-Rationalization Rules

- "I need more context before I can start" -> Start with the test.
- "Let me explore the codebase first" -> Read the plan.
- "I'll clean this up later" -> Clean it up now.

---

## 9. Definition of Done

- [ ] Implementation plan written before coding
- [ ] Code exists in appropriate directory
- [ ] All new code has corresponding tests in `tests/`
- [ ] Tests were written BEFORE implementation (TDD)
- [ ] All tests pass
- [ ] Spec compliance review passed
- [ ] Code quality review passed
- [ ] Directive file is marked as Complete

---

## 10. File Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Python modules | snake_case | `agent_service.py` |
| Python classes | PascalCase | `class AgentService` |
| Test files | `test_` prefix | `test_agent_service.py` |
| Directives | `NNN_description.md` | `001_initial_setup.md` |

---

## 11. Commit Message Format
`type(scope): description`

Refs: directive-NNN
