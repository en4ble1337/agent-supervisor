# Directive 005: Frontend Foundation & Global Dashboard

## Objective

Set up the React application foundation and build the global dashboard view displaying the agent list with business group filtering.

## Prerequisites

- [ ] Directive 004: Agent Registry API — Complete

## References

**PRD:**
- User Story: US-002 Filter Agents by Business Group
- Feature Specification: Global Dashboard
- Functional Requirements: FR-5

**ARCH.md:**
- Directory Structure: `frontend/src/components/AgentCard.tsx`, `frontend/src/pages/Dashboard.tsx`, `frontend/src/services/api.ts`
- Tech Stack: React, Tailwind CSS

## Scope

### In Scope
- React application scaffolding (Vite/TypeScript).
- Tailwind CSS configuration for dense, dark-mode technical aesthetic.
- API client setup (Axios or native fetch).
- Global dashboard layout with a Business Group dropdown.
- `AgentCard` component displaying high-level info.

### Out of Scope
- Add Agent form.
- Agent detail view/tabs.

## Acceptance Criteria

- [ ] Frontend successfully fetches and displays the agent list from `GET /api/agents`.
- [ ] Top-level dropdown filters the displayed `AgentCard` components by `business_group`.
- [ ] UI utilizes a terminal/hacker dark mode aesthetic as specified.
- [ ] All new code has corresponding tests in `tests/`
- [ ] `npm run test` (or equivalent vitest command) passes
- [ ] `npx tsc --noEmit` passes

## Status: [x] Complete

## Notes
