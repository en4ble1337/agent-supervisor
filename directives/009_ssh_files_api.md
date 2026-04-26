# Directive 009: SSH Files & Logs API

## Objective

Implement SSH-based backend endpoints for listing workspace directories and tailing log files.

## Prerequisites

- [ ] Directive 004: Agent Registry API — Complete

## References

**PRD:**
- User Story: US-004 View Agent Filesystem via SSH, US-005 View Operational Status (Logs)
- Functional Requirements: FR-3

**ARCH.md:**
- API Contracts: GET /api/agents/{id}/files, GET /api/agents/{id}/logs
- Directory Structure: `backend/api/ssh.py`

**RESEARCH.md:**
- Patterns: SSH File Stream pattern

## Scope

### In Scope
- Expand `SSHService` to perform SFTP `readdir` and standard `tail` commands.
- `GET /api/agents/{id}/files` endpoint (accepts `path` query param).
- `GET /api/agents/{id}/logs` endpoint.

### Out of Scope
- Write/edit access for files.
- Frontend UI.

## Acceptance Criteria

- [ ] `GET /api/agents/{id}/files` decrypts password, connects via SSH, and returns directory contents.
- [ ] `GET /api/agents/{id}/logs` returns the last 100 lines of a log file via SSH.
- [ ] Input validation ensures `path` cannot execute malicious commands (directory traversal protection).
- [ ] All new code has corresponding tests in `tests/`
- [ ] `pytest tests/ -v` passes

## Implementation Notes
- Ensure endpoints handle asyncssh timeouts gracefully and return `502 AGENT_UNREACHABLE` on failure.

## Status: [x] Complete

## Notes
