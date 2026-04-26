# Directive 010: Frontend File Browser

## Objective

Integrate a professional file browser to navigate the agent's remote workspace via SSH.

## Prerequisites

- [ ] Directive 008: Agent Operational UI — Complete
- [ ] Directive 009: SSH Files & Logs API — Complete

## References

**PRD:**
- User Story: US-004 View Agent Filesystem via SSH

**ARCH.md:**
- Directory Structure: `frontend/src/components/FileBrowser.tsx`

**RESEARCH.md:**
- Libraries: `chonky`

## Scope

### In Scope
- Integration of the `chonky` file browser UI component in the Files tab.
- Fetching directory contents via `GET /api/agents/{id}/files`.
- Click-to-view functionality for raw text files.

### Out of Scope
- File editing/saving logic.

## Acceptance Criteria

- [ ] Files tab displays the agent's workspace directory tree natively.
- [ ] Double-clicking a folder navigates into it (triggers a new API call).
- [ ] Clicking a text/csv file opens a read-only modal/view with its contents.
- [ ] Loading states are handled cleanly to account for SSH latency.
- [ ] All new code has corresponding tests in `tests/`
- [ ] `npm run test` passes

## Status: [x] Complete

## Notes
