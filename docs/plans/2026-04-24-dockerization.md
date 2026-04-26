# Implementation Plan: Dockerization & Container Orchestration

## 1. Objective
Containerize the backend and frontend using Docker and orchestrate them with Docker Compose.

## 2. Proposed Changes
- `docker/backend.Dockerfile`: Python FastAPI image.
- `docker/frontend.Dockerfile`: Node.js build stage + Nginx serve stage.
- `docker-compose.yml`: Orchestration file.
- `.dockerignore`: Ignore node_modules, .venv, etc.
- `backend/main.py`: (Optional) Ensure host is 0.0.0.0 for container accessibility.

## 3. Step-by-Step Execution Plan

### Step 1: Dockerfiles
- **Task 1: [GREEN]** Create `docker/backend.Dockerfile`. Use `python:3.11-slim`. Install dependencies, copy code, run with `uvicorn`. Use a non-root user.
- **Task 2: [GREEN]** Create `docker/frontend.Dockerfile`. Stage 1: Build with Node. Stage 2: Serve with `nginx:stable-alpine`. Configure Nginx to proxy `/api` requests to the backend container.
- **Task 3: [GREEN]** Create `.dockerignore` in root.

### Step 2: Orchestration
- **Task 4: [GREEN]** Create `docker-compose.yml` in the root.
    - `backend` service: build from `docker/backend.Dockerfile`. Env vars from `.env`. Volume for SQLite DB.
    - `frontend` service: build from `docker/frontend.Dockerfile`. Map port 80 to 3000.

### Step 3: Verification
- **Task 5: [REFACTOR]** Run `docker-compose config` to verify syntax.
- **Task 6: [GREEN]** (Manual mention) Verify logic for production build.

## 4. Verification Strategy
- **Docker Build:** `docker compose build` should succeed.
- **Compose Run:** `docker compose up -d` (not possible to fully verify "live" in this env without blocking, but I can check build steps).

## 5. Potential Risks & Mitigations
- **Risk:** SQLite database file permissions in Docker volume.
- **Mitigation:** Ensure the non-root user in the container has write access to the volume mount point.
- **Risk:** Nginx proxy configuration for SPA routing.
- **Mitigation:** Use `try_files $uri $uri/ /index.html;` in Nginx config.
