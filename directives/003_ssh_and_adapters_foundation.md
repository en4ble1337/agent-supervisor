# Directive 003: SSH & Agent Adapter Foundation

## Objective

Establish the base classes for agent communication (Adapters) and implement the basic SSH verification logic required for validating new agent registrations.

## Prerequisites

- [ ] Directive 002: Backend Core Setup (DB & Crypto) — Complete

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
- `SSHService.validate_connection` method to test SSH reachability and authentication without executing commands.

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

- SSH connections can hang. Ensure `asyncssh.connect` is wrapped with a strict 5-second timeout.

## Status: [x] Complete

## Notes
