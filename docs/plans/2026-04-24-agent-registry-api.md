# Implementation Plan: Agent Registry API

## 1. Objective
Implement the database models (`Agent`), Pydantic schemas, and REST endpoints (`POST /api/agents`, `GET /api/agents`) for registering, storing, and listing agents, ensuring SSH validation and password encryption.

## 2. Proposed Changes
- `backend/models/agent.py`: SQLAlchemy `Agent` model.
- `backend/schemas/agent_schemas.py`: Pydantic models for creation and response.
- `backend/api/agents.py`: FastAPI router for `/api/agents` endpoints.
- `backend/main.py`: FastAPI app initialization and router inclusion.
- `tests/api/test_agents.py`: Tests for API endpoints.
- `tests/models/test_agent.py`: Tests for agent model.

## 3. Step-by-Step Execution Plan

### Step 1: Data Models and Schemas
- **Task 1: [RED]** Write a test in `tests/models/test_agent.py` to ensure `Agent` model can be instantiated and saved to DB.
- **Task 2: [GREEN]** Implement `Agent` model in `backend/models/agent.py` and schemas (`AgentCreate`, `AgentResponse`) in `backend/schemas/agent_schemas.py`.
- **Task 3: [REFACTOR]** Ensure UUID generation and schema config (e.g., `from_attributes=True`).

### Step 2: GET /api/agents Endpoint
- **Task 4: [RED]** Write failing test in `tests/api/test_agents.py` for `GET /api/agents` including `business_group` filtering.
- **Task 5: [GREEN]** Implement `GET /api/agents` in `backend/api/agents.py`. Set up FastAPI app in `backend/main.py`. Use AsyncSession.
- **Task 6: [REFACTOR]** Ensure no passwords leak in response (handled by `AgentResponse` schema).

### Step 3: POST /api/agents Endpoint
- **Task 7: [RED]** Write failing tests for `POST /api/agents` for success, invalid SSH connection (`SSH_AUTH_FAILED`), invalid API endpoint (`AGENT_UNREACHABLE`).
- **Task 8: [GREEN]** Implement `POST /api/agents` using `SSHService.validate_connection` and `AgentAdapter.validate_endpoint`. Encrypt password with `CryptoService` before saving.
- **Task 9: [REFACTOR]** Ensure proper HTTP exception handling. Provide a mock for `AgentAdapter` or a way to select the correct one based on some logic (for MVP, we might default to Hermes or just pick one, or use a field). Since `api_endpoint` doesn't define the runtime type yet, we can just use `HermesAdapter` as a default for validation. Wait, the schema should probably have `runtime` or `type`? Let's check `ARCH.md`.

*Wait, `ARCH.md` Data Models doesn't specify `runtime` type in the `Agent` entity. Let's assume validation uses `HermesAdapter` for now, or just dummy validation.*

## 4. Verification Strategy
- **Unit Tests:** `pytest tests/api/test_agents.py tests/models/test_agent.py -v`.
- **Integration Tests:** The API test will use an in-memory or file test DB and mock `SSHService` and `AgentAdapter`.

## 5. Potential Risks & Mitigations
- **Risk:** Database schema creation (tables). We need to create tables before running queries.
- **Mitigation:** Since alembic is out of scope until Directive 018, add a startup event or use `Base.metadata.create_all` in `main.py` or within the tests explicitly.
