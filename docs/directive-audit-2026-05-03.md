# Directive Audit - 2026-05-03

## Summary

The directive set mostly describes the implemented scaffold, but it had drifted in three important ways:

- Some completed directives still had unchecked prerequisites or stale implementation notes.
- Several directives were marked complete without the verification evidence they claimed, especially Docker, migrations, and quality enforcement.
- The most important missing work was not basic UI code. It was real-runtime alignment: verifying the exact Hermes/OpenClaw API contracts, auth, workspace paths, and safe operational controls.

Fresh verification after the SSH readiness hardening:

- `.\scripts\check_quality.ps1` passed.
- Backend tests: `48 passed`.
- Frontend tests: `26 passed`.
- Frontend production build: `npm run build` passed.

## Existing Directive Findings

| Directive | Audit Result | Notes |
| --- | --- | --- |
| 001 Initial Setup | Environment-specific | The local `.venv` and node dependencies now exist, but `.env` is intentionally not tracked. Operators still need local `.env` setup before running the app. |
| 002 Backend Core | Updated | Fernet wording was stale. New writes use AES-256-GCM with legacy Fernet read support. |
| 003 SSH & Adapters | Updated | SSH validation now runs `true` and enforces the 5-second timeout target. |
| 004 Agent Registry API | Needs follow-up | Duplicate-agent `409` and exact API contract consistency are still not enforced. Covered by Directive 021. |
| 005 Dashboard | Needs follow-up | Business group options are hard-coded and filter persistence from the PRD is not implemented. Covered by Directive 021. |
| 006 Add Agent UI | Code complete | Still needs browser smoke testing against mock runtime. Covered by Directive 022. |
| 007 Status API | Code complete | Uses assumed Hermes/OpenClaw `/status` shape. Covered by Directive 020. |
| 008 Agent Detail UI | Code complete | Operations polling is tested. Real-runtime data shape still depends on Directive 020. |
| 009 SSH Files & Logs API | Updated | Now includes workspace confinement, file content, and strict SSH/SFTP timeouts. |
| 010 File Browser UI | Updated | Current MVP uses native table/inline preview instead of Chonky. |
| 011 Logs Viewer UI | Code complete | Needs browser smoke testing against mock runtime. |
| 012 Messaging API | Needs follow-up | Current request/response shape differs from ARCH.md. Covered by Directive 021 and Directive 020. |
| 013 Chat UI | Code complete | Real-runtime message endpoint still depends on Directive 020. |
| 014 Broadcast Messaging | Extended only | Implemented, but outside MVP and should get operator safety controls before production use. Covered by Directive 024. |
| 015 Dockerization | Not fully verified | Docker files exist, but compose plus migrations plus mock-agent connectivity needs a fresh smoke test. Covered by Directive 022. |
| 016 Quality Enforcement | Partially complete | The quality script passes, but pre-commit/Prettier are not configured. Covered by Directive 025. |
| 017 Mock Agent Runtime | Updated | Now includes real mock SSH/SFTP coverage. |
| 018 Database Migrations | Not fully verified | Migration exists, but migration application is not wired into the runbook/Docker startup. Covered by Directive 022. |
| 019 Agent Actions & Cron | Code complete, not real-runtime verified | Still uses assumed runtime API shape. Covered by Directive 020 and safety controls in Directive 024. |

## Added Follow-up Directives

- Directive 020: Real Runtime Adapter Audit & Selection
- Directive 021: API Contract Compliance Pass
- Directive 022: Local and Docker Smoke Test Runbook
- Directive 023: Agent Connection Profile Hardening
- Directive 024: Control-Plane Safety Review
- Directive 025: Quality Tooling Completion

## Recommended Next Order

1. **Directive 020**: First verify the real Hermes/OpenClaw API surfaces. This answers the user's core concern about basing the supervisor on working open-source products.
2. **Directive 021**: Align the internal API contracts after the real adapter shape is known.
3. **Directive 022**: Prove the full app can run locally and in Docker with migrations and the mock agent.
4. **Directive 023**: Add missing connection profile fields like runtime, SSH port, workspace path, and log path.
5. **Directive 024**: Add guardrails around broadcast/actions/cron before using control features operationally.
6. **Directive 025**: Finish pre-commit/Prettier so quality enforcement matches the directive.
