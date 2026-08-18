# Directive 022: Local and Docker Smoke Test Runbook

## Objective

Create and verify a repeatable operator runbook for starting the supervisor locally and with Docker Compose, including migrations and the mock agent.

## Prerequisites

- [x] Directive 015: Dockerization & Container Orchestration — Code Present
- [x] Directive 017: Mock Agent Runtime — Complete
- [ ] Directive 018: Database Migrations — Runbook Verified

## Scope

### In Scope
- Document local setup: `.env`, `.venv`, `npm install`, Alembic migration, backend start, frontend start, mock agent start.
- Document Docker setup: `.env`, `docker-compose up --build`, ports, expected service health.
- Decide whether backend startup should automatically run `alembic upgrade head`, and implement that if chosen.
- Add a smoke test path for adding the mock agent:
  - API endpoint: host-local `http://127.0.0.1:8081` or Docker-network `http://mock-agent:8000`
  - SSH target: host-local `127.0.0.1:8023` or Docker-network `mock-agent:8022`
  - username `agent`, password `agent_pass`
- Verify Add Agent, Operations, Files, file preview, Logs, and Chat in browser.

### Out of Scope
- Real VM provisioning.
- Production authentication or reverse proxy setup.

## Acceptance Criteria

- [ ] Fresh local checkout can run migrations and start backend/frontend without hidden manual steps.
- [ ] Fresh Docker Compose run starts frontend, backend, SQLite volume, and mock agent.
- [ ] Operator can add the mock agent through the UI and use Operations, Files, Logs, and Chat.
- [ ] Runbook includes troubleshooting for SSH/API hostnames inside Docker versus host-local testing.
- [ ] Browser verification evidence is included in the completion notes.

## Status: [x] Incomplete / [ ] Complete
