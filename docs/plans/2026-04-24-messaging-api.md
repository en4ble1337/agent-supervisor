# Implementation Plan: Messaging API

## 1. Objective
Implement the backend logic to send direct chat messages to agent runtimes and retrieve local history (`POST /api/agents/{id}/chat`, `GET /api/agents/{id}/chat`).

## 2. Proposed Changes
- `backend/models/chat.py`: SQLAlchemy `ChatMessage` model.
- `backend/schemas/chat_schemas.py`: Pydantic models for chat.
- `backend/api/proxy.py`: Add chat endpoints.
- `backend/services/agent_service.py`: Verify `send_message` in adapters (already stubbed).
- `tests/api/test_chat_api.py`: API tests for chat.
- `tests/models/test_chat.py`: Model tests for chat messages.

## 3. Step-by-Step Execution Plan

### Step 1: Data Models
- **Task 1: [RED]** Write test for `ChatMessage` model.
- **Task 2: [GREEN]** Implement `ChatMessage` model in `backend/models/chat.py`. (Fields: `id`, `agent_id`, `role` (user/agent), `content`, `timestamp`).

### Step 2: API Endpoints
- **Task 3: [RED]** Write failing tests for `POST /api/agents/{id}/chat` and `GET /api/agents/{id}/chat`.
- **Task 4: [GREEN]** Implement `POST /api/agents/{id}/chat` in `backend/api/proxy.py`.
    - Fetch Agent from DB.
    - Save User message to DB.
    - Call Adapter `send_message()`.
    - Save Agent reply to DB.
    - Return Agent reply.
- **Task 5: [GREEN]** Implement `GET /api/agents/{id}/chat` to return history from DB.
- **Task 6: [REFACTOR]** Clean up error handling.

## 4. Verification Strategy
- **Unit Tests:** `pytest tests/api/test_chat_api.py tests/models/test_chat.py -v`.

## 5. Potential Risks & Mitigations
- **Risk:** Chat history growing too large.
- **Mitigation:** For MVP, SQLite handles it fine. In production, we'd add pagination.
- **Risk:** Adapter `send_message` timeout.
- **Mitigation:** Ensure timeout handling in proxy.
