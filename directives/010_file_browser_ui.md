# Directive 010: Frontend File Browser

## Objective

Integrate a professional file browser to navigate the agent's remote workspace via SSH.

## Prerequisites

- [x] Directive 008: Agent Operational UI — Complete
- [x] Directive 009: SSH Files & Logs API — Complete

## References

**PRD:**
- User Story: US-004 View Agent Filesystem via SSH

**ARCH.md:**
- Directory Structure: `frontend/src/components/FileBrowser.tsx`

**RESEARCH.md:**
- Libraries: `chonky` was considered. The current MVP uses a native dense table and inline preview; Chonky remains an optional future enhancement.

## Scope

### In Scope
- Read-only file browser UI component in the Files tab.
- Fetching directory contents via `GET /api/agents/{id}/files`.
- Click-to-view functionality for raw text files.

### Out of Scope
- File editing/saving logic.

## Acceptance Criteria

- [ ] Files tab displays the agent's workspace directory tree natively.
- [ ] Clicking a folder navigates into it (triggers a new API call).
- [ ] Clicking a text/csv/markdown file opens a read-only view with its contents.
- [ ] Loading states are handled cleanly to account for SSH latency.
- [ ] All new code has corresponding tests in `tests/`
- [ ] `npm run test` passes

## Status: [x] Complete

## Notes

- 2026-05-03 audit: The original directive required Chonky and double-click behavior, but the shipped implementation is a tested native table with single-click navigation and inline previews. This is acceptable for MVP, but a richer file-browser library can be added later if needed.
