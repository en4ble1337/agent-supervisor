# Review Gates Guide

Every completed directive or significant task must pass through two review gates before being merged or considered "Done".

## Gate 1: Spec Compliance Review
**Goal:** Ensure the implementation matches the requirements defined in the PRD and the specific Directive.

- [ ] Does the implementation fulfill all "In Scope" items of the directive?
- [ ] Are all "Acceptance Criteria" met and verified?
- [ ] Does it follow the API contracts defined in `ARCH.md`?
- [ ] Does it use the terminology from the `ARCH.md` Dictionary?
- [ ] Are there any unintended changes to existing functionality (regressions)?

## Gate 2: Code Quality Review
**Goal:** Ensure the code is maintainable, secure, and follows project standards.

### Backend (Python/FastAPI)
- [ ] **TDD:** Is there a corresponding test for every new feature?
- [ ] **Typing:** Are all functions and classes fully type-hinted?
- [ ] **Security:** Are SSH credentials handled securely (encrypted at rest, never logged)?
- [ ] **Error Handling:** Are exceptions caught and mapped to the standard error response format?
- [ ] **Async:** Are all I/O operations (DB, SSH, API) properly `await`ed?

### Frontend (React/TypeScript)
- [ ] **Components:** Are components modular and reusable?
- [ ] **Typing:** Are there any `any` types that should be defined?
- [ ] **UX/UI:** Does it match the "hacker/terminal" dark-mode aesthetic?
- [ ] **Performance:** Are there unnecessary re-renders?

## Batch Checkpoints
After every 3 completed tasks, pause and produce a progress report highlighting:
1. What was accomplished.
2. Any technical debt incurred (to be addressed in the next batch).
3. Updated estimate for remaining tasks in the directive.
