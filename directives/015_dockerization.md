# Directive 015: Dockerization & Container Orchestration

## Objective

Containerize the backend, frontend, and development utilities to ensure consistent deployment and ease of self-hosting.

## Prerequisites

- [x] Directive 006: Add Agent UI — Complete (Base functionality should be working)

## References

**ARCH.md:**
- Tech Stack: Docker & Docker Compose
- Directory Structure: `docker/`, `docker-compose.yml`

## Scope

### In Scope
- `docker/backend.Dockerfile` (Multi-stage build for Python).
- `docker/frontend.Dockerfile` (Multi-stage build using Nginx for serving static files).
- `docker-compose.yml` orchestrating backend, frontend, and a shared network.
- Environment variable pass-through for `ENCRYPTION_KEY`, `DATABASE_URL`, etc.

### Out of Scope
- Kubernetes manifests.
- CI/CD pipeline automation (GitHub Actions).

## Acceptance Criteria

- [ ] `docker-compose up --build` starts the entire stack successfully.
- [ ] Backend container applies Alembic migrations or the runbook clearly instructs the operator to run them before first use.
- [ ] Frontend is accessible on port 3000 (or configured port).
- [ ] Backend API is accessible and connects to the persisted SQLite volume.
- [ ] Mock Agent is reachable from the backend container by API and SSH/SFTP.
- [ ] Docker images follow best practices (small size, non-root user).

## Status: [ ] Complete / [x] Code Present / [ ] Fresh Docker Smoke Verified

## Notes

- 2026-05-03 audit: Docker files exist, but this directive should not be called fully complete until a fresh `docker-compose up --build` smoke test proves the frontend, backend, SQLite migrations, and mock-agent network path all work together.
