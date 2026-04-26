# Directive 017: Mock Agent Runtime

## Objective

Develop a lightweight "Mock Agent" utility that simulates both the Hermes/OpenClaw REST APIs and an SSH server for local development and integration testing.

## Prerequisites

- [ ] Directive 003: SSH & Agent Adapter Foundation — Complete

## References

**PRD:**
- Phase 4: Advanced Operations (Extended)

**ARCH.md:**
- Directory Structure: `scripts/mock_agent.py`, `docker/mock_agent.Dockerfile`

## Scope

### In Scope
- A Python script using `FastAPI` to simulate agent API endpoints (`/status`, `/chat`).
- Integration of a mock SSH server (using `asyncssh` server capabilities).
- Dockerfile to run the mock agent as a container in the `docker-compose` environment.

### Out of Scope
- Simulating complex agent logic or real AI responses.

## Acceptance Criteria

- [ ] Dashboard can "Add" a Mock Agent and successfully validate SSH/API connections.
- [ ] Mock Agent returns predictable JSON responses for status and chat.
- [ ] Integration tests can run against the Mock Agent without requiring a real VM.

## Status: [x] Complete
