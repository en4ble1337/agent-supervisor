# Directive 015: Dockerization & Container Orchestration

## Objective

Containerize the backend, frontend, and development utilities to ensure consistent deployment and ease of self-hosting.

## Prerequisites

- [ ] Directive 006: Add Agent UI — Complete (Base functionality should be working)

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
- [ ] Frontend is accessible on port 3000 (or configured port).
- [ ] Backend API is accessible and connects to the persisted SQLite volume.
- [ ] Docker images follow best practices (small size, non-root user).

## Status: [x] Complete
