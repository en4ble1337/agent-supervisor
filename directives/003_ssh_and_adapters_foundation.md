# Directive 003: SSH & Agent Adapter Foundation

## Objective

Establish the base classes for agent communication (Adapters) and implement the basic SSH verification logic required for validating new agent registrations.

## Prerequisites

- [x] Directive 002: Backend Core Setup (DB & Crypto) — Complete

## References

**PRD:**
- User Story: US-001 Add Agent via SSH (Validation requirement)
- Functional Requirements: FR-3

**ARCH.md:**
- Directory Structure: `backend/services/agent_service.py` (Adapters), `backend/services/ssh_service.py`

**RESEARCH.md:**
- Patterns: Multi-Runtime Adapter (`AgentAdapter`, `HermesAdapter`, `OpenClawAdapter`)
- Libraries: `asyncssh`

## Scope

### In Scope
- Base `AgentAdapter` abstract class.
- Stubbed `HermesAdapter` and `OpenClawAdapter` implementing a `validate_endpoint` method.
- `SSHService.validate_connection` method to test SSH reachability, authentication, and ability to run a harmless `true` command.

### Out of Scope
- SFTP file browsing or log tailing (handled later).
- Actual task fetching or messaging implementations.

## Acceptance Criteria

- [ ] `SSHService.validate_connection(ip, user, pass)` successfully connects to a mock SSH server or returns an appropriate error boolean/enum.
- [ ] `AgentAdapter` defines abstract methods for validation, status, and messaging.
- [ ] Implementations of runtime adapters return mock success/failure for endpoint validation.
- [ ] All new code has corresponding tests in `tests/`
- [ ] `pytest tests/ -v` passes

## Implementation Notes

- SSH connections can hang. Ensure `asyncssh.connect` and the validation command are wrapped with a strict 5-second timeout.
- Development targets may include a host and port, such as `127.0.0.1:8022`, so the SSH service should support that form until a first-class SSH port field exists.

## Status: [x] Complete

## Notes

- 2026-05-03 audit: Updated to match the hardened SSH validation behavior. A connection-only check was not enough to prove a usable operator session.
