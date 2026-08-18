# Directive 024: Control-Plane Safety Review

## Objective

Add safety guardrails around features that mutate or command agents, especially broadcast messaging, task triggers, and cron management.

## Prerequisites

- [x] Directive 014: Multi-Agent Broadcast Messaging — Complete
- [x] Directive 019: Agent Actions & Cron Management — Code Complete
- [ ] Directive 020: Real Runtime Adapter Audit & Selection — Complete

## Scope

### In Scope
- Review whether broadcast/action/cron controls should remain enabled by default for MVP.
- Add explicit confirmation UX for broadcast and destructive cron operations.
- Require target preview before sending a broadcast.
- Add backend validation that rejects empty broadcasts or ambiguous target sets.
- Improve auditability by storing control-plane actions locally where appropriate.

### Out of Scope
- Full user authentication/authorization, unless the deployment model changes.
- Human-in-the-loop approval workflows inside the dashboard.

## Acceptance Criteria

- [ ] Broadcast UI clearly shows every target agent before submit.
- [ ] Destructive operations require confirmation.
- [ ] Backend rejects accidental broadcast-to-all unless explicitly requested.
- [ ] Tests cover partial failures and confirmation/validation logic.
- [ ] Completion notes state whether these features are MVP-enabled or feature-flagged.

## Status: [x] Incomplete / [ ] Complete
