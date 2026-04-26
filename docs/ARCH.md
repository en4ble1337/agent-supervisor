# ARCH: Single-Pane-of-Glass Supervisor Dashboard

## 1. Overview

The Agent Supervisor Dashboard is a single-pane-of-glass operator cockpit for monitoring and communicating directly with multiple autonomous AI agents (such as OpenClaw and Hermes). It acts as a thin, stateless supervisory layer deployed via Docker, leveraging a FastAPI backend for proxying API requests and executing SSH commands, paired with a dense, desktop-first React frontend for operational visibility.

## 2. Dictionary (Ubiquitous Language)

| Term | Definition | Example |
|------|------------|---------|
| Agent | An autonomous AI instance running on a remote server or container. | "Lead Gen Agent" (powered by Hermes) |
| Business Group | A logical grouping of agents belonging to a specific company or project. | "X Marketing", "Acme Corp" |
| Operator | The primary human user of the dashboard (technical entrepreneur). | The person viewing the dashboard UI. |
| Task | A single unit of work being executed by an Agent. | "Scrape target website for leads." |
| Cron Job | A scheduled task configured directly on an Agent. | "Daily CRM sync at midnight." |
| Session | An active operational period or interaction thread with an Agent. | A chat thread history with the Lead Gen Agent. |
| Workspace | The primary directory on the Agent's remote filesystem where it stores output, state, and logs. | `/opt/hermes/workspace` |

## 3. Tech Stack

| Layer | Technology | Version | Notes |
|-------|------------|---------|-------|
| Runtime | Python | 3.11+ | Backend execution environment |
| Backend Framework | FastAPI | 0.109+ | With Pydantic v2 for robust data validation |
| Database | SQLite | 3+ | Local storage for the agent registry (FR-1) |
| ORM | SQLAlchemy | 2.0+ | Async mode |
| SSH Client | AsyncSSH | 2.14+ | For non-blocking remote command execution and SFTP |
| Frontend | React | 18+ | With TypeScript |
| Styling | Tailwind CSS | 3.4+ | For dense, operator-cockpit aesthetic (Dark mode default) |
| Containerization | Docker & Docker Compose | 24+ | Primary deployment target |

## 4. Data Models

#### Entity: Agent

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, auto-generated | Unique identifier |
| name | string | max 100 chars, required | Display name of the agent |
| ip_address | string | required | Network address or hostname |
| ssh_username | string | required | SSH user for file/log access |
| ssh_password | string | required | Encrypted SSH password (MVP) |
| api_endpoint | string | required | Native REST API URL base (e.g., `http://10.0.0.5:8000`) |
| business_group | string | required | Associated company or project |
| created_at | datetime | auto, UTC | Creation timestamp |

**Relationships:**
- None in MVP. Agents are strictly independent entities grouped by a string `business_group`.

## 5. API Contracts

The frontend interacts with the backend via these primary endpoints:

#### POST /api/agents
Register a new agent.

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Agent display name |
| ip_address | string | Yes | Agent IP |
| ssh_username | string | Yes | SSH Username |
| ssh_password | string | Yes | SSH Password (plain, backend encrypts) |
| api_endpoint | string | Yes | Native API base URL |
| business_group | string | Yes | Group name |

**Response (201):**
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Created agent ID |
| name | string | Agent name |
| business_group | string | Group name |

**Errors:**
- 400: Invalid request body or connection validation failed
- 409: Agent already exists

#### GET /api/agents
List all agents.

**Query Parameters:**
- `business_group` (optional): Filter by business group.

**Response (200):**
List of Agent objects (Note: `ssh_password` is NEVER returned).

#### GET /api/agents/{id}/status
Fetch operational status, active tasks, and cron jobs. The backend proxies this request to the agent's native API.

#### POST /api/agents/{id}/chat
Send a direct message to the agent.

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| message | string | Yes | The command/message to send |

**Response (200):**
| Field | Type | Description |
|-------|------|-------------|
| reply | string | Agent's direct response (proxied from native API) |

#### POST /api/broadcast
Send a message to multiple agents simultaneously.

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| message | string | Yes | The command/message to send |
| business_group | string | No | Optional filter for the target group |
| agent_ids | list[UUID] | No | Optional explicit list of agent IDs |

#### GET /api/agents/{id}/files
List files in an agent's workspace via SSH.

**Query Parameters:**
- `path` (optional): Directory path to list. Defaults to root workspace.

#### GET /api/agents/{id}/logs
Tail the agent's log file via SSH.

**Query Parameters:**
- `lines` (optional): Number of lines to tail. Default is 100.

## 6. Directory Structure

| Path | Purpose | Contains |
|------|---------|----------|
| `backend/` | FastAPI application | |
| `backend/api/` | HTTP route handlers | `agents.py`, `proxy.py`, `ssh.py` |
| `backend/models/` | Database models (SQLAlchemy) | `agent.py` |
| `backend/schemas/` | Pydantic request/response schemas | `agent_schemas.py` |
| `backend/services/` | Business logic & external clients | `agent_service.py`, `ssh_service.py`, `crypto_service.py` |
| `backend/core/` | Config, database connection | `config.py`, `database.py` |
| `frontend/` | React SPA application | |
| `frontend/src/components/` | Reusable UI components | `AgentCard.tsx`, `ChatTerminal.tsx`, `FileBrowser.tsx` |
| `frontend/src/pages/` | Main views | `Dashboard.tsx`, `AgentDetail.tsx` |
| `frontend/src/services/` | API clients | `api.ts` |
| `docker-compose.yml` | Deployment configuration | Defines frontend, backend, and volume mounts |
| `docs/` | Project documentation | `PRD.md`, `ARCH.md` |

## 7. Error Handling Strategy

**HTTP API Errors:**
All dashboard backend errors return JSON with this structure:
```json
{
  "error": {
    "code": "AGENT_UNREACHABLE",
    "message": "SSH connection to Agent {id} timed out.",
    "details": {}
  }
}
```

**Error Codes:**
| Code | HTTP Status | When Used |
|------|-------------|-----------|
| VALIDATION_ERROR | 400 | Request body fails schema validation |
| NOT_FOUND | 404 | Requested agent does not exist in registry |
| AGENT_UNREACHABLE | 502 | The backend could not reach the agent via API or SSH |
| SSH_AUTH_FAILED | 401 | Invalid SSH credentials for the target agent |
| INTERNAL_ERROR | 500 | Unexpected dashboard server error |

**Logging:**
- Backend errors logged with full stack traces in the FastAPI container.
- Failed SSH connection attempts are logged but must NEVER output the attempted password.

## 8. Security Considerations

**Authentication (Dashboard Level):**
- **None built-in.** The dashboard relies 100% on external infrastructure (e.g., Authelia, Tailscale, Cloudflare Access, internal VPN) to protect access to the UI and API.

**Secrets Management:**
- Agent SSH passwords (`ssh_password`) MUST be encrypted at rest in the SQLite database using AES-256-GCM.
- The encryption master key is provided to the backend via the `ENCRYPTION_KEY` environment variable.
- Never commit `.env` files or the SQLite database file to version control.

**Input Validation & Execution:**
- All inputs validated via Pydantic schemas.
- Paths passed to SSH commands must be sanitized to prevent malicious directory traversal outside intended parameters (even though the operator is a trusted user).

## 9. Integration Points

| System | Purpose | Auth Method | Rate Limits |
|--------|---------|-------------|-------------|
| OpenClaw API | Task/status polling, messaging | Native Agent API Auth | N/A (Internal network) |
| Hermes API | Task/status polling, messaging | Native Agent API Auth | N/A (Internal network) |
| Agent SSH | File system reading, Log tailing | Password (encrypted locally) | N/A (Internal network) |

*This system is self-contained on the local network with no external SaaS API dependencies.*

## 10. Non-Functional Requirements

| Requirement | Target | Measurement |
|-------------|--------|-------------|
| Agent List Load Time | < 500ms | SQLite query + UI render time |
| SSH Command Timeout | 5 seconds | Strict timeout to prevent hanging the UI on dead agent connections |
| API Polling Interval | 15 minutes | Auto-refresh interval for task and status updates on the frontend |

## 11. Open Technical Questions

- What specific native API endpoints will we hit for Hermes and OpenClaw to send messages? (Need to audit their current Swagger/OpenAPI docs to build the adapters).
- What is the default file path for logs on the agents? (Assuming `/var/log/syslog` or `/opt/agent/app.log` for MVP tailing, but might need to be configurable per-agent later).
- Do Hermes and OpenClaw APIs support fetching historical chat threads, or does the dashboard need to temporarily cache session history locally?